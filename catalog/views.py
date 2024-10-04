from urllib.parse import urlencode
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from cart.forms import CartAddProductForm
from catalog.forms import ProductForm, ReviewForm, CategoryForm, BrandForm
from catalog.models import Product, Review, Category, Brand
from django.utils.translation import gettext_lazy as _
from transliterate import slugify as transliterate_slugify
from django.utils.text import slugify
from catalog.recommender import Recommender
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from order.tasks import test_task
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.is_staff

class Product_Catalog(View):

    def get(self, request):
        test_task.delay()
        language = request.LANGUAGE_CODE
        categories = Category.objects.all()
        brands = Brand.objects.all()
        objects = Product.objects.filter(availability=True)

        category_slug = request.GET.get('category')
        if category_slug:
            category = Category.objects.get(translations__language_code=language, translations__slug=category_slug)
            objects = objects.filter(category=category)

        brand_slug = request.GET.get('brand')
        if brand_slug:
            brand = Brand.objects.get(slug=brand_slug)
            objects = objects.filter(brand=brand)

        search = request.GET.get('search')
        if search:
            objects = objects.filter(translations__name__icontains=search, translations__language_code=language)

        paginator = Paginator(objects, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        query_params = request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        query_string = urlencode(query_params)

        context = {'categories': categories, 'brands': brands, 'objects': objects, 'page_obj': page_obj, 'query_string': query_string}
        return render(request, 'catalog/catalog_view.html', context)

class Product_Detail(View):
    def get(self, request, pk, slug):
        test_task.delay()
        language = request.LANGUAGE_CODE
        try:
            product = Product.objects.get(pk=pk, translations__language_code=language, translations__slug=slug)
            cart_form = CartAddProductForm()
            review_form = ReviewForm()
            reviews = Review.objects.filter(product=product, parent__isnull=True)
            category = _(str(product.category))
            r = Recommender()
            recommended_products = r.suggest_products_for([product], 4)
            context = {'object': product, 'cart_form': cart_form, 'review_form': review_form, 'reviews': reviews, 'category': category, 'recommended_products': recommended_products}
            return render(request, 'catalog/product_detail.html', context)
        except Product.DoesNotExist:
            error = _('There is no such product')
            return render(request, 'catalog/error_page.html', {'error': error})

    def post(self, request, pk, slug):
        language = request.LANGUAGE_CODE
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.product = Product.objects.get(pk=pk)
            if request.POST.get('parent', None):
                review.parent = Review.objects.get(pk=int(request.POST.get("parent")))
            review.save()
            return redirect('catalog:product_detail', pk=pk, slug=slug)
        else:
            object = Product.objects.get(pk=pk, translations__language_code=language,translations__slug=slug)
            return render(request, 'catalog/product_detail.html', {'form': form, 'object': object})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class Delete_Review(View):
    def get(self, request, pk):
        try:
            object = Review.objects.get(pk=pk)
            return render(request, 'catalog/delete_review.html', {'object': object})
        except Review.DoesNotExist:
            error = _('There is no such review')
            return render(request, 'catalog/error_page.html', {'error': error})

    def post(self, request, pk):
        try:
            object = Review.objects.get(pk=pk)
            object.delete()
            return redirect('catalog:catalog_view')
        except Review.DoesNotExist:
            error = _('There is no such review')
            return render(request, 'catalog/error_page.html', {'error': error})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class Create_Product(View):
    def get(self, request):
        return render(request, 'catalog/create_product.html', {'form': ProductForm()})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            object = form.save(commit=False)#создает запись не сохраняя ее в бд позволяя изменять ее
            translation_slug = transliterate_slugify(form.cleaned_data['name'])
            if not translation_slug:
                slug = slugify(form.cleaned_data['name'])
                if slug:
                    object.slug = slug
                else:
                    error = _('Incorrect form filling')
                    return render(request, 'catalog/error_page.html', {'error': error})
            elif translation_slug:
                object.slug = translation_slug
            object.save()
            return redirect('catalog:update_product', pk=object.pk)
        return render(request, 'catalog/create_product.html', {'form': form})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class Update_Product(View):
    def get(self, request, pk):
        try:
            object = Product.objects.get(pk=pk)
            form = ProductForm(instance=object)
            context = {'form': form, 'object': object}
            return render(request, 'catalog/update_product.html', context)
        except Product.DoesNotExist:
            error = _('There is no such product')
            context = {'error': error}
            return render(request, 'catalog/error_page.html', context)

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                product = form.save()#сначала обновляем продукт т.к если сохранить в конце объект перевода создастся повторно что приведет к ошибке уникальных ключей
                try:
                    object = product.translations.get(language_code=request.LANGUAGE_CODE, master_id = product.pk)
                    object.name=form.cleaned_data['name']
                    object.description=form.cleaned_data['description']
                except ObjectDoesNotExist:
                    object = product.translations.model(
                        language_code=request.LANGUAGE_CODE,
                        name=form.cleaned_data['name'],
                        description=form.cleaned_data['description'],
                        master_id=pk,
                    )
                translation_slug = transliterate_slugify(form.cleaned_data['name'])
                if not translation_slug:
                    slug = slugify(form.cleaned_data['name'])
                    if slug:
                        object.slug = slug
                    else:
                        error = _('Incorrect form filling')
                        return render(request, 'catalog/error_page.html', {'error': error})
                if translation_slug:
                    object.slug = translation_slug
                object.save()
                return redirect('catalog:update_product', pk=product.pk)
            else:
                return render(request, 'catalog/update_product.html', {'form': form, 'object': product})
        except Product.DoesNotExist:
            error = _('There is no such product')
            return render(request, 'catalog/error_page.html', {'error': error})
        except Exception as error:
            return render(request, 'catalog/error_page.html', {'error': error})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class Delete_Product(View):
    def get(self, request, pk):
        try:
            object = Product.objects.get(pk=pk)
            return render(request, 'catalog/delete_product.html' , {'object': object})
        except Product.DoesNotExist:
            error = _('There is no such product')
            return render(request, 'catalog/error_page.html', {'error': error})

    def post(self, request, pk):
        try:
            object = Product.objects.get(pk=pk)
            object.delete()
            return redirect('catalog:catalog_view')
        except Product.DoesNotExist:
            error = _('There is no such product')
            return render(request, 'catalog/error_page.html', {'error': error})

class Brand_List(View):
    def get(self, request):
        objects = Brand.objects.all()

        paginator = Paginator(objects, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'catalog/brand_list.html', {'objects': objects, 'page_obj': page_obj})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class Create_Brand(View):
    def get(self, request):
        return render(request, 'catalog/create_brand.html', {'form': BrandForm()})

    def post(self, request):
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            object = form.save(commit=False)
            translation_slug = transliterate_slugify(form.cleaned_data['name'])
            if not translation_slug:
                slug = slugify(form.cleaned_data['name'])
                if slug:
                    object.slug = slug
                else:
                    error = _('Incorrect form filling')
                    return render(request, 'catalog/error_page.html', {'error': error})
            if translation_slug:
                object.slug = translation_slug
            object.save()
            return redirect('catalog:update_brand', pk=object.pk)

        else:
            return render(request, 'catalog/create_brand.html', {'form': form})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class Update_Brand(View):
    def get(self, request, pk):
        try:
            object = Brand.objects.get(pk=pk)
            form = BrandForm(instance=object)
            return render(request, 'catalog/update_brand.html', {'form': form, 'object': object})
        except Brand.DoesNotExist:
            error = _('There is no such brand')
            return render(request, 'catalog/error_page.html', {'error': error})

    def post(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
            form = BrandForm(request.POST, request.FILES, instance=brand)
            if form.is_valid():
                brand = form.save()
                try:
                    object = brand.translations.get(language_code=request.LANGUAGE_CODE, master_id=brand.pk)
                except ObjectDoesNotExist:
                    object = None
                if not object:
                    brand.translations.create(
                        language_code=request.LANGUAGE_CODE,
                        description=form.cleaned_data['description'],
                        master_id=pk,
                    )
                else:
                    object = brand.translations.get(language_code=request.LANGUAGE_CODE, master_id = pk)
                    object.description=form.cleaned_data['description']
                    object.save()

                brand.name = form.cleaned_data['name']
                brand.image = form.cleaned_data['image']
                translation_slug = transliterate_slugify(form.cleaned_data['name'])
                if not translation_slug:
                    slug = slugify(form.cleaned_data['name'])
                    if slug:
                        brand.slug = slug
                    else:
                        error = _('Incorrect form filling')
                        return render(request, 'catalog/error_page.html', {'error': error})
                else:
                    brand.slug = translation_slug

                return redirect('catalog:update_brand', pk=brand.pk)
            else:
                return render(request, 'catalog/update_brand.html', {'form': form, 'object': brand})
        except Brand.DoesNotExist:
            error = _('There is no such brand')
            return render(request, 'catalog/error_page.html', {'error': error})

class Brand_Detail(View):
    def get(self, request, pk):
        try:
            object = Brand.objects.get(pk=pk)
            products = Product.objects.filter(brand=object)
            return render(request, 'catalog/brand_detail.html', {'object': object, 'products': products})
        except Brand.DoesNotExist:
            error = _('There is no such brand')
            return render(request, 'catalog/error_page.html', {'error': error})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class Delete_Brand(View):
    def get(self, request, pk):
        try:
            object = Brand.objects.get(pk=pk)
            return render(request, 'catalog/delete_brand.html' , {'object': object})
        except Brand.DoesNotExist:
            error = _('There is no such brand')
            return render(request, 'catalog/error_page.html', {'error': error})

    def post(self, request, pk):
        try:
            object = Brand.objects.get(pk=pk)
            object.delete()
            return redirect('catalog:brand_list')
        except Brand.DoesNotExist:
            error = _('There is no such brand')
            return render(request, 'catalog/error_page.html', {'error': error})

class Category_List(View):
    def get(self, request):
        objects = Category.objects.all()
        return render(request, 'catalog/brand_list.html', {'objects': objects})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class Create_Category(View):
    def get(self, request):
        return render(request, 'catalog/create_category.html', {'form': CategoryForm()})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            translation_slug = transliterate_slugify(form.cleaned_data['name'])
            if not translation_slug:
                slug = slugify(form.cleaned_data['name'])
                if slug:
                    object.slug = slug
                else:
                    error = _('Incorrect form filling')
                    return render(request, 'catalog/error_page.html', {'error': error})
            else:
                object.slug = translation_slug

            if Category.objects.filter(translations__slug=object.slug):
                form.add_error(None, _('Such category already exists'))
                return render(request, 'catalog/create_category.html', {'form': form})
            else:
                object.save()
                return redirect('catalog:translate_category', pk=object.pk)
        else:
            return render(request, 'catalog/create_category.html', {'form': form})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class Delete_Category(View):
    def get(self, request, pk):
        language = request.LANGUAGE_CODE
        try:
            object = Category.objects.get(translations__language_code=language, pk=pk)
            return render(request, 'catalog/delete_category.html' , {'object': object})
        except Category.DoesNotExist:
            error = _('There is no such category')
            return render(request, 'catalog/error_page.html', {'error': error})

    def post(self, request, pk):
        language = request.LANGUAGE_CODE
        try:
            object = Category.objects.get(translations__language_code=language, pk=pk)
            object.delete()
            return redirect('catalog:catalog_view')
        except Category.DoesNotExist:
            error = _('There is no such category')
            return render(request, 'catalog/error_page.html', {'error': error})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class Translate_Category(View):
    def get(self, request, pk):
        try:
            object = Category.objects.get(pk=pk)
            form = CategoryForm(instance=object)
            return render(request, 'catalog/translate_category.html', {'form': form, 'object': object})
        except Category.DoesNotExist:
            error = _('There is no such category')
            return render(request, 'catalog/error_page.html', {'error': error})
        except Exception as error:
            return render(request, 'catalog/error_page.html', {'error': error})

    def post(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                try:
                    object = category.translations.get(language_code=request.LANGUAGE_CODE, master_id = category.pk)
                    object.name=form.cleaned_data['name']
                except ObjectDoesNotExist:
                    object = category.translations.model(
                        language_code=request.LANGUAGE_CODE,
                        name=form.cleaned_data['name'],
                        master_id=pk,
                    )
                translation_slug = transliterate_slugify(form.cleaned_data['name'])
                if not translation_slug:
                    slug = slugify(form.cleaned_data['name'])
                    if slug:
                        object.slug = slug
                    else:
                        error = _('Incorrect form filling')
                        return render(request, 'catalog/error_page.html', {'error': error})
                else:
                    object.slug = translation_slug

                if Category.objects.filter(translations__slug=object.slug):
                    form.add_error(None, _('Such category already exists'))
                    return render(request, 'catalog/translate_category.html', {'form': form, 'object': category})
                else:
                    object.save()
                    return redirect('catalog:translate_category', pk=pk)
            else:
                return render(request, 'translate_category.html', {'form': form, 'object': category})
        except Category.DoesNotExist:
            error = _('There is no such category')
            return render(request, 'catalog/error_page.html', {'error': error})
        except Exception as error:
            return render(request, 'catalog/error_page.html', {'error': error})

def test_view(request):
    test_task.delay()
    time.sleep(2)
    # return HttpResponse(test_task())
    return redirect('catalog:brand_list')
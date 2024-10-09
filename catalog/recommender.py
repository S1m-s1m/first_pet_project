import redis
from django.conf import settings
from .models import Product

# r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
r = redis.Redis.from_url(settings.REDIS_URL)

class Recommender:
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
        # получить другие товары, купленные
        # вместе с каждым товаром
                if product_id != with_id:
        # увеличить балл товара,
        # купленного вместе
                    r.zincrby(self.get_product_key(product_id), 1, with_id)
                    '''
                    Функция zincrby используется для увеличения "веса" элемента в сортированном множестве (sorted set) в Redis.
                    Параметры:
                    Первый параметр (self.get_product_key(product_id)) - ключ сортированного множества в Redis.
                    Второй параметр (1) - величина, на которую нужно увеличить вес элемента.
                    Третий параметр (with_id) - сам элемент, вес которого увеличивается
                    product_ids = [101, 202, 303]
                    product:101:purchased_with: {202: 1, 303: 1}
                    product:202:purchased_with: {101: 1, 303: 1}
                    product:303:purchased_with: {101: 1, 202: 1}
                    '''

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]

        if len(products) == 1:
            # только 1 товар
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
            '''
            Функция zrange используется для получения элементов из сортированного множества.
            Параметры:
            Первый параметр (self.get_product_key(product_ids[0]) - ключ сортированного множества.
            Второй параметр (0) - начальный индекс (включительно).
            Третий параметр (-1) - конечный индекс (включительно, -1 означает последний элемент).
            desc=True - определяет порядок сортировки (по убыванию веса).
            product:101:purchased_with:
            1.  202 (балл: 15)
            2.  303 (балл: 10)
            3.  404 (балл: 5)
            4.  505 (балл: 2)
            5.  606 (балл: 1)
            suggestions = r.zrange(self.get_product_key(101), 0, -1, desc=True)[:max_results]
            результат:
            [202, 303, 404, 505, 606]
            '''
        else:
            # сгенерировать временный ключ
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # несколько товаров, объединить баллы всех товаров
            # сохранить полученное сортированное множество
            # во временном ключе
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)

            '''
            Функция zunionstore используется для объединения нескольких сортированных множеств в одно новое множество.
            Параметры:
            Первый параметр (tmp_key) - ключ, под которым будет сохранено новое объединенное множество.
            Второй параметр (keys) - список ключей сортированных множеств, которые нужно объединить.
            tmp_key = 'tmp_101202303404505'
            keys = ['product:101:purchased_with', 'product:202:purchased_with', 'product:303:purchased_with']
            r.zunionstore(tmp_key, keys)
            результат
            tmp_101202303404505: {101: 4, 202: 9, 303: 13, 404: 5, 505: 1}
            '''
            r.zrem(tmp_key, *product_ids)
            suggestions = r.zrange(tmp_key, 0, -1,
                                   desc=True)[:max_results]
            '''пример suggestions = ['202', '404', '505']'''
            r.delete(tmp_key)

        suggested_products_ids = [int(id) for id in suggestions]
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(int(id)))


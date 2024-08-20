import redis
from django.conf import settings
from .models import Product

r = redis.Redis(host=settings.REDIS_HOST,
port=settings.REDIS_PORT,
db=settings.REDIS_DB)

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
            # удалить идентификаторы товаров,
            # для которых дается рекомендация
            r.zrem(tmp_key, *product_ids)

            '''
            Функция zrem используется для удаления элементов из сортированного множества.
            Параметры:
            Первый параметр (tmp_key) - ключ сортированного множества.
            Второй параметр (*product_ids) - список элементов, которые нужно удалить
            tmp_101202303404505: {101: 4, 202: 9, 303: 13, 404: 5, 505: 1}
            self.redis.zrem('tmp_key', 101, 303)
            tmp_101202303404505: {202: 9, 404: 5, 505: 1}
            '''
            # получить идентификаторы товаров по их количеству,
            # сортировка по убыванию
            suggestions = r.zrange(tmp_key, 0, -1,
                                   desc=True)[:max_results]
            '''suggestions = ['202', '404', '505']'''
            # удалить временный ключ
            r.delete(tmp_key)
            '''
            Функция delete используется для удаления ключа из Redis.
            Параметры:
            Единственный параметр (tmp_key) - ключ, который нужно удалить
            '''
        suggested_products_ids = [int(id) for id in suggestions]
        # получить предлагаемые товары и
        # отсортировать их по порядку их появления
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        '''
        suggested_products = [
            <Product: Product 202>,
            <Product: Product 404>,
            <Product: Product 505>
        ]
        '''
        return suggested_products

    '''Из практических соображений давайте также добавим метод очистки ре-
    комендаций. Добавьте следующий ниже метод в класс Recommender:'''

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(int(id)))

'''
Давайте представим, что у нас есть класс `Recommender`, который предназначен для рекомендации товаров на основе анализа совместных покупок. Предположим, у нас есть следующие товары:

1. Товар A
2. Товар B
3. Товар C
4. Товар D

Давайте рассмотрим, как будет работать каждый метод этого класса на примере.

1. Метод `get_product_key`:
   - Этот метод просто формирует ключ для товара в Redis, который будет использоваться для хранения информации о совместных покупках.
   - Например, если мы вызовем `get_product_key(1)`, то получим строку `'product:1:purchased_with'`.

2. Метод `products_bought`:
   - Этот метод принимает список продуктов, которые были куплены вместе.
   - Для каждого продукта в списке он итерирует через все остальные продукты в списке.
   - Если два продукта имеют разные идентификаторы, то вызывается метод `zincrby` для увеличения счетчика совместных покупок в Redis.

3. Метод `suggest_products_for`:
   - Этот метод предназначен для рекомендации товаров на основе анализа совместных покупок.
   - Если у нас есть только один продукт, мы получаем рекомендации, вызывая метод `zrange` для получения топ-N продуктов, которые чаще всего покупаются вместе с этим продуктом.
   - Если у нас есть несколько продуктов, мы создаем временный ключ, объединяем все продукты в одно множество, удаляем идентификаторы самих продуктов, получаем список рекомендаций с помощью `zrange`, удаляем временный ключ и возвращаем рекомендации.

4. Метод `clear_purchases`:
   - Этот метод очищает все данные о совместных покупках для всех продуктов, удаляя соответствующие ключи из Redis.

Теперь давайте представим, что у нас есть следующие совместные покупки:

- Покупка 1: Товар A, Товар B
- Покупка 2: Товар B, Товар C
- Покупка 3: Товар A, Товар D

После вызова метода `products_bought` и обработки этих покупок, мы получим данные в Redis, которые будут выглядеть примерно так:

```
product:1:purchased_with:
   - 2 (Товар B)
   - 4 (Товар D)

product:2:purchased_with:
   - 1 (Товар A)
   - 3 (Товар C)

product:3:purchased_with:
   - 2 (Товар B)

product:4:purchased_with:
   - 1 (Товар A)
```

Теперь, когда мы вызовем метод `suggest_products_for`, например, для продукта с идентификатором 1 (Товар A), он вернет рекомендации на основе данных из Redis, указывающие, что чаще всего совместно покупаются Товары B и D.

Таким образом, этот класс анализирует совместные покупки и рекомендует товары на основе этого анализа.
'''
import pytest
from decimal import Decimal
from unittest.mock import patch, Mock
from django.urls import reverse
from order.models import Order, Order_Item


@pytest.mark.django_db
class TestPaymentProcessView:

    @patch('stripe.checkout.Session.create')
    @patch('stripe.Coupon.create')
    def test_payment_process_success(self, mock_stripe_coupon, mock_stripe_session, client, order, order_items):
        # Настройка моков для Stripe
        
        # Set up a mock object for the session with id and url attributes
        mock_stripe_session.return_value = Mock(id='session_id', url='https://example.com/checkout/session_id')

        # Set up a mock object for the coupon with an id attribute
        mock_stripe_coupon.return_value = Mock(id='coupon_id')

        # Добавляем идентификатор заказа в сессию
        session = client.session
        session['order_pk'] = order.pk
        session.save()

        # Отправляем POST-запрос к представлению
        url = reverse('payment:process')
        response = client.post(url)

        # Проверяем, что был произведен редирект
        assert response.status_code == 302
        assert response.url == 'https://example.com/checkout/session_id'

        # Проверяем, что Stripe был вызван с корректными данными
        mock_stripe_session.assert_called_once()
        mock_stripe_coupon.assert_called_once_with(
            name=order.coupon.code,
            percent_off=order.discount,
            duration='once'
        )

'''
Давай я объясню каждую строку кода в тесте по порядку.

### Импорты

```python
from unittest.mock import patch, Mock
from django.urls import reverse
import pytest
from order.models import Order, Order_Item
```

1. **`unittest.mock.patch` и `unittest.mock.Mock`:**
   - `patch`: используется для замены реальных объектов или функций в коде фиктивными (mock) объектами во время теста.
   - `Mock`: это объект-заглушка, который можно настроить так, чтобы он вел себя как реальный объект, возвращая значения, имитируя атрибуты и методы.

2. **`django.urls.reverse`**: 
   - Функция `reverse` используется для получения URL по имени представления. В Django для каждого представления можно задать уникальное имя, чтобы использовать его для получения URL.

3. **`pytest`**: 
   - Импортируется фреймворк для тестирования.

4. **Импорт моделей `Order` и `Order_Item`:**
   - Эти модели используются в тесте для создания заказа и его элементов.

### Тестовый класс

```python
@pytest.mark.django_db
class TestPaymentProcessView:
```

5. **`@pytest.mark.django_db`:**
   - Декоратор `django_db` сообщает pytest, что тест работает с базой данных, и Django должен подготовить тестовую БД для этого теста.

6. **`class TestPaymentProcessView`:**
   - Это тестовый класс. Внутри этого класса определяются методы, которые будут тестировать различные аспекты вашего кода.

### Тестовый метод

```python
    @patch('stripe.checkout.Session.create')
    @patch('stripe.Coupon.create')
    def test_payment_process_success(self, mock_stripe_coupon, mock_stripe_session, client, order, order_items):
```

7. **`@patch('stripe.checkout.Session.create')`:**
   - Этот декоратор заменяет реальную функцию `stripe.checkout.Session.create` на фиктивную во время выполнения теста. Все вызовы этой функции будут перенаправлены на объект `mock_stripe_session`.

8. **`@patch('stripe.Coupon.create')`:**
   - Аналогично предыдущему декоратору, эта строка заменяет реальную функцию `stripe.Coupon.create` фиктивной в течение теста. Все вызовы будут перенаправлены на объект `mock_stripe_coupon`.

9. **`test_payment_process_success`:**
   - Это основной тестовый метод, который будет запускаться. Он проверяет успешную обработку платежа.

10. **Аргументы `mock_stripe_coupon`, `mock_stripe_session`, `client`, `order`, `order_items`:**
    - `mock_stripe_coupon` и `mock_stripe_session`: фиктивные объекты, подставленные через декораторы `patch`.
    - `client`: фиктивный HTTP-клиент Django, который используется для выполнения запросов к вашему приложению.
    - `order`: объект `Order`, созданный для теста.
    - `order_items`: объект `Order_Item`, который представляет товар в заказе.

### Настройка mock объектов для Stripe

```python
        mock_stripe_session.return_value = Mock(id='session_id', url='https://example.com/checkout/session_id')
```

11. **`mock_stripe_session.return_value = Mock(...)`:**
    - Здесь мы указываем, что когда вызывается функция `stripe.checkout.Session.create`, она должна вернуть фиктивный объект с атрибутами `id` и `url`. Мы имитируем поведение реального ответа от Stripe, где `session_id` и URL являются важными параметрами.

```python
        mock_stripe_coupon.return_value = Mock(id='coupon_id')
```

12. **`mock_stripe_coupon.return_value = Mock(...)`:**
    - Когда вызывается функция `stripe.Coupon.create`, она возвращает фиктивный объект с атрибутом `id`. Мы создаем "фиктивный купон" с `coupon_id`.

### Сессия клиента

```python
        session = client.session
        session['order_pk'] = order.pk
        session.save()
```

13. **`session = client.session`:**
    - Получаем текущую сессию клиента.

14. **`session['order_pk'] = order.pk`:**
    - Добавляем идентификатор заказа (`order.pk`) в сессию, чтобы имитировать работу реального пользователя, который оформляет заказ.

15. **`session.save()`:**
    - Сохраняем изменения в сессии.

### Отправка POST-запроса

```python
        url = reverse('payment:process')
        response = client.post(url)
```

16. **`url = reverse('payment:process')`:**
    - Используем `reverse`, чтобы получить URL для представления `payment:process`.

17. **`response = client.post(url)`:**
    - Отправляем POST-запрос на URL, используя клиента Django, и сохраняем ответ в переменной `response`.

### Проверка ответа

```python
        assert response.status_code == 302
        assert response.url == 'https://example.com/checkout/session_id'
```

18. **`assert response.status_code == 302`:**
    - Проверяем, что ответ от сервера имеет код состояния 302, что означает, что был выполнен редирект (перенаправление).

19. **`assert response.url == 'https://example.com/checkout/session_id'`:**
    - Проверяем, что URL для редиректа совпадает с тем, что был установлен в mock объекте `mock_stripe_session`.

### Проверка вызова Stripe

```python
        mock_stripe_session.assert_called_once()
        mock_stripe_coupon.assert_called_once_with(
            name=order.coupon.code,
            percent_off=order.discount,
            duration='once'
        )
```

20. **`mock_stripe_session.assert_called_once()`:**
    - Проверяем, что функция `stripe.checkout.Session.create` была вызвана один раз.

21. **`mock_stripe_coupon.assert_called_once_with(...)`:**
    - Проверяем, что функция `stripe.Coupon.create` была вызвана с корректными параметрами: имя купона, скидка и время действия купона.

---

Таким образом, этот тест имитирует успешную обработку платежа через Stripe, проверяет работу представления и взаимодействие с сессией, купонами и элементами заказа.
'''
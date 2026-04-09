# Task_2
В данном проекте реализован набор тестов для API сервиса Stellar Burgers.
Тесты написаны на **Python** c применением **Pytest** и **Requests**.

- clients/ - описание API клиентов для вызова запросов
- tests/ - сами тестовые методы
- utils/ - вспомогательные методы для генерации данных
- conftest.py - фикстуры для создания методов
- data.py - тестовые данные
- endpoints.py - URL ресурсы для API методов
- messages.py - константы сообщений  

## Покрытые кейсы:
1. **Проверка API метода "Создание пользователя" (test_create_user.py):**  
   test_create_unique_user_success - успешное создание уникального пользователя;  
   test_create_user_duplicate_shows_error - проверка ошибки при создании дубликата курьера;  
   test_create_user_empty_fields_shows_error - проверка негативных кейсов для метода - попытка создания с
   пропущенными обязательными полями.


2. **Проверка API метода "Авторизация пользователя" (test_login_user.py):**  
   test_login_user_success - успешная авторизация пользователя в системе;  
   test_login_user_incorrect_fields_show_error - ошибка при авторизации с пустым имейлом или паролем;  


3. **Проверка API метода "Изменение данных пользователя" (test_update_user.py):**  
   test_update_user_authorized_user_success - успешное изменение данных пользователя с параметризацией по изменяемым полям;  
   test_update_user_unauthorized_user_shows_error - ошибка при попытке изменить данные для неавторизованного пользователя.   


4. **Проверка API метода "Создание заказа" (test_create_order.py):**  
   test_create_order_authorized_user_with_ingredients_success - создание заказа авторизованным пользователем с валидными ингредиентами;  
   test_create_order_unauthorized_user_with_ingredients_success - создание заказа неавторизованным пользователем;  
   test_create_order_authorized_user_without_ingredients_shows_error - создание заказа авторизованным пользователем без ингредиентов;  
   test_create_order_authorized_user_incorrect_ingredients_shows_error - создание заказа авторизованным пользователем с невалидными ингредиентами.  


5. **Проверка API метода "Получение заказов конкретного пользователя" (test_get_orders_for_user.py):**  
   test_get_orders_for_user_authorized_user_success - успешное получения списка заказов для авторизованного пользователя;  
   test_get_orders_for_user_unauthorized_user_shows_error - ошибка при попытке получения заказов для неавторизованного пользователя.  

### Запуск тестов

1. Установите зависимости:  
   pip install -r requirements.txt
2. Запустите тесты:  
   pytest tests

### Генерация отчета Allure

1. Запустите тесты с генерацией данных для отчета:  
   pytest --alluredir=allure-results
2. Сгенерируйте отчет и откройте его в браузере:
   allure serve allure-results
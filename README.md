# Django_Stripe
![workflow](https://github.com/Ilia-Pringless/Django_Stripe/actions/workflows/main_flow.yml/badge.svg)


В проекте реализован пример взаимодействия с сервисом Stripe и python библиотекой stripe.

stripe.com - платёжная система с помощью которой можно создавать платежные формы разных видов, 
сохранять данные клиента, и реализовывать прочие платежные функции.

## Запуск приложения в контейнерах

- Сборка образов и контейнеров из корневой дирректории проекта

```docker-compose up -d --build ```

- Страница администрирования
```
130.193.54.148/admin/
```

## Примеры запросов
### Получение определенного товара и его покупка.
```
http://localhost/item/1
```
(Пример товара без скидки)
```
http://localhost/item/2
```
(Пример товара со скидкой)
```
http://localhost/item/3
```
### Получение набора товаров и их покупка
```
http://localhost/order/1
```
(Пример заказа со скидкой)
```
http://localhost/order/2
```
(Пример заказа без скидки)
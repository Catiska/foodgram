
# [Foodgram](foodgram.catiska.ru)

![ci/cd_foodgram workflow](https://github.com/catiska/foodgram-project-react/actions/workflows/main.yml/badge.svg?event=push)

Продуктовый помощник - сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 


## Технологии


- Python 3.9
- Django 4.2.1
- Django REST framework 3.14
- Nginx
- Docker
- Postgres


## Запуск проекта

Проект запущен на пересборку после команды git push в основную ветку. Для работы над проектом склонируйте его

```bash
  git clone https://github.com/Catiska/foodgram-project-react.git
```

Для работы на новом сервере в секретах гитхаба понадобится обновить следующие данные:

`SSH_KEY` - ssh ключ сервера

`SSH_PASSPHRASE` - пароль ля входа на сервер

`USER` - имя юзера

`HOST` - хост сервера



## Создание суперюзера

Для работы на сайте понадобится администратор, который создаст необходимые тэги, без них публикация рецепта невозможна. На сервере введите команду и создайте суперюзера:

```bash
  sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```
    
## Готовый юзер-админ
```bash
  admin@admin.ru
  admin
```

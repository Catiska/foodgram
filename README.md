# не в той репе работала, rip

Проект на данный момент собран в контейнерах и может быть запущен локально
```angular2html
git clone https://github.com/Catiska/foodgram-project-react-1.git
```
```angular2html
cd infra
```
```angular2html
docker compose up
```
В отдельном терминале ввести
```angular2html
docker exec infra-backend-1 python manage.py migrate
```
Загрузить данные:
```angular2html
docker exec infra-backend-1 python manage.py load_data
```
Создать суперюзера
```angular2html
docker exec infra-backend-1 python manage.py createsuperuser
```
Или использовать данные готового админа
```angular2html
admin@admin.ru   # login email
admin   # password
```

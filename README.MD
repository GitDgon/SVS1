Сохранение библиотек:
`pip freeze > reqiurements.txt`

install requirements: 
`pip install -r requirements.txt`

run project:
`python manage.py runserver`

run django-extensions console: 
`python manage.py shell_plus --ipython`

Откатить до определенного commita на Githab
`git reset --hard <hash коммита: ea06...dd7v>`

Создаем миграцию:
`python manage.py makemigrations`

Применяем миграцию:
`python manage.py migrate`

Сохранение на GIT:
`git add .`
`git commit -m "Изменил модель bd svs_k"`
`git push origin master`

Создать supper-user
`python manage.py createsuperuser`

Сохранить данные в fixtures:
`python manage.py dumpdata MainApp > MainApp/fixtures/save_all.json`
`python manage.py dumpdata MainApp auth.User > MainApp/fixtures/save_all.json`

Очистить БД:
`python manage.py flush`

Добавить информацию в БД из fixture:
`python manage.py loaddata save_all.json`
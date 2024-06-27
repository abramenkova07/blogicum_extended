#  Проект Blogicum

## Описание проекта

Проект представляет собой социальную сеть для публикации личных дневников, которая реализована в виде веб-сайта. На данном сайте пользователи могут публиковать свои посты, оставлять комментарии, а также просматривать страницы других пользователей и их посты.

## Стек использованных технологий

Проект представляет собой сайт, состоящий из **frontend** и **backend** части.
* **Frontend:** HTML, CSS
* **Backend:** СУБД Sqlite3, Django

## Развертывание проекта локально

Чтобы запустить проект нужно: <br>
1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:abramenkova07/blogicum_extended.git
```
```bash
cd blogicum_extended/
```
2. Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
```
3. Установить зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
4. Выполнить миграции:
```bash
python manage.py migrate
```
5. Запустить проект:
```bash
python manage.py runserver
```
#### Автор проекта:
[Арина Абраменкова](https://github.com/abramenkova07)

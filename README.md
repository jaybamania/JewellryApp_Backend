# JeweleryAppBackend

Jeweler's app MVP

## Technologies and Tools

- TextEditor - Visual Studio Code
- VSCode Extensions
  - Prettier - for code formatting
- Python - 3.7.7
- Pip - 20.1.1
- Django
- Django Rest Framework
- Database - PostgreSQL - 12.3.1
- Development OS - Window 10

## Initial Setup

```cmd
git clone https://github.com/vijay-anand-dev/JeweleryAppBackend.git

cd JeweleryAppBackend

python -m venv venv

venv\Scripts\activate # to activate the Virtual Environment

pip install -r requirements.txt

cd src

python manage.py runserver
```

- Update the **DATABASES** in `settings.py` and Create `jewelleryapp` DB in **PostgreSQL**

```sql
CREATE DATABASE jewelleryapp;
```

## Development Note

- Main branch - master
- Development branch - dev

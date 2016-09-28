# [Setup](README.md) | [Development](README_DEV.md) | [Git Guide](README_GIT.md)

## Running development server
You can start a devserver by this command:

    python manage.py runserver

This command starts a dev server on <http://localhost:8000> that you can view with your browser.

---

## Using admin panel
You can access admin panel from <http://localhost:8000/admin>. In admin panel you can make
changes to any data in the database. For example you can add or remove projects, tasks or events.

---

## Changing models
The file `teamwork/models.py` defines what data is stored in different "models". In our
web application models are things such as projects, events, tasks, users. If you change these
models then afterwards you must run following commands so that the changes come in effect:

    python manage.py makemigrations
    python manage.py migrate

---

## Django framework
For more information about the Django framework go to <https://www.djangoproject.com/>.

---

### [> Setup instructions](README.md)
### [> Git guide](README_GIT.md)

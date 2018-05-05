# project-name

make sure your machine running mysql

create mysql database named 'projectdb'

```
source env/bin/activate

pip install -r requirements.pip

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

in browser, go to http://localhost:8000/docs to see api docs


## API

Login
```
/auth/login
method='POST'
content_type='JSON'
data=
{
  "username": <USERNAME>,
  "password": <PASSWORD>
}
```

Register
```
/auth/register
method='POST'
content_type='JSON'
data=
{
  "username": <USERNAME>,
  "email": <EMAIL>,
  "password": <PASSWORD>
}
```

Change password
```
/auth/change_password
method='POST'
content_type='JSON'
data=
{
  "username": <USERNAME>,
  "password": <PASSWORD>
}
```

Logout
```
/auth/logout
method='GET'
```

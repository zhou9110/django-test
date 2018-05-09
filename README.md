# project-name

make sure your machine running mysql

create mysql database named 'test-db'

clone this project and then

```
cd project-name

virtualenv env

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
content_type='application/json'
data=
{
  "username": <USERNAME>,
  "password": <PASSWORD>
}
OR
{
  "email": <EMAIL>,
  "password": <PASSWORD>
}
```

Register
```
/auth/register
method='POST'
content_type='application/json'
data=
{
  "username": <USERNAME>,
  "email": <EMAIL>,
  "password": <PASSWORD>
}
```

Update password
```
/auth/update_password
method='PUT'
content_type='application/json'
data=
{
  "password": <PASSWORD>
}
```

Logout
```
/auth/logout
method='GET'
```

Get profile
```
/user/profile/
method='GET'
```

Get profile by id
```
/user/profile/<id>/
method='GET'
```

Update profile
```
/user/update_profile/
method='PUT'
content_type='application/json'
data=
{
  "mobile": <MOBILE>, (optional)
  "bio": <BIO>, (optional)
  "gender": <GENDER>, (optional)
  "profile_image": <PROFILE_IMAGE> (optional)
}
```

Follow
```
/user/follow/<id>/
method='POST'
content_type='application/json'
data={}
```

Unfollow
```
/user/unfollow/<id>/
method='POST'
content_type='application/json'
data={}
```

Get following
```
/user/following/
method='GET'
```

Get following by id
```
/user/following/<id>/
method='GET'
```

Get followers
```
/user/followers/
method='GET'
```

Get followers by id
```
/user/followers/<id>/
method='GET'
```

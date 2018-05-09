# project-name

make sure your machine running mysql

create mysql database named 'projectdb'

clone this project and then

```
cd project-name

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
/user/get_profile
method='GET'
```

Update profile
```
/user/update_profile
method='PUT'
content_type='application/json'
data=
{
  "mobile": <MOBILE>,
  "bio": <BIO>,
  "gender": <GENDER>,
  "profile_image": <PROFILE_IMAGE>
}
```

Follow
```
/user/follow
method='POST'
content_type='application/json'
data=
{
  "username": <USERNAME>
}
```

Unfollow
```
/user/unfollow
method='POST'
content_type='application/json'
data=
{
  "username": <USERNAME>
}
```

Get following
```
/user/get_following
method='GET'
```

Get followers
```
/user/get_followers
method='GET'
```

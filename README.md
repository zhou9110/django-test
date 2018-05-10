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
/auth/login/
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
/auth/register/
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
/auth/update_password/
method='PUT'
content_type='application/json'
data=
{
  "password": <PASSWORD>
}
```

Logout
```
/auth/logout/
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
  "gender": <GENDER-enum"M"/"F"/"NS">, (optional)
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

Get posts of the user
```
/post/posts/
method='GET'
```

Get posts of the user by uid
```
/post/posts/<uid>/
method='GET'
```

Get post by post id
```
/post/post/<id>/
method='GET'
```

Create post
```
/post/create/
method='POST'
{
  "text": <TEXT>,
	"images": <IMAGES>,
	"location": <LOCATION>,
	"tags": [<TAG_NAME>] (optional)
}
```

Update post by post id
```
/post/update/<id>/
method='PUT'
data=
{
  "text": <TEXT>,
	"images": <IMAGES>,
	"location": <LOCATION>,
	"tags": [<TAG_NAME>]
}
```

Comment post by post id
```
/post/comment/<id>/
method='POST'
data=
{
  "text": <TEXT>
}
```

Like post by post id
```
/post/like/<id>/
method='POST'
data={}
```

Get tag by tag id
```
/post/tag/<id>/
method='GET'
```

Convert tags id list to tags string list
```
/post/convert_tags/
method='POST'
{
  "tags": [<TAG_ID>]
}
```

Create tag
```
/post/create_tag/
method='POST'
data=
{
  "name": <TAG_NAME>
}
```

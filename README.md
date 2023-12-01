![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Positive Social Network API, a project for the Code Institute Full Stack Software Development Diploma.

## Introduction

This project is a Django API for the Positive Social Network, a social network for people to share only positive reviews of restaurants, bars, hotels, etc.
Why only positive reviews? Because we want to create a positive environment for people to share their experiences and recommendations. We believe that there are already too many negative reviews on the internet, and we want to change that.

In my experience as a movie and music reviewer, people feel also attracted to check the negatively scored movies. We humans are curious by nature, and we want to know why a movie is so bad, or why a restaurant is so bad. We even want to contradict others opinions, so we also want to prove people wrong. This is why I believe that a social network with only positive reviews will be a success. Not only because really good places will have more notoriety, but also because people won't have information about bad places, so these places will need to strive harder to at least, have presence in the Internet.

Also, when one writes a negative review, it is very easy to get carried away and write a very long one, losing even scope. But, when one writes a positive review, needs to really focus on explaining why the place is so good, and this is a good exercise for the brain and also, to hihglight why the place is worth visiting.

## Basic configuration

Start by installing Django (in this case, I used the latest version to date 4.2.7)

```bash
pip3 install django
```

Then, create a new project

```bash
django-admin startproject <project_name> .
```

My project name is positive_api, as I will be creating an API for the Positive Social Network.

NOTE: The dot at the end of the command is to create the project in the current directory. Please, do not forget it (I know why I am saying this ;-) ).

We are going to use CLOUDINARY to store the images of the users. So, we need to install the cloudinary package

```bash
pip install django-cloudinary-storage
```

Then, we need to install also [Pillow](https://pypi.org/project/Pillow/), which is a Python Imaging Library

```bash
pip install Pillow
```

But, I know that when you are reading (or even watching tutorials), you are to install and do things that you don't know what they are for. So, check this [![YouTube video](https://img.youtube.com/vi/6Qs3wObeWwc/0.jpg)](https://www.youtube.com/watch?v=6Qs3wObeWwc) that will tell you what is Pillow and why we need it.

Add the Cloudinary storage to the INSTALLED_APPS in the settings.py file (following the order below)

```python
    ...
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    ...
```

Now, as we don't want to make the variables and keys of our accounts public, we need to create a .env file in the root of our project.

```python
import os
os.environ['CLOUDINARY_URL'] = 'cloudinary://YOUR_CLOUDINARY_URL'
```

Then, we need to add the following lines to the settings.py file

```python
from pathlib import Path
import os

if os.path.exists('env.py'):
    import env

# Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')
}

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```
The MEDIA_URL is the URL where the images will be stored by Django. In this case, we will use the default one, which is /media/

## Creating the apps

Now, we need to create the apps that we will use in our project. In this case, we will create the following apps:

- profiles
- posts
- comments
- likes

To create an app, we need to run the following command

```bash
python3 manage.py startapp <app_name>
```

Then, we need to add the app to the INSTALLED_APPS in the settings.py file

```python
    ...
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'profiles',
    'posts',
    'comments',
    'likes',
    ...
```

### Profiles app

This app will be used to manage the users of the Positive Social Network. We will use the default Django User model, but we will add some extra fields to it.

Then, we need to add the app to the INSTALLED_APPS in the settings.py file

```python
    ...
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'profiles',
    'posts',
    'comments',
    'likes',
    ...
```

The profiles will have the following fields:

- owner
- name
- created_at
- updated_at
- content
- image

After creating the model, we need to create a signals.py file in the profiles app.

Signals are just pieces of code that are executed when a certain action is performed or there is an event. In this case, we want to create a profile for each user that is created.

```python
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)

post_save.connect(create_profile, sender=User)
```

Basically, we are saying that when a user is created, we want to create a profile for that user. Remember, a user is not the same as a profile. A user is the one that logs in, and a profile is the one that is shown in the social network.

Make migrations and migrate

Remember to add the Profile to your admin panel, and a superuser to be able to log in.
All this was covered in my previous project, [The WC](https://github.com/Parbelaez/ci_fsd_pp4_the_wc/blob/main/README.md).


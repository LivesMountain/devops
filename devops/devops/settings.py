import os
import sys
#加入conf
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from conf import config as CONFIG

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#加入工作app的路径
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))
DEBUG = CONFIG.DEBUG

print(DEBUG)
print(sys.path)
APPS_DIR = os.path.join(BASE_DIR, 'apps')

print("...............................",BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in  production secret!
SECRET_KEY = 'pcb$c!_6luzanqhscf7fb&-sk7=0ba44bhy^h^u$t5=3$8xi=a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.DEBUG or False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'apps.ServerAccount',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'devops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'devops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
<<<<<<< HEAD
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'devops',
        'USER':'root',
        'PASSWORD':'Wangxiaobao,123456',
        'HOST':'172.17.17.3',
        'PORT':'3306',
=======
        'ENGINE': 'django.db.backends.{}'.format(CONFIG.DB_ENGINE),
        'NAME': CONFIG.DB_NAME,
        'USER':CONFIG.DB_USER,
        'PASSWORD':CONFIG.DB_PASSWORD,
        'HOST':CONFIG.DB_HOST,
        'PORT':CONFIG.DB_PORT,
>>>>>>> 修改用户表
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
CRONJOBS = [
    ('*/1 * * * *', 'apps.ServerAccount.cron.my_scheduled_job'),
]
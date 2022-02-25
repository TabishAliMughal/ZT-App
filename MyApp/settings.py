import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'dd^d35%b(x!ee+rnaewa_(l9#++ke@uh^gmwu6=eyt30ft^*jv'

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # {'NAME':'Authentication', 'DEFAULT_DB': 'zt_app_data'},
    # {'NAME':'Main', 'DEFAULT_DB': 'zt_app_data'},
    # {'NAME':'Creator', 'DEFAULT_DB': 'zt_app_data'},
    # {'NAME':'Shop.Shop', 'DEFAULT_DB': 'zt_shop_data'},
    # {'NAME':'Shop.Cart', 'DEFAULT_DB': 'zt_shop_data'},
    # {'NAME':'Shop.Orders', 'DEFAULT_DB': 'zt_shop_data'},
    # {'NAME':'Shop.Customer', 'DEFAULT_DB': 'zt_shop_data'},
    # {'NAME':'Shop.Delivery', 'DEFAULT_DB': 'zt_shop_data'},
    # {'NAME':'Shop.Accounts', 'DEFAULT_DB': 'zt_shop_data'},
    # {'NAME':'Blog.Blog', 'DEFAULT_DB': 'zt_blog_data'},
    # {'NAME':'Blog.Bunch', 'DEFAULT_DB': 'zt_blog_data'},
    # {'NAME':'Blog.Post', 'DEFAULT_DB': 'zt_blog_data'},
    # {'NAME':'School.School', 'DEFAULT_DB': 'db1'},
    # {'NAME':'Relationships.Info', 'DEFAULT_DB': 'zt_matrinomial_data'},
    # {'NAME':'Relationships.Matching', 'DEFAULT_DB': 'zt_matrinomial_data'},
    'Authentication',
    'Main',
    'Creator',
    'Shop.Shop',
    'Shop.Cart',
    'Shop.Orders',
    'Shop.Customer',
    'Shop.Delivery',
    'Shop.Accounts',
    'Blog.Blog',
    'Blog.Bunch',
    'Blog.Post',
    'School.School',
    'Relationships.Info',
    'Relationships.Matching',
    'Relationships.Candidate',
    'social_django',
    'mapwidgets',
    'geocoder',
    'storages',
    'import_export',
]

SOCIAL_AUTH_FACEBOOK_KEY = '154485483318786' # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '6878449e81a93b8b55feeae65fc8efae' # Facebook App Secret

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '792973645164-72jeaeme574usd1h671vp0kmnahtuph4.apps.googleusercontent.com' # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'L6yMwg-1DkATJujbY0uIAHwh' # Google Consumer Secret

MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocationName", "karachi"),
        ("GooglePlaceAutocompleteOptions", {'componentRestrictions': {'country': 'pakistan'}}),
        ("markerFitZoom", 12),
    ),
    "GOOGLE_MAP_API_KEY": "AIzaSyBgzluEvlveyfNKaigwEClXvhSaUyTmLLI"
}

GOOGLE_MAPS_API_KEY =  "AIzaSyBgzluEvlveyfNKaigwEClXvhSaUyTmLLI"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MyApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Main/templates/Includes')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'Shop.Cart.context_processors.cart',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

WSGI_APPLICATION = 'MyApp.wsgi.application'

DATABASES = {
    'blog': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'zt_blog_data',
        'USER': 'comsoft',
        'PASSWORD': 'Comsoft',
        'HOST': '127.0.0.1' ,
        'PORT': '5432' ,
    },
    'matrinomial': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'zt_matrinomial_data',
        'USER': 'comsoft',
        'PASSWORD': 'Comsoft',
        'HOST': '127.0.0.1' ,
        'PORT': '5432' ,
    },
    'shop': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'zt_shop_data',
        'USER': 'comsoft',
        'PASSWORD': 'Comsoft',
        'HOST': '127.0.0.1' ,
        'PORT': '5432' ,
    },
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'zt_app_data',
        'USER': 'comsoft',
        'PASSWORD': 'Comsoft',
        'HOST': '127.0.0.1' ,
        'PORT': '5432' ,
    },
}

DATABASE_ROUTERS = [
    'MyApp.routers.BlogRouter',
    'MyApp.routers.MatronomialRouter',
    'MyApp.routers.ShopRouter',
    'MyApp.routers.AuthRouter',
    ]

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AWS_ACCESS_KEY_ID = 'AKIAZBPKQPWOCBNQ5M55'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'zt-storage'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.ap-south-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'MyApp.storage_backends.MediaStorage'

SESSION_EXPIRE_SECONDS = 1500  # 1500 seconds = 25 minutes

SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'Authentication.Authentication.EmailAuthBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ztapp000@gmail.com'
EMAIL_HOST_PASSWORD = 'ZT-App@123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

SECURE_SSL_REDIRECT = True

CART_SESSION_ID = 'cart'


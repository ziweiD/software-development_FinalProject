# Baggage recovery Application for United

## Getting Started
Requires:
* Git
* Python3 (including package: Pillow, imageHash, openCV, numpy)
* Django2
* PostgreSQL >=10.0.0
* pgAdmin 4

0. Install Pillow, imageHash, openCV, numpy
```
pip3 install Pillow
pip3 install imageHash
pip3 install openCV-Python
pip3 install numpy
```

1. Clone the repo with

```
git clone https://github.com/SuperFeed/SuperFeed
```

2. Setup database
* Open pgAdmin 4 and connect to your PostgreSQL. Add a database named "United_Baggage_Manager".
* Change the settings.py with your username and password:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'United_Baggage_Manager',
        'USER': 'postgres',
        'PASSWORD': your password,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Migrate DB
```
python3 manage.py makemigrations
python3 manage.py migrate
```

4. Import data
```
python3 import_data.py
```

5. Run server
```
python3 manage.py runserver
```


# Proyecto -> Ecommerce.
# Config .env
### dev
SECRET_KEY_DEV = secret_key

DEBUG_DEV = True

ALLOWED_HOSTS_DEV = 127.0.0.1,localhost,my_web.com

DB_ENGINE_DEV = engine_db

DB_NAME_DEV = name_db

DB_USER_DEV = user_db

DB_PASSWORD_DEV = pw_db

HOST_DEV = host_db

PORT_DEV = port_db

### qas
SECRET_KEY_QAS = secret_key

DEBUG_QAS = False

ALLOWED_HOSTS_QAS = 127.0.0.1,localhost,my_web.com

DB_ENGINE_QAS = engine_db

DB_NAME_QAS = name_db

DB_USER_QAS = user_db

DB_PASSWORD_QAS = pw_db

HOST_QAS = host_db

PORT_QAS = port_db

### prd
SECRET_KEY_PRD = secret_key

DEBUG_PRD = False

ALLOWED_HOSTS_PRD = 127.0.0.1,localhost,my_web.com

DB_ENGINE_PRD = engine_db

DB_NAME_PRD = name_db

DB_USER_PRD = user_db

DB_PASSWORD_PRD = pw_db

HOST_PRD = host_db

PORT_PRD = port_db

# Config  and execute django - in window
## 1. Instalar python y pip en el equipo.
### -> Instalar python y pip.
## 2. Crear venv con pip.
### -> python -m venv nombre_del_entorno
## 3. Activar venv.
### -> .\venv\Scripts\activate
## 4. Instalar los requerimientos.
### -> pip install -r requirements.txt
## 5. Generar secret_key (fomar web) y pegar en el .env en la variable SECRET_KEY_DEV.
### -> https://djecrety.ir/
## 6. Generar secret_key (fomar console) y pegar en el .env en la variable SECRET_KEY_DEV.
### -> py -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
### -> py generar_secret_key.py
## 7. Ejecutar makemigrations.
### -> py manage.py makemigrations
## 8. Ejecutar migrate.
### -> py manage.py migrate
## 9. Crear el superuser.
### -> py manage.py createsuperuser
## 10. Limpiar la base de datos (opcional en desarrollo).
### -> py manage.py flush
## 11. Ver todas las rutas (URLs) registradas.
### -> py manage.py show_urls
## 12. Ejecutar el proyecto.
### -> py manage.py runserver
## 13. Desativar el venv.
### -> deactivate
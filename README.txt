CURSO PRO - 29/11/2020


django comands

======================== Crear Entorno ==============================
python -m venv 'name'
pip install -r requirements.txt
pip freeze


==================== Crear base de datos =============================
shell postgresql

username=postgres;
pass=rafa2020;

CREATE DATABASE blodbd;
CREATE USER rafa;
\c blogdb;
ALTER ROLE rafa WITH PASSWORD 'rafa2020';

# Sacar respaldos de la base de datos
python manage.py dumpdata

# Cargar respaldo a la base de datos
python manage.py loaddata name.json


======================== Instalar paquetes ============================
pip install name
pip install django


=======================cls= Crear Proyecto =============================
django-admin startproject name


======================== Crear App ==================================
# Crear carpeta 'applications', movernos ahí
django-admin startapp mame


======================== Ejecutar Servidor ==========================
python manage.py runserver


======================== Actualizar pip =============================
python -m pip install --upgrade pip


======================== Crear Tablas ===============================
# Cada que se afecte la base de datos ejecutar
python manage.py makemigrations
python manage.py migrate


======================== Crear SuperUsuario =========================
python manage.py createsuperuser




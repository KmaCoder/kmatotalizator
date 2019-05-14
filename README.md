# KmaTotalizator
> 3rd year course work, NaUKMA, Faculty of Informatics, Software Engineering, created by **Nesterov Maksym**

### Setup project
* Make sure that you have installed Python 3 and PostgreSQL.
* Create file `.env` in the root of project folder for configuring DB and Secret Key. Example:
```
SECRET_KEY='secret_key_example'
DB_HOST='localhost'
DB_USER='db_user'
DB_NAME='kmatotalizator_db'
DB_PASS='db_pass'
DB_PORT='5432'
```
* Install requirements `pip install -r requirements.txt`
* Install bower requirements `bower i`

### Run
Run application with `python3 run.py`
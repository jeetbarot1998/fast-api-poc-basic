from dotenv import find_dotenv, load_dotenv
import os

dot_env = find_dotenv()
load_dotenv(dot_env)

host = os.environ['HOST']
port = os.environ['PORT']
user = os.environ['USER']
passwd = os.environ['PASSWD']
database_name = os.environ['DATABASE_NAME']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']


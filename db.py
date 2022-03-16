from pymongo import MongoClient
from env import env_variables
# db 설정
# dev
client = MongoClient("localhost", 27017)
# production
# client = MongoClient(f'mongodb://{env_variables["DB_ID"]}{env_variables["DB_PW"]}@0.0.0.0:27017')
db = client.sunny

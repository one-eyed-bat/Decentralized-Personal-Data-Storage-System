import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SESSION_PERMANENT=False
    print(basedir)

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'the-default-unsafe-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                    'sqlite:///' + os.path.join(basedir, 'app.db')
    IPFS_HOST = '127.0.0.1'
    IPFS_PORT = 5001
    IPFS_HTTP_CLIENT = f'/ip4/{IPFS_HOST}/tcp/{IPFS_PORT}/http'
    URI = os.environ.get('MONGODB_URI') 
    CLIENT = MongoClient(URI, server_api=ServerApi('1'))


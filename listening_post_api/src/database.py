import mongoengine

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_NAME = 'request'

def start():
    mongoengine.connect(
        db=MONGODB_NAME, 
        host=MONGODB_HOST, 
        port=MONGODB_PORT
    )


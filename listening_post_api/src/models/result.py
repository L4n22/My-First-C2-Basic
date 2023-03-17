import uuid
from mongoengine import Document, \
    UUIDField, \
    StringField, \
    BooleanField

    

class Result(Document):
    result_id = UUIDField(
        default=lambda: uuid.uuid4().hex,
        binary=False)

    meta = {
        'collection': 'results'
    }

    success = BooleanField(required=True)
    task_uuid = UUIDField(binary=False, required=True)
    result = StringField(required=True)
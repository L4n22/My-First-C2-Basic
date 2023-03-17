import uuid
from mongoengine import DynamicDocument, \
    fields


class Task(DynamicDocument):
    task_uuid = fields.UUIDField(
        default=lambda: uuid.uuid4(),
        binary=False)
    
    task_type = fields.IntField(required=True)
    #task_options = fields.DictField(default={})
    #task_key = fields.StringField(required=True)

    meta = {
        'collection': 'tasks'
    }
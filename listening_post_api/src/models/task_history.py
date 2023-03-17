from mongoengine import Document, fields


class TaskHistory(Document):
    meta = {
        'collection': 'task_history'
    }

    task_uuid = fields.UUIDField(binary=False, required=True)
    task_type = fields.IntField(required=True)
    task_result = fields.StringField(required=True)

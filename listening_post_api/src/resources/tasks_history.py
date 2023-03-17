from flask_restful import Resource
from flask import request, json
from flask import json, make_response
from models.task_history import TaskHistory

class TasksHistory(Resource):
    def get(self):
        task_history_json = TaskHistory.objects().to_json()
        response = make_response(task_history_json, 200)
        response.headers['Content-Type'] = 'application/json'
        return response
from flask_restful import Resource
from flask import json, make_response
from flask import request
from mongoengine import ValidationError, FieldDoesNotExist

from models.task import Task


class Tasks(Resource):
    def __init__(self):
      self.tasks = []

    def get(self):
      tasks_json = Task.objects().to_json()
      response = make_response(tasks_json, 200)
      response.headers['Content-Type'] = 'application/json'
      return response
    
    def post(self):
      if not request.is_json:
        return make_response(
          json.jsonify({'error': 'Only JSON data is accepted.'}),
          400)

      self._add_task_to_list()
      self._save_tasks_to_db()
      tasks_json = self._get_tasks_to_json()
      response = make_response(tasks_json, 200)
      response.headers['Content-Type'] = 'application/json'
      return response

    def _get_tasks_to_json(self):
      tasks_json = []
      for i in range(len(self.tasks)):
        task_dict = json.loads(self.tasks[i].to_json())
        tasks_json.append(task_dict)

      return tasks_json

    def _add_task_to_list(self):
      tasks_json = request.get_json()
      for i in range(len(tasks_json)):
        try:
            task = Task(**tasks_json[i])
            task.validate()
            self.tasks.append(task)

        except (ValidationError, FieldDoesNotExist):
            continue
      
    def _save_tasks_to_db(self):
      for i in range(len(self.tasks)):
        self.tasks[i].save()
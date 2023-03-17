from flask_restful import Resource
from flask import request, json, jsonify, make_response
from mongoengine import ValidationError, FieldDoesNotExist
from models.result import Result
from models.task import Task
from models.task_history import TaskHistory


class Results(Resource):
    def __init__(self):
        self.results = []

    def get(self):
        results_json = Result.objects().to_json()
        response = make_response(results_json, 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    def post(self):
        if not request.is_json:
            return make_response(
                json.jsonify({'error': 'Only JSON data is accepted.'}),
                400)
        
        self._add_result_to_list()
        self._add_result_to_db()
        self._add_task_to_taskhistory()
        self._delete_completed_tasks()

        if not self._were_all_results_saved():
            return make_response(jsonify({
                "success": "false", 
                "message": "Some results were not saved."})
                , 400)
        
        return make_response(
            jsonify({ "success": "true", "message": "All results have been stored correctly."}),
            200)
        

    def _were_all_results_saved(self):
        return len(self.results) == len(request.get_json()) and len(request.get_json()) != 0


    def _add_result_to_list(self):
      results_json = request.get_json()
      for i in range(len(results_json)):
        try:
            result = Result(**results_json[i])
            result.validate()
            result_json = results_json[i]
            if (self._is_valid_result(result_json)):
                self.results.append(result)

        except (ValidationError, FieldDoesNotExist):
            continue

    def _is_valid_result(self, result_json):
        found = len(Task.objects().filter(
            task_uuid=result_json.get('task_uuid'))) != 0
            
        return found

    def _add_task_to_taskhistory(self):
        tasks = Task.objects()
        for i in range(len(self.results)):
            result_json = json.loads(self.results[i].to_json())
            task = tasks.get(task_uuid=result_json.get('task_uuid'))
            task_json = json.loads(task.to_json())
            TaskHistory(
                task_uuid=task_json['task_uuid'],
                task_type=task_json['task_type'],
                task_result=result_json['result']).save()

    def _delete_completed_tasks(self):
        for i in range(len(self.results)):
            result_json = json.loads(self.results[i].to_json())
            task = Task.objects().get(task_uuid=result_json['task_uuid'])
            task.delete()

    def _add_result_to_db(self):
        for i in range(len(self.results)):
            self.results[i].save()
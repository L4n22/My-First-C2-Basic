from flask import Flask
from flask_restful import Api
import database
from resources.tasks import Tasks
from resources.results import Results
from resources.tasks_history import TasksHistory

app = Flask(__name__)
api = Api(app)

api.add_resource(Tasks, '/api/tasks')
api.add_resource(Results, '/api/results')
api.add_resource(TasksHistory, '/api/tasks_history')


if __name__ == '__main__':
    database.start()
    app.run(debug=True)
import click
import requests
import pprint
import json

from task_type import TaskType

SERVER_URL = "http://127.0.0.1:5000"


def get_resource_api(url):
    response = requests.get(url) 
    return json.loads(response.text)


def format_json(json_data):
    format = ""
    for data in json_data:
        for key, value in data.items():
            format += key + ": " + str(value).rstrip() + "\n"

        format += "\n"

    return format


def post_resource_api(url, data):
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.text


@click.group()
def app_cli():
    pass


@click.command(name="list_tasktype")
def list_tasktype():
    click.echo()
    click.echo(TaskType.get_options())


@click.command(name="list_tasks")
def list_tasks():
    API_ENDPOINT = "/api/tasks"
    url = SERVER_URL + API_ENDPOINT
    json_tasks = get_resource_api(url=url)
    pending_tasks = "\n" * 2 + "[PENDING TASKS]" + "\n" * 2
    pending_tasks += format_json(json_tasks)
    click.echo(pending_tasks)


@click.command(name="list_results")
def list_results():
    API_ENDPOINT = "/api/results"
    url = SERVER_URL + API_ENDPOINT
    json_results = get_resource_api(url=url)
    results = "\n" * 2 + "[RESULTS]" + "\n" * 2 
    results += format_json(json_results)
    click.echo(results)


@click.command(name="list_history")
def list_history():
    API_ENDPOINT = "/api/tasks_history"
    url = SERVER_URL + API_ENDPOINT
    json_task_history = get_resource_api(url=url)
    task_history = "\n" * 2 + "[TASKS HISTORY]" + "\n" * 2 
    task_history += format_json(json_task_history)
    click.echo(task_history)


@click.command(name="add_tasks")
@click.option(
    '--task_id', '-t', 
    multiple=True, 
    required=True, 
    type=click.IntRange(1, len(TaskType)), 
    help='Type of task id to submit.')
@click.option(
    '--options', 
    '-o', 
    multiple=True, 
    help='Key-value options for task.')
def add_tasks(task_id, options):
    API_ENDPOINT = "/api/tasks"
    url = SERVER_URL + API_ENDPOINT
    tasks = []
    for index, type_value in enumerate(task_id):
        task_json = {}
        task_json['task_type'] = type_value
        if index < len(options):        
            _, value_option = options[index].split("=")
            match type_value:
                case TaskType.COMMAND.value:
                    task_json['task_command'] = value_option

                case TaskType.DOWNLOADFILE.value:
                    task_json['task_url'] = value_option

                
        tasks.append(task_json)
        print(tasks)

    response = post_resource_api(url=url, data=tasks)
    click.echo()
    click.echo("Response: " + response)


app_cli.add_command(list_tasktype)
app_cli.add_command(list_tasks)
app_cli.add_command(list_results)
app_cli.add_command(list_history)
app_cli.add_command(add_tasks)


if __name__ == '__main__':
    app_cli()
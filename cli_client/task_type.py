from enum import Enum
from prettytable import PrettyTable

class TaskType(Enum):
    COMMAND = 1
    DOWNLOADFILE = 2

    @classmethod
    def get_options(cls):
        options = {
            "COMMAND": "command=<COMMAND HERE>",
            "DOWNLOADFILE": ""
        }

        table = PrettyTable()
        table.field_names = ["ID", "TASK TYPE", "OPTIONS"]
        task_number = 1
        for command, option in options.items():
            table.add_row([task_number, command, option])
            task_number += 1

        return table

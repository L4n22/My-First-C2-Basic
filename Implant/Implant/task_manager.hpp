#ifndef TASKMANAGER_HPP
#define TASKMANAGER_HPP

#include <future>
#include <cpr/cpr.h>
#include <boost/property_tree/json_parser.hpp>
#include <nlohmann/json.hpp>

#include "config.hpp"
#include "task.hpp"
#include "task_command.hpp"

class TaskManager {

public:
    TaskManager() {};

    void processTasks();
    
    ~TaskManager() {
        for (auto& task : this->tasks) {
            task.reset();
        }
    }

private:
    std::vector<std::unique_ptr<Task>> tasks;

    void addNewTasks(boost::property_tree::ptree& tasksTree);

    void requestTasks();
    
    void executeTasks();

    void sendTaskResults();

    bool checkTasksPending();

    std::unique_ptr<Task> createTask(const std::pair<const std::string,
        boost::property_tree::ptree>& taskTree);
};

#endif
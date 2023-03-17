#include "task_manager.hpp"


void TaskManager::requestTasks()
{
	std::string urlTasks = Config::URL_SERVER + Config::PATH_TASKS;
	auto tasksResponse = cpr::GetAsync(cpr::Url{ urlTasks }).get();
	std::stringstream tasksJson(tasksResponse.text);
	boost::property_tree::ptree tasksTree;
	boost::property_tree::read_json(tasksJson, tasksTree);
	this->addNewTasks(tasksTree);
}


void TaskManager::executeTasks()
{	
	std::vector<std::future<void>> futures;
	for (auto& task : this->tasks) {
		futures.emplace_back(std::async(std::launch::async, [&task]() {
			task->execute();
		}));
	}

	while (!std::all_of(futures.begin(),
		futures.end(), 
		[](const std::future<void>& f) { 
			return f.wait_for(std::chrono::seconds(0)) == std::future_status::ready; 
		})) {
		
		std::this_thread::sleep_for(std::chrono::milliseconds(100));
	}
}


void TaskManager::sendTaskResults()
{
	nlohmann::json results = nlohmann::json::array();
	for (const auto& task : this->tasks) {
		nlohmann::json taskJson = nlohmann::json::parse(task->getResult());
		results.push_back(taskJson);
	}

	std::string urlResults = Config::URL_SERVER + Config::PATH_RESULTS;

	cpr::AsyncResponse response = cpr::PostAsync(
		cpr::Url{ urlResults },
		cpr::Body{ results.dump() },
		cpr::Header{ {"Content-Type", "application/json"} }
	);
	
	this->tasks.clear();
	results.clear();
}

bool TaskManager::checkTasksPending()
{
	return !this->tasks.empty();
}


void TaskManager::processTasks() {
	if (!this->checkTasksPending()) {
		this->requestTasks();
	}
	else {
		this->executeTasks();
		this->sendTaskResults();
	}
}


void TaskManager::addNewTasks(boost::property_tree::ptree& tasksTree)
{
	for (const auto& taskTree : tasksTree) {
		std::unique_ptr<Task> task = this->createTask(taskTree);
		if (task == nullptr) {
			continue;
		}

		this->tasks.push_back(std::move(task));
	}
}


std::unique_ptr<Task> TaskManager::createTask(
	const std::pair<const std::string, 
		boost::property_tree::ptree> &taskTree)
{
	std::string taskUUID = taskTree.second.get<std::string>("task_uuid");
	int taskTypeInt = taskTree.second.get<int>("task_type");
	Task::Type taskType = static_cast<Task::Type>(taskTypeInt);
	std::unique_ptr<Task> task = nullptr;
	if (taskType == Task::Type::COMMAND) {
		std::string taskCommand = taskTree.second.get<std::string>("task_command");
		task = std::make_unique<TaskCommand>(taskUUID, taskCommand);
	}
	else if (taskType == Task::Type::DOWNLOADFILE) {
		//std::string taskURL = taskTree.second.get<std::string>("task_url");
		//task = std::make_unique<TaskDownloadFile>(taskUUID, taskURL);
	}

	return task;
}

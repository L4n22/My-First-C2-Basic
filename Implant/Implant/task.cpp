#include "task.hpp"


void Task::setResult(std::string result)
{
    boost::property_tree::ptree resultree;
    resultree.put("task_uuid", this->uuid);
    resultree.put("result", result);
    resultree.put("success", this->success);
    std::stringstream resultStream;
    boost::property_tree::write_json(resultStream, resultree);
    this->result = resultStream.str();
}


void Task::setSuccess(bool success)
{
    this->success = success;
}


std::string Task::getResult()
{
    return this->result;
}

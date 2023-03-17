#include "task_command.hpp"



void TaskCommand::execute() {
    std::string result = "";
    try {
        std::array<char, 128> buffer;
        std::string commandResult = "";
        std::unique_ptr<FILE, decltype(&_pclose)> pipe(_popen(this->command.c_str(), "r"), _pclose);
        if (!pipe) {
            throw std::runtime_error("popen() failed!");
        }

        while (fgets(buffer.data(), sizeof(buffer), pipe.get()) != nullptr) {
            commandResult += buffer.data();
        }
        
        this->setSuccess(true);
        result = commandResult;
    }
    catch (const std::exception& e) {
        this->setSuccess(false);
        result = e.what();
    }

    this->setResult(result);
}

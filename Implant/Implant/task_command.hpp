#ifndef TASK_COMMAND_HPP
#define TASK_COMMAND_HPP

#include "task.hpp"
#include <array>



class TaskCommand : public Task {
	public:
		TaskCommand(const std::string& uuid,
			const std::string& command) : Task(uuid), command(command) {}

		void execute() override;

	private:
		std::string command;
};

#endif

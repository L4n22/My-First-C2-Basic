#ifndef TASK_HPP
#define TASK_HPP

#include <string>
#include <boost/property_tree/json_parser.hpp>

class Task {
	public:
		enum class Type {
			COMMAND = 1,
			DOWNLOADFILE = 2
		};

		Task(const std::string& uuid) : uuid(uuid) {}
		
		virtual void execute() = 0;

		void setResult(std::string result);

		void setSuccess(bool success);

		std::string getResult();
		
	private:
		std::string uuid;
		std::string result;
		bool success = false;
};

#endif

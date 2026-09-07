#pragma once
#include <string>
#include <utility>

using namespace std;

// Customer: Holds customer contact and identity information
class Customer {
private:
    string name;
    string phone;

public:
    Customer() noexcept : name("Guest"), phone("") {}

    explicit Customer(string name, string phone)
        : name(move(name)), phone(move(phone)) {}

    const string& getName() const noexcept {
        return this->name;
    }

    const string& getPhone() const noexcept {
        return this->phone;
    }
};

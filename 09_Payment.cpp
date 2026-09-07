#pragma once
#include <string>

using namespace std;

// Payment: Abstract strategy interface for payment processors
class Payment {
public:
    virtual ~Payment() = default;

    virtual bool pay(double amount) = 0;
    virtual const char* getPaymentMethodName() const noexcept = 0;
};

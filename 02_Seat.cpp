#pragma once
#include <string>
#include <utility>

using namespace std;

enum class SeatType {
    SILVER,
    GOLD,
    PLATINUM
};

// Seat: Represents a physical chair in an auditorium with fixed tier & number
class Seat {
private:
    string seatNumber;
    SeatType seatType;

public:
    Seat() noexcept : seatNumber(""), seatType(SeatType::SILVER) {}

    explicit Seat(string seatNumber, SeatType seatType)
        : seatNumber(move(seatNumber)), seatType(seatType) {}

    const string& getSeatNumber() const noexcept {
        return this->seatNumber;
    }

    SeatType getSeatType() const noexcept {
        return this->seatType;
    }

    const char* getTypeName() const noexcept {
        switch (this->seatType) {
            case SeatType::SILVER:   return "SILVER";
            case SeatType::GOLD:     return "GOLD";
            case SeatType::PLATINUM: return "PLATINUM";
            default:                 return "UNKNOWN";
        }
    }
};

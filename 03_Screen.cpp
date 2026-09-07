#pragma once
#include <string>
#include <vector>
#include <utility>
#include "02_Seat.cpp"

using namespace std;

// Screen: Auditorium screen that owns its physical Seat collection
class Screen {
private:
    int screenNumber;
    string screenName;
    vector<Seat> seats;

public:
    Screen() noexcept : screenNumber(0), screenName("") {}

    explicit Screen(int screenNumber, string screenName)
        : screenNumber(screenNumber), screenName(move(screenName)) {}

    void reserveSeats(size_t capacity) {
        this->seats.reserve(capacity);
    }

    void addSeat(const string& seatNumber, SeatType seatType) {
        this->seats.emplace_back(seatNumber, seatType);
    }

    int getScreenNumber() const noexcept {
        return this->screenNumber;
    }

    const string& getScreenName() const noexcept {
        return this->screenName;
    }

    const vector<Seat>& getSeats() const noexcept {
        return this->seats;
    }

    int getTotalSeats() const noexcept {
        return static_cast<int>(this->seats.size());
    }
};

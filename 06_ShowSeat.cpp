#pragma once
#include <string>
#include "02_Seat.cpp"

using namespace std;

enum class SeatStatus {
    AVAILABLE,
    BOOKED
};

// ShowSeat: Tracks the per-screening availability status (AVAILABLE/BOOKED) of a seat
class ShowSeat {
private:
    const Seat* physicalSeat;
    SeatStatus seatStatus;

public:
    ShowSeat() noexcept : physicalSeat(nullptr), seatStatus(SeatStatus::AVAILABLE) {}

    explicit ShowSeat(const Seat* seat) noexcept 
        : physicalSeat(seat), seatStatus(SeatStatus::AVAILABLE) {}

    bool isAvailable() const noexcept {
        return this->seatStatus == SeatStatus::AVAILABLE;
    }

    bool bookSeat() noexcept {
        if (this->seatStatus == SeatStatus::AVAILABLE) {
            this->seatStatus = SeatStatus::BOOKED;
            return true;
        }
        return false;
    }

    void releaseSeat() noexcept {
        this->seatStatus = SeatStatus::AVAILABLE;
    }

    SeatStatus getStatus() const noexcept {
        return this->seatStatus;
    }

    const string& getSeatNumber() const noexcept {
        static const string emptySeat = "";
        return this->physicalSeat ? this->physicalSeat->getSeatNumber() : emptySeat;
    }

    SeatType getSeatType() const noexcept {
        return this->physicalSeat ? this->physicalSeat->getSeatType() : SeatType::SILVER;
    }

    const char* getTypeName() const noexcept {
        return this->physicalSeat ? this->physicalSeat->getTypeName() : "UNKNOWN";
    }

    const Seat* getPhysicalSeat() const noexcept {
        return this->physicalSeat;
    }
};

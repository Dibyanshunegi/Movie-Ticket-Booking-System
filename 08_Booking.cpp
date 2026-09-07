#pragma once
#include <string>
#include <vector>
#include "05_Show.cpp"
#include "07_Customer.cpp"
#include "06_ShowSeat.cpp"

using namespace std;

enum class BookingStatus {
    CONFIRMED,
    FAILED,
    CANCELLED
};

// Booking: Encapsulates confirmed/cancelled ticket transaction records with unique auto-generated IDs
class Booking {
private:
    static int nextBookingId;

    string bookingId;
    const Customer* customer;
    const Show* show;
    vector<ShowSeat*> bookedSeats;
    double totalAmount;
    BookingStatus status;

    static string generateBookingId() {
        return "BK" + to_string(nextBookingId++);
    }

public:
    Booking() noexcept
        : bookingId(""), customer(nullptr), show(nullptr), totalAmount(0.0), status(BookingStatus::FAILED) {}

    explicit Booking(const Customer* customer, const Show* show, const vector<ShowSeat*>& seats, double totalAmount)
        : bookingId(generateBookingId()), customer(customer), show(show), bookedSeats(seats),
          totalAmount(totalAmount), status(BookingStatus::CONFIRMED) {}

    void markConfirmed() noexcept {
        this->status = BookingStatus::CONFIRMED;
    }

    void markFailed() noexcept {
        this->status = BookingStatus::FAILED;
    }

    void markCancelled() noexcept {
        this->status = BookingStatus::CANCELLED;
    }

    const string& getBookingId() const noexcept {
        return this->bookingId;
    }

    const Customer* getCustomer() const noexcept {
        return this->customer;
    }

    const Show* getShow() const noexcept {
        return this->show;
    }

    const vector<ShowSeat*>& getBookedSeats() const noexcept {
        return this->bookedSeats;
    }

    double getTotalAmount() const noexcept {
        return this->totalAmount;
    }

    BookingStatus getStatus() const noexcept {
        return this->status;
    }

    const char* getStatusName() const noexcept {
        switch (this->status) {
            case BookingStatus::CONFIRMED: return "CONFIRMED";
            case BookingStatus::FAILED:    return "FAILED";
            case BookingStatus::CANCELLED: return "CANCELLED";
            default:                       return "UNKNOWN";
        }
    }
};

int Booking::nextBookingId = 1001;

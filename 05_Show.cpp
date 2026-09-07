#pragma once
#include <string>
#include <vector>
#include <utility>
#include "01_Movie.cpp"
#include "03_Screen.cpp"
#include "06_ShowSeat.cpp"

using namespace std;

// Show: Scheduled movie screening on a specific screen at a start time
class Show {
private:
    int showId;
    string startTime;
    const Movie* movie;
    const Screen* screen;
    vector<ShowSeat> showSeats;

public:
    Show() noexcept : showId(0), startTime(""), movie(nullptr), screen(nullptr) {}

    explicit Show(int showId, const Movie* movie, const Screen* screen, string startTime)
        : showId(showId), startTime(move(startTime)), movie(movie), screen(screen) {
        if (this->screen != nullptr) {
            const auto& physicalSeats = this->screen->getSeats();
            this->showSeats.reserve(physicalSeats.size());
            for (const auto& physicalSeat : physicalSeats) {
                this->showSeats.emplace_back(&physicalSeat);
            }
        }
    }

    int getShowId() const noexcept {
        return this->showId;
    }

    const Movie* getMovie() const noexcept {
        return this->movie;
    }

    const Screen* getScreen() const noexcept {
        return this->screen;
    }

    const string& getStartTime() const noexcept {
        return this->startTime;
    }

    const vector<ShowSeat>& getShowSeats() const noexcept {
        return this->showSeats;
    }

    ShowSeat* findShowSeat(const string& seatNumber) noexcept {
        for (auto& showSeat : this->showSeats) {
            if (showSeat.getSeatNumber() == seatNumber) {
                return &showSeat;
            }
        }
        return nullptr;
    }

    const ShowSeat* findShowSeat(const string& seatNumber) const noexcept {
        for (const auto& showSeat : this->showSeats) {
            if (showSeat.getSeatNumber() == seatNumber) {
                return &showSeat;
            }
        }
        return nullptr;
    }

    bool isSeatAvailable(const string& seatNumber) const noexcept {
        const ShowSeat* seat = findShowSeat(seatNumber);
        return (seat != nullptr && seat->isAvailable());
    }

    bool bookSeat(const string& seatNumber) noexcept {
        ShowSeat* seat = findShowSeat(seatNumber);
        return (seat != nullptr) ? seat->bookSeat() : false;
    }

    void releaseSeat(const string& seatNumber) noexcept {
        ShowSeat* seat = findShowSeat(seatNumber);
        if (seat != nullptr) {
            seat->releaseSeat();
        }
    }
};

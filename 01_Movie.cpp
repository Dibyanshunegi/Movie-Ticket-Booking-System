#pragma once
#include <string>
#include <utility>

using namespace std;

// Movie: Manages title, language, and runtime duration metadata
class Movie {
private:
    string title;
    string language;
    int durationMinutes;

public:
    Movie() noexcept : title(""), language(""), durationMinutes(0) {}

    explicit Movie(string title, string language, int durationMinutes)
        : title(move(title)), language(move(language)), durationMinutes(durationMinutes) {}

    const string& getTitle() const noexcept {
        return this->title;
    }

    const string& getLanguage() const noexcept {
        return this->language;
    }

    int getDurationMinutes() const noexcept {
        return this->durationMinutes;
    }
};

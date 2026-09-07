#pragma once
#include <string>
#include <vector>
#include <utility>
#include "03_Screen.cpp"

using namespace std;

// Cinema: Top-level theatre entity managing its auditorium screens
class Cinema {
private:
    string name;
    vector<Screen> screens;

public:
    Cinema() noexcept : name("") {}

    explicit Cinema(string name) : name(move(name)) {}

    void addScreen(const Screen& screen) {
        this->screens.push_back(screen);
    }

    void addScreen(Screen&& screen) {
        this->screens.push_back(move(screen));
    }

    const string& getName() const noexcept {
        return this->name;
    }

    const vector<Screen>& getScreens() const noexcept {
        return this->screens;
    }

    const Screen* getScreen(int screenNumber) const noexcept {
        for (const auto& scr : this->screens) {
            if (scr.getScreenNumber() == screenNumber) {
                return &scr;
            }
        }
        return nullptr;
    }
};

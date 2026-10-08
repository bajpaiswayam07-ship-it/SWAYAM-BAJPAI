#ifndef HISTORY_STACK_HPP
#define HISTORY_STACK_HPP

#include "Song.hpp"
#include <vector>

class HistoryStack {
private:
    std::vector<Song> stack;
    int maxCapacity;

public:
    explicit HistoryStack(int capacity = 100) : maxCapacity(capacity) {}

    void push(const Song& song) {
        // If already at top or exists recently, we still push to track playback sequence
        stack.push_back(song);
        if (static_cast<int>(stack.size()) > maxCapacity) {
            stack.erase(stack.begin()); // remove oldest
        }
    }

    bool pop(Song& outSong) {
        if (stack.empty()) return false;
        outSong = stack.back();
        stack.pop_back();
        return true;
    }

    bool peek(Song& outSong) const {
        if (stack.empty()) return false;
        outSong = stack.back();
        return true;
    }

    int size() const {
        return static_cast<int>(stack.size());
    }

    bool isEmpty() const {
        return stack.empty();
    }

    void clear() {
        stack.clear();
    }

    std::vector<Song> getRecent(int limit = 20) const {
        std::vector<Song> recent;
        int n = static_cast<int>(stack.size());
        int count = (limit < n) ? limit : n;
        for (int i = n - 1; i >= n - count; --i) {
            recent.push_back(stack[i]);
        }
        return recent;
    }
};

#endif // HISTORY_STACK_HPP

#ifndef PLAY_QUEUE_HPP
#define PLAY_QUEUE_HPP

#include "Song.hpp"
#include <deque>
#include <vector>

class PlayQueue {
private:
    std::deque<Song> queue;

public:
    PlayQueue() = default;

    void enqueue(const Song& song) {
        queue.push_back(song);
    }

    bool dequeue(Song& outSong) {
        if (queue.empty()) return false;
        outSong = queue.front();
        queue.pop_front();
        return true;
    }

    bool peek(Song& outSong) const {
        if (queue.empty()) return false;
        outSong = queue.front();
        return true;
    }

    bool removeAt(int index) {
        if (index < 0 || index >= static_cast<int>(queue.size())) return false;
        queue.erase(queue.begin() + index);
        return true;
    }

    int size() const {
        return static_cast<int>(queue.size());
    }

    bool isEmpty() const {
        return queue.empty();
    }

    void clear() {
        queue.clear();
    }

    std::vector<Song> getAll() const {
        return std::vector<Song>(queue.begin(), queue.end());
    }
};

#endif // PLAY_QUEUE_HPP

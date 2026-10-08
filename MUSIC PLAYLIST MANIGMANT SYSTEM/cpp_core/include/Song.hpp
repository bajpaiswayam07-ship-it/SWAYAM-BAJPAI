#ifndef SONG_HPP
#define SONG_HPP

#include <string>
#include <iostream>

struct Song {
    int id;
    std::string title;
    std::string artist;
    std::string album;
    std::string genre;
    int duration;   // in seconds
    int bpm;        // beats per minute
    int playCount;  // total plays
    std::string filePath; // audio file path

    Song()
        : id(0), title("Unknown"), artist("Unknown"), album("Unknown"),
          genre("Pop"), duration(0), bpm(120), playCount(0), filePath("") {}

    Song(int id, const std::string& title, const std::string& artist,
         const std::string& album, const std::string& genre,
         int duration, int bpm, int playCount, const std::string& filePath)
        : id(id), title(title), artist(artist), album(album),
          genre(genre), duration(duration), bpm(bpm),
          playCount(playCount), filePath(filePath) {}
};

#endif // SONG_HPP

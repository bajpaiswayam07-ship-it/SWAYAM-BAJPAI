#ifndef PLAYLIST_MANAGER_HPP
#define PLAYLIST_MANAGER_HPP

#include "Song.hpp"
#include "DoublyLinkedList.hpp"
#include "PlayQueue.hpp"
#include "HistoryStack.hpp"
#include "TrieSearch.hpp"
#include "Sorter.hpp"
#include "RecommendationEngine.hpp"

#include <unordered_map>
#include <string>
#include <vector>
#include <memory>

class PlaylistManager {
private:
    std::unordered_map<int, Song> library;
    std::unordered_map<std::string, DoublyLinkedList> playlists;
    std::string activePlaylistName;
    int currentPlayingIndex;
    int nextSongId;

    PlayQueue playQueue;
    HistoryStack historyStack;
    TrieSearch searchIndex;

public:
    PlaylistManager();
    ~PlaylistManager() = default;

    // Library Operations
    int addSong(const Song& song); // returns assigned ID
    bool removeSong(int songId);
    Song* getSong(int songId);
    std::vector<Song> getAllSongs() const;
    int getLibrarySize() const;

    // Playlist Operations
    bool createPlaylist(const std::string& name);
    bool deletePlaylist(const std::string& name);
    bool hasPlaylist(const std::string& name) const;
    std::vector<std::string> getPlaylistNames() const;

    bool addSongToPlaylist(const std::string& playlistName, int songId);
    bool removeSongFromPlaylist(const std::string& playlistName, int index);
    bool moveSongInPlaylist(const std::string& playlistName, int fromIndex, int toIndex);

    DoublyLinkedList* getPlaylist(const std::string& name);
    int getPlaylistSize(const std::string& name) const;
    Song* getSongAt(const std::string& playlistName, int index);

    // Playback State Navigation
    void setActivePlaylist(const std::string& name);
    std::string getActivePlaylist() const;
    void setCurrentIndex(int index);
    int getCurrentIndex() const;

    Song* getNextSong();
    Song* getPreviousSong();
    Song* getCurrentSong();

    // Queue & History
    void enqueue(int songId);
    bool dequeue(Song& outSong);
    std::vector<Song> getQueue() const;
    void clearQueue();

    void recordPlay(int songId);
    std::vector<Song> getRecentlyPlayed(int limit = 10) const;

    // Search & Recommendations
    std::vector<Song> search(const std::string& query) const;
    std::vector<Song> getRecommendationsForSong(int songId, int count = 5) const;

    // Sorting & Shuffling
    void sortPlaylist(const std::string& playlistName, SortCriteria criteria, bool ascending);
    void shufflePlaylist(const std::string& playlistName);

    // Persistence
    bool saveToFile(const std::string& filePath) const;
    bool loadFromFile(const std::string& filePath);
};

#endif // PLAYLIST_MANAGER_HPP

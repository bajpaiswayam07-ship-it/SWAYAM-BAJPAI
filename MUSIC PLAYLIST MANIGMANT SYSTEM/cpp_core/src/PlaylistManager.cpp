#include "../include/PlaylistManager.hpp"
#include <fstream>
#include <sstream>
#include <iostream>

PlaylistManager::PlaylistManager()
    : activePlaylistName("All Songs"), currentPlayingIndex(-1), nextSongId(1) {
    createPlaylist("All Songs");
    createPlaylist("Favorites");
}

int PlaylistManager::addSong(const Song& s) {
    Song song = s;
    if (song.id <= 0) {
        song.id = nextSongId++;
    } else if (song.id >= nextSongId) {
        nextSongId = song.id + 1;
    }

    library[song.id] = song;
    searchIndex.indexSong(song.id, song.title, song.artist, song.album, song.genre);

    // Also add to "All Songs" master playlist
    playlists["All Songs"].append(song);
    return song.id;
}

bool PlaylistManager::removeSong(int songId) {
    auto it = library.find(songId);
    if (it == library.end()) return false;

    library.erase(it);

    // Remove from all playlists
    for (auto& pair : playlists) {
        pair.second.removeById(songId);
    }

    // Rebuild search index
    searchIndex.clear();
    for (const auto& pair : library) {
        const Song& s = pair.second;
        searchIndex.indexSong(s.id, s.title, s.artist, s.album, s.genre);
    }

    return true;
}

Song* PlaylistManager::getSong(int songId) {
    auto it = library.find(songId);
    if (it != library.end()) {
        return &(it->second);
    }
    return nullptr;
}

std::vector<Song> PlaylistManager::getAllSongs() const {
    std::vector<Song> list;
    list.reserve(library.size());
    for (const auto& pair : library) {
        list.push_back(pair.second);
    }
    return list;
}

int PlaylistManager::getLibrarySize() const {
    return static_cast<int>(library.size());
}

bool PlaylistManager::createPlaylist(const std::string& name) {
    if (name.empty() || playlists.find(name) != playlists.end()) return false;
    playlists[name] = DoublyLinkedList();
    return true;
}

bool PlaylistManager::deletePlaylist(const std::string& name) {
    if (name == "All Songs" || playlists.find(name) == playlists.end()) return false;
    playlists.erase(name);
    if (activePlaylistName == name) {
        activePlaylistName = "All Songs";
        currentPlayingIndex = 0;
    }
    return true;
}

bool PlaylistManager::hasPlaylist(const std::string& name) const {
    return playlists.find(name) != playlists.end();
}

std::vector<std::string> PlaylistManager::getPlaylistNames() const {
    std::vector<std::string> names;
    names.reserve(playlists.size());
    // Put "All Songs" first, "Favorites" second, then the rest
    if (playlists.find("All Songs") != playlists.end()) names.push_back("All Songs");
    if (playlists.find("Favorites") != playlists.end()) names.push_back("Favorites");
    for (const auto& pair : playlists) {
        if (pair.first != "All Songs" && pair.first != "Favorites") {
            names.push_back(pair.first);
        }
    }
    return names;
}

bool PlaylistManager::addSongToPlaylist(const std::string& playlistName, int songId) {
    auto itPl = playlists.find(playlistName);
    auto itSong = library.find(songId);
    if (itPl == playlists.end() || itSong == library.end()) return false;

    itPl->second.append(itSong->second);
    return true;
}

bool PlaylistManager::removeSongFromPlaylist(const std::string& playlistName, int index) {
    auto itPl = playlists.find(playlistName);
    if (itPl == playlists.end()) return false;
    return itPl->second.removeAt(index);
}

bool PlaylistManager::moveSongInPlaylist(const std::string& playlistName, int fromIndex, int toIndex) {
    auto itPl = playlists.find(playlistName);
    if (itPl == playlists.end()) return false;
    return itPl->second.move(fromIndex, toIndex);
}

DoublyLinkedList* PlaylistManager::getPlaylist(const std::string& name) {
    auto it = playlists.find(name);
    if (it != playlists.end()) return &(it->second);
    return nullptr;
}

int PlaylistManager::getPlaylistSize(const std::string& name) const {
    auto it = playlists.find(name);
    if (it != playlists.end()) return it->second.size();
    return 0;
}

Song* PlaylistManager::getSongAt(const std::string& playlistName, int index) {
    auto it = playlists.find(playlistName);
    if (it != playlists.end()) {
        return it->second.get(index);
    }
    return nullptr;
}

void PlaylistManager::setActivePlaylist(const std::string& name) {
    if (playlists.find(name) != playlists.end()) {
        activePlaylistName = name;
        currentPlayingIndex = 0;
    }
}

std::string PlaylistManager::getActivePlaylist() const {
    return activePlaylistName;
}

void PlaylistManager::setCurrentIndex(int index) {
    currentPlayingIndex = index;
}

int PlaylistManager::getCurrentIndex() const {
    return currentPlayingIndex;
}

Song* PlaylistManager::getCurrentSong() {
    return getSongAt(activePlaylistName, currentPlayingIndex);
}

Song* PlaylistManager::getNextSong() {
    // 1. Check if there's anything in playQueue
    Song queuedSong;
    if (playQueue.dequeue(queuedSong)) {
        recordPlay(queuedSong.id);
        // Find in active playlist if present or return pointer
        auto it = library.find(queuedSong.id);
        if (it != library.end()) return &(it->second);
    }

    // 2. Otherwise advance in active playlist
    DoublyLinkedList* pl = getPlaylist(activePlaylistName);
    if (!pl || pl->isEmpty()) return nullptr;

    currentPlayingIndex = (currentPlayingIndex + 1) % pl->size();
    Song* s = pl->get(currentPlayingIndex);
    if (s) recordPlay(s->id);
    return s;
}

Song* PlaylistManager::getPreviousSong() {
    DoublyLinkedList* pl = getPlaylist(activePlaylistName);
    if (!pl || pl->isEmpty()) return nullptr;

    currentPlayingIndex--;
    if (currentPlayingIndex < 0) {
        currentPlayingIndex = pl->size() - 1;
    }
    Song* s = pl->get(currentPlayingIndex);
    if (s) recordPlay(s->id);
    return s;
}

void PlaylistManager::enqueue(int songId) {
    Song* s = getSong(songId);
    if (s) {
        playQueue.enqueue(*s);
    }
}

bool PlaylistManager::dequeue(Song& outSong) {
    return playQueue.dequeue(outSong);
}

std::vector<Song> PlaylistManager::getQueue() const {
    return playQueue.getAll();
}

void PlaylistManager::clearQueue() {
    playQueue.clear();
}

void PlaylistManager::recordPlay(int songId) {
    auto it = library.find(songId);
    if (it != library.end()) {
        it->second.playCount++;
        historyStack.push(it->second);
    }
}

std::vector<Song> PlaylistManager::getRecentlyPlayed(int limit) const {
    return historyStack.getRecent(limit);
}

std::vector<Song> PlaylistManager::search(const std::string& query) const {
    if (query.empty()) return getAllSongs();
    std::vector<int> ids = searchIndex.searchPrefix(query);
    std::vector<Song> results;
    results.reserve(ids.size());
    for (int id : ids) {
        auto it = library.find(id);
        if (it != library.end()) {
            results.push_back(it->second);
        }
    }
    return results;
}

std::vector<Song> PlaylistManager::getRecommendationsForSong(int songId, int count) const {
    auto it = library.find(songId);
    if (it == library.end()) return {};

    std::vector<Song> all = getAllSongs();
    return RecommendationEngine::getRecommendations(it->second, all, count);
}

void PlaylistManager::sortPlaylist(const std::string& playlistName, SortCriteria criteria, bool ascending) {
    auto it = playlists.find(playlistName);
    if (it == playlists.end()) return;

    std::vector<Song> songs = it->second.toVector();
    Sorter::mergeSort(songs, criteria, ascending);

    it->second.clear();
    for (const auto& s : songs) {
        it->second.append(s);
    }
}

void PlaylistManager::shufflePlaylist(const std::string& playlistName) {
    auto it = playlists.find(playlistName);
    if (it != playlists.end()) {
        it->second.shuffle();
    }
}

// Simple JSON helper functions
static std::string escapeJson(const std::string& s) {
    std::ostringstream o;
    for (char c : s) {
        if (c == '"') o << "\\\"";
        else if (c == '\\') o << "\\\\";
        else if (c == '\b') o << "\\b";
        else if (c == '\f') o << "\\f";
        else if (c == '\n') o << "\\n";
        else if (c == '\r') o << "\\r";
        else if (c == '\t') o << "\\t";
        else o << c;
    }
    return o.str();
}

bool PlaylistManager::saveToFile(const std::string& filePath) const {
    std::ofstream file(filePath);
    if (!file.is_open()) return false;

    file << "{\n";
    file << "  \"nextSongId\": " << nextSongId << ",\n";
    file << "  \"songs\": [\n";

    bool firstSong = true;
    for (const auto& pair : library) {
        const Song& s = pair.second;
        if (!firstSong) file << ",\n";
        firstSong = false;
        file << "    {\n"
             << "      \"id\": " << s.id << ",\n"
             << "      \"title\": \"" << escapeJson(s.title) << "\",\n"
             << "      \"artist\": \"" << escapeJson(s.artist) << "\",\n"
             << "      \"album\": \"" << escapeJson(s.album) << "\",\n"
             << "      \"genre\": \"" << escapeJson(s.genre) << "\",\n"
             << "      \"duration\": " << s.duration << ",\n"
             << "      \"bpm\": " << s.bpm << ",\n"
             << "      \"playCount\": " << s.playCount << ",\n"
             << "      \"filePath\": \"" << escapeJson(s.filePath) << "\"\n"
             << "    }";
    }
    file << "\n  ],\n";

    file << "  \"playlists\": {\n";
    bool firstPl = true;
    for (const auto& pair : playlists) {
        if (!firstPl) file << ",\n";
        firstPl = false;
        file << "    \"" << escapeJson(pair.first) << "\": [";
        std::vector<Song> songs = pair.second.toVector();
        for (size_t i = 0; i < songs.size(); ++i) {
            file << songs[i].id;
            if (i + 1 < songs.size()) file << ", ";
        }
        file << "]";
    }
    file << "\n  }\n";
    file << "}\n";

    return true;
}

bool PlaylistManager::loadFromFile(const std::string& filePath) {
    std::ifstream file(filePath);
    if (!file.is_open()) return false;

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string content = buffer.str();

    // Clear current state
    library.clear();
    playlists.clear();
    searchIndex.clear();
    createPlaylist("All Songs");
    createPlaylist("Favorites");

    // Very simple robust parser for our JSON structure
    size_t songArrPos = content.find("\"songs\":");
    if (songArrPos != std::string::npos) {
        size_t start = content.find('[', songArrPos);
        size_t end = content.find(']', start);
        if (start != std::string::npos && end != std::string::npos) {
            std::string songsBlock = content.substr(start, end - start);
            size_t objStart = 0;
            while ((objStart = songsBlock.find('{', objStart)) != std::string::npos) {
                size_t objEnd = songsBlock.find('}', objStart);
                if (objEnd == std::string::npos) break;
                std::string obj = songsBlock.substr(objStart, objEnd - objStart + 1);

                auto getField = [&](const std::string& key) -> std::string {
                    std::string needle = "\"" + key + "\":";
                    size_t pos = obj.find(needle);
                    if (pos == std::string::npos) return "";
                    pos += needle.size();
                    while (pos < obj.size() && (obj[pos] == ' ' || obj[pos] == '\"')) pos++;
                    size_t endPos = pos;
                    while (endPos < obj.size() && obj[endPos] != '\"' && obj[endPos] != ',' && obj[endPos] != '\n' && obj[endPos] != '\r' && obj[endPos] != '}') endPos++;
                    return obj.substr(pos, endPos - pos);
                };

                Song s;
                std::string idStr = getField("id");
                if (!idStr.empty()) s.id = std::stoi(idStr);
                s.title = getField("title");
                s.artist = getField("artist");
                s.album = getField("album");
                s.genre = getField("genre");
                std::string durStr = getField("duration");
                if (!durStr.empty()) s.duration = std::stoi(durStr);
                std::string bpmStr = getField("bpm");
                if (!bpmStr.empty()) s.bpm = std::stoi(bpmStr);
                std::string pcStr = getField("playCount");
                if (!pcStr.empty()) s.playCount = std::stoi(pcStr);
                s.filePath = getField("filePath");

                if (s.id > 0) {
                    addSong(s);
                }
                objStart = objEnd + 1;
            }
        }
    }

    // Parse playlists block
    size_t plPos = content.find("\"playlists\":");
    if (plPos != std::string::npos) {
        size_t plStart = content.find('{', plPos);
        if (plStart != std::string::npos) {
            size_t plEnd = content.find('}', plStart);
            std::string plBlock = content.substr(plStart + 1, plEnd - plStart - 1);
            std::stringstream ss(plBlock);
            std::string line;
            while (std::getline(ss, line)) {
                size_t q1 = line.find('\"');
                if (q1 == std::string::npos) continue;
                size_t q2 = line.find('\"', q1 + 1);
                if (q2 == std::string::npos) continue;
                std::string plName = line.substr(q1 + 1, q2 - q1 - 1);

                createPlaylist(plName);

                size_t arrStart = line.find('[', q2);
                size_t arrEnd = line.find(']', arrStart);
                if (arrStart != std::string::npos && arrEnd != std::string::npos) {
                    std::string idsStr = line.substr(arrStart + 1, arrEnd - arrStart - 1);
                    std::stringstream idSS(idsStr);
                    std::string singleId;
                    while (std::getline(idSS, singleId, ',')) {
                        while (!singleId.empty() && (singleId.front() == ' ' || singleId.front() == '\t')) singleId.erase(0, 1);
                        while (!singleId.empty() && (singleId.back() == ' ' || singleId.back() == '\t')) singleId.pop_back();
                        if (!singleId.empty()) {
                            try {
                                int sId = std::stoi(singleId);
                                if (plName != "All Songs") { // "All Songs" is populated in addSong
                                    addSongToPlaylist(plName, sId);
                                }
                            } catch (...) {}
                        }
                    }
                }
            }
        }
    }

    return true;
}

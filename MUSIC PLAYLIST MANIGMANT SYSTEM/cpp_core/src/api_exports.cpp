#ifndef BUILDING_CORE_DLL
#define BUILDING_CORE_DLL
#endif
#include "../include/api_exports.h"
#include "../include/PlaylistManager.hpp"
#include <cstring>
#include <vector>

static PlaylistManager* g_manager = nullptr;

static void safeCopyString(char* dest, const std::string& src, int maxLen) {
    if (!dest || maxLen <= 0) return;
    int len = static_cast<int>(src.length());
    if (len >= maxLen) len = maxLen - 1;
    std::memcpy(dest, src.c_str(), len);
    dest[len] = '\0';
}

void engine_init() {
    if (!g_manager) {
        g_manager = new PlaylistManager();
    }
}

void engine_destroy() {
    if (g_manager) {
        delete g_manager;
        g_manager = nullptr;
    }
}

int engine_add_song(int id, const char* title, const char* artist,
                    const char* album, const char* genre,
                    int duration, int bpm, int play_count, const char* file_path) {
    if (!g_manager) engine_init();
    Song s(id,
           title ? title : "Unknown",
           artist ? artist : "Unknown",
           album ? album : "Unknown",
           genre ? genre : "Pop",
           duration, bpm, play_count,
           file_path ? file_path : "");
    return g_manager->addSong(s);
}

int engine_remove_song(int song_id) {
    if (!g_manager) return 0;
    return g_manager->removeSong(song_id) ? 1 : 0;
}

int engine_get_library_count() {
    if (!g_manager) return 0;
    return g_manager->getLibrarySize();
}

int engine_get_song_info(int song_id, char* out_title, char* out_artist,
                         char* out_album, char* out_genre,
                         int* out_duration, int* out_bpm, int* out_play_count,
                         char* out_file_path, int max_len) {
    if (!g_manager) return 0;
    Song* s = g_manager->getSong(song_id);
    if (!s) return 0;

    safeCopyString(out_title, s->title, max_len);
    safeCopyString(out_artist, s->artist, max_len);
    safeCopyString(out_album, s->album, max_len);
    safeCopyString(out_genre, s->genre, max_len);
    safeCopyString(out_file_path, s->filePath, max_len);

    if (out_duration) *out_duration = s->duration;
    if (out_bpm) *out_bpm = s->bpm;
    if (out_play_count) *out_play_count = s->playCount;

    return 1;
}

int engine_create_playlist(const char* name) {
    if (!g_manager || !name) return 0;
    return g_manager->createPlaylist(name) ? 1 : 0;
}

int engine_delete_playlist(const char* name) {
    if (!g_manager || !name) return 0;
    return g_manager->deletePlaylist(name) ? 1 : 0;
}

int engine_add_to_playlist(const char* playlist_name, int song_id) {
    if (!g_manager || !playlist_name) return 0;
    return g_manager->addSongToPlaylist(playlist_name, song_id) ? 1 : 0;
}

int engine_remove_from_playlist(const char* playlist_name, int index) {
    if (!g_manager || !playlist_name) return 0;
    return g_manager->removeSongFromPlaylist(playlist_name, index) ? 1 : 0;
}

int engine_move_in_playlist(const char* playlist_name, int from_idx, int to_idx) {
    if (!g_manager || !playlist_name) return 0;
    return g_manager->moveSongInPlaylist(playlist_name, from_idx, to_idx) ? 1 : 0;
}

int engine_get_playlist_count(const char* playlist_name) {
    if (!g_manager || !playlist_name) return 0;
    return g_manager->getPlaylistSize(playlist_name);
}

int engine_get_playlist_song_id(const char* playlist_name, int index) {
    if (!g_manager || !playlist_name) return -1;
    Song* s = g_manager->getSongAt(playlist_name, index);
    return s ? s->id : -1;
}

void engine_set_active_playlist(const char* name) {
    if (!g_manager || !name) return;
    g_manager->setActivePlaylist(name);
}

void engine_get_active_playlist(char* out_buf, int max_len) {
    if (!g_manager) return;
    safeCopyString(out_buf, g_manager->getActivePlaylist(), max_len);
}

void engine_get_playlist_names(char* out_buffer, int max_len) {
    if (!g_manager || !out_buffer || max_len <= 0) return;
    std::vector<std::string> names = g_manager->getPlaylistNames();
    std::string joined;
    for (size_t i = 0; i < names.size(); ++i) {
        joined += names[i];
        if (i + 1 < names.size()) joined += ";";
    }
    safeCopyString(out_buffer, joined, max_len);
}

void engine_set_current_index(int index) {
    if (!g_manager) return;
    g_manager->setCurrentIndex(index);
}

int engine_get_current_index() {
    if (!g_manager) return -1;
    return g_manager->getCurrentIndex();
}

int engine_get_next_song_id() {
    if (!g_manager) return -1;
    Song* s = g_manager->getNextSong();
    return s ? s->id : -1;
}

int engine_get_prev_song_id() {
    if (!g_manager) return -1;
    Song* s = g_manager->getPreviousSong();
    return s ? s->id : -1;
}

int engine_get_current_song_id() {
    if (!g_manager) return -1;
    Song* s = g_manager->getCurrentSong();
    return s ? s->id : -1;
}

void engine_sort_playlist(const char* playlist_name, int criteria, int ascending) {
    if (!g_manager || !playlist_name) return;
    g_manager->sortPlaylist(playlist_name, static_cast<SortCriteria>(criteria), ascending != 0);
}

void engine_shuffle_playlist(const char* playlist_name) {
    if (!g_manager || !playlist_name) return;
    g_manager->shufflePlaylist(playlist_name);
}

void engine_enqueue(int song_id) {
    if (!g_manager) return;
    g_manager->enqueue(song_id);
}

int engine_dequeue() {
    if (!g_manager) return -1;
    Song s;
    if (g_manager->dequeue(s)) return s.id;
    return -1;
}

int engine_get_queue_count() {
    if (!g_manager) return 0;
    return static_cast<int>(g_manager->getQueue().size());
}

int engine_get_queue_ids(int* out_arr, int max_count) {
    if (!g_manager || !out_arr || max_count <= 0) return 0;
    std::vector<Song> q = g_manager->getQueue();
    int limit = std::min(max_count, static_cast<int>(q.size()));
    for (int i = 0; i < limit; ++i) {
        out_arr[i] = q[i].id;
    }
    return limit;
}

void engine_clear_queue() {
    if (!g_manager) return;
    g_manager->clearQueue();
}

void engine_record_play(int song_id) {
    if (!g_manager) return;
    g_manager->recordPlay(song_id);
}

int engine_get_history_ids(int* out_arr, int max_count) {
    if (!g_manager || !out_arr || max_count <= 0) return 0;
    std::vector<Song> hist = g_manager->getRecentlyPlayed(max_count);
    int limit = std::min(max_count, static_cast<int>(hist.size()));
    for (int i = 0; i < limit; ++i) {
        out_arr[i] = hist[i].id;
    }
    return limit;
}

int engine_search(const char* query, int* out_ids, int max_count) {
    if (!g_manager || !out_ids || max_count <= 0) return 0;
    std::vector<Song> found = g_manager->search(query ? query : "");
    int limit = std::min(max_count, static_cast<int>(found.size()));
    for (int i = 0; i < limit; ++i) {
        out_ids[i] = found[i].id;
    }
    return limit;
}

int engine_get_recommendations(int song_id, int* out_ids, int max_count) {
    if (!g_manager || !out_ids || max_count <= 0) return 0;
    std::vector<Song> recs = g_manager->getRecommendationsForSong(song_id, max_count);
    int limit = std::min(max_count, static_cast<int>(recs.size()));
    for (int i = 0; i < limit; ++i) {
        out_ids[i] = recs[i].id;
    }
    return limit;
}

int engine_save_file(const char* file_path) {
    if (!g_manager || !file_path) return 0;
    return g_manager->saveToFile(file_path) ? 1 : 0;
}

int engine_load_file(const char* file_path) {
    if (!g_manager || !file_path) return 0;
    return g_manager->loadFromFile(file_path) ? 1 : 0;
}

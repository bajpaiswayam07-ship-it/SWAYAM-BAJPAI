#ifndef API_EXPORTS_H
#define API_EXPORTS_H

#ifdef _WIN32
    #ifdef BUILDING_CORE_DLL
        #define API_DECL extern "C" __declspec(dllexport)
    #else
        #define API_DECL extern "C" __declspec(dllimport)
    #endif
#else
    #define API_DECL extern "C"
#endif

// Engine lifecycle
API_DECL void engine_init();
API_DECL void engine_destroy();

// Library
API_DECL int engine_add_song(int id, const char* title, const char* artist,
                             const char* album, const char* genre,
                             int duration, int bpm, int play_count, const char* file_path);
API_DECL int engine_remove_song(int song_id);
API_DECL int engine_get_library_count();
API_DECL int engine_get_song_info(int song_id, char* out_title, char* out_artist,
                                  char* out_album, char* out_genre,
                                  int* out_duration, int* out_bpm, int* out_play_count,
                                  char* out_file_path, int max_len);

// Playlists
API_DECL int engine_create_playlist(const char* name);
API_DECL int engine_delete_playlist(const char* name);
API_DECL int engine_add_to_playlist(const char* playlist_name, int song_id);
API_DECL int engine_remove_from_playlist(const char* playlist_name, int index);
API_DECL int engine_move_in_playlist(const char* playlist_name, int from_idx, int to_idx);
API_DECL int engine_get_playlist_count(const char* playlist_name);
API_DECL int engine_get_playlist_song_id(const char* playlist_name, int index);
API_DECL void engine_set_active_playlist(const char* name);
API_DECL void engine_get_active_playlist(char* out_buf, int max_len);
API_DECL void engine_get_playlist_names(char* out_buffer, int max_len);

// Playback navigation
API_DECL void engine_set_current_index(int index);
API_DECL int engine_get_current_index();
API_DECL int engine_get_next_song_id();
API_DECL int engine_get_prev_song_id();
API_DECL int engine_get_current_song_id();

// Algorithms
API_DECL void engine_sort_playlist(const char* playlist_name, int criteria, int ascending);
API_DECL void engine_shuffle_playlist(const char* playlist_name);

// Queue
API_DECL void engine_enqueue(int song_id);
API_DECL int engine_dequeue();
API_DECL int engine_get_queue_count();
API_DECL int engine_get_queue_ids(int* out_arr, int max_count);
API_DECL void engine_clear_queue();

// History
API_DECL void engine_record_play(int song_id);
API_DECL int engine_get_history_ids(int* out_arr, int max_count);

// Search & Recommendations
API_DECL int engine_search(const char* query, int* out_ids, int max_count);
API_DECL int engine_get_recommendations(int song_id, int* out_ids, int max_count);

// Persistence
API_DECL int engine_save_file(const char* file_path);
API_DECL int engine_load_file(const char* file_path);

#endif // API_EXPORTS_H

import ctypes
import os
import sys
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class SongInfo:
    id: int
    title: str
    artist: str
    album: str
    genre: str
    duration: int
    bpm: int
    play_count: int
    file_path: str

    def format_duration(self) -> str:
        mins = self.duration // 60
        secs = self.duration % 60
        return f"{mins}:{secs:02d}"

class CppEngineBridge:
    def __init__(self, dll_path: Optional[str] = None):
        self.is_native = False
        self._dll = None

        if dll_path is None:
            # Look in parent or local dir
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            dll_path = os.path.join(base_dir, "cpp_core", "playlist_core.dll")

        if os.path.exists(dll_path):
            try:
                dll_dir = os.path.dirname(os.path.abspath(dll_path))
                if hasattr(os, 'add_dll_directory'):
                    try:
                        os.add_dll_directory(dll_dir)
                    except Exception:
                        pass
                    # Also add MinGW directory if found in PATH
                    for p in os.environ.get('PATH', '').split(';'):
                        if os.path.isdir(p) and ('mingw' in p.lower() or 'gcc' in p.lower() or 'winlibs' in p.lower()):
                            try:
                                os.add_dll_directory(p)
                            except Exception:
                                pass
                self._dll = ctypes.CDLL(dll_path)
                self._bind_functions()
                self._dll.engine_init()
                self.is_native = True
                print(f"[CppBridge] Successfully loaded native C++ core from: {dll_path}")
            except Exception as e:
                print(f"[CppBridge] Warning: Failed to load DLL ({e}). Falling back to Python DSA core.")
        else:
            print(f"[CppBridge] Warning: DLL not found at {dll_path}. Falling back to Python DSA core.")

        if not self.is_native:
            self._init_python_fallback()

    def _bind_functions(self):
        # engine_init & engine_destroy
        self._dll.engine_init.restype = None
        self._dll.engine_destroy.restype = None

        # engine_add_song
        self._dll.engine_add_song.argtypes = [
            ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
            ctypes.c_char_p, ctypes.c_char_p,
            ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p
        ]
        self._dll.engine_add_song.restype = ctypes.c_int

        # engine_remove_song
        self._dll.engine_remove_song.argtypes = [ctypes.c_int]
        self._dll.engine_remove_song.restype = ctypes.c_int

        # engine_get_library_count
        self._dll.engine_get_library_count.restype = ctypes.c_int

        # engine_get_song_info
        self._dll.engine_get_song_info.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
            ctypes.c_char_p, ctypes.c_int
        ]
        self._dll.engine_get_song_info.restype = ctypes.c_int

        # Playlists
        self._dll.engine_create_playlist.argtypes = [ctypes.c_char_p]
        self._dll.engine_create_playlist.restype = ctypes.c_int

        self._dll.engine_delete_playlist.argtypes = [ctypes.c_char_p]
        self._dll.engine_delete_playlist.restype = ctypes.c_int

        self._dll.engine_add_to_playlist.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self._dll.engine_add_to_playlist.restype = ctypes.c_int

        self._dll.engine_remove_from_playlist.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self._dll.engine_remove_from_playlist.restype = ctypes.c_int

        self._dll.engine_move_in_playlist.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        self._dll.engine_move_in_playlist.restype = ctypes.c_int

        self._dll.engine_get_playlist_count.argtypes = [ctypes.c_char_p]
        self._dll.engine_get_playlist_count.restype = ctypes.c_int

        self._dll.engine_get_playlist_song_id.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self._dll.engine_get_playlist_song_id.restype = ctypes.c_int

        self._dll.engine_set_active_playlist.argtypes = [ctypes.c_char_p]
        self._dll.engine_set_active_playlist.restype = None

        self._dll.engine_get_active_playlist.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self._dll.engine_get_active_playlist.restype = None

        self._dll.engine_get_playlist_names.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self._dll.engine_get_playlist_names.restype = None

        # Playback navigation
        self._dll.engine_set_current_index.argtypes = [ctypes.c_int]
        self._dll.engine_set_current_index.restype = None

        self._dll.engine_get_current_index.restype = ctypes.c_int
        self._dll.engine_get_next_song_id.restype = ctypes.c_int
        self._dll.engine_get_prev_song_id.restype = ctypes.c_int
        self._dll.engine_get_current_song_id.restype = ctypes.c_int

        # Sorter & Shuffle
        self._dll.engine_sort_playlist.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        self._dll.engine_sort_playlist.restype = None

        self._dll.engine_shuffle_playlist.argtypes = [ctypes.c_char_p]
        self._dll.engine_shuffle_playlist.restype = None

        # Queue
        self._dll.engine_enqueue.argtypes = [ctypes.c_int]
        self._dll.engine_enqueue.restype = None

        self._dll.engine_dequeue.restype = ctypes.c_int
        self._dll.engine_get_queue_count.restype = ctypes.c_int

        self._dll.engine_get_queue_ids.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self._dll.engine_get_queue_ids.restype = ctypes.c_int

        self._dll.engine_clear_queue.restype = None

        # History
        self._dll.engine_record_play.argtypes = [ctypes.c_int]
        self._dll.engine_record_play.restype = None

        self._dll.engine_get_history_ids.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self._dll.engine_get_history_ids.restype = ctypes.c_int

        # Search & Recs
        self._dll.engine_search.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self._dll.engine_search.restype = ctypes.c_int

        self._dll.engine_get_recommendations.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self._dll.engine_get_recommendations.restype = ctypes.c_int

        # Persistence
        self._dll.engine_save_file.argtypes = [ctypes.c_char_p]
        self._dll.engine_save_file.restype = ctypes.c_int

        self._dll.engine_load_file.argtypes = [ctypes.c_char_p]
        self._dll.engine_load_file.restype = ctypes.c_int

    # Native implementation wrappers
    def add_song(self, song: SongInfo) -> int:
        if self.is_native:
            assigned_id = self._dll.engine_add_song(
                song.id,
                song.title.encode('utf-8'),
                song.artist.encode('utf-8'),
                song.album.encode('utf-8'),
                song.genre.encode('utf-8'),
                song.duration,
                song.bpm,
                song.play_count,
                song.file_path.encode('utf-8')
            )
            return assigned_id
        else:
            return self._py_add_song(song)

    def remove_song(self, song_id: int) -> bool:
        if self.is_native:
            return bool(self._dll.engine_remove_song(song_id))
        return self._py_remove_song(song_id)

    def get_library_count(self) -> int:
        if self.is_native:
            return self._dll.engine_get_library_count()
        return len(self._py_library)

    def get_song(self, song_id: int) -> Optional[SongInfo]:
        if self.is_native:
            buf_len = 512
            title = ctypes.create_string_buffer(buf_len)
            artist = ctypes.create_string_buffer(buf_len)
            album = ctypes.create_string_buffer(buf_len)
            genre = ctypes.create_string_buffer(buf_len)
            file_path = ctypes.create_string_buffer(buf_len)
            dur = ctypes.c_int(0)
            bpm = ctypes.c_int(0)
            plays = ctypes.c_int(0)

            ok = self._dll.engine_get_song_info(
                song_id, title, artist, album, genre,
                ctypes.byref(dur), ctypes.byref(bpm), ctypes.byref(plays),
                file_path, buf_len
            )
            if ok:
                return SongInfo(
                    id=song_id,
                    title=title.value.decode('utf-8', errors='ignore'),
                    artist=artist.value.decode('utf-8', errors='ignore'),
                    album=album.value.decode('utf-8', errors='ignore'),
                    genre=genre.value.decode('utf-8', errors='ignore'),
                    duration=dur.value,
                    bpm=bpm.value,
                    play_count=plays.value,
                    file_path=file_path.value.decode('utf-8', errors='ignore')
                )
            return None
        else:
            return self._py_library.get(song_id)

    def create_playlist(self, name: str) -> bool:
        if self.is_native:
            return bool(self._dll.engine_create_playlist(name.encode('utf-8')))
        if name not in self._py_playlists:
            self._py_playlists[name] = []
            return True
        return False

    def delete_playlist(self, name: str) -> bool:
        if self.is_native:
            return bool(self._dll.engine_delete_playlist(name.encode('utf-8')))
        if name in self._py_playlists and name not in ("All Songs", "Favorites"):
            del self._py_playlists[name]
            return True
        return False

    def add_to_playlist(self, playlist_name: str, song_id: int) -> bool:
        if self.is_native:
            return bool(self._dll.engine_add_to_playlist(playlist_name.encode('utf-8'), song_id))
        if playlist_name in self._py_playlists and song_id in self._py_library:
            self._py_playlists[playlist_name].append(song_id)
            return True
        return False

    def remove_from_playlist(self, playlist_name: str, index: int) -> bool:
        if self.is_native:
            return bool(self._dll.engine_remove_from_playlist(playlist_name.encode('utf-8'), index))
        if playlist_name in self._py_playlists:
            pl = self._py_playlists[playlist_name]
            if 0 <= index < len(pl):
                pl.pop(index)
                return True
        return False

    def move_in_playlist(self, playlist_name: str, from_idx: int, to_idx: int) -> bool:
        if self.is_native:
            return bool(self._dll.engine_move_in_playlist(playlist_name.encode('utf-8'), from_idx, to_idx))
        if playlist_name in self._py_playlists:
            pl = self._py_playlists[playlist_name]
            if 0 <= from_idx < len(pl) and 0 <= to_idx < len(pl):
                item = pl.pop(from_idx)
                pl.insert(to_idx, item)
                return True
        return False

    def get_playlist_count(self, playlist_name: str) -> int:
        if self.is_native:
            return self._dll.engine_get_playlist_count(playlist_name.encode('utf-8'))
        return len(self._py_playlists.get(playlist_name, []))

    def get_playlist_songs(self, playlist_name: str) -> List[SongInfo]:
        count = self.get_playlist_count(playlist_name)
        songs = []
        if self.is_native:
            for i in range(count):
                sid = self._dll.engine_get_playlist_song_id(playlist_name.encode('utf-8'), i)
                if sid > 0:
                    s = self.get_song(sid)
                    if s: songs.append(s)
        else:
            ids = self._py_playlists.get(playlist_name, [])
            for sid in ids:
                if sid in self._py_library:
                    songs.append(self._py_library[sid])
        return songs

    def get_playlist_names(self) -> List[str]:
        if self.is_native:
            buf = ctypes.create_string_buffer(4096)
            self._dll.engine_get_playlist_names(buf, 4096)
            raw = buf.value.decode('utf-8', errors='ignore')
            if not raw: return ["All Songs", "Favorites"]
            return [x for x in raw.split(';') if x]
        return list(self._py_playlists.keys())

    def set_active_playlist(self, name: str):
        if self.is_native:
            self._dll.engine_set_active_playlist(name.encode('utf-8'))
        else:
            self._py_active_playlist = name

    def get_active_playlist(self) -> str:
        if self.is_native:
            buf = ctypes.create_string_buffer(256)
            self._dll.engine_get_active_playlist(buf, 256)
            return buf.value.decode('utf-8', errors='ignore') or "All Songs"
        return self._py_active_playlist

    def set_current_index(self, index: int):
        if self.is_native:
            self._dll.engine_set_current_index(index)
        else:
            self._py_current_index = index

    def get_current_index(self) -> int:
        if self.is_native:
            return self._dll.engine_get_current_index()
        return self._py_current_index

    def get_current_song(self) -> Optional[SongInfo]:
        if self.is_native:
            sid = self._dll.engine_get_current_song_id()
            return self.get_song(sid) if sid > 0 else None
        pl = self.get_playlist_songs(self.get_active_playlist())
        if 0 <= self._py_current_index < len(pl):
            return pl[self._py_current_index]
        return None

    def get_next_song(self) -> Optional[SongInfo]:
        if self.is_native:
            sid = self._dll.engine_get_next_song_id()
            return self.get_song(sid) if sid > 0 else None
        # Python fallback queue check
        if self._py_queue:
            sid = self._py_queue.pop(0)
            self.record_play(sid)
            return self.get_song(sid)
        pl = self.get_playlist_songs(self.get_active_playlist())
        if not pl: return None
        self._py_current_index = (self._py_current_index + 1) % len(pl)
        s = pl[self._py_current_index]
        self.record_play(s.id)
        return s

    def get_prev_song(self) -> Optional[SongInfo]:
        if self.is_native:
            sid = self._dll.engine_get_prev_song_id()
            return self.get_song(sid) if sid > 0 else None
        pl = self.get_playlist_songs(self.get_active_playlist())
        if not pl: return None
        self._py_current_index -= 1
        if self._py_current_index < 0:
            self._py_current_index = len(pl) - 1
        s = pl[self._py_current_index]
        self.record_play(s.id)
        return s

    def sort_playlist(self, playlist_name: str, criteria: int, ascending: bool = True):
        """
        Criteria: 0=Title, 1=Artist, 2=Duration, 3=PlayCount, 4=BPM
        """
        if self.is_native:
            self._dll.engine_sort_playlist(playlist_name.encode('utf-8'), criteria, 1 if ascending else 0)
        else:
            keys = [
                lambda s: s.title.lower(),
                lambda s: s.artist.lower(),
                lambda s: s.duration,
                lambda s: s.play_count,
                lambda s: s.bpm
            ]
            if playlist_name in self._py_playlists:
                ids = self._py_playlists[playlist_name]
                songs = [self._py_library[sid] for sid in ids if sid in self._py_library]
                songs.sort(key=keys[criteria], reverse=not ascending)
                self._py_playlists[playlist_name] = [s.id for s in songs]

    def shuffle_playlist(self, playlist_name: str):
        if self.is_native:
            self._dll.engine_shuffle_playlist(playlist_name.encode('utf-8'))
        else:
            import random
            if playlist_name in self._py_playlists:
                random.shuffle(self._py_playlists[playlist_name])

    def enqueue(self, song_id: int):
        if self.is_native:
            self._dll.engine_enqueue(song_id)
        else:
            self._py_queue.append(song_id)

    def dequeue(self) -> Optional[SongInfo]:
        if self.is_native:
            sid = self._dll.engine_dequeue()
            return self.get_song(sid) if sid > 0 else None
        if self._py_queue:
            return self.get_song(self._py_queue.pop(0))
        return None

    def get_queue(self) -> List[SongInfo]:
        if self.is_native:
            count = self._dll.engine_get_queue_count()
            if count <= 0: return []
            arr = (ctypes.c_int * count)()
            written = self._dll.engine_get_queue_ids(arr, count)
            res = []
            for i in range(written):
                s = self.get_song(arr[i])
                if s: res.append(s)
            return res
        return [self._py_library[sid] for sid in self._py_queue if sid in self._py_library]

    def clear_queue(self):
        if self.is_native:
            self._dll.engine_clear_queue()
        else:
            self._py_queue.clear()

    def record_play(self, song_id: int):
        if self.is_native:
            self._dll.engine_record_play(song_id)
        else:
            if song_id in self._py_library:
                self._py_library[song_id].play_count += 1
                self._py_history.append(song_id)
                if len(self._py_history) > 50:
                    self._py_history.pop(0)

    def get_history(self, limit: int = 10) -> List[SongInfo]:
        if self.is_native:
            arr = (ctypes.c_int * limit)()
            written = self._dll.engine_get_history_ids(arr, limit)
            res = []
            for i in range(written):
                s = self.get_song(arr[i])
                if s: res.append(s)
            return res
        rev = list(reversed(self._py_history))[:limit]
        return [self._py_library[sid] for sid in rev if sid in self._py_library]

    def search(self, query: str, max_results: int = 50) -> List[SongInfo]:
        if not query.strip():
            return self.get_playlist_songs("All Songs")
        if self.is_native:
            arr = (ctypes.c_int * max_results)()
            found = self._dll.engine_search(query.encode('utf-8'), arr, max_results)
            res = []
            for i in range(found):
                s = self.get_song(arr[i])
                if s: res.append(s)
            return res
        else:
            q = query.lower()
            return [s for s in self._py_library.values()
                    if q in s.title.lower() or q in s.artist.lower() or q in s.genre.lower() or q in s.album.lower()]

    def get_recommendations(self, song_id: int, count: int = 5) -> List[SongInfo]:
        if self.is_native:
            arr = (ctypes.c_int * count)()
            found = self._dll.engine_get_recommendations(song_id, arr, count)
            res = []
            for i in range(found):
                s = self.get_song(arr[i])
                if s: res.append(s)
            return res
        else:
            target = self.get_song(song_id)
            if not target: return []
            recs = [s for s in self._py_library.values() if s.id != song_id]
            recs.sort(key=lambda s: (s.genre == target.genre, s.artist == target.artist), reverse=True)
            return recs[:count]

    def save_file(self, filepath: str) -> bool:
        if self.is_native:
            return bool(self._dll.engine_save_file(filepath.encode('utf-8')))
        return False

    def load_file(self, filepath: str) -> bool:
        if self.is_native:
            return bool(self._dll.engine_load_file(filepath.encode('utf-8')))
        return False

    # Python Fallback Data Structures
    def _init_python_fallback(self):
        self._py_library: Dict[int, SongInfo] = {}
        self._py_playlists: Dict[str, List[int]] = {"All Songs": [], "Favorites": []}
        self._py_queue: List[int] = []
        self._py_history: List[int] = []
        self._py_active_playlist = "All Songs"
        self._py_current_index = 0
        self._next_id = 1

    def _py_add_song(self, song: SongInfo) -> int:
        sid = song.id if song.id > 0 else self._next_id
        self._next_id = max(self._next_id, sid + 1)
        s = SongInfo(sid, song.title, song.artist, song.album, song.genre, song.duration, song.bpm, song.play_count, song.file_path)
        self._py_library[sid] = s
        if sid not in self._py_playlists["All Songs"]:
            self._py_playlists["All Songs"].append(sid)
        return sid

    def _py_remove_song(self, song_id: int) -> bool:
        if song_id in self._py_library:
            del self._py_library[song_id]
            for pl in self._py_playlists.values():
                if song_id in pl:
                    pl.remove(song_id)
            return True
        return False

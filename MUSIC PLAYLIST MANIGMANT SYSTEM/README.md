# 🎵 SoundWave: Modern Music Playlist Management System
### *High-Performance C++ DSA Core Engine with Spotify-Style Python GUI*

[![Language](https://img.shields.io/badge/Languages-C%2B%2B17%20%7C%20Python%203.12-blue.svg)](#)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-emerald.svg)](#)
[![Audio](https://img.shields.io/badge/Audio-Pygame%20Mixer-purple.svg)](#)
[![Architecture](https://img.shields.io/badge/Core-Native%20DLL%20(ctypes)-orange.svg)](#)

---

## 🌟 Overview
**SoundWave** is an advanced, college-level group project designed for high marks and live demonstrations. It unites the raw computational performance of **C++ Data Structures & Algorithms (DSA)** with a gorgeous, dark-themed **Python CustomTkinter GUI** and **real audio playback engine**.

---

## 🚀 Key Features

### 1. ⚡ High-Performance C++ DSA Core Engine
- **Doubly Linked List (DLL)**: Core playlist representation with $O(1)$ bidirectional traversal (`Next` / `Prev`), arbitrary position insertion, deletion, and node shifting.
- **Play Queue (FIFO)**: Dedicated "Up Next" queue for dynamic track sequencing.
- **Playback History (LIFO Stack)**: Tracks recently played songs and supports history inspection.
- **Prefix Tree (Trie Search)**: Lightning-fast $O(L)$ search-as-you-type autocomplete across song title, artist, album, and genre.
- **MergeSort & QuickSort**: Multi-column sorting (Title A-Z, Artist A-Z, Duration, Play Count, BPM).
- **Fisher-Yates Shuffle**: Algorithmic randomized track shuffling.
- **Smart Recommendation Engine**: Content-based multi-feature similarity scoring (Genre, Artist, BPM proximity, Duration).
- **JSON Data Persistence**: Automatic saving and loading of libraries and playlists.

### 2. 🎨 100% Authentic Spotify Dark Desktop GUI
- Pixel-perfect Spotify Desktop Dark design (`#121212`, `#000000`, `#1DB954`).
- Live search bar with instant autocomplete powered by the C++ Trie.
- Interactive progress slider with real-time seeking and volume control.
- Playlist manager (create custom playlists, add/remove songs).
- **DSA Architecture Inspector Modal**: Live interactive inspector displaying internal node states, queue contents, history stack, and complexity tables for examiners!

### 3. 👑 Dual Login, Self-Registration (Sign Up) & Admin RBAC
- **User Self-Registration (Sign Up)**: Users can create their own accounts directly by clicking *"Don't have an account? Sign up free"* or *"✨ Create New Account (Sign Up)"*. They enter their Display Name, Username, Email, and Password and are instantly logged in.
- **Dual Authentication**: Users can log in using either their **Email** or **Username** (case-insensitive).
- **Default Accounts**:
  - **Administrator**: Email `adminswayam@gmail.com` (or username `adminswayam`) / Password `admin@123`
  - **Standard Listener**: Email `swayam@gmail.com` (or username `user`) / Password `user123`
- **Admin Exclusive Privileges**:
  - Access to dedicated **👥 User Accounts Management** portal.
  - Delete user accounts (with protection against deleting the sole active admin).
  - Delete tracks from the Master Library (`✕` button is role-protected).
  - Import new local MP3/WAV audio tracks into the Master Library.
  - One-click user switcher in the top profile pill.
- **Persistent Storage**: Credentials and emails stored in `data/users.json`.

### 4. 🖥️ Standalone C++ Terminal Application (`music_core_cli.exe`)
- Can be run independently in the terminal to demonstrate pure C++ DSA operations without Python during viva evaluations.

---

## 📂 Project Directory Structure

```
MUSIC PLAYLIST MANAGEMENT SYSTEM/
├── cpp_core/                       # Native C++ DSA Engine
│   ├── include/
│   │   ├── Song.hpp                # Song metadata struct
│   │   ├── DoublyLinkedList.hpp    # Custom Doubly Linked List
│   │   ├── PlayQueue.hpp           # FIFO Play Queue
│   │   ├── HistoryStack.hpp        # LIFO Playback History Stack
│   │   ├── TrieSearch.hpp          # Prefix Tree (Trie) Search
│   │   ├── RecommendationEngine.hpp# Vector Similarity Recommender
│   │   ├── Sorter.hpp              # MergeSort & QuickSort algorithms
│   │   ├── PlaylistManager.hpp     # Master Coordinator
│   │   └── api_exports.h           # C-linkage export declarations
│   ├── src/
│   │   ├── DoublyLinkedList.cpp
│   │   ├── TrieSearch.cpp
│   │   ├── RecommendationEngine.cpp
│   │   ├── Sorter.cpp
│   │   ├── PlaylistManager.cpp
│   │   ├── api_exports.cpp         # DLL Entrypoints
│   │   └── main_cli.cpp            # Standalone Terminal CLI App
│   └── playlist_core.dll           # Compiled shared library
├── python_ui/                      # Python Frontend & Audio Engine
│   ├── cpp_bridge.py               # ctypes binding layer with fallback
│   ├── audio_player.py             # Pygame mixer audio pipeline
│   ├── auth_manager.py             # Role-Based User & Admin Authentication
│   └── gui.py                      # 100% Authentic Spotify Dark Desktop App
├── data/
│   ├── library.json                # Master library metadata
│   ├── users.json                  # Admin and user account credentials
│   └── audio/                      # Audio track files (.wav/.mp3)
├── tests/
│   ├── test_cpp.cpp                # C++ DSA unit tests
│   └── test_bridge.py              # Python-C++ bridge integration tests
├── build.bat                       # One-click compile & test script
├── run.bat                         # One-click launch Python GUI
├── run_cli.bat                     # One-click launch C++ CLI
├── PROJECT_REPORT.md               # Complete academic report & Viva Q&A
└── README.md                       # Documentation
```

---

## ⚡ Quick Start Guide

### 1. Launch Modern Python GUI (Recommended)
Simply double click or run:
```cmd
run.bat
```
*(Or in terminal)*
```cmd
python python_ui/gui.py
```

### 2. Launch Pure C++ Terminal CLI App
Double click or run:
```cmd
run_cli.bat
```

### 3. Recompile Everything & Run Unit Tests
```cmd
build.bat
```

---

## 🎯 Viva / Evaluation Highlights (For College Examiners)
1. **Doubly Linked List**: Demonstrates why linked lists are superior to arrays for audio playlists (bidirectional $O(1)$ sequential access, instant pointer re-linking on deletions without memory reallocation).
2. **Trie Autocomplete**: Proves mastery of advanced trees with $O(L)$ search time complexity versus $O(N \times M)$ linear scans.
3. **Queue & Stack**: Practical dual application of FIFO (next up songs) and LIFO (history/undo stack).
4. **MergeSort**: Demonstrates divide-and-conquer stable sorting.
5. **Cross-Language Integration**: Demonstrates production-grade interoperability between C++ and Python using dynamic link libraries.

---

## 👥 Suggested Group Division
- **Member 1**: C++ Core Engine & Doubly Linked List Architecture
- **Member 2**: Queue, Stack & Trie Autocomplete Search Engine
- **Member 3**: MergeSort Algorithms & Vector Recommendation Engine
- **Member 4**: ctypes Bridge, CustomTkinter Modern UI & Audio Pipeline

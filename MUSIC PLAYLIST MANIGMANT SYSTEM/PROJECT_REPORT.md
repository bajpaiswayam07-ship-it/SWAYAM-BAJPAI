# ACADEMIC PROJECT REPORT
## SoundWave: Modern Music Playlist Management System
### Cross-Language High-Performance Architecture (C++ DSA Core Engine & Python GUI)

---

### 1. ABSTRACT
Modern music streaming and management systems (e.g., Spotify, Apple Music) require low-latency data operations for managing dynamic playlists, real-time prefix-based song searches, queue processing, and song recommendations. This project presents **SoundWave**, a hybrid software architecture combining a **C++17 high-performance Data Structures & Algorithms (DSA) core engine** with a **modern Python CustomTkinter graphical user interface and Pygame audio playback system**.

The C++ core implements custom, memory-efficient data structures including:
1. **Doubly Linked Lists** for playlists ($O(1)$ bidirectional traversal, node reordering, circular looping).
2. **First-In-First-Out (FIFO) Queues** for dynamic "Up Next" play queues.
3. **Last-In-First-Out (LIFO) Stacks** for playback history tracking and undo operations.
4. **Prefix Trees (Trie)** for $O(L)$ instant search-as-you-type queries across titles, artists, and genres.
5. **MergeSort and QuickSort** for multi-criteria sorting (Title, Artist, Duration, Play Count, BPM).
6. **Vector Cosine/Proximity Content-Based Recommendation Engine** for smart music discovery.

The Python client communicates with the compiled C++ shared library (`playlist_core.dll`) via foreign function interface (`ctypes`), presenting users with a sleek dark-themed interface, interactive progress tracking, and procedural audio synthesis.

---

### 2. SUGGESTED GROUP ROLES & WORK DIVISION
*(Ideal for submission and presentation by a team of 2 to 4 members)*

| Team Member | Module Assigned | Key Responsibilities |
|---|---|---|
| **Member 1 (Lead / DSA Architect)** | C++ Core & Linked List Module | Designed `Song` model, custom `DoublyLinkedList`, node pointer operations, shuffle, and memory management. |
| **Member 2 (Algorithms & Search)** | Search Index & Queues/Stacks | Implemented `TrieSearch` (Prefix Tree), `PlayQueue` (FIFO), `HistoryStack` (LIFO), and JSON persistence. |
| **Member 3 (Recommendation & Sorting)** | Analytics & Sorter Engine | Developed `Sorter` (MergeSort & QuickSort algorithms) and content-based `RecommendationEngine`. |
| **Member 4 (Bridge & Frontend UI)** | Python GUI & Audio Pipeline | Developed `cpp_bridge.py` (`ctypes` binding layer), CustomTkinter UI, Pygame mixer integration, and procedural audio generator. |

---

### 3. SYSTEM ARCHITECTURE & DATA FLOW

```
+-------------------------------------------------------------------------+
|                              PYTHON LAYER                               |
|                                                                         |
|   +-----------------------+                    +--------------------+   |
|   |  CustomTkinter Modern | <================> | AudioPlayer Engine |   |
|   |  Dark-Mode GUI        |                    |   (Pygame Mixer)   |   |
|   +-----------------------+                    +--------------------+   |
|               |                                                         |
|               v                                                         |
|   +-----------------------------------------------------------------+   |
|   |         C-Types Dynamic Link Library Bridge (cpp_bridge.py)     |   |
|   +-----------------------------------------------------------------+   |
+-----------------------------------|-------------------------------------+
                                    | C Foreign Function Interface (FFI)
+-----------------------------------v-------------------------------------+
|                          NATIVE C++ CORE ENGINE                         |
|                           (playlist_core.dll)                           |
|                                                                         |
|  +--------------------+   +-------------------+   +------------------+  |
|  | Doubly Linked List |   |  Play Queue       |   |  History Stack   |  |
|  | (Playlists / Loop) |   |  (FIFO 'Up Next') |   |  (LIFO Recent)   |  |
|  +--------------------+   +-------------------+   +------------------+  |
|                                                                         |
|  +--------------------+   +-------------------+   +------------------+  |
|  | Trie (Prefix Tree) |   | Sorter Engine     |   | Recommendation   |  |
|  | (O(L) Fast Search) |   | (Merge/QuickSort) |   | (Similarity Heap)|  |
|  +--------------------+   +-------------------+   +------------------+  |
|                                                                         |
|  +-------------------------------------------------------------------+  |
|  | Master PlaylistManager (Unordered Maps & JSON File Persistence)   |  |
|  +-------------------------------------------------------------------+  |
+-------------------------------------------------------------------------+
```

---

### 4. DATA STRUCTURES & ALGORITHM COMPLEXITY ANALYSIS

| Data Structure / Algorithm | Purpose in SoundWave | Operation | Time Complexity | Space Complexity |
|---|---|---|---|---|
| **Doubly Linked List** | Sequential Playlist Management | Next / Previous Song | $O(1)$ | $O(1)$ |
| | | Insert End / Prepend | $O(1)$ | $O(1)$ |
| | | Insert / Remove at Index | $O(N)$ | $O(1)$ |
| | | Node Reordering (Move) | $O(N)$ | $O(1)$ |
| **Queue (FIFO)** | "Up Next" Song Queue | Enqueue / Dequeue | $O(1)$ | $O(K)$ |
| **Stack (LIFO)** | Recently Played History | Push / Pop | $O(1)$ | $O(M)$ |
| **Trie (Prefix Tree)** | Real-time Search Autocomplete | Prefix Lookup | $O(L)$ where $L$ = query length | $O(\Sigma \cdot N)$ |
| **MergeSort** | Multi-Column Playlist Sorting | Stable Sort | $O(N \log N)$ | $O(N)$ |
| **Fisher-Yates Shuffle** | Playlist Shuffling | Random Permutation | $O(N)$ | $O(1)$ |
| **Vector Similarity Engine** | Music Recommendations | Nearest Neighbors | $O(N \log K)$ | $O(K)$ |

---

### 5. FREQUENTLY ASKED VIVA QUESTIONS & ANSWERS (FOR EXAMINERS)

#### Q1: Why did you use a Doubly Linked List instead of an Array / Vector for the playlist?
**Answer:**
A Doubly Linked List allows true $O(1)$ bidirectional navigation (`next_node` and `prev_node` pointers) without index recalculation. In a continuous audio player, shifting songs or inserting a track into the middle of a playlist requires $O(1)$ pointer rewiring once the node is reached, without needing array elements to be copied or reallocated in memory. Furthermore, connecting tail to head provides seamless circular looping.

#### Q2: Why is a Trie better than standard string search (`std::string::find`)?
**Answer:**
Standard substring search scans through all $N$ songs and compares characters, costing $O(N \times M)$ where $M$ is string length. In contrast, a Trie organizes characters into a prefix tree. Traversing the Trie depends solely on the length of the query $L$, giving $O(L)$ time complexity regardless of whether the library contains 10 songs or 1,000,000 songs.

#### Q3: How do Python and C++ communicate in this system?
**Answer:**
We compile the C++ core into a 64-bit dynamic link library (`playlist_core.dll`) exposing clean C-linkage functions (`extern "C"` and `__declspec(dllexport)`). In Python, we use the `ctypes` library to bind to these exported functions, passing standard primitives (integers, strings, arrays) across the FFI boundary.

#### Q4: How does the Recommendation Engine work?
**Answer:**
It uses a content-based multi-feature similarity scoring algorithm. Each song is modeled with attributes: Genre (40% weight), Artist (30% weight), Tempo/BPM proximity (20% weight), and Duration similarity (10% weight). It ranks library songs against the target track and outputs the top $K$ recommendations using a priority queue / sorted vector.

#### Q5: What sorting algorithm did you implement and why?
**Answer:**
We implemented **MergeSort** because it is a stable divide-and-conquer algorithm with guaranteed $O(N \log N)$ worst-case time complexity, ensuring predictable performance regardless of initial playlist ordering.

#### Q6: How is Authentication and Role-Based Access Control (RBAC) implemented?
**Answer:**
We implemented an authentication manager (`AuthManager`) that supports multi-user sessions with role segregation (`admin` and `user`) and dual identifier resolution (users can log in using either their registered **Email** or **Username** with case-insensitivity). Sensitive operations—such as permanent song deletion from the master library, importing new audio files, and database backups—are strictly guarded behind admin authorization (`is_current_admin()` check). Administrators also have access to an Admin Portal that audits internal C++ DSA memory states and manages registered user accounts with email addresses.

---

### 6. CONCLUSION
SoundWave demonstrates an industry-grade approach to software development by leveraging the raw computational efficiency of C++ for algorithmic logic and the rich user interface capabilities of Python. The project fulfills all curriculum requirements for Data Structures and Algorithms while delivering a complete, interactive, real-world application.

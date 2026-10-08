#include "../include/PlaylistManager.hpp"
#include <iostream>
#include <iomanip>
#include <string>

void printBanner() {
    std::cout << "\n======================================================\n";
    std::cout << "  * SOUNDWAVE: MUSIC PLAYLIST MANAGEMENT SYSTEM *     \n";
    std::cout << "         [High Performance C++ DSA Core Engine]       \n";
    std::cout << "======================================================\n";
}

void printSongRow(const Song& s, int idx = -1) {
    if (idx >= 0) {
        std::cout << "[" << std::setw(2) << idx << "] ";
    }
    std::cout << "ID: " << std::setw(3) << s.id
              << " | " << std::left << std::setw(22) << s.title.substr(0, 20)
              << " | " << std::setw(16) << s.artist.substr(0, 15)
              << " | " << std::setw(10) << s.genre
              << " | " << s.duration << "s"
              << " | " << s.bpm << " BPM"
              << " | Plays: " << s.playCount << "\n";
}

int main() {
    PlaylistManager mgr;
    mgr.loadFromFile("data/library.json");

    int choice = -1;
    while (choice != 0) {
        printBanner();
        std::cout << " Active Playlist: [" << mgr.getActivePlaylist() << "]\n";
        Song* cur = mgr.getCurrentSong();
        if (cur) {
            std::cout << " Currently Playing: " << cur->title << " - " << cur->artist << " (Index: " << mgr.getCurrentIndex() << ")\n";
        } else {
            std::cout << " Currently Playing: None\n";
        }
        std::cout << "------------------------------------------------------\n";
        std::cout << " 1. Display Current Playlist (Doubly Linked List)\n";
        std::cout << " 2. Play Next Song [DLL forward traversal ->]\n";
        std::cout << " 3. Play Previous Song [DLL backward traversal <-]\n";
        std::cout << " 4. Add Song to Library & Playlist\n";
        std::cout << " 5. Delete Song from Playlist\n";
        std::cout << " 6. Move Song Position (DLL Node Relink)\n";
        std::cout << " 7. Enqueue Song (FIFO Play Queue)\n";
        std::cout << " 8. View / Dequeue from Play Queue\n";
        std::cout << " 9. View Playback History (LIFO Stack)\n";
        std::cout << " 10. Search Songs by Keyword / Prefix (Trie Index)\n";
        std::cout << " 11. Sort Playlist (MergeSort / QuickSort DSA)\n";
        std::cout << " 12. Shuffle Playlist (Fisher-Yates Algorithm)\n";
        std::cout << " 13. Smart Recommendations (Vector Similarity Engine)\n";
        std::cout << " 14. Switch / Create / View Playlists\n";
        std::cout << " 15. Save Library to JSON File\n";
        std::cout << " 16. Load Library from JSON File\n";
        std::cout << " 0. Exit\n";
        std::cout << "======================================================\n";
        std::cout << " Enter choice: ";

        if (!(std::cin >> choice)) {
            std::cin.clear();
            std::string dummy;
            std::cin >> dummy;
            continue;
        }

        std::cout << "\n";
        switch (choice) {
            case 1: {
                DoublyLinkedList* pl = mgr.getPlaylist(mgr.getActivePlaylist());
                if (!pl || pl->isEmpty()) {
                    std::cout << "Playlist is empty.\n";
                } else {
                    std::cout << "--- Playlist: " << mgr.getActivePlaylist() << " (" << pl->size() << " songs) ---\n";
                    std::vector<Song> songs = pl->toVector();
                    for (int i = 0; i < static_cast<int>(songs.size()); ++i) {
                        printSongRow(songs[i], i);
                    }
                }
                break;
            }
            case 2: {
                Song* next = mgr.getNextSong();
                if (next) {
                    std::cout << ">> Now Playing: " << next->title << " by " << next->artist << "\n";
                } else {
                    std::cout << "No next song available.\n";
                }
                break;
            }
            case 3: {
                Song* prev = mgr.getPreviousSong();
                if (prev) {
                    std::cout << "<< Now Playing: " << prev->title << " by " << prev->artist << "\n";
                } else {
                    std::cout << "No previous song available.\n";
                }
                break;
            }
            case 4: {
                std::cin.ignore();
                Song s;
                std::cout << "Enter Title: "; std::getline(std::cin, s.title);
                std::cout << "Enter Artist: "; std::getline(std::cin, s.artist);
                std::cout << "Enter Album: "; std::getline(std::cin, s.album);
                std::cout << "Enter Genre: "; std::getline(std::cin, s.genre);
                std::cout << "Enter Duration (seconds): "; std::cin >> s.duration;
                std::cout << "Enter BPM: "; std::cin >> s.bpm;
                int id = mgr.addSong(s);
                if (mgr.getActivePlaylist() != "All Songs") {
                    mgr.addSongToPlaylist(mgr.getActivePlaylist(), id);
                }
                std::cout << "[SUCCESS] Song added with ID: " << id << "\n";
                break;
            }
            case 5: {
                int idx;
                std::cout << "Enter song index in playlist to remove: ";
                std::cin >> idx;
                if (mgr.removeSongFromPlaylist(mgr.getActivePlaylist(), idx)) {
                    std::cout << "[SUCCESS] Song removed.\n";
                } else {
                    std::cout << "[ERROR] Invalid index.\n";
                }
                break;
            }
            case 6: {
                int fromIdx, toIdx;
                std::cout << "Move from index: "; std::cin >> fromIdx;
                std::cout << "Move to index: "; std::cin >> toIdx;
                if (mgr.moveSongInPlaylist(mgr.getActivePlaylist(), fromIdx, toIdx)) {
                    std::cout << "[SUCCESS] Song moved successfully.\n";
                } else {
                    std::cout << "[ERROR] Failed to move song.\n";
                }
                break;
            }
            case 7: {
                int id;
                std::cout << "Enter Song ID to enqueue: "; std::cin >> id;
                mgr.enqueue(id);
                std::cout << "[SUCCESS] Song ID " << id << " added to play queue.\n";
                break;
            }
            case 8: {
                std::vector<Song> q = mgr.getQueue();
                std::cout << "--- Up Next Queue (" << q.size() << " songs) ---\n";
                for (size_t i = 0; i < q.size(); ++i) {
                    printSongRow(q[i], static_cast<int>(i));
                }
                if (!q.empty()) {
                    std::cout << "Dequeue front song? (1 = Yes, 0 = No): ";
                    int dq; std::cin >> dq;
                    if (dq == 1) {
                        Song s;
                        if (mgr.dequeue(s)) {
                            std::cout << "[DEQUEUED] " << s.title << " by " << s.artist << "\n";
                        }
                    }
                }
                break;
            }
            case 9: {
                std::vector<Song> hist = mgr.getRecentlyPlayed(10);
                std::cout << "--- Recently Played (LIFO Stack) ---\n";
                for (size_t i = 0; i < hist.size(); ++i) {
                    printSongRow(hist[i], static_cast<int>(i));
                }
                break;
            }
            case 10: {
                std::cin.ignore();
                std::string q;
                std::cout << "Enter search prefix or title/artist/genre: ";
                std::getline(std::cin, q);
                std::vector<Song> found = mgr.search(q);
                std::cout << "Found " << found.size() << " matching songs in Trie:\n";
                for (size_t i = 0; i < found.size(); ++i) {
                    printSongRow(found[i], static_cast<int>(i));
                }
                break;
            }
            case 11: {
                std::cout << "Sort criteria:\n";
                std::cout << " 0: Title | 1: Artist | 2: Duration | 3: Play Count | 4: BPM\n";
                std::cout << "Enter criteria (0-4): ";
                int crit; std::cin >> crit;
                std::cout << "Ascending? (1 = Yes, 0 = No): ";
                int asc; std::cin >> asc;
                mgr.sortPlaylist(mgr.getActivePlaylist(), static_cast<SortCriteria>(crit), asc != 0);
                std::cout << "[SUCCESS] Playlist sorted using MergeSort.\n";
                break;
            }
            case 12: {
                mgr.shufflePlaylist(mgr.getActivePlaylist());
                std::cout << "[SUCCESS] Playlist shuffled using Fisher-Yates algorithm.\n";
                break;
            }
            case 13: {
                int sId;
                std::cout << "Enter Song ID to get recommendations for: ";
                std::cin >> sId;
                std::vector<Song> recs = mgr.getRecommendationsForSong(sId, 5);
                std::cout << "--- Top Smart Recommendations for Song ID " << sId << " ---\n";
                for (size_t i = 0; i < recs.size(); ++i) {
                    printSongRow(recs[i], static_cast<int>(i));
                }
                break;
            }
            case 14: {
                std::vector<std::string> names = mgr.getPlaylistNames();
                std::cout << "Available Playlists:\n";
                for (size_t i = 0; i < names.size(); ++i) {
                    std::cout << " " << (i + 1) << ". " << names[i] << "\n";
                }
                std::cout << "Options: (1: Switch Playlist, 2: Create New Playlist, 0: Back): ";
                int sub; std::cin >> sub;
                if (sub == 1) {
                    std::cin.ignore();
                    std::cout << "Enter playlist name to activate: ";
                    std::string plName; std::getline(std::cin, plName);
                    if (mgr.hasPlaylist(plName)) {
                        mgr.setActivePlaylist(plName);
                        std::cout << "[SUCCESS] Active playlist set to " << plName << "\n";
                    } else {
                        std::cout << "[ERROR] Playlist does not exist.\n";
                    }
                } else if (sub == 2) {
                    std::cin.ignore();
                    std::cout << "Enter new playlist name: ";
                    std::string plName; std::getline(std::cin, plName);
                    if (mgr.createPlaylist(plName)) {
                        std::cout << "[SUCCESS] Playlist '" << plName << "' created.\n";
                    } else {
                        std::cout << "[ERROR] Failed to create playlist (name may already exist).\n";
                    }
                }
                break;
            }
            case 15: {
                if (mgr.saveToFile("data/library.json")) {
                    std::cout << "[SUCCESS] Library saved to data/library.json\n";
                } else {
                    std::cout << "[ERROR] Failed to save library.\n";
                }
                break;
            }
            case 16: {
                if (mgr.loadFromFile("data/library.json")) {
                    std::cout << "[SUCCESS] Library loaded from data/library.json\n";
                } else {
                    std::cout << "[ERROR] Failed to load library.\n";
                }
                break;
            }
            case 0:
                std::cout << "Exiting SoundWave. Goodbye!\n";
                break;
            default:
                std::cout << "Invalid choice.\n";
        }
        std::cout << "\nPress Enter to continue...";
        std::cin.ignore();
        std::cin.get();
    }
    return 0;
}

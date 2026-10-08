#include "../cpp_core/include/DoublyLinkedList.hpp"
#include "../cpp_core/include/PlayQueue.hpp"
#include "../cpp_core/include/HistoryStack.hpp"
#include "../cpp_core/include/TrieSearch.hpp"
#include "../cpp_core/include/Sorter.hpp"
#include "../cpp_core/include/RecommendationEngine.hpp"

#include <iostream>
#include <cassert>

void testDoublyLinkedList() {
    std::cout << "[TEST] DoublyLinkedList... ";
    DoublyLinkedList list;
    Song s1(1, "Song A", "Artist 1", "Album 1", "Pop", 180, 120, 5, "");
    Song s2(2, "Song B", "Artist 2", "Album 2", "Rock", 210, 130, 10, "");
    Song s3(3, "Song C", "Artist 1", "Album 3", "Pop", 150, 110, 2, "");

    list.append(s1);
    list.append(s2);
    list.prepend(s3); // Order: s3, s1, s2

    assert(list.size() == 3);
    assert(list.get(0)->title == "Song C");
    assert(list.get(1)->title == "Song A");
    assert(list.get(2)->title == "Song B");

    // Test move
    list.move(0, 2); // s3 moves to end: s1, s2, s3
    assert(list.get(0)->title == "Song A");
    assert(list.get(2)->title == "Song C");

    // Test remove
    list.removeAt(1); // removes s2
    assert(list.size() == 2);
    assert(list.get(1)->title == "Song C");

    std::cout << "PASSED\n";
}

void testQueueAndStack() {
    std::cout << "[TEST] Queue & History Stack... ";
    PlayQueue q;
    Song s1(1, "Q1", "A1", "", "", 100, 120, 0, "");
    Song s2(2, "Q2", "A2", "", "", 100, 120, 0, "");
    q.enqueue(s1);
    q.enqueue(s2);
    assert(q.size() == 2);
    Song out;
    assert(q.dequeue(out) && out.id == 1);
    assert(q.dequeue(out) && out.id == 2);
    assert(q.isEmpty());

    HistoryStack stack(5);
    stack.push(s1);
    stack.push(s2);
    assert(stack.size() == 2);
    assert(stack.pop(out) && out.id == 2);
    assert(stack.pop(out) && out.id == 1);
    assert(stack.isEmpty());
    std::cout << "PASSED\n";
}

void testTrie() {
    std::cout << "[TEST] Trie Autocomplete & Search... ";
    TrieSearch trie;
    trie.indexSong(1, "Midnight City", "M83", "Hurry Up", "Electronic");
    trie.indexSong(2, "City Lights", "Ray", "Urban", "Jazz");
    trie.indexSong(3, "Blinding Lights", "The Weeknd", "After Hours", "Synthwave");

    auto r1 = trie.searchPrefix("City");
    assert(r1.size() == 2); // IDs 1 and 2

    auto r2 = trie.searchPrefix("weeknd");
    assert(r2.size() == 1 && r2[0] == 3);

    auto r3 = trie.searchPrefix("Lights");
    assert(r3.size() == 2); // IDs 2 and 3

    std::cout << "PASSED\n";
}

void testSorter() {
    std::cout << "[TEST] Sorter (MergeSort)... ";
    std::vector<Song> songs = {
        Song(1, "Zebra", "A", "", "", 300, 120, 1, ""),
        Song(2, "Apple", "B", "", "", 150, 130, 50, ""),
        Song(3, "Mango", "C", "", "", 200, 100, 20, "")
    };

    Sorter::mergeSort(songs, SortCriteria::TITLE, true);
    assert(songs[0].title == "Apple");
    assert(songs[1].title == "Mango");
    assert(songs[2].title == "Zebra");

    Sorter::mergeSort(songs, SortCriteria::DURATION, true);
    assert(songs[0].duration == 150);
    assert(songs[2].duration == 300);

    Sorter::mergeSort(songs, SortCriteria::PLAY_COUNT, false);
    assert(songs[0].playCount == 50);
    assert(songs[2].playCount == 1);

    std::cout << "PASSED\n";
}

void testRecommendations() {
    std::cout << "[TEST] Recommendation Engine... ";
    Song target(1, "Neon Glow", "Synth Master", "Album 1", "Synthwave", 210, 120, 10, "");
    std::vector<Song> library = {
        target,
        Song(2, "Retro Sunset", "Synth Master", "Album 1", "Synthwave", 215, 122, 5, ""), // High match
        Song(3, "Acoustic Sun", "Folk Band", "Album 2", "Folk", 120, 80, 2, ""),          // Low match
        Song(4, "Cyber Runner", "Techno Guy", "Album 3", "Synthwave", 200, 125, 8, "")   // Medium match
    };

    auto recs = RecommendationEngine::getRecommendations(target, library, 2);
    assert(recs.size() == 2);
    assert(recs[0].id == 2); // Retro Sunset should be #1 match
    std::cout << "PASSED\n";
}

int main() {
    std::cout << "=== RUNNING DSA UNIT TESTS ===\n";
    testDoublyLinkedList();
    testQueueAndStack();
    testTrie();
    testSorter();
    testRecommendations();
    std::cout << "=== ALL TESTS COMPLETED SUCCESSFULLY! ===\n";
    return 0;
}

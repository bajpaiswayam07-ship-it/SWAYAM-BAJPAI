import os
import sys

# Add python_ui to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "python_ui")))

from cpp_bridge import CppEngineBridge, SongInfo

def test_bridge_integration():
    print("=== Testing Python to C++ DLL Bridge ===")
    bridge = CppEngineBridge()
    assert bridge.is_native, "Expected bridge to load native C++ DLL!"

    # 1. Add songs
    s1 = SongInfo(1, "Blinding Lights", "The Weeknd", "After Hours", "Synthwave", 200, 171, 0, "dummy.mp3")
    s2 = SongInfo(2, "Levitating", "Dua Lipa", "Future Nostalgia", "Pop", 203, 103, 0, "dummy2.mp3")
    s3 = SongInfo(3, "Save Your Tears", "The Weeknd", "After Hours", "Synthwave", 215, 118, 0, "dummy3.mp3")

    id1 = bridge.add_song(s1)
    id2 = bridge.add_song(s2)
    id3 = bridge.add_song(s3)

    assert id1 == 1 and id2 == 2 and id3 == 3
    assert bridge.get_library_count() >= 3

    # 2. Test Song Info retrieval from C++
    fetched1 = bridge.get_song(1)
    assert fetched1 is not None
    assert fetched1.title == "Blinding Lights"
    assert fetched1.artist == "The Weeknd"
    assert fetched1.bpm == 171
    print("[PASS] Native C++ Song retrieval verified.")

    # 3. Test Playlist Operations
    assert bridge.create_playlist("Retro Waves")
    bridge.add_to_playlist("Retro Waves", 1)
    bridge.add_to_playlist("Retro Waves", 3)
    assert bridge.get_playlist_count("Retro Waves") == 2
    pl_songs = bridge.get_playlist_songs("Retro Waves")
    assert len(pl_songs) == 2
    assert pl_songs[0].id == 1 and pl_songs[1].id == 3
    print("[PASS] Native C++ Playlist Operations (Doubly Linked List) verified.")

    # 4. Test Queue and History
    bridge.enqueue(2)
    q = bridge.get_queue()
    assert len(q) == 1 and q[0].id == 2
    deq = bridge.dequeue()
    assert deq is not None and deq.id == 2
    assert len(bridge.get_queue()) == 0
    print("[PASS] Native C++ PlayQueue verified.")

    bridge.record_play(1)
    hist = bridge.get_history(5)
    assert len(hist) >= 1 and hist[0].id == 1
    print("[PASS] Native C++ History Stack verified.")

    # 5. Test Trie Autocomplete Search
    results = bridge.search("Weeknd")
    assert len(results) >= 2
    print(f"[PASS] Native C++ Trie Prefix Search verified (found {len(results)} matches for 'Weeknd').")

    # 6. Test Smart Recommendations
    recs = bridge.get_recommendations(1, 2)
    assert len(recs) >= 1
    # Save Your Tears should be top recommendation for Blinding Lights (same artist, same genre Synthwave)
    assert recs[0].id == 3
    print(f"[PASS] Native C++ Recommendation Engine verified (Recommended: '{recs[0].title}' for '{s1.title}').")

    # 7. Test Sorting (MergeSort in C++)
    bridge.sort_playlist("Retro Waves", criteria=0, ascending=True) # Title A-Z
    sorted_songs = bridge.get_playlist_songs("Retro Waves")
    assert sorted_songs[0].title == "Blinding Lights"
    assert sorted_songs[1].title == "Save Your Tears"
    print("[PASS] Native C++ MergeSort verified.")

    print("\n>>> ALL PYTHON-C++ BRIDGE INTEGRATION TESTS PASSED 100%! <<<\n")

if __name__ == "__main__":
    test_bridge_integration()

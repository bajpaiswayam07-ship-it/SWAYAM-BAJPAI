#ifndef DOUBLY_LINKED_LIST_HPP
#define DOUBLY_LINKED_LIST_HPP

#include "Song.hpp"
#include <vector>
#include <stdexcept>
#include <algorithm>
#include <random>

struct ListNode {
    Song song;
    ListNode* prev;
    ListNode* next;

    ListNode(const Song& s) : song(s), prev(nullptr), next(nullptr) {}
};

class DoublyLinkedList {
private:
    ListNode* head;
    ListNode* tail;
    int count;

public:
    DoublyLinkedList();
    ~DoublyLinkedList();

    // Copy and Move semantics
    DoublyLinkedList(const DoublyLinkedList& other);
    DoublyLinkedList& operator=(const DoublyLinkedList& other);
    DoublyLinkedList(DoublyLinkedList&& other) noexcept;
    DoublyLinkedList& operator=(DoublyLinkedList&& other) noexcept;

    // Core Operations
    void append(const Song& song);
    void prepend(const Song& song);
    bool insertAt(int index, const Song& song);
    bool removeAt(int index);
    bool removeById(int songId);
    bool move(int fromIndex, int toIndex);

    // Accessors
    Song* get(int index);
    const Song* get(int index) const;
    Song* getById(int songId);
    int size() const;
    bool isEmpty() const;
    void clear();

    // High level algorithms
    void reverse();
    void shuffle();
    std::vector<Song> toVector() const;

    // Iterators / Node pointers for fast traversal
    ListNode* getHead() const { return head; }
    ListNode* getTail() const { return tail; }
};

#endif // DOUBLY_LINKED_LIST_HPP

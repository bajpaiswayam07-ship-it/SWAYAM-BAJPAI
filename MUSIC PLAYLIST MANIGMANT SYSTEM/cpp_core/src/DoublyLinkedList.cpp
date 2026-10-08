#include "../include/DoublyLinkedList.hpp"
#include <chrono>

DoublyLinkedList::DoublyLinkedList() : head(nullptr), tail(nullptr), count(0) {}

DoublyLinkedList::~DoublyLinkedList() {
    clear();
}

void DoublyLinkedList::clear() {
    ListNode* curr = head;
    while (curr != nullptr) {
        ListNode* nxt = curr->next;
        delete curr;
        curr = nxt;
    }
    head = nullptr;
    tail = nullptr;
    count = 0;
}

DoublyLinkedList::DoublyLinkedList(const DoublyLinkedList& other) : head(nullptr), tail(nullptr), count(0) {
    ListNode* curr = other.head;
    while (curr != nullptr) {
        append(curr->song);
        curr = curr->next;
    }
}

DoublyLinkedList& DoublyLinkedList::operator=(const DoublyLinkedList& other) {
    if (this == &other) return *this;
    clear();
    ListNode* curr = other.head;
    while (curr != nullptr) {
        append(curr->song);
        curr = curr->next;
    }
    return *this;
}

DoublyLinkedList::DoublyLinkedList(DoublyLinkedList&& other) noexcept
    : head(other.head), tail(other.tail), count(other.count) {
    other.head = nullptr;
    other.tail = nullptr;
    other.count = 0;
}

DoublyLinkedList& DoublyLinkedList::operator=(DoublyLinkedList&& other) noexcept {
    if (this == &other) return *this;
    clear();
    head = other.head;
    tail = other.tail;
    count = other.count;
    other.head = nullptr;
    other.tail = nullptr;
    other.count = 0;
    return *this;
}

void DoublyLinkedList::append(const Song& song) {
    ListNode* newNode = new ListNode(song);
    if (!head) {
        head = tail = newNode;
    } else {
        tail->next = newNode;
        newNode->prev = tail;
        tail = newNode;
    }
    count++;
}

void DoublyLinkedList::prepend(const Song& song) {
    ListNode* newNode = new ListNode(song);
    if (!head) {
        head = tail = newNode;
    } else {
        newNode->next = head;
        head->prev = newNode;
        head = newNode;
    }
    count++;
}

bool DoublyLinkedList::insertAt(int index, const Song& song) {
    if (index < 0 || index > count) return false;
    if (index == 0) {
        prepend(song);
        return true;
    }
    if (index == count) {
        append(song);
        return true;
    }

    ListNode* curr = head;
    for (int i = 0; i < index; ++i) {
        curr = curr->next;
    }

    ListNode* newNode = new ListNode(song);
    newNode->prev = curr->prev;
    newNode->next = curr;
    curr->prev->next = newNode;
    curr->prev = newNode;
    count++;
    return true;
}

bool DoublyLinkedList::removeAt(int index) {
    if (index < 0 || index >= count || !head) return false;

    ListNode* target = nullptr;
    if (index == 0) {
        target = head;
        head = head->next;
        if (head) head->prev = nullptr;
        else tail = nullptr;
    } else if (index == count - 1) {
        target = tail;
        tail = tail->prev;
        if (tail) tail->next = nullptr;
        else head = nullptr;
    } else {
        // Optimize traversal from head or tail depending on index
        if (index < count / 2) {
            target = head;
            for (int i = 0; i < index; ++i) target = target->next;
        } else {
            target = tail;
            for (int i = count - 1; i > index; --i) target = target->prev;
        }
        target->prev->next = target->next;
        target->next->prev = target->prev;
    }

    delete target;
    count--;
    return true;
}

bool DoublyLinkedList::removeById(int songId) {
    ListNode* curr = head;
    int idx = 0;
    while (curr != nullptr) {
        if (curr->song.id == songId) {
            return removeAt(idx);
        }
        curr = curr->next;
        idx++;
    }
    return false;
}

bool DoublyLinkedList::move(int fromIndex, int toIndex) {
    if (fromIndex < 0 || fromIndex >= count || toIndex < 0 || toIndex >= count || fromIndex == toIndex) {
        return false;
    }
    Song* s = get(fromIndex);
    if (!s) return false;
    Song songCopy = *s;
    removeAt(fromIndex);
    insertAt(toIndex, songCopy);
    return true;
}

Song* DoublyLinkedList::get(int index) {
    if (index < 0 || index >= count) return nullptr;
    ListNode* curr = head;
    if (index < count / 2) {
        for (int i = 0; i < index; ++i) curr = curr->next;
    } else {
        curr = tail;
        for (int i = count - 1; i > index; --i) curr = curr->prev;
    }
    return &(curr->song);
}

const Song* DoublyLinkedList::get(int index) const {
    if (index < 0 || index >= count) return nullptr;
    ListNode* curr = head;
    if (index < count / 2) {
        for (int i = 0; i < index; ++i) curr = curr->next;
    } else {
        curr = tail;
        for (int i = count - 1; i > index; --i) curr = curr->prev;
    }
    return &(curr->song);
}

Song* DoublyLinkedList::getById(int songId) {
    ListNode* curr = head;
    while (curr != nullptr) {
        if (curr->song.id == songId) return &(curr->song);
        curr = curr->next;
    }
    return nullptr;
}

int DoublyLinkedList::size() const {
    return count;
}

bool DoublyLinkedList::isEmpty() const {
    return count == 0;
}

void DoublyLinkedList::reverse() {
    if (count <= 1) return;
    ListNode* curr = head;
    ListNode* temp = nullptr;
    while (curr != nullptr) {
        temp = curr->prev;
        curr->prev = curr->next;
        curr->next = temp;
        curr = curr->prev;
    }
    if (temp != nullptr) {
        tail = head;
        head = temp->prev;
    }
}

void DoublyLinkedList::shuffle() {
    if (count <= 1) return;
    std::vector<Song> songs = toVector();
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::shuffle(songs.begin(), songs.end(), std::default_random_engine(seed));

    clear();
    for (const auto& s : songs) {
        append(s);
    }
}

std::vector<Song> DoublyLinkedList::toVector() const {
    std::vector<Song> result;
    result.reserve(count);
    ListNode* curr = head;
    while (curr != nullptr) {
        result.push_back(curr->song);
        curr = curr->next;
    }
    return result;
}

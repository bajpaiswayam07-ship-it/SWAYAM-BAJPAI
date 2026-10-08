#include "../include/Sorter.hpp"
#include <cctype>

static std::string toLower(const std::string& s) {
    std::string res = s;
    for (char& c : res) c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
    return res;
}

bool Sorter::compare(const Song& a, const Song& b, SortCriteria criteria, bool ascending) {
    bool less = false;
    switch (criteria) {
        case SortCriteria::TITLE:
            less = toLower(a.title) < toLower(b.title);
            break;
        case SortCriteria::ARTIST:
            less = toLower(a.artist) < toLower(b.artist);
            break;
        case SortCriteria::DURATION:
            less = a.duration < b.duration;
            break;
        case SortCriteria::PLAY_COUNT:
            less = a.playCount < b.playCount;
            break;
        case SortCriteria::BPM:
            less = a.bpm < b.bpm;
            break;
    }
    return ascending ? less : !less;
}

void Sorter::merge(std::vector<Song>& arr, int left, int mid, int right, SortCriteria criteria, bool ascending) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    std::vector<Song> L(n1);
    std::vector<Song> R(n2);

    for (int i = 0; i < n1; ++i) L[i] = arr[left + i];
    for (int j = 0; j < n2; ++j) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (compare(L[i], R[j], criteria, ascending) || 
            (!compare(R[j], L[i], criteria, ascending))) { // handle equality stably
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }

    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void Sorter::mergeSortHelper(std::vector<Song>& arr, int left, int right, SortCriteria criteria, bool ascending) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSortHelper(arr, left, mid, criteria, ascending);
        mergeSortHelper(arr, mid + 1, right, criteria, ascending);
        merge(arr, left, mid, right, criteria, ascending);
    }
}

void Sorter::mergeSort(std::vector<Song>& songs, SortCriteria criteria, bool ascending) {
    if (songs.size() <= 1) return;
    mergeSortHelper(songs, 0, static_cast<int>(songs.size()) - 1, criteria, ascending);
}

int Sorter::partition(std::vector<Song>& arr, int low, int high, SortCriteria criteria, bool ascending) {
    Song pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; ++j) {
        if (compare(arr[j], pivot, criteria, ascending)) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void Sorter::quickSortHelper(std::vector<Song>& arr, int low, int high, SortCriteria criteria, bool ascending) {
    if (low < high) {
        int pi = partition(arr, low, high, criteria, ascending);
        quickSortHelper(arr, low, pi - 1, criteria, ascending);
        quickSortHelper(arr, pi + 1, high, criteria, ascending);
    }
}

void Sorter::quickSort(std::vector<Song>& songs, SortCriteria criteria, bool ascending) {
    if (songs.size() <= 1) return;
    quickSortHelper(songs, 0, static_cast<int>(songs.size()) - 1, criteria, ascending);
}

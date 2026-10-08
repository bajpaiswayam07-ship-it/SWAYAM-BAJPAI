#ifndef SORTER_HPP
#define SORTER_HPP

#include "Song.hpp"
#include <vector>
#include <string>
#include <algorithm>

enum class SortCriteria {
    TITLE = 0,
    ARTIST = 1,
    DURATION = 2,
    PLAY_COUNT = 3,
    BPM = 4
};

class Sorter {
private:
    static bool compare(const Song& a, const Song& b, SortCriteria criteria, bool ascending);
    static void merge(std::vector<Song>& arr, int left, int mid, int right, SortCriteria criteria, bool ascending);
    static void mergeSortHelper(std::vector<Song>& arr, int left, int right, SortCriteria criteria, bool ascending);

    static int partition(std::vector<Song>& arr, int low, int high, SortCriteria criteria, bool ascending);
    static void quickSortHelper(std::vector<Song>& arr, int low, int high, SortCriteria criteria, bool ascending);

public:
    static void mergeSort(std::vector<Song>& songs, SortCriteria criteria, bool ascending = true);
    static void quickSort(std::vector<Song>& songs, SortCriteria criteria, bool ascending = true);
};

#endif // SORTER_HPP

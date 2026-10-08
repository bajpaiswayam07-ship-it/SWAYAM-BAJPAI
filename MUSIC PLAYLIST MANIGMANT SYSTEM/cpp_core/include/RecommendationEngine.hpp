#ifndef RECOMMENDATION_ENGINE_HPP
#define RECOMMENDATION_ENGINE_HPP

#include "Song.hpp"
#include <vector>
#include <queue>
#include <cmath>
#include <algorithm>

struct ScoredSong {
    Song song;
    double score;

    bool operator<(const ScoredSong& other) const {
        // Min-heap by score so top scores stay in heap
        return score > other.score;
    }
};

class RecommendationEngine {
public:
    static double calculateSimilarity(const Song& a, const Song& b);
    static std::vector<Song> getRecommendations(const Song& target,
                                                const std::vector<Song>& library,
                                                int topK = 5);
};

#endif // RECOMMENDATION_ENGINE_HPP

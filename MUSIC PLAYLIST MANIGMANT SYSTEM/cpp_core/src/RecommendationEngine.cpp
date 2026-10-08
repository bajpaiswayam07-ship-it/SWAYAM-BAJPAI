#include "../include/RecommendationEngine.hpp"

static std::string toLowerStr(const std::string& s) {
    std::string res = s;
    for (char& c : res) c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
    return res;
}

double RecommendationEngine::calculateSimilarity(const Song& a, const Song& b) {
    if (a.id == b.id) return -1.0; // Don't recommend the exact same song

    double score = 0.0;

    // 1. Genre match (Weight: 40%)
    if (toLowerStr(a.genre) == toLowerStr(b.genre)) {
        score += 40.0;
    }

    // 2. Artist match (Weight: 30%)
    if (toLowerStr(a.artist) == toLowerStr(b.artist)) {
        score += 30.0;
    }

    // 3. BPM proximity (Weight: 20%)
    double bpmDiff = std::abs(a.bpm - b.bpm);
    double bpmSim = std::max(0.0, 1.0 - (bpmDiff / 80.0));
    score += (bpmSim * 20.0);

    // 4. Duration similarity (Weight: 10%)
    double durDiff = std::abs(a.duration - b.duration);
    double durSim = std::max(0.0, 1.0 - (durDiff / 180.0));
    score += (durSim * 10.0);

    return score;
}

std::vector<Song> RecommendationEngine::getRecommendations(const Song& target,
                                                           const std::vector<Song>& library,
                                                           int topK) {
    if (topK <= 0 || library.empty()) return {};

    // Max-heap approach using standard sort or priority queue
    std::vector<std::pair<double, Song>> scored;
    scored.reserve(library.size());

    for (const auto& song : library) {
        if (song.id == target.id) continue;
        double s = calculateSimilarity(target, song);
        if (s > 0.0) {
            scored.push_back({s, song});
        }
    }

    // Sort descending by score
    std::sort(scored.begin(), scored.end(),
              [](const std::pair<double, Song>& p1, const std::pair<double, Song>& p2) {
                  return p1.first > p2.first;
              });

    std::vector<Song> result;
    int limit = std::min(topK, static_cast<int>(scored.size()));
    for (int i = 0; i < limit; ++i) {
        result.push_back(scored[i].second);
    }
    return result;
}

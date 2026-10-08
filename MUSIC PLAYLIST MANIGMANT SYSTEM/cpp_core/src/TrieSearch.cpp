#include "../include/TrieSearch.hpp"
#include <cctype>
#include <sstream>

TrieNode::~TrieNode() {
    for (auto& pair : children) {
        delete pair.second;
    }
}

TrieSearch::TrieSearch() {
    root = new TrieNode();
}

TrieSearch::~TrieSearch() {
    delete root;
}

void TrieSearch::clear() {
    delete root;
    root = new TrieNode();
}

std::string TrieSearch::normalize(const std::string& str) const {
    std::string res;
    for (char c : str) {
        if (std::isalnum(static_cast<unsigned char>(c))) {
            res += static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        } else if (c == ' ' || c == '-' || c == '_') {
            res += ' ';
        }
    }
    return res;
}

void TrieSearch::insertWord(const std::string& word, int songId) {
    if (word.empty()) return;
    TrieNode* curr = root;
    for (char c : word) {
        if (curr->children.find(c) == curr->children.end()) {
            curr->children[c] = new TrieNode();
        }
        curr = curr->children[c];
        curr->songIds.insert(songId);
    }
    curr->isEndOfWord = true;
}

void TrieSearch::indexSong(int songId, const std::string& title, const std::string& artist,
                           const std::string& album, const std::string& genre) {
    std::string fullText = title + " " + artist + " " + album + " " + genre;
    std::string cleaned = normalize(fullText);
    std::stringstream ss(cleaned);
    std::string word;
    while (ss >> word) {
        insertWord(word, songId);
    }
}

void TrieSearch::collectAllIds(TrieNode* node, std::unordered_set<int>& results) const {
    if (!node) return;
    for (int id : node->songIds) {
        results.insert(id);
    }
    for (const auto& pair : node->children) {
        collectAllIds(pair.second, results);
    }
}

std::vector<int> TrieSearch::searchPrefix(const std::string& prefix) const {
    std::string cleanPrefix = normalize(prefix);
    std::stringstream ss(cleanPrefix);
    std::string word;
    std::vector<std::string> words;
    while (ss >> word) {
        words.push_back(word);
    }

    if (words.empty()) return {};

    // For multi-word queries (e.g., "Taylor Pop"), compute intersection of results
    std::unordered_set<int> finalIds;
    bool isFirst = true;

    for (const auto& w : words) {
        TrieNode* curr = root;
        bool found = true;
        for (char c : w) {
            if (curr->children.find(c) == curr->children.end()) {
                found = false;
                break;
            }
            curr = curr->children[c];
        }

        std::unordered_set<int> wordIds;
        if (found && curr != nullptr) {
            collectAllIds(curr, wordIds);
        }

        if (isFirst) {
            finalIds = wordIds;
            isFirst = false;
        } else {
            std::unordered_set<int> intersected;
            for (int id : finalIds) {
                if (wordIds.find(id) != wordIds.end()) {
                    intersected.insert(id);
                }
            }
            finalIds = intersected;
        }
    }

    return std::vector<int>(finalIds.begin(), finalIds.end());
}

#ifndef TRIE_SEARCH_HPP
#define TRIE_SEARCH_HPP

#include <unordered_map>
#include <vector>
#include <string>
#include <unordered_set>

struct TrieNode {
    std::unordered_map<char, TrieNode*> children;
    std::unordered_set<int> songIds;
    bool isEndOfWord;

    TrieNode() : isEndOfWord(false) {}
    ~TrieNode();
};

class TrieSearch {
private:
    TrieNode* root;

    void collectAllIds(TrieNode* node, std::unordered_set<int>& results) const;
    std::string normalize(const std::string& str) const;

public:
    TrieSearch();
    ~TrieSearch();

    void insertWord(const std::string& word, int songId);
    void indexSong(int songId, const std::string& title, const std::string& artist,
                   const std::string& album, const std::string& genre);
    void removeSong(int songId); // Clears and rebuilds or removes
    std::vector<int> searchPrefix(const std::string& prefix) const;
    void clear();
};

#endif // TRIE_SEARCH_HPP

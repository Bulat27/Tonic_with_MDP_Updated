// File: Unbiased_Space_Saving.h
#ifndef UNBIASED_SPACE_SAVING_H
#define UNBIASED_SPACE_SAVING_H

#include <vector>
#include <unordered_map>
#include <random>
#include <utility>

class UnbiasedSpaceSaving {
public:
    UnbiasedSpaceSaving(int k, int seed);

    void update(int node);

    std::vector<std::pair<int, int>> top_k() const;

private:
    struct HeapNode {
        int node;
        int freq;
    };

    int capacity_;
    std::vector<HeapNode> heap_;
    std::unordered_map<int, int> node_to_index_;
    std::mt19937 gen_;
    std::uniform_real_distribution<double> dist_;

    int left(int i) const;
    int right(int i) const;
    void sift_down(int i);
    void swap_nodes(int i, int j);
};

#endif
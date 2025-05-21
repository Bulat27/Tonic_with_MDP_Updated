#include "Unbiased_Space_Saving.h"
#include <algorithm>

#include <iostream>

UnbiasedSpaceSaving::UnbiasedSpaceSaving(int k, int seed)
    : capacity_(k), gen_(seed), dist_(0.0, 1.0) {
    heap_.resize(k, {-1, 0});  // Dummy node: -1 means unused
}

void UnbiasedSpaceSaving::update(int node) {
    auto it = node_to_index_.find(node);
    if (it != node_to_index_.end()) {
        int i = it->second;
        heap_[i].freq++;
        sift_down(i);
    } else {
        int min_idx = 0;
        if (heap_[min_idx].node == -1) {
            // Place new node at root
            heap_[min_idx] = {node, 1};
            node_to_index_[node] = min_idx;
            sift_down(min_idx);
        } else {
            int min_freq = heap_[min_idx].freq;
            double prob = 1.0 / (min_freq + 1);
            if (dist_(gen_) < prob) {
                int evicted = heap_[min_idx].node;
                node_to_index_.erase(evicted);
                heap_[min_idx] = {node, min_freq + 1};
                node_to_index_[node] = min_idx;
                sift_down(min_idx);
            }
        }
    }
}

const std::vector<UnbiasedSpaceSaving::HeapNode>& UnbiasedSpaceSaving::top_n(int n) {
    if (n > static_cast<int>(heap_.size()))
        n = heap_.size();

    std::partial_sort(
        heap_.begin(), heap_.begin() + n, heap_.end(),
        [](const HeapNode& a, const HeapNode& b) {
            return a.freq > b.freq;
        });

    heap_.resize(n);  // keep only top-n
    return heap_;
}

int UnbiasedSpaceSaving::left(int i) const {
    return 2 * i + 1;
}

int UnbiasedSpaceSaving::right(int i) const {
    return 2 * i + 2;
}

void UnbiasedSpaceSaving::sift_down(int i) {
    int n = capacity_;
    while (true) {
        int l = left(i), r = right(i), smallest = i;
        if (l < n && heap_[l].freq < heap_[smallest].freq) smallest = l;
        if (r < n && heap_[r].freq < heap_[smallest].freq) smallest = r;
        if (smallest != i) {
            swap_nodes(i, smallest);
            i = smallest;
        } else break;
    }
}

void UnbiasedSpaceSaving::swap_nodes(int i, int j) {
    std::swap(heap_[i], heap_[j]);
    node_to_index_[heap_[i].node] = i;
    node_to_index_[heap_[j].node] = j;
}
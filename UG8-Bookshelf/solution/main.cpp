#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>

// ADDED: supplied range-add/minimum tree; the learner task is the DP model.
class RangeCosts {
    static constexpr std::int64_t infinity = 4000000000000000000LL;
    int size_;
    std::vector<std::int64_t> minimum_, pending_;
    void apply(int node, std::int64_t value) {
        minimum_[node] += value; pending_[node] += value;
    }
    void push(int node) {
        if (pending_[node] == 0) return;
        apply(2 * node, pending_[node]); apply(2 * node + 1, pending_[node]);
        pending_[node] = 0;
    }
    void assign(int node, int left, int right, int index, std::int64_t value) {
        if (right - left == 1) { minimum_[node] = value; pending_[node] = 0; return; }
        push(node);
        const int middle = left + (right - left) / 2;
        if (index < middle) assign(2 * node, left, middle, index, value);
        else assign(2 * node + 1, middle, right, index, value);
        minimum_[node] = std::min(minimum_[2 * node], minimum_[2 * node + 1]);
    }
    void add(int node, int left, int right, int begin, int end, std::int64_t value) {
        if (end <= left || right <= begin) return;
        if (begin <= left && right <= end) { apply(node, value); return; }
        push(node);
        const int middle = left + (right - left) / 2;
        add(2 * node, left, middle, begin, end, value);
        add(2 * node + 1, middle, right, begin, end, value);
        minimum_[node] = std::min(minimum_[2 * node], minimum_[2 * node + 1]);
    }
    std::int64_t query(int node, int left, int right, int begin, int end) {
        if (end <= left || right <= begin) return infinity;
        if (begin <= left && right <= end) return minimum_[node];
        push(node);
        const int middle = left + (right - left) / 2;
        return std::min(query(2 * node, left, middle, begin, end),
                        query(2 * node + 1, middle, right, begin, end));
    }
public:
    explicit RangeCosts(int size) : size_(size), minimum_(4 * size, infinity), pending_(4 * size, 0) {}
    void assign(int index, std::int64_t value) { assign(1, 0, size_, index, value); }
    void add(int begin, int end, std::int64_t value) { if (begin < end) add(1, 0, size_, begin, end, value); }
    std::int64_t query(int begin, int end) { return query(1, 0, size_, begin, end); }
};

struct Book { int height; std::int64_t width; };

// ADDED: candidate j is dp[j] plus the height of the shelf containing books j..i.
std::int64_t minimumHeight(const std::vector<Book>& books, std::int64_t limit) {
    const int n = static_cast<int>(books.size());
    RangeCosts costs(n);
    std::vector<std::int64_t> best(n + 1, 0);
    std::vector<std::pair<int, int>> maxima;
    std::int64_t width = 0;
    int first = 0;
    for (int i = 0; i < n; ++i) {
        const int height = books[i].height;
        int start = i;
        while (!maxima.empty() && maxima.back().first <= height) {
            const auto [oldHeight, oldStart] = maxima.back();
            costs.add(oldStart, start, static_cast<std::int64_t>(height) - oldHeight);
            start = oldStart;
            maxima.pop_back();
        }
        costs.assign(i, best[i] + height);
        maxima.emplace_back(height, start);
        width += books[i].width;
        while (width > limit) width -= books[first++].width;
        best[i + 1] = costs.query(first, i + 1);
    }
    return best[n];
}

// ADDED: each book line is HEIGHT then WIDTH, not the reverse.
int main() {
    try {
        std::ifstream input("bookshelf.in");
        int n;
        std::int64_t limit;
        if (!(input >> n >> limit) || n < 1 || n > 100000 || limit < 1 || limit > 1000000000LL)
            throw std::runtime_error("Invalid N or L in bookshelf.in");
        std::vector<Book> books(n);
        for (auto& book : books)
            if (!(input >> book.height >> book.width) || book.height < 1 || book.height > 1000000 || book.width < 1 || book.width > limit)
                throw std::runtime_error("Invalid book height or width");
        const auto answer = minimumHeight(books, limit);
        std::ofstream output("bookshelf.out");
        if (!output) throw std::runtime_error("Cannot write bookshelf.out");
        output << answer << '\n';
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n'; return 2;
    }
}

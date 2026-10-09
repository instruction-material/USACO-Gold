#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

// ADDED: iterative tree storage. Every range uses half-open indices [left, right).
class AggregateTree {
    int width_ = 1;
    bool maximum_;
    std::vector<std::int64_t> nodes_;
    std::int64_t combine(std::int64_t a, std::int64_t b) const {
        return maximum_ ? std::max(a, b) : a + b;
    }
public:
    AggregateTree(int size, bool maximum) : maximum_(maximum) {
        while (width_ < size) width_ *= 2;
        nodes_.assign(2 * width_, 0);
    }
    void set(int index, std::int64_t value) {
        (void)index; (void)value;
        // TODO 1: assign a leaf and rebuild its ancestors with combine().
        throw std::logic_error("Complete AggregateTree::set before running the starter");
    }
    std::int64_t range(int left, int right) const {
        (void)left; (void)right;
        // TODO 2: aggregate exactly [left, right), returning zero for an empty range.
        throw std::logic_error("Complete AggregateTree::range before running the starter");
    }
};

struct Point { int x, y; };

std::int64_t distance(Point a, Point b) {
    return std::abs(static_cast<std::int64_t>(a.x) - b.x)
         + std::abs(static_cast<std::int64_t>(a.y) - b.y);
}

// ADDED: edge i joins points i and i+1; gain i is the saving from skipping point i.
class Route {
    std::vector<Point> points_;
    AggregateTree edges_, gains_;
    std::int64_t gain(int i) const {
        if (i <= 0 || i + 1 >= static_cast<int>(points_.size())) return 0;
        return distance(points_[i-1], points_[i]) + distance(points_[i], points_[i+1])
             - distance(points_[i-1], points_[i+1]);
    }
public:
    explicit Route(const std::vector<Point>& points)
        : points_(points), edges_(static_cast<int>(points.size()) - 1, false),
          gains_(static_cast<int>(points.size()), true) {
        for (int i = 0; i + 1 < static_cast<int>(points_.size()); ++i)
            edges_.set(i, distance(points_[i], points_[i+1]));
        for (int i = 0; i < static_cast<int>(points_.size()); ++i)
            gains_.set(i, gain(i));
    }
    std::int64_t query(int left, int right) const {
        const auto full = edges_.range(left, right);
        if (right - left < 2) return full;
        return full - gains_.range(left + 1, right);
    }
    void update(int index, Point point) {
        (void)index; (void)point;
        // TODO 3: replace one point, then refresh only its affected edges and gains.
        throw std::logic_error("Complete Route::update before running the starter");
    }
};

// ADDED: preserve official one-based input; tree storage uses zero-based indices.
int main() {
    try {
        std::ifstream input("marathon.in");
        int n, q;
        if (!(input >> n >> q) || n < 1 || n > 100000 || q < 1 || q > 100000)
            throw std::runtime_error("Expected valid N and Q in marathon.in");
        std::vector<Point> points(n);
        for (auto& point : points)
            if (!(input >> point.x >> point.y) || point.x < -1000 || point.x > 1000 || point.y < -1000 || point.y > 1000)
                throw std::runtime_error("Invalid checkpoint");
        Route route(points);
        std::vector<std::int64_t> answers;
        for (int k = 0; k < q; ++k) {
            char command;
            int a;
            if (!(input >> command >> a) || a < 1 || a > n)
                throw std::runtime_error("Invalid command or checkpoint index");
            if (command == 'U') {
                Point point;
                if (!(input >> point.x >> point.y) || point.x < -1000 || point.x > 1000 || point.y < -1000 || point.y > 1000)
                    throw std::runtime_error("Invalid updated checkpoint");
                route.update(a - 1, point);
            } else if (command == 'Q') {
                int b;
                if (!(input >> b) || b < a || b > n) throw std::runtime_error("Invalid sub-route");
                answers.push_back(route.query(a - 1, b - 1));
            } else throw std::runtime_error("Unknown command");
        }
        std::ofstream output("marathon.out");
        if (!output) throw std::runtime_error("Cannot write marathon.out");
        for (auto answer : answers) output << answer << '\n';
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}

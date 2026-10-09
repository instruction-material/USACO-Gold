#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

// ADDED: advantage belongs to whoever moves next in the remaining interval.
std::int64_t maximumFirstPlayerTotal(const std::vector<int>& coins) {
    std::vector<std::int64_t> advantage(coins.begin(), coins.end());
    const int n = static_cast<int>(coins.size());
    for (int length = 2; length <= n; ++length) {
        // Left-to-right preserves both shorter intervals until they are used.
        for (int left = 0; left + length <= n; ++left) {
            const int right = left + length - 1;
            advantage[left] = std::max(coins[left] - advantage[left + 1],
                                       coins[right] - advantage[left]);
        }
    }
    const auto total = std::accumulate(coins.begin(), coins.end(), std::int64_t{0});
    return (total + advantage[0]) / 2;
}

// ADDED: supplied file driver; failed attempts leave any existing output untouched.
int main() {
    try {
        std::ifstream input("treasure.in");
        int n;
        if (!(input >> n) || n < 1 || n > 5000)
            throw std::runtime_error("Invalid coin count in treasure.in");
        std::vector<int> coins(n);
        for (int& value : coins)
            if (!(input >> value) || value < 1 || value > 5000)
                throw std::runtime_error("Invalid coin value in treasure.in");
        std::string extra;
        if (input >> extra) throw std::runtime_error("Invalid trailing data in treasure.in");
        const auto answer = maximumFirstPlayerTotal(coins);
        std::ofstream output("treasure.out");
        if (!output) throw std::runtime_error("Cannot write treasure.out");
        output << answer << '\n';
        if (!output) throw std::runtime_error("Cannot finish treasure.out");
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}

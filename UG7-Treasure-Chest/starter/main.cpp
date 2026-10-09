#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

// ADDED: learner task; retain the supplied input/output driver.
std::int64_t maximumFirstPlayerTotal(const std::vector<int>& coins) {
    (void)coins;
    // TODO: evaluate both end choices while accounting for an optimal opponent.
    throw std::logic_error("Complete maximumFirstPlayerTotal before checking treasure.out");
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

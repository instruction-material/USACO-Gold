#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

// ADDED: learner task. The driver guarantees 0 <= n <= 92.
std::int64_t fibonacci(int n) {
    (void)n;
    // TODO: define the state, handle F(0) and F(1), then evaluate the recurrence.
    throw std::logic_error("Complete fibonacci before running the starter");
}

// ADDED: file driver with the signed 64-bit index boundary.
int main() {
    try {
        std::ifstream input("fibonacci.in");
        int n;
        if (!(input >> n) || n < 0 || n > 92)
            throw std::runtime_error("Expected an index from 0 through 92 in fibonacci.in");
        const auto answer = fibonacci(n);
        std::ofstream output("fibonacci.out");
        if (!output) throw std::runtime_error("Cannot write fibonacci.out");
        output << answer << '\n';
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}

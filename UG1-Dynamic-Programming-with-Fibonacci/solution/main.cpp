#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

// ADDED: state[k] stores F(k); dependencies are evaluated before their users.
std::int64_t fibonacci(int n) {
    std::vector<std::int64_t> state(n + 1, 0);
    if (n >= 1) state[1] = 1;
    for (int k = 2; k <= n; ++k)
        state[k] = state[k - 1] + state[k - 2];
    return state[n];
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

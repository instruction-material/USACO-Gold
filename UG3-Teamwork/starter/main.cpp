#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>

// ADDED: learner task. File handling and valid input bounds are provided.
std::int64_t bestTeamwork(const std::vector<int>& skills, int maximumTeam) {
    (void)skills; (void)maximumTeam;
    // TODO: define a prefix DP, consider every allowable final team,
    // and update its running maximum skill while extending backward.
    throw std::logic_error("Complete bestTeamwork before running the starter");
}

// ADDED: retain official teamwork.in / teamwork.out file conventions.
int main() {
    try {
        std::ifstream input("teamwork.in");
        int n, maximumTeam;
        if (!(input >> n >> maximumTeam) || n < 1 || n > 10000 || maximumTeam < 1 || maximumTeam > 1000)
            throw std::runtime_error("Invalid N or K in teamwork.in");
        std::vector<int> skills(n);
        for (auto& skill : skills)
            if (!(input >> skill) || skill < 1 || skill > 100000)
                throw std::runtime_error("Invalid cow skill");
        const auto answer = bestTeamwork(skills, maximumTeam);
        std::ofstream output("teamwork.out");
        if (!output) throw std::runtime_error("Cannot write teamwork.out");
        output << answer << '\n';
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n'; return 2;
    }
}

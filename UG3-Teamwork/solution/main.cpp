#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>

// ADDED: best[i] covers exactly the first i cows; every final team is considered.
std::int64_t bestTeamwork(const std::vector<int>& skills, int maximumTeam) {
    const int n = static_cast<int>(skills.size());
    std::vector<std::int64_t> best(n + 1, 0);
    for (int end = 1; end <= n; ++end) {
        int maximumSkill = 0;
        for (int size = 1; size <= maximumTeam && size <= end; ++size) {
            maximumSkill = std::max(maximumSkill, skills[end - size]);
            best[end] = std::max(best[end], best[end - size]
                + static_cast<std::int64_t>(size) * maximumSkill);
        }
    }
    return best[n];
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

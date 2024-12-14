#include <iostream>
#include <vector>
#include <fstream>
#include <regex>
#include <ranges>
#include <algorithm>
#include <chrono>
#include <sstream>

using namespace std;

const int WIDTH = 101;
const int HEIGHT = 103;

struct Vec2
{
    int x;
    int y;
};

struct Robot
{
    Vec2 pos;
    Vec2 vel;
};

vector<Robot> read_input(const std::string &file_name)
{
    vector<Robot> robots;
    ifstream input_file(file_name);
    stringstream ss;
    ss << input_file.rdbuf();
    string str;
    match_results<std::string::const_iterator> match;
    basic_regex regex(R"(p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+))");
    while (getline(ss, str))
    {
        regex_match(str, match, regex);
        auto vec = match | ranges::views::drop(1) | ranges::views::transform([](auto &m)
                                                                             { return stoi(m.str()); });
        robots.emplace_back(Robot({vec[0], vec[1]}, {vec[2], vec[3]}));
    }
    return robots;
}

int better_mod(int n, int m)
{
    return n < 0 ? n - m * (n / m - 1) : n % m;
}

vector<Vec2> calc_positions(const vector<Robot> &robots, int t)
{
    vector<Vec2> positions;
    positions.reserve(robots.size());
    for (auto &robot : robots)
    {
        positions.push_back({better_mod(robot.pos.x + robot.vel.x * t, WIDTH), better_mod(robot.pos.y + robot.vel.y * t, HEIGHT)});
    }
    return positions;
}

pair<int, int> calc_scores(const vector<Vec2> &positions)
{
    vector<int> v_scores(WIDTH, 0);
    vector<int> h_scores(HEIGHT, 0);
    for (const Vec2 &pos : positions)
    {
        v_scores[pos.x] += 1;
        h_scores[pos.y] += 1;
    }
    return {*max_element(h_scores.cbegin(), h_scores.cend()), *max_element(v_scores.cbegin(), v_scores.cend())};
}

pair<int, int> find_offsets(const vector<Robot> &robots)
{
    int h_best_score[] = {0, -1};
    int v_best_score[] = {0, -1};
    for (int t : ranges::views::iota(0, max(WIDTH, HEIGHT)))
    {
        auto [h_score, v_score] = calc_scores(calc_positions(robots, t));
        if (h_score > h_best_score[0])
        {
            h_best_score[0] = h_score;
            h_best_score[1] = t;
        }
        if (v_score > v_best_score[0])
        {
            v_best_score[0] = v_score;
            v_best_score[1] = t;
        }
    }
    return {v_best_score[1], h_best_score[1]};
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        cerr << "ERROR: Takes one and only one argument." << endl;
        return -1;
    }
    auto timer_start = chrono::high_resolution_clock::now();
    auto robots = read_input(argv[1]);
    auto read_duration = chrono::high_resolution_clock::now() - timer_start;
    auto [delta_x, delta_y] = find_offsets(robots);
    int delta_n = delta_y - delta_x;
    int nx = delta_n * 51;
    int factor = nx / HEIGHT;
    if (nx < 0)
    {
        factor -= 1;
    }
    nx -= HEIGHT * factor;
    int t = delta_x + nx * WIDTH;
    auto duration = chrono::high_resolution_clock::now() - timer_start - read_duration;
    cout << "Found t=" << t << " in " << duration_cast<chrono::microseconds>(duration) << " (Reading the input file took " << duration_cast<chrono::microseconds>(read_duration) << ")" << endl;
    return 0;
}
#include <bitset>
#include <chrono>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

using namespace std;

vector<ulong> read_input(const std::string& file_name) {
    vector<ulong> secrets;
    ifstream input_file(file_name);
    stringstream ss;
    ss << input_file.rdbuf();
    string str;
    while (getline(ss, str)) {
        secrets.push_back(stoi(str));
    }
    return secrets;
}

ulong next_secret(ulong secret) {
    const ulong modulo = 16777216;
    secret ^= secret << 6;
    secret %= modulo;
    secret ^= secret >> 5;
    secret %= modulo;
    secret ^= secret << 11;
    secret %= modulo;
    return secret;
}

ulong conduct_banana_trade(ulong secret, vector<ulong>* bananas, bitset<19 * 19 * 19 * 19>* touched) {
    int_fast8_t last_price = secret % 10;
    int_fast8_t seq[4] = {0, 0, 0, 0};
    ulong n = 0;
    while (n < 3) {
        secret = next_secret(secret);
        int_fast8_t price = secret % 10;
        seq[++n] = price - last_price;
        last_price = price;
    }
    while (n++ < 2000) {
        secret = next_secret(secret);
        int_fast8_t price = secret % 10;
        seq[0] = seq[1];
        seq[1] = seq[2];
        seq[2] = seq[3];
        seq[3] = price - last_price;
        last_price = price;
        uint_fast32_t index = 19 * 19 * 19 * (seq[0] + 9) + 19 * 19 * (seq[1] + 9) + 19 * (seq[2] + 9) + (seq[3] + 9);
        if (!(*touched)[index]) {
            (*touched)[index] = true;
            (*bananas)[index] += price;
        }
    }
    return secret;
}

pair<ulong, ulong> trade(const vector<ulong>& secrets) {
    ulong secret_sum = 0;
    vector<ulong> bananas(19 * 19 * 19 * 19, 0);
    bitset<19 * 19 * 19 * 19> touched;
    vector<int_fast8_t> seq(4, 0);
    for (ulong secret : secrets) {
        touched.reset();
        secret_sum += conduct_banana_trade(secret, &bananas, &touched);
    }
    return pair<ulong, ulong>(secret_sum, *max_element(bananas.cbegin(), bananas.cend()));
}

int main(int argc, char** argv) {
    if (argc != 2) {
        cerr << "ERROR: Takes one and only one argument." << endl;
        return -1;
    }
    auto timer_start = chrono::high_resolution_clock::now();
    auto secrets = read_input(argv[1]);
    auto timer_read = chrono::high_resolution_clock::now();
    auto [secret_sum, bananas] = trade(secrets);
    auto timer_part1and2 = chrono::high_resolution_clock::now();
    cout << "Calculated the secret sum: " << secret_sum << ", and aquired " << bananas << " bananas in "
         << duration_cast<chrono::microseconds>(timer_part1and2 - timer_read) << ", while reading the input file took "
         << duration_cast<chrono::microseconds>(timer_read - timer_start) << endl;
    return 0;
}

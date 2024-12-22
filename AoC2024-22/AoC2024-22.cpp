#include <iostream>
#include <vector>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <chrono>
#include <sstream>
#include <numeric>

using namespace std;

vector<ulong> read_input(const std::string &file_name)
{
    vector<ulong> secrets;
    ifstream input_file(file_name);
    stringstream ss;
    ss << input_file.rdbuf();
    string str;
    while (getline(ss, str))
    {
        secrets.push_back(stoi(str));
    }
    return secrets;
}

ulong next_secret(ulong secret)
{
    const ulong modulo = 16777216;
    secret ^= secret << 6;
    secret %= modulo;
    secret ^= secret >> 5;
    secret %= modulo;
    secret ^= secret << 11;
    secret %= modulo;
    return secret;
}

ulong predict_secrets(const vector<ulong> &seller_secrets)
{
    ulong secret_sum = 0;
    for (auto secret : seller_secrets)
    {
        for (auto n = 0; n < 2000; ++n)
        {
            secret = next_secret(secret);
        }
        secret_sum += secret;
    }
    return secret_sum;
}

bool unreasonable_sequence(const int_fast8_t *seq)
{
    return abs(seq[0] + seq[1] + seq[2] + seq[3]) > 9;
}

ulong sell_to_single_buyer_with_sequence(ulong secret, const int_fast8_t *seq)
{
    int_fast8_t last_price = secret % 10;
    int_fast8_t last_seq[4] = {-100, -100, -100, -100};
    ulong n = 0;
    while (n++ < 2000)
    {
        secret = next_secret(secret);
        int_fast8_t price = secret % 10;
        last_seq[0] = last_seq[1];
        last_seq[1] = last_seq[2];
        last_seq[2] = last_seq[3];
        last_seq[3] = price - last_price;
        last_price = price;
        if (seq[0] == last_seq[0] && seq[1] == last_seq[1] && seq[2] == last_seq[2] && seq[3] == last_seq[3])
        {
            return price;
        }
    }
    return 0uL;
}

ulong sell_for_bananas(const vector<ulong> &secrets)
{
    ulong record_bananas = 0;
    vector<int_fast8_t> record_seq(4);
    int_fast8_t seq[4] = {0, 0, 0, 0};
    for (seq[0] = -9; seq[0] < 10; ++seq[0])
    {
        for (seq[1] = -9; seq[1] < 10; ++seq[1])
        {
            for (seq[2] = -9; seq[2] < 10; ++seq[2])
            {
                for (seq[3] = -9; seq[3] < 10; ++seq[3])
                {
                    if (unreasonable_sequence(seq))
                    {
                        continue;
                    }
                    ulong bananas = 0;
                    for (ulong secret : secrets)
                    {
                        bananas += sell_to_single_buyer_with_sequence(secret, seq);
                    }
                    if (bananas > record_bananas)
                    {
                        record_bananas = bananas;
                        record_seq[0] = seq[0];
                        record_seq[1] = seq[1];
                        record_seq[2] = seq[2];
                        record_seq[3] = seq[3];
                    }
                }
            }
        }
    }
    cout << "Record sequence: ";
    for (int_fast8_t i : record_seq)
    {
        cout << int(i) << " ";
    }
    cout << " yielding " << record_bananas << " bananas" << endl;
    return record_bananas;
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        cerr << "ERROR: Takes one and only one argument." << endl;
        return -1;
    }
    auto timer_start = chrono::high_resolution_clock::now();
    auto secrets = read_input(argv[1]);
    auto timer_read = chrono::high_resolution_clock::now();
    auto secret_sum = predict_secrets(secrets);
    auto timer_part1 = chrono::high_resolution_clock::now();
    ulong bananas = sell_for_bananas(secrets);
    auto timer_part2 = chrono::high_resolution_clock::now();
    cout << "Calculated the secret sum: " << secret_sum << " in " << duration_cast<chrono::microseconds>(timer_part1 - timer_read) << endl;
    cout << "Aquired " << bananas << " bananas in " << duration_cast<chrono::microseconds>(timer_part2 - timer_part1) << endl;
    cout << "Reading the input file took " << duration_cast<chrono::microseconds>(timer_read - timer_start) << endl;
    return 0;
}

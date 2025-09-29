#include <iostream>
using namespace std;

// PRIMARY: accepts pointer to array of 5 T
template <class T>
void function(T (*arr)[5]) {
    // (empty or generic)
}

// FULL SPECIALIZATION for T = int
template <>
void function<int>(int (*arr)[5]) {
    cout << "Enter the values:\n";
    for (int i = 0; i < 4; ++i)
        for (int j = 0; j < 5; ++j)
            cin >> arr[i][j];

    cout << "Here are the values entered:\n";
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 5; ++j)
            cout << arr[i][j] << ' ';
        cout << '\n';
    }
}

int main() {
    using col = int[5];
    using row = col[4];

    row a{};             // int a[4][5]
    function(a);         // a decays to int (*)[5] → T deduces to int → specialization chosen
}

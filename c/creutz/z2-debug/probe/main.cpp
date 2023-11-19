#include <iostream>
#include <fstream>

void reader(std::ifstream& file, int& inc) {
    double rnum;
    while (file >> rnum) {
        std::cout << ++inc << " " << rnum << std::endl;
    }
}

int main() {
    std::ifstream inputFile("numbers.txt");

    if (!inputFile.is_open()) {
        std::cerr << "Error opening file." << std::endl;
        return 1;
    }

    int inc = 0;

    std::cout << "file randoms.txt opened" << std::endl;
    
    reader(inputFile, inc);

    std::cout << "file randoms.txt closed" << std::endl;

    inputFile.close();

    return 0;
}

// https://www.fiverr.com/ranazaviyar?source=inbox
// Zaviyar@ranazaviyar

// dantopa@Quaxolotl.local:probe $ g++ -Wall -p -g main.cpp -o main

// dantopa@Quaxolotl.local:probe $ ./main
// file randoms.txt opened
// 1 0.474664
// 2 0.791912
// 3 0.704909
// 4 0.29375
// file randoms.txt closed

// dantopa@Quaxolotl.local:probe $ date
// Sat Nov 18 21:11:17 MST 2023

// dantopa@Quaxolotl.local:probe $ pwd
// /Volumes/T7-Touch/repos/github/jop/c/creutz/z2-debug/probe

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

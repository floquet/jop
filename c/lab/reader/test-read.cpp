#include<iostream>        
#include<fstream>
using namespace std;
int main(){
    double random;
    int inc;
    inc = 1;
    ifstream FileName;               
    FileName.open( "/Volumes/T7-Touch/repos/github/f/projects/lattice/z2/randoms/list_randoms.txt", ios::in );    
    // FileName >> random;
    // printf ( "%d. %lf\n", inc++, random );
    // FileName >> random;
    // printf ( "%d. %lf\n", inc++, random );
    // FileName >> random;
    // printf ( "%d. %lf\n", inc++, random );   
    while ( FileName.good() && !FileName.eof() )
    {
        // Read the file
        FileName >> random;
        printf ( "%d. %lf\n", inc++, random );
    }

    FileName.close( );
    return 0;
}

// https://stackoverflow.com/questions/28710052/read-line-in-c-till-eof

// dantopa@Quaxolotl.local:reader $ date
// Thu Nov  2 19:12:27 MDT 2023

// g++ -Wall -Wextra -pedantic -o test-read test-read.cpp 

// ./test-read 
// 1. 0.474664
// 2. 0.791912

// 999999. 0.080451
// 1000000. 0.258497

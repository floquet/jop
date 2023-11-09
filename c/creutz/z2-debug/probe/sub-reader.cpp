#include<iostream>        
#include<fstream>
using namespace std;

// void reader(ifstream& file){
//    while ( file.good() && !file.eof() )
// void reader(FILE **fp, int inc){
void reader(istream & FileName, int inc){
    //while (( read = getline( &key, &len, fp )) != 1 )
    //{
        // Read the file
        //fp >> random;
        FileName >> random
        printf ( "%d. %lf\n", inc++, random );
    //}
    return;
}

int main(){
    double random;
    int inc;
    inc = 1;
    ifstream FileName; 
    // FILE *fp;
    // FileName = fopen( "/Volumes/T7-Touch/repos/github/f/projects/lattice/z2/randoms/list_randoms.txt", "r" )
    // fp = fopen( "/Volumes/T7-Touch/repos/github/f/projects/lattice/z2/randoms/list_randoms.txt", "r" )             
    FileName.open( "/Volumes/T7-Touch/repos/github/f/projects/lattice/z2/randoms/list_randoms.txt", ios::in );    
        // reader( FileName )
    // reader ( &fp, inc );
    // reader ( fp, inc );
    reader ( FileName, inc );

    // FileName >> random;
    // printf ( "%d. %lf\n", inc++, random );
    // FileName >> random;
    // printf ( "%d. %lf\n", inc++, random );
    // FileName >> random;
    // printf ( "%d. %lf\n", inc++, random );   

    FileName.close( );
    return 0;
}

// https://stackoverflow.com/questions/28710052/read-line-in-c-till-eof

// dantopa@Quaxolotl.local:reader $ date
// Wed Nov  1 20:51:20 MDT 2023

// dantopa@Quaxolotl.local:reader $ g++ -Wall test-read.cpp 

// dantopa@Quaxolotl.local:reader $ ./a.out 
// 1. 0.474664
// 2. 0.791912

// 999999. 0.080451
// 1000000. 0.258497

// https://solarianprogrammer.com/2014/08/28/cpp-14-lambda-tutorial/

#include <iostream>  // cout, endl
#include <cstdlib>   // EXIT_SUCCESS, EXIT_FAILURE
#include <complex>   // complex number

int main (  int argc, const char * argv[ ] )
{
    char a = 'a';
    char b = 'b';

        // Store a generalized lambda that squares a number in a variable
        auto func = [](auto input) { return input * input; };

        std::cout << "Testing a genralized lambda function which squares a number" << std::endl << std::endl;

        // Usage examples:
        // square of an int
        std::cout << "func ( 10 )     = " << func ( 10 ) << std::endl;
        std::cout << "expected answer = 100" << std::endl << std::endl;

        // square of a double
        std::cout << "func ( 2.345 )  = " << func ( 2.345 ) << std::endl;
        std::cout << "expected answer = 5.499025" << std::endl << std::endl;

        // square of a complex number
        std::cout << "func ( std::complex<double> ( 3, -2 ) ) = " << func ( std::complex<double> ( 3, -2 ) ) << std::endl;
        std::cout << "func ( std::complex<double> ( x, y ) )  = ( x^2 - y^2, 2xy ) = ( 5, -12 )" << std::endl << std::endl;

        // square of a character
        std::cout << "func ( char a ) = " << func ( a ) << std::endl;
        std::cout << "expected answer = 97 * 97 = 9409" << std::endl << std::endl;
        std::cout << "func ( char b ) = " << func ( b ) << std::endl;
        std::cout << "expected answer = 98 * 98 = 9604" << std::endl << std::endl;

    return EXIT_SUCCESS;
}

// dan-topas-pro-2:c++14 rditldmt$ date
// Tue Jan 12 18:59:30 CST 2016
// dan-topas-pro-2:c++14 rditldmt$ pwd
// /Users/rditldmt/Box Sync/c++/c++14
// dan-topas-pro-2:c++14 rditldmt$ clang++ -std=c++1y -Wall -g -pedantic -fcheck=bounds -Wconversion generalized\ lambda.cpp
// clang: warning: argument unused during compilation: '-fcheck=bounds'
// dan-topas-pro-2:c++14 rditldmt$ ./a.out
// func ( 10 )     = 100
// expected answer = 100
//
// func ( 2.345 )  = 5.49903
// expected answer = 5.499025
//
// func ( std::complex<double> ( 3, -2 ) ) = (5,-12)
// func ( std::complex<double> ( x, y ) )  = ( x^2 - y^2, 2xy ) = ( 5, -12 )
//
// func ( char a ) = 9409
// expected answer = 97 * 97 = 9409
//
// func ( char b ) = 9604
// expected answer = 98 * 98 = 9604
//
// dan-topas-pro-2:c++14 rditldmt$ g++ -pedantic -Wall -Wconversion -std=c++1y generalized\ lambda.cpp
// dan-topas-pro-2:c++14 rditldmt$ ./a.out
// func ( 10 )     = 100
// expected answer = 100
//
// func ( 2.345 )  = 5.49903
// expected answer = 5.499025
//
// func ( std::complex<double> ( 3, -2 ) ) = (5,-12)
// func ( std::complex<double> ( x, y ) )  = ( x^2 - y^2, 2xy ) = ( 5, -12 )
//
// func ( char a ) = 9409
// expected answer = 97 * 97 = 9409
//
// func ( char b ) = 9604
// expected answer = 98 * 98 = 9604

// rditldmt@ITLDMT-MD-O2034:c++14 $ date
// Mon Nov 14 16:02:31 CST 2016
// rditldmt@ITLDMT-MD-O2034:c++14 $ pwd
// /Users/rditldmt/hpc/c/c++14
// rditldmt@ITLDMT-MD-O2034:c++14 $ g++ -std=c++1y -Wall -g -pedantic generalized\ lambda.cpp -o generalized\ lambda
// rditldmt@ITLDMT-MD-O2034:c++14 $ ./generalized\ lambda
// Testing a genralized lambda function which squares a number
//
// func ( 10 )     = 100
// expected answer = 100
//
// func ( 2.345 )  = 5.49903
// expected answer = 5.499025
//
// func ( std::complex<double> ( 3, -2 ) ) = (5,-12)
// func ( std::complex<double> ( x, y ) )  = ( x^2 - y^2, 2xy ) = ( 5, -12 )
//
// func ( char a ) = 9409
// expected answer = 97 * 97 = 9409
//
// func ( char b ) = 9604
// expected answer = 98 * 98 = 9604
// 

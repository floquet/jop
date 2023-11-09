#include <iostream>
#include <fstream>
using namespace std;

int main()
{
  ofstream out("test.txt"); // output, normal file

  if(!out) {
    cout << "Cannot open test.txt file.\n";
    return 1;
  }

  out << "R " << 9.9 << endl;
  out << "T " << 9.9 << endl;
  out << "M " << 4.8 << endl;

  out.close();


  ifstream in("test.txt"); // input

  if(!in) {
    cout << "Cannot open test.txt file.\n";
    return 1;
  }

  char item[20];
  float cost;

  in >> item >>  cost;
  cout << item << " " << cost << "\n";
  in >> item >> cost;
  cout << item << " " << cost << "\n";
  in >> item >> cost;
  cout << item << " " << cost << "\n";

  in.close();
  return 0;
}

// http://www.java2s.com/Tutorial/Cpp/0240__File-Stream/Readstringandfloatvaluefromafile.htm
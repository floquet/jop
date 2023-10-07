#include <stdio.h>
#include <stdlib.h>

struct threeNum
{
   int n1, n2, n3;
};

int main()
{
   int n;
   struct threeNum num;
   FILE *fptr;

   if ((fptr = fopen("output.bin","wb")) == NULL){
       printf("Error! opening file");

       // Program exits if the file pointer returns NULL.
       exit(1);
   }

   for(n = 1; n < 5; ++n)
   {
      num.n1 = n;
      num.n2 = 5*n;
      num.n3 = 5*n + 1;
      printf("%d\t%d\t%d\n", num.n1, num.n2, num.n3 );
      fwrite(&num, sizeof(struct threeNum), 1, fptr); 
   }
   fclose(fptr); 
  
   return 0;
}

/* https://www.programiz.com/c-programming/c-file-input-output */
/* Example 3 */

// dantopa@Quaxolotl.local:binary $ date
// Fri Oct  6 11:10:07 MDT 2023

// dantopa@Quaxolotl.local:binary $ pwd
// /Volumes/T7-Touch/repos/github/jop/c/lab/binary

// dantopa@Quaxolotl.local:binary $ gcc bin-write.c 

// dantopa@Quaxolotl.local:binary $ ./a.out 
// 1  5  6
// 2  10 11
// 3  15 16
// 4  20 21

// /Users/dantopa/Mathematica_files/nb/projects/paris/lattice/z2/z2-01.nb
// BinaryReadList[dirData <> "output.bin", "Integer32"]
// {1, 5, 6, 2, 10, 11, 3, 15, 16, 4, 20, 21}

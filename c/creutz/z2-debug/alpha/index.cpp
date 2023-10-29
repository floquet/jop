#include <math.h>
#include <stdio.h>

using namespace std;

/* the lattice is of dimensions SIZE**4  */
#define SIZE 3
int lnk[SIZE][SIZE][SIZE][SIZE][4]; /* last index gives lnk direction */

/* utility functions */
void moveup(int x[],int d) {
  x[d]+=1;
  if (x[d]>=SIZE) x[d]-=SIZE; 
  return;
}
void movedown(int x[],int d) {
  x[d]-=1;
  if (x[d]<0) x[d]+=SIZE;
  return;
}
void coldstart(){  /* set all lnks to unity */
  int x[4],d;
  for (x[0]=0;x[0]<SIZE;x[0]++)
    for (x[1]=0;x[1]<SIZE;x[1]++)
      for (x[2]=0;x[2]<SIZE;x[2]++)
        for (x[3]=0;x[3]<SIZE;x[3]++)
          for (d=0;d<4;d++){
            printf( "%d %d %d %d %d \n", x[0], x[1], x[2], x[3], d );
	          lnk[x[0]][x[1]][x[2]][x[3]][d]=1;
            printf( "%d \n", lnk[x[0]][x[1]][x[2]][x[3]][d] );
          }
  return;
}


/******************************/
int main(){
    coldstart();
    exit(0);
}
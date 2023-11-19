/* Z_2 lattice gauge simulation */
/* Michael Creutz <creutz@bnl.gov>     */
/* http://thy.phy.bnl.gov/~creutz/z2.c */
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
//#include <iostream>
#include <fstream>

using namespace std;

/* the lattice is of dimensions SIZE**4  */
#define SIZE 6
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
          for (d=0;d<4;d++)
	    lnk[x[0]][x[1]][x[2]][x[3]][d]=1;
  return;
}
/* for a random start: call coldstart() and then update once at beta=0 */

/* do a Monte Carlo sweep; return energy */
// double update(double beta, FILE** fr){
// https://stackoverflow.com/questions/2581493/c-newbie-passing-an-fstream-to-a-function-to-read-data
double update(double beta, int& inc, ifstream &file){
  int x[4],d,dperp,staple,staplesum;    
  double bplus,bminus,action=0.0;
  double rnum=0.0; 
  for (x[0]=0; x[0]<SIZE; x[0]++)
    for (x[1]=0; x[1]<SIZE; x[1]++)
      for (x[2]=0; x[2]<SIZE; x[2]++)
        for (x[3]=0; x[3]<SIZE; x[3]++)
          for (d=0; d<4; d++) {
            staplesum=0;
            for (dperp=0;dperp<4;dperp++){
              if (dperp!=d){
                /*  move around thusly:
                    dperp        6--5
                    ^            |  |
                    |            1--4
                    |            |  |
                    -----> d     2--3  */
                /* plaquette 1234 */
                movedown(x,dperp);
                staple=lnk[x[0]][x[1]][x[2]][x[3]][dperp]
                      *lnk[x[0]][x[1]][x[2]][x[3]][d];
                moveup(x,d);
                staple*=lnk[x[0]][x[1]][x[2]][x[3]][dperp];  
                moveup(x,dperp);
                staplesum+=staple;
                /* plaquette 1456 */
                staple=lnk[x[0]][x[1]][x[2]][x[3]][dperp];
                moveup(x,dperp);
                movedown(x,d);
                staple*=lnk[x[0]][x[1]][x[2]][x[3]][d];
                movedown(x,dperp);
                staple*=lnk[x[0]][x[1]][x[2]][x[3]][dperp];
                staplesum+=staple;
              }
	          }
             /* calculate the Boltzmann weight */
            bplus=exp(beta*staplesum);
            bminus=1/bplus;
            bplus=bplus/(bplus+bminus);
            /* the heatbath algorithm */
            // rnum = drand48();
            inc++;
            file >> rnum;
            // printf( "%d \t %g \t %g\n", staplesum, rnum, bplus );
            // printf( "rnum = %3f, bplus = %3f \n", rnum, bplus );
            // fprintf(fr, "%g\t%g\n", rnum, bplus);
            if ( rnum < bplus ){
              // printf( ": rnum < bplus");
              lnk[x[0]][x[1]][x[2]][x[3]][d]=1;
              action+=staplesum;
              printf ( "%d. %lf action = %lf staplesum = %d bplus = %lf \n", inc, rnum, action, staplesum, bplus );
            }
            else{ 
              lnk[x[0]][x[1]][x[2]][x[3]][d]=-1;
              action-=staplesum;
              // printf( "F action = action - staplesum = %g - %d = %g \n", action, staplesum, action - staplesum );
              printf ( "%d. %lf action = %lf staplesum = %d bplus = %lf \n", inc , rnum, action, staplesum, bplus );
            }
          }
  action /= (SIZE*SIZE*SIZE*SIZE*4*6);
  return 1.-action;
}

/* https://www.programiz.com/c-programming/c-file-input-output */
struct doublet
{   
    double beta, action;
};
    
/******************************/
int main(){
    double dbeta;
    struct doublet pair;
    // int sz = sizeof(struct doublet), inc;
    int inc;
    srand48(1234L);  /* initialize random number generator */
    /* do your experiment here; this example is a thermal cycle */
    dbeta=0.0006;
    dbeta=0.015625;
    dbeta=0.125;
    inc=0;
    ifstream FileName;               
    FileName.open( "/Volumes/T7-Touch/repos/github/f/projects/lattice/z2/randoms/list_randoms.txt", ios::in );    
    /* heat it up */
    for (pair.beta=1.2; pair.beta>0.0; pair.beta-=dbeta){
        pair.action=update(pair.beta, inc, FileName);
    }

    printf("\n heating cycle completed - now cooling\n ");
    /* cool it down */
    for (pair.beta=0; pair.beta<1.2; pair.beta+=dbeta){
        pair.action=update(pair.beta, inc, FileName);
    }
    FileName.close( );
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        printf("Current working dir: %s\n", cwd);
        printf("size  = %d\n", SIZE);
        printf("dbeta = %g\n", dbeta);
    } else {
        perror("getcwd() error");
        return 1;
   }

    exit(0);
}

// dantopa@Quaxolotl.local:probe $ g++ -Wall -p -g -o alpha-probe alpha-probe.cpp 

// dantopa@Quaxolotl.local:probe $ ./alpha-probe > text-out.txt

// dantopa@Quaxolotl.local:probe $ date
// Sat Nov 18 21:42:28 MST 2023

// dantopa@Quaxolotl.local:probe $ pwd
// /Volumes/T7-Touch/repos/github/jop/c/creutz/z2-debug/probe

// Current working dir: /Volumes/T7-Touch/repos/github/jop/c/creutz/z2-debug/probe
// size  = 3
// dbeta = 0.125

/* 165. M. Creutz, "Simulating quarks," Computers in Science & Engineering, March/April 2004, p. 80 (IEEE CS and AIP, 2004). */

/* “Experiments with a Gauge Invariant Ising System,” Physical Rev. Letters, vol. 42, no. 21, 1979, pp. 1390–1393.
*/

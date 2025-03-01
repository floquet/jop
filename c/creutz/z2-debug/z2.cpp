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
          for (d=0;d<4;d++)
	    lnk[x[0]][x[1]][x[2]][x[3]][d]=1;
  return;
}
/* for a random start: call coldstart() and then update once at beta=0 */

/* do a Monte Carlo sweep; return energy */
double update(double beta, FILE** fr){
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
                // printf( "%d %d %d %d %d %d \n", x[0], x[1], x[2], x[3], d, dperp );
                // printf( "%d = %d * %d \n", staple, lnk[x[0]][x[1]][x[2]][x[3]][dperp], lnk[x[0]][x[1]][x[2]][x[3]][d] );
                moveup(x,d);
                staple*=lnk[x[0]][x[1]][x[2]][x[3]][dperp];  
                moveup(x,dperp);
                printf("%d A staplesum = staplesum + staple = %d + %d = %d\n", dperp, staplesum, staple, staple + staplesum );
                staplesum+=staple;
                /* plaquette 1456 */
                staple=lnk[x[0]][x[1]][x[2]][x[3]][dperp];
                moveup(x,dperp);
                movedown(x,d);
                staple*=lnk[x[0]][x[1]][x[2]][x[3]][d];
                movedown(x,dperp);
                staple*=lnk[x[0]][x[1]][x[2]][x[3]][dperp];
                printf("%d B staplesum = staplesum + staple = %d + %d = %d\n", dperp, staplesum, staple, staple + staplesum );
                staplesum+=staple;
              }
	          }
            printf("staplesum = %d\n", staplesum );
            /* calculate the Boltzmann weight */
            bplus=exp(beta*staplesum);
            bminus=1/bplus;
            bplus=bplus/(bplus+bminus);
            /* the heatbath algorithm */
            rnum = drand48();
            // printf( "%d \t %g \t %g\n", staplesum, rnum, bplus );
            // printf( "rnum = %3f, bplus = %3f \n", rnum, bplus );
            // fprintf(fr, "%g\t%g\n", rnum, bplus);
            if ( rnum < bplus ){
              // printf( ": rnum < bplus");
              lnk[x[0]][x[1]][x[2]][x[3]][d]=1;
              printf( "T action = action + staplesum = %g + %d = %g \n", action, staplesum, action + staplesum );
              action+=staplesum;
            }
            else{ 
              lnk[x[0]][x[1]][x[2]][x[3]][d]=-1;
              action-=staplesum;
              printf( "F action = action - staplesum = %g - %d = %g \n", action, staplesum, action - staplesum );
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
    int sz = sizeof(struct doublet);
    FILE *fptr;
    FILE *fr;
    srand48(1234L);  /* initialize random number generator */
    /* do your experiment here; this example is a thermal cycle */
    dbeta=0.0006;
    dbeta=0.015625;
    dbeta=0.125;
    coldstart();
    /* heat it up */
    fr = fopen("randoms.txt", "w");
    fptr = fopen("heat.txt", "w");
    for (pair.beta=1.2; pair.beta>0.0; pair.beta-=dbeta){
        pair.action=update(pair.beta, &fr);
        /* printf("%g\t%g\n",beta,action); */
        // fprintf(fptr, "%g\t%g\n", pair.beta, pair.action);
        // fwrite(&pair, sz, 1, fptr);
    }
    fclose(fptr); 

    printf("\n heating cycle completed - now cooling\n ");
    /* cool it down */
    // fptr = fopen("cool.txt", "w");
    // std::ofstream myfile;
    // myfile.open ("cool.txt");
    FILE *fp;
    fp = fopen("cool.txt", "w");
    for (pair.beta=0; pair.beta<1.2; pair.beta+=dbeta){
        pair.action=update(pair.beta, &fr);
        // printf("%g\t%g\n",pair.beta,pair.action); 
        //myfile << pair;
        // fprintf(fp, "%g\t%g\n", pair.beta, pair.action);
        // fputc(pair, fptr);
        // fptr << pair
        // fwrite(&pair, sz, 1, fptr);
    }
    fclose( fp );
    fclose( fr );
    // myfile.close();
    // fclose(fptr); 
    // printf("\n\n");
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

// dantopa@Quaxolotl.local:z2-debug $ date
// Wed Oct 25 21:02:47 MDT 2023

// dantopa@Quaxolotl.local:z2-debug $ gcc z2.cpp 

// dantopa@Quaxolotl.local:z2-debug $ time ./a.out

//  heating cycle completed - now cooling
//  Current working dir: /Volumes/T7-Touch/repos/github/jop/c/creutz/z2-debug
// size  = 6
// dbeta = 0.0006

// real  0m3.029s
// user  0m2.923s
// sys 0m0.034s



/* 165. M. Creutz, "Simulating quarks," Computers in Science & Engineering, March/April 2004, p. 80 (IEEE CS and AIP, 2004). */

/* “Experiments with a Gauge Invariant Ising System,” Physical Rev. Letters, vol. 42, no. 21, 1979, pp. 1390–1393.
*/

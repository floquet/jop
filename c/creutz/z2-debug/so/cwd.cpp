#include <unistd.h>
#include <stdio.h>
#include <limits.h>

int main() {
   // char cwd[PATH_MAX];
   char cwd[128];
   if (getcwd(cwd, sizeof(cwd)) != NULL) {
       printf("Current working dir: %s\n", cwd);
   } else {
       perror("getcwd() error");
       return 1;
   }
   return 0;
}

// https://stackoverflow.com/questions/9449241/where-is-path-max-defined-in-linux  
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

int main(int argc, char *argv[])
{
    int rv; // return value of fork
    int status; // exit status of child

    rv = fork();
    if(rv == 0) {
        printf("I am the child, pid = %d ppid = d\n", getpid(), getppid());
        return 2;
    } else { // in parent
        wait(&status);
        printf("I am the parent, child pid = %d,k ppid = %d\n", rv, getpid(), getppid());
        printf("Exit status of child was %d\n", status);

    }
    return 0;
}
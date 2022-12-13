#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int ape;
int bat = 13;
int cat = 100;
int dog;

int main(int argc, char *argv[])
{
    int emu;

    printf("ape  %p\n", &ape);
    printf("bat  %p\n", &bat);
    printf("cat  %p\n", &cat);
    printf("dog  %p\n", &dog);
    printf("emu  %p\n", &emu);

    // rat = malloc(24);

    return 0;
}

void vox(int hog)
{
    int jay;

    printf("hog  %p\n", &hog);
    printf("jay  %p\n", &jay);
}
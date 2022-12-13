/*
* serialization: jobA must be done before jobB
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <pthread.h>
#include <semaphore.h>

#define NTHREADS    2

sem_t s;          /* a semaphore */

void *threadA(void *nothing);
void *threadB(void *nothing);

int main(int argc, char *argv[])
{

    pthread_t th[NTHREADS];

    sem_init(&s, 0, 0);

    pthread_create(&th[0], 0, (void *) threadA, 0);
    pthread_create(&th[1], 0, (void *) threadB, 0);

    pthread_join(th[0], 0);
    pthread_join(th[1], 0);

    return 0;

}

void *threadA(void *nothing)
{
    sleep(1 + random() % 5);

    printf("Hello, ");
    sem_post(&s);
    pthread_exit(0);

}

void *threadB(void *nothing)
{
    sleep(1 + random() % 5);

    sem_wait(&s);
    printf("world.\n");
    pthread_exit(0);

}

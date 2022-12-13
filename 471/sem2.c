/*
* mutual exclusion: critical section, one process is allowed at a time
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define NTHREADS    2

sem_t s;          /* a semaphore */

int shared_var = 0;

void *threadC(void *nothing);

int main(int argc, char *argv[])
{

    pthread_t th[NTHREADS];

    srandom(getpid());

    sem_init(&s, 0, 1);

    for( int i = 0; i < NTHREADS; i++)
        pthread_create(&th[i], 0, (void *) threadC, 0);


    for( int i = 0; i < NTHREADS; i++)
            pthread_join(th[i], 0);

    printf("%d\n", shared_var);

    return 0;

}

void *threadC(void *nothing)
{

    int local_copy;

    sem_wait(&s);
    usleep(random() % 100000);      // work to do before starting main job

// beginning of critical section
    local_copy = shared_var;
    usleep(random() % 100000);      // work required to do the main job
    local_copy += 1;
    shared_var = local_copy;
//end of critical section

    sem_post(&s);

    pthread_exit(0);

}

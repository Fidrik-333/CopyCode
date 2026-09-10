#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <signal.h>

int fd[2];

volatile sig_atomic_t signal_received = 0;

void handle_sigusr1(int sig)
{
    signal_received = 1;
}

int main()
{
    pid_t pid;

    char write_msg[] = "Hello from parent";
    char read_msg[100];

    // Create pipe
    if (pipe(fd) == -1)
    {
        perror("pipe");
        exit(1);
    }

    // Register signal handler for SIGUSR1
    signal(SIGUSR1, handle_sigusr1);

    pid = fork();

    if (pid < 0)
    {
        perror("fork");
        exit(1);
    }

    else if (pid > 0)   // Parent
    {
        close(fd[0]);   // Close reading end

        // Write message
        printf("Parent: Writing to pipe: %s\n", write_msg);
        write(fd[1], write_msg, strlen(write_msg) + 1);
        close(fd[1]);  // Done writing

        // Wait for signal from child
        printf("Parent: Waiting for signal from child...\n");

        while (!signal_received)
        {
            pause();
        }

        printf("Parent: Received SIGUSR1 from child!\n");

        wait(NULL);    // Wait for child to finish
    }

    else    // Child
    {
        close(fd[1]);   // Close writing end

        // Read message
        read(fd[0], read_msg, sizeof(read_msg));
        printf("Child: Read from pipe: %s\n", read_msg);

        close(fd[0]);

        // Send signal to parent
        kill(getppid(), SIGUSR1);
        printf("Child: Sent SIGUSR1 to parent.\n");

        exit(0);
    }

    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#define BUFFER_LEN 1024

int main()
{
    char input[BUFFER_LEN];
    char *argv[100];
    int argc;

    while (1)
    {
        printf("myshell> ");

        // Read input
        if (fgets(input, BUFFER_LEN, stdin) == NULL)
            break;

        // Remove newline
        size_t length = strlen(input);
        if (length > 0 && input[length - 1] == '\n')
            input[length - 1] = '\0';

        // Exit shell
        if (strcmp(input, "exit") == 0)
            break;

        // Parse input into arguments
        argc = 0;

        char *token = strtok(input, " ");

        while (token != NULL && argc < 99)
        {
            argv[argc++] = token;
            token = strtok(NULL, " ");
        }

        // NULL terminate argv
        argv[argc] = NULL;

        // Empty input
        if (argc == 0)
            continue;

        // Create child process
        pid_t pid = fork();

        if (pid == 0)
        {
            // Child process: execute command
            if (execvp(argv[0], argv) == -1)
            {
                perror("Command execution failed");
                exit(EXIT_FAILURE);
            }
        }
        else if (pid > 0)
        {
            // Parent process: wait for child
            wait(NULL);
        }
        else
        {
            perror("fork failed");
        }
    }

    printf("Exiting shell.\n");

    return 0;
}

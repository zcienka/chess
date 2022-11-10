#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <time.h>
#include<string>

void childend(int signo)
{
    wait(NULL);
}

// int main(int argc, char *argv[])
int main()
{
    socklen_t slt;
    int sfd, cfd, on = 1;
    struct sockaddr_in saddr, caddr;

    signal(SIGCHLD, childend); // dodanie tego zeby nie powstawaly procesy zombie
    saddr.sin_family = AF_INET;
    saddr.sin_addr.s_addr = INADDR_ANY;
    saddr.sin_port = htons(5050);

    sfd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, (char *)&on, sizeof(on));
    bind(sfd, (struct sockaddr *)&saddr, sizeof(saddr));
    listen(sfd, 10);
    int clientRequest;

    while (1)
    {
        slt = sizeof(caddr);
        cfd = accept(sfd, (struct sockaddr *)&caddr, &slt);
        // printf("%d", cfd);
        // printf("%s", caddr.sin_port);
        // printf("\n\n");
        std::cout << "New connection from: "<< inet_ntoa((struct in_addr)caddr.sin_addr) << std::endl;

        if (fork() == 0)
        {
            close(sfd);
            char query[129];
            memset(query, 0, strlen(query));

            while (1)
            {
                memset(query, 0, strlen(query));
                clientRequest = read(cfd, query, 128);

               if (clientRequest != -1)
                {
                    printf("%s", query);
                    write(cfd, query, strlen(query));
                }
            }

            close(cfd);
            exit(0);
        }
        else
        {
            close(cfd);
        }
    }
    close(sfd);
    return EXIT_SUCCESS;
}
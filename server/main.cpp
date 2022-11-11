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
#include <string>
#include <random>
#include <algorithm>

void childend(int signo)
{
    wait(NULL);
}

struct Game
{
    std::vector<int> players;
    int id;
};

int getNewId(std::vector<Game> games)
{
    return games.size();
};

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
    int randomColor;
    char clientId[10];
    std::vector<Game> games;
    int currentUserId;

    while (1)
    {
        slt = sizeof(caddr);
        cfd = accept(sfd, (struct sockaddr *)&caddr, &slt);
        std::cout << "cfd:" << cfd << std::endl<<std::endl;

        std::cout << "New connection from: " << inet_ntoa((struct in_addr)caddr.sin_addr) << std::endl;
        std::cout << "cfd" << cfd << std::endl;

        char query[129];

        if (fork() == 0)
        {
            close(sfd);
            char query[128];
            memset(query, 0, strlen(query));

            while (1)
            {
                memset(query, 0, 128);
                clientRequest = read(cfd, query, 128);
                bool addedToNewGame = false;
                Game game = Game();

                std::cout << std::endl;

                if (clientRequest != -1 && strcmp(query, "First connection") == 0)
                {
                    for (int i = 0; i < games.size(); i++)
                    {
                        if (games[i].players.size() == 1)
                        {
                            addedToNewGame = true;
                            games[i].players.emplace_back(cfd);
                            game = games[i];
                            break;
                        }
                    }

                    if (!addedToNewGame)
                    {
                        game.players.emplace_back(cfd);
                        game.id = getNewId(games);
                        games.emplace_back(game);
                        
                        std::cout << "game.id " << game.id << std::endl;

                        for (int player : game.players)
                        {
                            std::cout << "player: " << player << std::endl;
                        }
                        std::cout << std::endl;
                        std::cout << "game.id " << game.id << std::endl;
                    }
                    std::cout << "addedToNewGame" << addedToNewGame << std::endl;
                    char gameIdString[3];

                    sprintf(gameIdString, "%d", game.id);

                    for (int player_cfd : game.players)
                    {
                        write(cfd, gameIdString, strlen(gameIdString)); 
                    }
                }
                else if (clientRequest != -1)
                {
                    std::cout << "query" << query <<std::endl;
                    int currentGameId = 0;
                    for (int i = 0; i < games.size(); i++)
                    {
                        if  (std::find(games[i].players.begin(), games[i].players.end(), cfd) != games[i].players.end())
                        {
                            currentGameId = i;
                            std::cout << "currentGameId: " << currentGameId << std::endl;
                        }
                    }

                    for (int playerCfd : games[currentGameId].players)
                    {
                        write(playerCfd, query, strlen(query));
                    }
                }
            }

            close(sfd);
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
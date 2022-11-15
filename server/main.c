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
#include <threads.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdbool.h>

char *ASSIGN_COLOR = "ASSIGN_COLOR";

struct cln
{
	int cfd;
	struct sockaddr_in caddr;
};

struct User
{
	// int gameId;
	int cfd;
	int color;
	bool isConnected;
};

typedef struct
{
	int id;
	struct User users[2];
	int userIdturn;
} Game;

const int MAX_USERS = 6;
const int MAX_GAMES = MAX_USERS / 2;
int users_num = 0;
Game *games;

void *test(int client_socket)
{
	int currentGameId, currentUserId;
	struct User currentUser;

	for (int i = 0; i < MAX_GAMES; i++)
	{
		for (int j = 0; j < 2; j++)
		{
			if (games[i].users[j].cfd == client_socket)
			{
				currentGameId = i;
				currentUser = games[i].users[j];
				currentUserId = j;
				break;
			}
		}
	}

	char query[128];
	memset(query, 0, strlen(query));

	int userRequest = recv(client_socket, query, 128, 0);

	// if (userRequest != 0)
	// {

	if (!currentUser.isConnected && strcmp(query, ASSIGN_COLOR) == 0)
	{
		char colorStr[2];
		int color = games[currentGameId].users[currentUserId].color;

		memset(colorStr, 0, strlen(colorStr));
		sprintf(colorStr, "%d", color);

		send(client_socket, colorStr, strlen(colorStr), 0);
		games[currentGameId].users[currentUserId].isConnected = true;
	}
	else if ( games[currentGameId].users[0].isConnected && games[currentGameId].users[1].isConnected)
	{
		// recv(client_socket, query, 128, 0);
		printf("query %s\n\n", query);
		int turn = games[currentGameId].userIdturn;

		send(games[currentGameId].users[turn].cfd, query, strlen(query), 0);

		if (turn == 0)
		{
			games[currentGameId].userIdturn = 1;
		}
		else if (turn == 1)
		{
			games[currentGameId].userIdturn = 0;
		}
		// }
	}
}

int main(int argc, char *argv[])
{
	games = (Game *)malloc(sizeof(Game) * MAX_GAMES);

	pthread_t tid;
	socklen_t slt;
	int sfd, on = 1;
	struct sockaddr_in saddr;

	saddr.sin_family = AF_INET;
	saddr.sin_addr.s_addr = INADDR_ANY;
	saddr.sin_port = htons(5050);

	sfd = socket(AF_INET, SOCK_STREAM, 0);
	setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, (char *)&on, sizeof(on));
	bind(sfd, (struct sockaddr *)&saddr, sizeof(saddr));
	listen(sfd, MAX_GAMES);

	fd_set mask, rmask;

	FD_ZERO(&mask);
	FD_SET(sfd, &mask);

	srand(time(NULL));

	for (int i = 0; i < MAX_GAMES; i++)
	{
		Game game;
		int color1 = rand() % 2;
		// int color1 = 0;

		game.users[0].color = color1;
		game.users[1].color = (color1 + 1) % 2;

		game.users[0].isConnected = false;
		game.users[1].isConnected = false;

		if (game.users[0].color)
		{
			game.userIdturn = 0;
		}
		else
		{
			game.userIdturn = 1;
		}

		games[i] = game;
	}
	// for (int i = 0; i < 10; i++)
	// {
	// 	printf("color %d game.users[0].color: %d, game.users[1].color: %d\n\n", i, games[i].users[0].color, games[i].users[1].color);
	// }

	for (int i = 0; i < MAX_GAMES; i++)
	{
		printf("games[i].isConnected %d\n", games[i].users[0].isConnected);
	}

	for (;;)
	{
		rmask = mask;
		if (select(FD_SETSIZE, &rmask, NULL, NULL, NULL) < 0)
		{
			perror("select error");
		}

		for (int i = 0; i < FD_SETSIZE; i++)
		{
			if (FD_ISSET(i, &rmask))
			{
				if (i == sfd)
				{
					struct cln *c = malloc(sizeof(struct cln));
					slt = sizeof(c->caddr);
					c->cfd = accept(sfd, (struct sockaddr *)&c->caddr, &slt);
					int availableId = -1;

					for (int i = 0; i < MAX_GAMES; i++)
					{
						if (games[i].users[0].isConnected == true && games[i].users[1].isConnected == false)
						{
							availableId = i;
							// games[i].users[1].isConnected = true;
							printf("availableId: asdadsdas%d\n", availableId);
							printf("games[i].users[0].isConnected %d\n", games[i].users[0].isConnected);
							games[i].users[1].cfd = c->cfd;
							// games[i].users[1].isConnected = true;
							// games[i].users[1].gameId = i
							break;
						}
					}

					if (availableId == -1)
					{
						for (int i = 0; i < MAX_GAMES; i++)
						{
							if (games[i].users[0].isConnected == false && games[i].users[0].isConnected == false)
							{
								availableId = i;
								printf("availableId: %d\n", availableId);
								games[i].users[0].cfd = c->cfd;
								// games[i].users[0].isConnected = true;

								break;
							}
						}
					}

					if (availableId != -1)
					{
						FD_SET(c->cfd, &mask);
					}
				}
				else
				{
					test(i);
					FD_CLR(i, &mask);
				}
			}
		}


	}

	close(sfd);
	return EXIT_SUCCESS;
}

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

const char *ASSIGN_COLOR = "ASSIGN_COLOR";
const char *DISCONNECT_USER = "DISCONNECT_USER";
const char *OPPONENT_DISCONNECTED = "OPPONENT_DISCONNECTED";
const char *OPPONENT_CONNECTED = "OPPONENT_CONNECTED";
const char *IS_OPPONENT_CONNECTED = "IS_OPPONENT_CONNECTED";
const char *OPPONENT_CONNECTING = "OPPONENT_CONNECTING";

struct cln
{
	int cfd;
	struct sockaddr_in caddr;
};

struct User
{
	int gameId;
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

int users_num = 0;
// int turn = 0;
Game *games;

const int MAX_USERS = 6;
const int MAX_GAMES = MAX_USERS / 2;

void *cthread(void *arg)
{
	struct cln *c = (struct cln *)arg;

	int currentUserId;
	struct User currentUser;

	int availableId = -1;
	for (int i = 0; i < MAX_GAMES; i++)
	{
		if (games[i].users[0].isConnected == true && games[i].users[1].isConnected == false)
		{
			availableId = i;
			printf("availableId dsahdshjdsakjdsakj: %d\n", availableId);

			games[i].users[1].cfd = c->cfd;
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
				break;
			}
		}
	}
	// games[availableId].users[users_num % 2].cfd = c->cfd;

	char query[129];

	int userRequest = 0;

	userRequest = 0;

	while (1)
	{
		memset(query, 0, strlen(query));
		userRequest = recv(c->cfd, query, 128, 0);
		printf("query %s \n", query);

		if (userRequest != 0)
		{
			// printf("query %s \n\n", query);

			if (strcmp(query, ASSIGN_COLOR) == 0)
			{
				int color = games[availableId].users[users_num % 2].color;

				// if (color == 1)
				// {
				// 	turn = users_num % 2;
				// }

				char colorStr[2];
				memset(colorStr, 0, strlen(colorStr));
				sprintf(colorStr, "%d", color);
				// printf("games[0].users[(users_num ) 2].color: %d \n", games[currentGameId].users[users_num % 2].color);

				send(c->cfd, colorStr, strlen(colorStr), 0);
				games[availableId].users[users_num % 2].isConnected = true;
				users_num++;
			}
			else if (strcmp(query, "") != 0 && games[availableId].users[0].isConnected && games[availableId].users[1].isConnected)
			{
				int turn = games[availableId].userIdturn;
				printf("turn %d\n", turn);
				printf("availableId  %d\n", availableId);

				if (turn == 0)
				{
					games[availableId].userIdturn = 1;
				}
				else if (turn == 1)
				{
					games[availableId].userIdturn = 0;
				}
				turn = games[availableId].userIdturn;

				send(games[availableId].users[turn].cfd, query, strlen(query), 0);
			}
		}
	}

	close(c->cfd);
	free(c);
	return EXIT_SUCCESS;
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
	srand(time(NULL));

	for (int i = 0; i < MAX_GAMES; i++)
	{
		Game game;
		game.id = i;
		int color1 = rand() % 2;

		game.users[0].color = color1;
		game.users[1].color = (color1 + 1) % 2;

		if (color1 == 1)
		{
			game.userIdturn = 0;
		}
		else
		{
			game.userIdturn = 1;
		}

		game.users[0].isConnected = false;
		game.users[1].isConnected = false;

		games[i] = game;
	}

	for (;;)
	{
		struct cln *c = malloc(sizeof(struct cln));
		slt = sizeof(c->caddr);
		c->cfd = accept(sfd, (struct sockaddr *)&c->caddr, &slt);
		pthread_create(&tid, NULL, cthread, c);
		pthread_detach(tid);
	}

	close(sfd);
	return EXIT_SUCCESS;
}

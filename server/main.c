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
const char *REMATCH = "REMATCH";

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
	bool wantsRematch;
};

typedef struct
{
	int id;
	struct User users[2];
	int userIdturn;
} Game;

int users_num = 0;
Game *games;

const int MAX_USERS = 6;
const int MAX_GAMES = MAX_USERS / 2;

void generateNewGame(int gameId)
{
	Game game;
	game.id = gameId;
	int color = rand() % 2;

	game.users[0].color = color;
	game.users[1].color = (color + 1) % 2;

	if (color == 1)
	{
		game.userIdturn = 0;
	}
	else
	{
		game.userIdturn = 1;
	}

	game.users[0].isConnected = false;
	game.users[1].isConnected = false;

	game.users[0].wantsRematch = false;
	game.users[1].wantsRematch = false;

	games[gameId] = game;
}


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
			currentUserId = 1;
			currentUser = games[i].users[1];
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
				currentUserId = 0;
				currentUser = games[i].users[0];
				games[i].users[0].cfd = c->cfd;
				break;
			}
		}
	}
	char request[128], query[128];
	int userRequest = 0;
	memset(request, 0, strlen(request));
	memset(query, 0, strlen(query));
	while (1)
	{

		memset(query, 0, strlen(query));

		// userRequest = recv(c->cfd, request, 128, 0);
		// userRequest = recv(c->cfd, request, 128, 0);
		if ((userRequest = recv(c->cfd, query, 128, 0)) == 0)
		{
			break;
		}
		// printf("request %s \n", request);

		// for (int i = 0; i < 128; i++)
		// {
		// 	char newline = '\n';
		// 	printf("xd i %c\n", request[i]);
		// 	if (request[i] == newline)
		// 	{
		// 		break;
		// 	}
		// 	query[i] = request[i];
		// 	if (strcmp(query, ASSIGN_COLOR) == 0)
		// 	{
		// 		break;
		// 	}
		// }
		// printf("query %s \n", query);

		if (userRequest != 0)
		{

			if (strcmp(query, ASSIGN_COLOR) == 0)
			{

				int color = games[availableId].users[users_num % 2].color;

				char colorStr[2];
				memset(colorStr, 0, strlen(colorStr));
				sprintf(colorStr, "%d", color);

				send(c->cfd, colorStr, strlen(colorStr), 0);
				games[availableId].users[users_num % 2].isConnected = true;
				users_num++;
			}
			else if (strcmp(query, IS_OPPONENT_CONNECTED) == 0)
			{
				int opponentId = (currentUserId + 1) % 2;

				struct User opponent = games[availableId].users[opponentId];

				char isOpponentConnectedStr[2];
				bool isOpponentConnected = opponent.isConnected;

				memset(isOpponentConnectedStr, 0, strlen(isOpponentConnectedStr));
				sprintf(isOpponentConnectedStr, "%d", isOpponentConnected);

				if (isOpponentConnected)
				{
					send(c->cfd, OPPONENT_CONNECTED, strlen(OPPONENT_CONNECTED), 0);
					send(opponent.cfd, OPPONENT_CONNECTED, strlen(OPPONENT_CONNECTED), 0);
				}
				else
				{
					send(c->cfd, OPPONENT_CONNECTING, strlen(OPPONENT_CONNECTING), 0);
				}
			}
			else if (strcmp(query, DISCONNECT_USER) == 0)
			{
				int opponentId = (currentUserId + 1) % 2;
				struct User opponent = games[availableId].users[opponentId];

				send(opponent.cfd, OPPONENT_DISCONNECTED, strlen(OPPONENT_DISCONNECTED), 0);
				games[availableId].users[currentUserId].isConnected = false;
				// pthread_exit(NULL);

				break;
			}
			else if (strcmp(query, REMATCH) == 0)
			{
				int opponentId = (currentUserId + 1) % 2;
				struct User opponent = games[availableId].users[opponentId];

				send(opponent.cfd, REMATCH, strlen(REMATCH), 0);

				if (opponent.wantsRematch)
				{
					if (currentUser.color == 0)
					{
						games[availableId].userIdturn = currentUserId;
						games[availableId].users[currentUserId].color = 1;
						games[availableId].users[opponentId].color = 0;
					}
					else
					{
						games[availableId].userIdturn = (currentUserId + 1) % 2;
						games[availableId].users[currentUserId].color = 0;
						games[availableId].users[opponentId].color = 1;
					}
					games[availableId].users[currentUserId].wantsRematch = false;
					games[availableId].users[opponentId].wantsRematch = false;
				}
			}
			else if (games[availableId].users[0].isConnected &&
					 games[availableId].users[1].isConnected &&
					 strcmp(query, "") != 0)
			{
				int turn = games[availableId].userIdturn;

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

	// printf("xd\n");
	close(c->cfd);
	// free(c);
	generateNewGame(availableId);
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
		generateNewGame(i);
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

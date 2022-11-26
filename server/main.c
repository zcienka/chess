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
const char *CAN_USER_CONNECT = "CAN_USER_CONNECT";

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

	int gameId = -1;
	for (int i = 0; i < MAX_GAMES; i++)
	{
		if (games[i].users[0].isConnected == true && games[i].users[1].isConnected == false)
		{
			gameId = i;
			currentUserId = 1;
			games[i].users[1].cfd = c->cfd;
			break;
		}
	}

	if (gameId == -1)
	{
		for (int i = 0; i < MAX_GAMES; i++)
		{
			if (games[i].users[0].isConnected == false && games[i].users[0].isConnected == false)
			{
				gameId = i;
				currentUserId = 0;
				games[i].users[0].cfd = c->cfd;
				break;
			}
		}
	}

	char query[128];
	int userRequest = 0;

	while (1)
	{
		memset(query, 0, strlen(query));

		if ((userRequest = recv(c->cfd, query, 128, 0)) == 0)
		{
			break;
		}

		// if the maximum amout of users are connected, the server responds with 0
		// otherwise it responds with 1
		if (strcmp(query, CAN_USER_CONNECT) == 0) 
		{
			int ok;
			char isOk[2];

			if (gameId == -1)
			{
				ok = 0;
			}
			else
			{
				ok = 1;
			}

			memset(isOk, 0, strlen(isOk));
			sprintf(isOk, "%d", ok);
			send(c->cfd, isOk, strlen(isOk), 0);

			if (ok == 0)
			{
				break;
			}
		}
		// server sends information about a color that was randomly generated
		else if (strcmp(query, ASSIGN_COLOR) == 0)
		{
			int color = games[gameId].users[currentUserId].color;

			char colorStr[2];
			memset(colorStr, 0, strlen(colorStr));
			sprintf(colorStr, "%d", color);

			send(c->cfd, colorStr, strlen(colorStr), 0);
			games[gameId].users[currentUserId].isConnected = true;
		}
		// if the user is connected, server sends string "OPPONENT_CONNECTED" to the user and the opponent
		// else it sends string "OPPONENT_CONNECTING"
		else if (strcmp(query, IS_OPPONENT_CONNECTED) == 0)
		{
			int opponentId = (currentUserId + 1) % 2;

			struct User opponent = games[gameId].users[opponentId];

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
		// if the client wants to disconnect, it gets marked as disconnected and 
		// it exits the loop and the memory gets freed
		else if (strcmp(query, DISCONNECT_USER) == 0)
		{
			int opponentId = (currentUserId + 1) % 2;
			struct User opponent = games[gameId].users[opponentId];

			send(opponent.cfd, OPPONENT_DISCONNECTED, strlen(OPPONENT_DISCONNECTED), 0);
			games[gameId].users[currentUserId].isConnected = false;

			break;
		}
		// when a user wants a rematch, the information about that is saved to the 
		// array and if both users want rematch the user colors in an array
		// are getting changed
		else if (strcmp(query, REMATCH) == 0)
		{
			int opponentId = (currentUserId + 1) % 2;
			struct User opponent = games[gameId].users[opponentId];

			games[gameId].users[currentUserId].wantsRematch = true;

			send(opponent.cfd, REMATCH, strlen(REMATCH), 0);

			if (opponent.wantsRematch)
			{
				if (games[gameId].users[currentUserId].color == 0)
				{
					games[gameId].userIdturn = currentUserId;
					games[gameId].users[currentUserId].color = 1;
					games[gameId].users[opponentId].color = 0;
				}
				else
				{
					games[gameId].userIdturn = (currentUserId + 1) % 2;
					games[gameId].users[currentUserId].color = 0;
					games[gameId].users[opponentId].color = 1;
				}
				games[gameId].users[currentUserId].wantsRematch = false;
				games[gameId].users[opponentId].wantsRematch = false;
			}
		}
		// if the server receives FEN sequence, it sends it to the opponent
		else if (games[gameId].users[0].isConnected &&
				 games[gameId].users[1].isConnected &&
				 strcmp(query, "") != 0)
		{
			int turn = games[gameId].userIdturn;

			if (turn == 0)
			{
				games[gameId].userIdturn = 1;
			}
			else if (turn == 1)
			{
				games[gameId].userIdturn = 0;
			}
			turn = games[gameId].userIdturn;

			send(games[gameId].users[turn].cfd, query, strlen(query), 0);
		}
	}
	int opponentId = (currentUserId + 1) % 2;

	struct User opponent = games[gameId].users[opponentId];

	// when both users disconnect, the new game gets generated
	if (!opponent.isConnected && !games[gameId].users[currentUserId].isConnected)
	{
		generateNewGame(gameId);
	}

	close(c->cfd); // after the client disconnects, the memory needs to be released

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
	listen(sfd, MAX_GAMES + 100);
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
		pthread_detach(tid); // when thread ends, it automatically gets deleted from the system
	}

	close(sfd);
	free(games);

	return EXIT_SUCCESS;
}

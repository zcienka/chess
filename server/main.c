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

// typedef enum { false, true } bool;

char *ASSIGN_COLOR = "ASSIGN_COLOR";

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

struct Game
{
	int id;
	struct User users[2];
};

struct Game games[10];
int users_num = 0;
int turn = 0;

void *cthread(void *arg)
{
	struct cln *c = (struct cln *)arg;
	// struct User currUser;
	// currUser.gameId = 0;
	// currUser.cfd = c->cfd;

	games[0].users[users_num % 2].cfd = c->cfd;

	printf("currUser.cfd %d\n", games[0].users[users_num % 2].cfd);

	printf("New connection: %s\n", inet_ntoa((struct in_addr)c->caddr.sin_addr));

	while (1)
	{
		char query[129];

		int userRequest = 0;
		memset(query, 0, strlen(query));
		// query[0] = '\0';
		// strcpy(query, "");

		// for (int i = 0; i < 2; i++)
		// {
		// if (games[0].users[0].isConnected && games[0].users[1].isConnected)
		// {
		// 	printf("xd\n");
		// 	userRequest = 0;

		// 	userRequest = read(games[0].users[turn].cfd, query, 128);
		// 	// if (userRequest != 0)
		// 	// {
		// 	// break;
		// 	// }
		// }
		// else
		// {
			userRequest = 0;
			// userRequest = read(games[0].users[users_num].cfd, query, 128);
			userRequest = recv(games[0].users[users_num % 2].cfd, query, 1024, 0);

			// printf("xddddddddd\n\n");
		// }
		// }

		if (userRequest != 0)
		{
			printf("query %s \n\n", query);

			if (strcmp(query, ASSIGN_COLOR) == 0)
			{
					int color = games[0].users[users_num % 2].color;

				char colorStr[2];
				memset(colorStr, 0, strlen(colorStr));
				sprintf(colorStr, "%d", color);
				printf("games[0].users[(users_num ) 2].color: %d \n", games[0].users[users_num % 2].color);

				// send(games[0].users[users_num - 1].cfd ,	colorStr, strlen(colorStr), 0);
				send(games[0].users[users_num % 2].cfd, colorStr, strlen(colorStr), 0);
				games[0].users[users_num % 2].isConnected = true;
				users_num++;
			}
			// else if (userRequest != 0 && strcmp(query, "") != 0 && games[0].users[0].isConnected && games[0].users[1].isConnected)
			// {
			// 	printf("query %s\n", query);

			// 	// for (int i = 0; i < 2; i++)
			// 	// {
			// 	// if (games[0].users[i].isConnected)
			// 	// {
			// send(games[0].users[turn].cfd, query, strlen(query), 0);
			// 	// }
			// 	// }
			// }
		}


	}
			close(c->cfd);
		free(c);
		return EXIT_SUCCESS;
}

int main(int argc, char *argv[])
{
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
	listen(sfd, 10);
	srand(time(NULL));

	for (int i = 0; i < 10; i++)
	{
		struct Game game;
		game.id = i;
		int color1 = rand() % 2;
		// int color1 = 0;

		game.users[0].color = color1;
		game.users[1].color = (color1 + 1) % 2;

		games[i].users[0].isConnected = false;
		games[i].users[1].isConnected = false;

		games[i] = game;
	}
	// for (int i = 0; i < 10; i++)
	// {
	// 	printf("color %d game.users[0].color: %d, game.users[1].color: %d\n\n", i, games[i].users[0].color, games[i].users[1].color);
	// }

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
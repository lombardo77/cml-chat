#ifndef TMCHAT_H
#define TMCHAT_H


#include <asm-generic/socket.h>
#include <bits/stdc++.h>
#include <cstddef>
#include <cstring>
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>
#include <vector>
#include <algorithm>

#define PORT 19000
#define SA struct sockaddr
#define MAXLINE 2048
#define CAST_INFO( ptr ) ((clinfo *)ptr)

// function prototypes
void *handle_connection(void *args);
void broadcast_msg(std::string msg, int senderfd);
int oblsock(int port);
int wait_for_connection(int sockfd);

// structs
typedef struct client_info {
	int clientfd;
	std::string ip_addr;
} clinfo;

#endif // !TMCHAT_H

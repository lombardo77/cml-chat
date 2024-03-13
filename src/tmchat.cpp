#include "tmchat.h"

using namespace std;
// global variables
vector<int> clients;

int wait_for_connection(int sockfd) {
	int clientfd;
	while (true) {
		struct sockaddr_in clntaddr;
		string ip_addr;
		cout << "waiting for connections...\n";

		socklen_t clen = sizeof(clntaddr);
		clientfd = accept(sockfd, (SA*)&clntaddr, &clen);
		clients.push_back(clientfd);

		// once connected we send the client to a new thread
		ip_addr = inet_ntoa(clntaddr.sin_addr);
		cout << "We have a connection with: " << ip_addr << "\n";

		clinfo cl_info = {clientfd, ip_addr};
		pthread_t thread;
		pthread_create(&thread, NULL, handle_connection, &cl_info);
	}
}

int oblsock(int port) {
	int sockfd;
	struct sockaddr_in server;

	if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		std::cout << "socket failed\n";
		exit(127);
	}

	server.sin_addr.s_addr = htonl(INADDR_ANY);
	server.sin_port = htons(port);
	server.sin_family = AF_INET;

	int one = 1;
	setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one));

	if (bind(sockfd, (SA*)&server, sizeof(server)) < 0) { 
		cout << "bind failed\n";
		exit(127);
	}

	if (listen(sockfd, 100) < 0) {
		cout << "listen failed\n";
		exit(127);
	}
	return sockfd;
}

void *handle_connection(void *args) {
	int clientfd = CAST_INFO(args)->clientfd;
	string ip_addr = CAST_INFO(args)->ip_addr;
	string msg;
	char client_buff[8 * (MAXLINE - 1)];

	while (true) {
		// read client msg and send to all other chatters
		read(clientfd, client_buff, MAXLINE);
		msg = client_buff;
		if (msg == "exit") {
			close(clientfd);
			cout << ip_addr << " has left the chat\n";
			clients.erase(remove(clients.begin(), clients.end(), clientfd), clients.end());
			break;
		}
		broadcast_msg("<" + ip_addr + "> " + msg, clientfd);
		cout << "<"<< ip_addr << "> " << msg << "\n";
		memset(client_buff, 0, MAXLINE);
		msg.clear();
	}
	return NULL;
}

void broadcast_msg(string msg, int senderfd) {
	for (const int &i: clients) {
		if (senderfd != i)
			write(i, msg.c_str(), msg.length() + 1);
	}
}

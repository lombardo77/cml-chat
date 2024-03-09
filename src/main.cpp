#include "tmchat.h"

int main (int argc, char *argv[]) {
	int sockfd = oblsock(PORT);
	wait_for_connection(sockfd);
	return 0;
}



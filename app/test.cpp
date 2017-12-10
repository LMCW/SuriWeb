#include <stdlib.h>
#include <stdio.h>
#include <string>
using namespace std;
int main(int argc, char** argv) {
	int now;
	for (int i=0; i<atoi(argv[1]); i++) {
		now = 1;
	}
	freopen(argv[2], "w", stdout);
	printf("%s\n", argv[2]);
	return 0;
}
#include <stdio.h>
#include <stdlib.h>

// read the file main.c and print out the contents

int main(int argc, char *argv[]) {
  if (argc < 2) {
    exit(0);
  }

  for (int i = 1; i < argc; ++i) {

    FILE *fp = fopen(argv[i], "r");

    if (fp == NULL) {
      printf("wcat: cannot open file\n");
      exit(1);
    }

    char buffer[1000];

    while (fgets(buffer, 50, fp)) {
      printf("%s", buffer);
    }

    fclose(fp);
  }
  return 0;
}

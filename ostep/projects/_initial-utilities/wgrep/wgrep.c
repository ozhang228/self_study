#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
  if (argc < 2) {
    printf("wgrep: searchterm [file ...]\n");
    exit(1);
  }

  char *searchTerm = argv[1];
  if (strlen(searchTerm) == 0) {
    return 0;
  }

  char buffer[500];
  if (argc == 2) {
    while (fgets(buffer, 500, stdin)) {
      if (strstr(buffer, searchTerm) != NULL) {
        printf("%s", buffer);
      }
    }
  } else {
    for (int i = 2; i < argc; ++i) {
      FILE *fp = fopen(argv[i], "r");

      if (fp == NULL) {
        printf("wgrep: cannot open file\n");
        exit(1);
      }

      while (fgets(buffer, 500, fp)) {
        if (strstr(buffer, searchTerm) != NULL) {
          printf("%s", buffer);
        }
      }
      fclose(fp);
    }
  }

  // ./wgrep search file1 file2
  // print lines that contain search term case sensitive(use getline)

  return 0;
}

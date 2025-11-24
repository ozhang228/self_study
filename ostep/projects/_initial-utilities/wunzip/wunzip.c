#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
  if (argc < 2) {
    printf("wunzip: file1 [file2 ...]\n");
    exit(EXIT_FAILURE);
  }

  FILE *fp;

  for (size_t i = 1; i < argc; ++i) {
    if ((fp = fopen(argv[i], "r")) == NULL) {
      printf("wunzip: cannot open file\n");
      exit(EXIT_FAILURE);
    }

    int cnt = 0;
    while (fread(&cnt, 4, 1, fp)) {
      char c;
      fread(&c, 1, 1, fp);
      for (size_t i = 0; i < cnt; ++i) {
        printf("%c", c);
      }
    }
    fclose(fp);
  }
  return 0;
}

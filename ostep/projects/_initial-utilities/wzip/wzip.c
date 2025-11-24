#include <stdio.h>

int main(int argc, char *argv[]) {
  if (argc < 2) {
    printf("wzip: file1 [file2 ...]\n");
    return 1;
  }

  int cnt = 1;
  char prev = 0;
  for (size_t i = 1; i < argc; ++i) {
    FILE *fp = fopen(argv[i], "r");

    if (fp == NULL) {
      printf("wzip: cannot open file\n");
      return 1;
    }

    if (prev == 0) {
      char new = fgetc(fp);

      if (new == EOF) {
        continue;
      }
      prev = new;
    }

    while (1) {
      char c = fgetc(fp);

      if (c == EOF) {
        break;
      }

      if (c != prev) {
        fwrite(&cnt, sizeof(int), 1, stdout);
        fwrite(&prev, sizeof(char), 1, stdout);

        prev = c;
        cnt = 1;
      } else {
        cnt++;
      }
    }

    fclose(fp);
  }

  fwrite(&cnt, sizeof(int), 1, stdout);
  fwrite(&prev, sizeof(char), 1, stdout);

  return 0;
}

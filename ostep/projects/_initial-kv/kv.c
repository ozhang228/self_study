#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *storageFilePath = "database.txt";

/**
 * Lazily appends to kv store (latest entry is the correct one)
 **/
int putCommand(char *key, char *value) {
  FILE *fp = fopen(storageFilePath, "a");

  if (fp == NULL) {
    printf("Error created file pointer");
    return EXIT_FAILURE;
  }

  fprintf(fp, "%s,%s\n", key, value);
  fclose(fp);

  return EXIT_SUCCESS;
}

int clearCommand() {
  FILE *fp = fopen(storageFilePath, "w");

  if (fp == NULL) {
    printf("Error created file pointer");
    return EXIT_FAILURE;
  }

  fclose(fp);

  return EXIT_SUCCESS;
}

int deleteCommand(char *key) {
  FILE *fp = fopen(storageFilePath, "r");
  FILE *tmp = fopen("temp_storage.txt", "w");

  if (fp == NULL || tmp == NULL) {
    printf("Error created file pointer");
    return EXIT_FAILURE;
  }

  char *line = NULL;
  size_t size = 0;
  ssize_t nread;

  char *deleted = NULL;

  while ((nread = getline(&line, &size, fp)) != -1) {
    char *dupLine = strdup(line);
    char *curKey = strsep(&dupLine, ",");
    char *curValue = strsep(&dupLine, ",");

    if (strcmp(key, curKey) != 0) {
      fwrite(line, 1, nread, tmp);
    } else {
      deleted = strdup(curValue);
    }
    free(dupLine);
  }

  if (deleted == NULL) {
    printf("%s not found\n", key);
  }

  free(line);
  fclose(fp);
  fclose(tmp);

  remove(storageFilePath);
  rename("temp_storage.txt", storageFilePath);
  return EXIT_SUCCESS;
}

int getCommand(char *key) {
  FILE *fp = fopen(storageFilePath, "r");

  if (fp == NULL) {
    printf("Error created file pointer");
    return EXIT_FAILURE;
  }

  char *line = NULL;
  size_t size = 0;
  ssize_t nread;

  char *target = NULL;

  while ((nread = getline(&line, &size, fp)) != -1) {
    char *dupLine = strdup(line);
    char *curKey = strsep(&dupLine, ",");
    char *curValue = strsep(&dupLine, ",");

    if (strcmp(curKey, key) == 0) {
      target = strdup(curValue);
    }
    free(dupLine);
  }

  if (target == NULL) {
    printf("%s not found\n", key);
  } else {
    printf("%s,%s", key, target);
  }

  free(line);
  fclose(fp);

  return EXIT_SUCCESS;
}

int main(int argc, char **argv) {
  if (argc == 1) {
    return 0;
  }

  for (int i = 1; i < argc; ++i) {
    char *s = strdup(argv[i]);
    char *command = strsep(&s, ",");

    if (*command == 'p') {
      char *key = strsep(&s, ",");
      char *value = strsep(&s, ",");

      if (putCommand(key, value) == EXIT_FAILURE) {
        return EXIT_FAILURE;
      }
    } else if (*command == 'c') {
      if (clearCommand() == EXIT_FAILURE) {
        return EXIT_FAILURE;
      }
    } else if (*command == 'd') {
      char *key = strsep(&s, ",");
      if (deleteCommand(key) == EXIT_FAILURE) {
        return EXIT_FAILURE;
      }
    } else if (*command == 'g') {
      char *key = strsep(&s, ",");
      if (getCommand(key) == EXIT_FAILURE) {
        return EXIT_FAILURE;
      };
    } else if (*command == 'a') {
      FILE *fp = fopen(storageFilePath, "r");

      if (fp == NULL) {
        printf("Error created file pointer");
        return EXIT_FAILURE;
      }

      char *line = NULL;
      size_t size = 0;
      ssize_t nread;

      char *target = NULL;
      int first = 1;

      while ((nread = getline(&line, &size, fp)) != -1) {
        printf("%s", line);
      }
    } else {
      printf("bad command\n");
    }
  }

  return EXIT_SUCCESS;
}

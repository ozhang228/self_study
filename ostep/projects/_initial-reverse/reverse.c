#include <stdio.h>
#include <stdlib.h>

typedef struct linkedList {
  char *data;
  struct linkedList *next;
} LinkedList;

int main(int argc, char *argv[]) {
  if (argc > 3) {
    fprintf(stderr, "usage: reverse <input> <output>\n");
    exit(EXIT_FAILURE);
  }

  if (argc == 3 && argv[1] == argv[2]) {
    fprintf(stderr, "Input and output file must differ\n");
    exit(EXIT_FAILURE);
  }

  char *buf = NULL;
  LinkedList *prev = NULL;
  LinkedList *head = (LinkedList *)malloc(sizeof(LinkedList));

  FILE *fp;
  if (argc == 1) {
    fp = stdin;
  } else {
    if ((fp = fopen(argv[1], "r")) == NULL) {
      fprintf(stderr, "reverse: cannot open file '%s'\n", argv[1]);
      exit(EXIT_FAILURE);
    }
  }

  while (fgets(buf, 1024, fp)) {
    LinkedList *newNode = (LinkedList *)malloc(sizeof(LinkedList));

    head->next = prev;
    prev = head;

    newNode->data = buf;
    newNode->next = head;
    head = newNode;
  }

  fclose(fp);
  FILE *outfp;
  if (argc == 3) {
    if ((fp = fopen(argv[2], "a")) == NULL) {
      fprintf(stderr, "reverse: cannot open file '%s'\n", argv[1]);
      exit(EXIT_FAILURE);
    }
  } else {
    outfp = stdout;
  }

  while (head != NULL) {
    fprintf(outfp, "%s\n", head->data);
    LinkedList *temp = head->next;
    free(head->data);
    free(head);
    head = temp;
  }

  fclose(outfp);
  exit(EXIT_SUCCESS);
}

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void add(int argc, char *argv[]) {
    
    int count = 0;
    for (int i = 0; i < argc; i++) {
        int num = atoi(argv[i]);
        count += num;
    }

    printf("%d", count);
}

void minus(int argc, char *argv[]) {
    int result = atoi(argv[0]);

    for (int i = 1; i < argc; i++) {
        result -= atoi(argv[i]);
    }

    printf("%d", result);


}
void multiply(int argc, char *argv[]) {
    int count = 1;
    for (int i = 0; i < argc; i++) {
        int num = atoi(argv[i]);
        count *= num;
    }
    printf("%d", count);
}

struct entry {
    const char *name;
    void (*fn)(int argc, char *argv[]);
};

struct entry table[] = {
    {"add", add},
    {"minus", minus},
    {"multiply",multiply},
};

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <function> [args...]\n", argv[0]);
        return 1;
    }

    for (int i = 0; i < sizeof(table) / sizeof(table[0]); i++) {
        if (strcmp(argv[1], table[i].name) == 0) {
            /* pass remaining arguments to the function */
            table[i].fn(argc - 2, argv + 2);
            return 0;
        }
    }

    printf("Unknown function: %s\n", argv[1]);
    return 1;
}

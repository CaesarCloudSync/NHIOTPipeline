#include <stdio.h>
#include <string.h>

void foo(int argc, char *argv[]) {
    printf("foo hello\n");
    for (int i = 0; i < argc; i++) {
        printf("foo arg[%d] = %s\n", i, argv[i]);
    }
}

void bar(int argc, char *argv[]) {
    printf("bar\n");
    for (int i = 0; i < argc; i++) {
        printf("bar arg[%d] = %s\n", i, argv[i]);
    }
}

void baz(int argc, char *argv[]) {
    printf("baz\n");
    for (int i = 0; i < argc; i++) {
        printf("baz arg[%d] = %s\n", i, argv[i]);
    }
}

struct entry {
    const char *name;
    void (*fn)(int argc, char *argv[]);
};

struct entry table[] = {
    {"foo", foo},
    {"bar", bar},
    {"baz", baz},
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

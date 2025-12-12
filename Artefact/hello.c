#include <stdio.h>
#include <string.h>

void foo() { printf("foo\n"); }
void bar() { printf("bar\n"); }
void baz() { printf("baz\n"); }

struct entry {
    const char *name;
    void (*fn)();
};

struct entry table[] = {
    {"foo", foo},
    {"bar", bar},
    {"baz", baz},
};

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <function>\n", argv[0]);
        return 1;
    }

    for (int i = 0; i < sizeof(table)/sizeof(table[0]); i++) {
        if (strcmp(argv[1], table[i].name) == 0) {
            table[i].fn();   // Call the function
            return 0;
        }
    }

    printf("Unknown function: %s\n", argv[1]);
    return 1;
}

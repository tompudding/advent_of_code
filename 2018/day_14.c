#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <inttypes.h>

#define MAX_RECIPES 21000000

void cook(uint8_t *recipes, size_t *elves, size_t *num_recipes) {
    uint8_t next = recipes[elves[0]] + recipes[elves[1]];
    if(next >= 10) {
        recipes[(*num_recipes)++] = 1;
    }
    recipes[(*num_recipes)++] = next % 10;
    elves[0] = (recipes[elves[0]] + 1 + elves[0]) % *num_recipes;
    elves[1] = (recipes[elves[1]] + 1 + elves[1]) % *num_recipes;
}

int main(void) {
    uint8_t *recipes = calloc(MAX_RECIPES, sizeof*recipes);

    recipes[0] = 3;
    recipes[1] = 7;
    size_t num_recipes = 2;

    size_t elves[2] = {0, 1};
    uint8_t target[6] = {0, 8, 4, 6, 0, 1};
    size_t target_len = sizeof(target)/sizeof(target[0]);
    size_t matched = 0;
    size_t matched_pos = 0;

    while(num_recipes + 2 < MAX_RECIPES) {
        cook(recipes, elves, &num_recipes);

        while(num_recipes >= target_len && matched_pos < num_recipes - target_len) {
            if(recipes[matched_pos++] == target[matched]) {
                matched++;
                if(matched == target_len) {
                    printf("%zd\n", matched_pos - matched);
                    return 0;
                }
            }
            else {
                matched = 0;
            }
        }
    }
}

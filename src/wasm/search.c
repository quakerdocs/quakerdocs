/**
 * This file contains the search engine backend. TODO
 */

#include <stdlib.h>

#ifdef EMSCRIPTEN
    #include <emscripten/emscripten.h>
#else
    #include <stdio.h>
    #define EMSCRIPTEN_KEEPALIVE
#endif

#include "search.h"
#include "vector.h"

/*
 * The global data used by the searcher.
 */
typedef struct GLOBALS {
    /* The array containing the search result pages. */
    page_t *result;
    int result_size;
    int result_index;

    /* Reusable stack and words list. */
    vector_t *stack;
    vector_t *words;

    /* Reusable page and temporary page maps. */
    int *map_a;
    int *map_b;
} globals_t;

/* Global variables. */
static int initialised = 0;
static globals_t g;


/*
 * Initialise the global variables and memory.
 */
void globals_init() {
    initialised = 1;
    g.result = malloc(total_page_count * sizeof (page_t));
    g.result_size = 0;
    g.result_index = 0;
    g.stack = vector_make(8);
    g.words = vector_make(2);
    g.map_a = malloc(total_page_count * sizeof (int));
    g.map_b = malloc(total_page_count * sizeof (int));
}

/*
 * Free the globally allocated memory.
 */
void globals_free() {
    initialised = 0;
    free(g.result);
    vector_free(g.stack);
    vector_free(g.words);
    free(g.map_a);
    free(g.map_b);
}

/*
 * Parse the input string to split it into words. This overwrites the input
 * string, and adds the words to the global words vector.
 *
 * input: the input string to read from and write to.
 */
void parse_input(char *input) {
    char *cleaned_it = input;
    char *found_word = NULL;

    /* Transform the input. */
    for (char *input_it = input; *input_it; ++input_it) {
        switch (*input_it) {
            case 'A': case 'B': case 'C': case 'D': case 'E': case 'F':
            case 'G': case 'H': case 'I': case 'J': case 'K': case 'L':
            case 'M': case 'N': case 'O': case 'P': case 'Q': case 'R':
            case 'S': case 'T': case 'U': case 'V': case 'W': case 'X':
            case 'Y': case 'Z':
                /* Convert the letter to lower case. */
                *input_it += 32;
            case 'a': case 'b': case 'c': case 'd': case 'e': case 'f':
            case 'g': case 'h': case 'i': case 'j': case 'k': case 'l':
            case 'm': case 'n': case 'o': case 'p': case 'q': case 'r':
            case 's': case 't': case 'u': case 'v': case 'w': case 'x':
            case 'y': case 'z': case '0': case '1': case '2': case '3':
            case '4': case '5': case '6': case '7': case '8': case '9':
                /* Add this letter, and possibly start a new word. */
                if (!found_word)
                    found_word = cleaned_it;
                *(cleaned_it++) = *input_it;
                break;
            case ' ': case '\n': case '\t': case '\r':
                /* Split into a new word. */
                if (found_word) {
                    *(cleaned_it++) = '\0';
                    g.words = vector_push(g.words, found_word);
                    found_word = NULL;
                }
                break;
            default:
                /* Ignore other characters. */
                break;
        }
    }

    /* Add the last word. */
    *cleaned_it = '\0';
    if (found_word)
        g.words = vector_push(g.words, found_word);
}

/*
 * Find a node which matches with the word, or NULL if no match can be found.
 * The lookup is done in the prefix trie from search.h.
 *
 * word: the word to find.
 *
 * returns: the node directly or indirectly associated with the word.
 */
const node_t *find_node(const char *word) {
    const node_t *current = nodes;
    int progress = 0;

    /* Iterate over the word to find the matching node. */
    while (word[progress]) {
        int match = 0;
        for (child_s i = 0; i < current->child_count; i++) {
            const node_t *child = nodes + current->children + i;
            const char *str = chars + child->chars;

            /* We have a match if the first character is the same. */
            if (str[0] == word[progress]) {
                match = 1;

                /* Check if the rest of the str matches. */
                for (str++, progress++; *str && word[progress]; str++, progress++) {
                    if (*str != word[progress]) {
                        /* This is not a match after all, return empty. */
                        return NULL;
                    }
                }

                /* Move to the next node. */
                current = child;
                break;
            }
        }

        /* We can give up if no match has been found. */
        if (!match)
            return NULL;
    }

    return current;
}

/*
 * Fill a page map with all the pages which contain (a part of) a word.
 *
 * page_map: the page map to place the results in.
 * word:     the word to search.
 *
 * returns: 0 if no pages have been found, 1 if this word should be ignored,
 *          and 2 otherwise.
 */
int search_word(int *page_map, const char *word) {
    /* Check if a matching node exists. */
    const node_t *node = find_node(word);
    if (node == NULL)
        return 0;

    /* Ignore this node, as it is a stopword. */
    if (node->page_count == ignore_node_value)
        return 1;

    /* Clear the page map. */
    for (int i = 0; i < total_page_count; ++i)
        page_map[i] = 0;

    /* Now combine all of the pages starting from the found word node. */
    g.stack = vector_push(g.stack, node);
    while (!vector_empty(g.stack)) {
        const node_t *node = vector_pop(g.stack);

        /* Push the nodes children on the stack. */
        for (child_s i = 0; i < node->child_count; i++)
            g.stack = vector_push(g.stack, nodes + node->children + i);

        /* Add the pages to the list. */
        for (page_s i = 0; i < node->page_count; i++) {
            const page_t *page = pages + (node->pages + i);
            page_map[page->index] += page->count;
        }
    }

    return 2;
}

/*
 * Search all the words of the global word stack, combine the results, and
 * return the final page map.
 *
 * returns: a page map containing the results of the search.
 */
int *search_and_combine_words() {
    int *page_map = g.map_a, *temp_map = g.map_b;
    int page_map_empty = 1;

    /* Iterate over the words to fill the page map. */
    for (int i = 0, l = vector_size(g.words); i < l; ++i) {
        int found_map = search_word(temp_map, vector_at(g.words, i));

        if (found_map == 0) {
            /* A word was not found, so there are no results. */
            return NULL;
        }
        else if (found_map == 2) {
            if (page_map_empty) {
                /* Replace the empty page map with the temp map. */
                page_map_empty = 0;
                int *temp = temp_map;
                temp_map = page_map;
                page_map = temp;
            }
            else {
                /* Intersect the two maps, adding the two counts only if
                 * the page exists in both maps. */
                for (int i = 0; i < total_page_count; i++) {
                    if (page_map[i] && temp_map[i])
                        page_map[i] += temp_map[i];
                    else
                        page_map[i] = 0;
                }
            }
        }
    }

    /* Return the page map if it is not empty. */
    return page_map_empty ? NULL : page_map;
}

/*
 * Compare two pages for sorting purposes.
 *
 * a: a pointer to the first page.
 * b: a pointer to the second page.
 *
 * returns: the count of the second page minus the first.
 */
int page_compare(const void *a, const void *b) {
    const page_t *page_a = (const page_t *) a;
    const page_t *page_b = (const page_t *) b;
    return page_b->count - page_a->count;
}


/*
 * Perform the search on an input query and store the found
 * page entries in memory.
 *
 * input: the input string.
 */
EMSCRIPTEN_KEEPALIVE
void performSearch(char *input) {
    if (!initialised)
        globals_init();

    /* Clear the previous search. */
    g.result_size = 0;
    g.result_index = 0;

    /* Parse the input and create the page map. */
    parse_input(input);
    int *page_map = search_and_combine_words();
    vector_clear(g.words);

    /* Update the result array if the page map is not empty. */
    if (page_map) {
        /* Add the final page map contents to the results vector. */
        for (int i = 0; i < total_page_count; ++i) {
            if (page_map[i] != 0)
                g.result[g.result_size++] = (page_t){i, page_map[i]};
        }

        /* Sort the results based on most occurrences count. */
        qsort(g.result, g.result_size, sizeof (page_t), page_compare);
    }
}

/*
 * Return the next found page as a url, title, and section title.
 *
 * returns: a url, title and section title of a page, seperated by newlines.
 */
EMSCRIPTEN_KEEPALIVE
const char* getSearch() {
    /* Check that we don't exceed the found results. */
    if (!initialised || g.result_index >= g.result_size)
        return NULL;

    /* Get the next entry from the array. */
    page_t found = g.result[g.result_index++];

    /* Translate the index to the page info and return. */
    return urltitles[found.index];
}

/*
 * This is main function for if we are running the search locally. The search query
 * can then be given as command line arguments. This is mainly used for testing
 * purposes.
 *
 * n: the number of arguments
 * input: an array of the arguments.
 *
 * returns: 0.
 */
#ifndef EMSCRIPTEN
int main(int n, char **input) {
    char buffer[1024];

    /* Fill the buffer with the input strings. */
    char *buffer_it = buffer;
    for (int i = 1; i < n; i++) {
        char *str = input[i];
        for (int j = 0, l = strlen(str); j < l; j++)
            *(buffer_it++) = str[j];

        if (i != n - 1)
            *(buffer_it++) = ' ';
    }

    *(buffer_it++) = 0;

    /* Search the query. */
    printf("Results for [%s]\n", buffer);
    performSearch(buffer);

    /* Print the results. */
    const char *result;
    while ((result = getSearch())) {
        printf("%s\n", result);
    }

    return 0;
}
#endif

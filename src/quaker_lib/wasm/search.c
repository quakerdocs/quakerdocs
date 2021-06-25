/**
 * This file contains the search engine backend. TODO
 */

#include "search.h"

#define NULL 0
#define WORDS_MAX 64
#define INPUT_MAX_SIZE 1024

typedef unsigned int page_map_t;

/**
 * TODO
 */
typedef struct RESULT {
    page_i page;
    page_map_t count;
} result_t;

/**
 * The global variables and arrays used by the searcher.
 */
typedef struct GLOBALS {
    /* The array containing the search result pages. */
    result_t results[PAGE_COUNT];
    int results_size;

    /* Reusable words list. */
    const char *words[WORDS_MAX];
    int word_count;

    /* Reusable page and temporary page maps. */
    page_map_t map_a[PAGE_COUNT];
    page_map_t map_b[PAGE_COUNT];
} globals_t;

/* Global variables. */
static globals_t g = {0};

/* The input buffer for communicating with javascript. */
char input_output[INPUT_MAX_SIZE];


/**
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
                    g.words[g.word_count++] = found_word;
                    found_word = NULL;
                    if (g.word_count == WORDS_MAX)
                        return;
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
        g.words[g.word_count++] = found_word;
}

/**
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

/**
 * TODO
 */
void fill_page_map(const node_t *node, page_map_t *page_map) {
    /* Add the pages of this node to the list. */
    for (page_s i = 0; i < node->page_count; ++i) {
        const page_t *page = pages + (node->pages + i);
        page_map[page->index] += page->count;
    }

    /* Add the pages of all the children.  */
    for (child_s i = 0; i < node->child_count; ++i)
        fill_page_map(nodes + node->children + i, page_map);
}

/**
 * Fill a page map with all the pages which contain (a part of) a word.
 *
 * page_map: the page map to place the results in.
 * word:     the word to search.
 *
 * returns: 0 if no pages have been found, 1 if this word should be ignored,
 *          and 2 otherwise.
 */
int search_word(page_map_t *page_map, const char *word) {
    /* Check if a matching node exists. */
    const node_t *node = find_node(word);
    if (node == NULL)
        return -1;

    /* Clear the page map. */
    for (int i = 0; i < PAGE_COUNT; ++i)
        page_map[i] = 0;

    /* Now combine all of the pages starting from the found word node. */
    fill_page_map(node, page_map);

    /* Ignore this node, as it is a stopword. */
    return node->pages == IGNORE_NODE_VALUE;
}

/**
 * Search all the words of the global word stack, combine the results, and
 * return the final page map.
 *
 * returns: a page map containing the results of the search.
 */
page_map_t *search_and_combine_words() {
    page_map_t *page_map = g.map_a, *temp_map = g.map_b;
    int page_map_empty = 1;
    int added_non_stopword = 0;

    /* Iterate over the words to fill the page map. */
    for (int i = 0; i < g.word_count; ++i) {
        int found_map = search_word(temp_map, g.words[i]);

        if (found_map == -1) {
            /* The word was not found, so there are no results. */
            return NULL;
        }
        else {
            if (page_map_empty) {
                /* Replace the empty page map with the temp map. */
                page_map_empty = 0;
                page_map_t *temp = temp_map;
                temp_map = page_map;
                page_map = temp;

                /* Half stopword contributions. */
                if (found_map == 1) {
                    for (int i = 0; i < PAGE_COUNT; i++)
                        page_map[i] /= 2;
                }
                else
                    added_non_stopword = 1;
            }
            else if (found_map == 1 || !added_non_stopword) {
                /* The word was a stopword, so union both maps. */
                for (int i = 0; i < PAGE_COUNT; i++) {
                    page_map[i] += temp_map[i] / 2;
                }
            }
            else if (found_map == 0) {
                if (!added_non_stopword) {
                    for (int i = 0; i < PAGE_COUNT; i++) {
                        if (temp_map[i])
                            page_map[i] += temp_map[i];
                        else
                            page_map[i] = 0;
                    }
                    added_non_stopword = 1;
                }
                else {
                    /* Intersect the two maps, adding the two counts only if
                    * the page exists in both maps. */
                    for (int i = 0; i < PAGE_COUNT; i++) {
                        if (page_map[i] && temp_map[i])
                            page_map[i] += temp_map[i];
                        else
                            page_map[i] = 0;
                    }
                }
            }
        }
    }

    /* Return the page map if it is not empty. */
    return page_map_empty ? NULL : page_map;
}

/**
 * TODO
 */
__attribute__((export_name("getIOBuffer")))
char *get_io_buffer() {
    return input_output;
}

/**
 * TODO
 */
__attribute__((export_name("getIOBufferSize")))
int get_io_buffer_size() {
    return INPUT_MAX_SIZE;
}

/**
 * Perform the search on an input query and store the found
 * page entries in memory.
 *
 * input: the input string.
 */
__attribute__((export_name("performSearch")))
void perform_search() {
    /* Clear the previous search. */
    g.results_size = 0;
    g.word_count = 0;

    /* Parse the input and create the page map. */
    parse_input(input_output);
    page_map_t *page_map = search_and_combine_words();

    /* Update the result array if the page map is not empty. */
    if (page_map) {
        /* Add the final page map contents to the results vector. */
        for (int i = 0; i < PAGE_COUNT; ++i) {
            if (page_map[i] != 0)
                g.results[g.results_size++] = (result_t){i, page_map[i]};
        }
    }
}

/**
 * Return the next found page as a url, title, and section title.
 *
 * returns: a url, title and section title of a page, seperated by newlines.
 */
 __attribute__((export_name("getSearch")))
int get_search() {
    /* Return 0 if no results are left. */
    if (g.results_size == 0)
        return 0;

    /* Get the highest result from the result array. */
    int max_i = 0, max_count = 0;
    for (int i = 0; i < g.results_size; i++) {
        if (g.results[i].count > max_count) {
            max_count = g.results[i].count;
            max_i = i;
        }
    }

    /* Get the next entry from the array. */
    g.results[max_i].count = 0;
    const char *result_it = urltitles[g.results[max_i].page];

    /* Remove already returned results from the back. */
    int temp = g.results_size;
    while (g.results_size != 0 && g.results[--temp].count == 0) {
        g.results_size = temp;
    }

    /* Copy the output to the input_output and return its length. */
    int i;
    for (i = 0; *result_it; ++result_it, ++i) {
        input_output[i] = *result_it;
    }

    return i;
}


#ifdef RUN_LOCAL
#include <stdlib.h>
#include <stdio.h>

/**
 * This is main function for if we are running the search locally. The search query
 * can then be given as command line arguments. This is mainly used for testing
 * purposes.
 *
 * n: the number of arguments
 * input: an array of the arguments.
 *
 * returns: 0.
 */
int main(int n, char **input) {
    /* Fill the buffer with the input strings. */
    char *buffer_it = input_output;
    for (int i = 1; i < n; i++) {
        for (char *str = input[i]; *str; ++str)
            *(buffer_it++) = *str;

        if (i != n - 1)
            *(buffer_it++) = ' ';
    }

    *(buffer_it++) = 0;

    /* Search the query. */
    printf("Results for [%s]\n", input_output);
    perform_search();

    /* Print the results. */
    int length;
    while ((length = get_search())) {
        input_output[length] = 0;
        printf("%s\n", input_output);
    }

    return 0;
}
#endif

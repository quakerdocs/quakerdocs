#include <stdio.h>
#include <string>
#include <string.h>
#include <vector>
#include <algorithm>
#include <emscripten/emscripten.h>
#include "libstemmer.h"

#include "index.hpp"

/* A wrapper class around the stemmer to easily deconstruct it. */
class Stemmer {
public:
    /* Initialise the stemmer. */
    Stemmer() {
        stemmer = sb_stemmer_new("english", "UTF_8");
    }

    /* Deconstruct the stemmer. */
    ~Stemmer() {
        sb_stemmer_delete(stemmer);
    }

    /* Return the stem of the input word. */
    const char *stem(const char *word) {
        return (const char *) sb_stemmer_stem(stemmer, (const sb_symbol *) word, strlen(word));
    }

private:
    sb_stemmer *stemmer;
};

std::vector<Entry> searchWord(const char *word) {
    const Node *current = nodes[0];
    int progress = 0;

    while (word[progress] == '\0') {
        bool match = false;
        for (child_s i = 0; i < current->child_count; i++) {
            const Node *child = nodes + children[children + i];
            const char *str = chars + child->chars;

            if (str[0] == word[progress]) {
                match = true;

                // Check if the rest of the str matches,


                if (match) {

                }
                else {
                    return {};
                }
            }
        }

        if (!match)
            return {};
    }
}



/* Find the intersection between two vectors. */
std::vector<Entry> intersect(const std::vector<Entry>& current, const std::vector<Entry>& next) {
    std::vector<Entry> intersection;

    /* Loop over both vectors and store the entries linking to the same page. */
    for (const Entry& entr1 : current) {
        for (const Entry& entr2 : next) {
            /* Check that the entries link to the same page. */
            if (entr1.page_index == entr2.page_index) {
                intersection.push_back(Entry{entr1.page_index, (short) (entr1.count + entr2.count)});
                break;
            }
        }
    }

    return intersection;
}

static std::vector<Entry> result;
static size_t result_index;


extern "C" {

    /* Perform the search and store the found entries in memory. */
    EMSCRIPTEN_KEEPALIVE
    void performSearch(char *input) {
        /* Clear the previous search. */
        result.clear();
        result_index = 0;

        /* Get the first word. */
        const char *word = strtok(input, " ");
        if (word == NULL)
            return;

        /* Stem the initial word. */
        Stemmer stemmer;
        word = stemmer.stem(word);

        /* Find the pages where the initial word is found. */
        auto it = idx.find(word);
        if (it != idx.end())
            result = it->second;
        if (result.empty())
            return;

        /* Loop over any remaining words. */
        while ((word = strtok(NULL, " ")) != NULL) {
            /* Stem the word. */
            word = stemmer.stem(word);

            /* Find the pages. */
            auto it = idx.find(word);
            if (it != idx.end())
                /* Store only common pages. */
                result = intersect(result, it->second);
            else
                result.clear();

            /* If any word was not found stop execution. */
            if (result.empty())
                return;
        }

        /* Sort the found entries by the count/priority. */
        std::sort(std::begin(result), std::end(result),
                [](Entry a, Entry b) {
                    return a.count > b.count;
                });
    }


    /* Return a found page as a url, title, and section title. */
    EMSCRIPTEN_KEEPALIVE
    const char* getSearch() {
        /* Check that we don't exceed the found results. */
        if (result_index >= result.size()) {
            return NULL;
        }

        /* Get the next entry from the array. */
        Entry found = result[result_index];
        result_index++;

        /* Translate the index to the page info and return. */
        return urltitles[found.page_index];
    }

}

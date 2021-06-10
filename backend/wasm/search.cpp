#include <string>
#include <string.h>
#include <vector>
#include <algorithm>
#include <map>
#include <regex>
#include <iostream>

#ifdef EMSCRIPTEN
#include <emscripten/emscripten.h>
#else
#define EMSCRIPTEN_KEEPALIVE
#endif

#include "libstemmer.h"
#include "index.hpp"
#include "print.hpp"


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

std::map<short,short> searchWord(const char *word) {
    const Node *current = nodes;
    int progress = 0;

    while (word[progress]) {
        bool match = false;
        for (child_s i = 0; i < current->child_count; i++) {
            const Node *child = nodes + children[current->children + i];
            const char *str = chars + child->chars;

            /* We have a match if the first character is the same. */
            if (str[0] == word[progress]) {
                match = true;

                /* Check if the rest of the str matches. */
                for (str++, progress++; *str && word[progress]; str++, progress++) {
                    if (*str != word[progress]) {
                        /* This is not a match after all, return empty. */
                        return {};
                    }
                }

                /* Move to the next node. */
                current = child;
                break;
            }
        }

        if (!match)
            return {};
    }

    /* Page map {page_index => total_count}. */
    std::map<short,short> page_map;

    /* The most closely matching node has been found. Now combine all of its pages. */
    std::vector<const Node*> stack = {current};
    while (!stack.empty()) {
        const Node* node = stack.back();
        stack.pop_back();

        /* Push the nodes children on the stack. */
        for (child_s i = 0; i < node->child_count; i++)
            stack.push_back(nodes + children[node->children + i]);

        /* Add the pages to the list. */
        for (page_s i = 0; i < node->page_count; i++) {
            const Page *page = pages + (node->pages + i);
            page_map.try_emplace(page->page_index, 0).first->second += page->count;
        }
    }

    return page_map;
}


void intersectMap(std::map<short,short>& map, const std::map<short,short>& new_map) {
    /* Check if each page exists in the other map. */
    for (auto it = map.begin(); it != map.end();) {
        auto other_it = new_map.find(it->first);
        if (other_it != new_map.end()) {
            /* Add the two counts if the page exists in both maps. */
            it->second += other_it->second;
            ++it;
        }
        else {
            /* Delete the page if it does not exist in the new map. */
            it = map.erase(it);
        }
    }

}



// /* Find the intersection between two vectors. */
// std::vector<Entry> intersect(const std::vector<Entry>& current, const std::vector<Entry>& next) {
//     std::vector<Entry> intersection;

//     /* Loop over both vectors and store the entries linking to the same page. */
//     for (const Entry& entr1 : current) {
//         for (const Entry& entr2 : next) {
//             /* Check that the entries link to the same page. */
//             if (entr1.page_index == entr2.page_index) {
//                 intersection.push_back(Entry{entr1.page_index, (short) (entr1.count + entr2.count)});
//                 break;
//             }
//         }
//     }

//     return intersection;
// }

static std::vector<Page> result;
static size_t result_index;
static std::regex reg("[^\\w\\s]|_");


extern "C" {

    // /* Perform the search and store the found entries in memory. */
    // EMSCRIPTEN_KEEPALIVE
    // void performSearch(char *input) {
    //     /* Clear the previous search. */
    //     result.clear();
    //     result_index = 0;

    //     /* Get the first word. */
    //     const char *word = strtok(input, " ");
    //     if (word == NULL)
    //         return;

    //     /* Stem the initial word. */
    //     Stemmer stemmer;
    //     word = stemmer.stem(word);

    //     /* Find the pages where the initial word is found. */
    //     auto it = idx.find(word);
    //     if (it != idx.end())
    //         result = it->second;
    //     if (result.empty())
    //         return;

    //     /* Loop over any remaining words. */
    //     while ((word = strtok(NULL, " ")) != NULL) {
    //         /* Stem the word. */
    //         word = stemmer.stem(word);

    //         /* Find the pages. */
    //         auto it = idx.find(word);
    //         if (it != idx.end())
    //             /* Store only common pages. */
    //             result = intersect(result, it->second);
    //         else
    //             result.clear();

    //         /* If any word was not found stop execution. */
    //         if (result.empty())
    //             return;
    //     }

    //     /* Sort the found entries by the count/priority. */
    //     std::sort(std::begin(result), std::end(result),
    //             [](Entry a, Entry b) {
    //                 return a.count > b.count;
    //             });
    // }

    /* Perform the search and store the found entries in memory. */
    EMSCRIPTEN_KEEPALIVE
    void performSearch(char *input) {
        /* Clear the previous search. */
        result.clear();
        result_index = 0;

        std::cout << input << std::endl;

        /* Transform the input. */
        for (int i = 0; input[i]; i++) {
            input[i] = tolower(input[i]);
            if (input[i] == '_')
                input[i] = ' ';
        }
        std::cout << input << std::endl;

        /* Only keep alphabetic characters, and get the first word. */
        std::string cleaned_input = std::regex_replace(input, reg, "");
        std::cout << cleaned_input << std::endl;

        const char *word = strtok(&cleaned_input[0], " ");
        if (word == NULL)
            return;

        std::cout << word << std::endl;

        /* Create the initial page map with the first stemmed word. */
        Stemmer stemmer;
        std::map<short,short> page_map = searchWord(stemmer.stem(word));

        /* Combine the results with the remaining words. */
        while ((word = strtok(NULL, " ")) != NULL && !page_map.empty())
            intersectMap(page_map, searchWord(stemmer.stem(word)));

        /* Add the final page map to the results. */
        result.reserve(page_map.size());
        for (std::pair<const short,short>& page : page_map)
            result.push_back(Page{page.first, page.second});

        /* Sort the found entries by the count/priority. */
        std::sort(std::begin(result), std::end(result),
                [](const Page a, const Page b) {
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
        Page found = result[result_index];
        result_index++;

        /* Translate the index to the page info and return. */
        return urltitles[found.page_index];
    }

}


#ifndef EMSCRIPTEN

int main(int n, char **input) {

    std::string query;

    for (int i = 1; i < n; i++) {
        query += input[i];
        query += " ";
    }
    std::cout << "Helo " << query << std::endl;

    performSearch(&query[0]);

    const char *result;
    while ((result = getSearch())) {
        std::cout << result << std::endl << std::endl;
    }

    return 0;
}
#endif
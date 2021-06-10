#include <algorithm>
#include <map>
#include <vector>

#ifdef EMSCRIPTEN
#include <emscripten/emscripten.h>
#else
#define EMSCRIPTEN_KEEPALIVE
#endif

#include "search.hpp"

static std::vector<Page> result;
static size_t result_index;

/* Find a node which matches with the word, or null if no match can be found. */
const Node *findNode(const char *word) {
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
                        return nullptr;
                    }
                }

                /* Move to the next node. */
                current = child;
                break;
            }
        }

        if (!match)
            return nullptr;
    }

    return current;
}

/* TODO */
std::map<short,short> searchWord(const char *word) {
    /* Check if a matching node exists. */
    const Node *node = findNode(word);
    if (node == nullptr)
        return {};

    std::map<short,short> page_map;

    /* The most closely matching node has been found. Now combine all of its pages. */
    std::vector<const Node*> stack = {node};
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

/* TODO */
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

/* TODO */
class InputParser {
public:
    InputParser(const char *input) {
        cleaned_input = new char[strlen(input)];

        /* Transform the input. */
        char *cleaned_it = cleaned_input;
        char *found_word = nullptr;

        for (const char *input_it = input; *input_it; ++input_it) {
            switch (*input_it) {
                case 'A': case 'B': case 'C': case 'D': case 'E': case 'F':
                case 'G': case 'H': case 'I': case 'J': case 'K': case 'L':
                case 'M': case 'N': case 'O': case 'P': case 'Q': case 'R':
                case 'S': case 'T': case 'U': case 'V': case 'W': case 'X':
                case 'Y': case 'Z':
                    if (!found_word)
                        found_word = cleaned_it;
                    *(cleaned_it++) = *input_it + 32;
                    break;
                case 'a': case 'b': case 'c': case 'd': case 'e': case 'f':
                case 'g': case 'h': case 'i': case 'j': case 'k': case 'l':
                case 'm': case 'n': case 'o': case 'p': case 'q': case 'r':
                case 's': case 't': case 'u': case 'v': case 'w': case 'x':
                case 'y': case 'z': case '0': case '1': case '2': case '3':
                case '4': case '5': case '6': case '7': case '8': case '9':
                    if (!found_word)
                        found_word = cleaned_it;
                    *(cleaned_it++) = *input_it;
                    break;
                case ' ': case '\n': case '\t':
                    /* Split into a new word. */
                    if (found_word) {
                        *(cleaned_it++) = '\0';
                        words.push_back(found_word);
                        found_word = nullptr;
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
            words.push_back(found_word);
    }

    ~InputParser() {
        delete cleaned_input;
    }

    char *cleaned_input;
    std::vector<char *> words;
};


extern "C" {
    /* Perform the search and store the found entries in memory. */
    EMSCRIPTEN_KEEPALIVE
    void performSearch(char *input) {
        /* Clear the previous search. */
        result.clear();
        result_index = 0;

        /* Parse the input and check if it contains any words.*/
        InputParser parsedInput(input);
        std::vector<char *> words = parsedInput.words;
        if (words.empty())
            return;

        /* Create the initial page map with the first word. */
        std::map<short,short> page_map = searchWord(words[0]);

        /* Combine the map with the remaining words. */
        for (int i = 1, l = words.size(); i < l && !page_map.empty(); ++i)
            intersectMap(page_map, searchWord(words[i]));

        /* Add the final page map contents to the results vector. */
        result.reserve(page_map.size());
        for (std::pair<const short,short>& page : page_map)
            result.push_back(Page{page.first, page.second});

        /* Sort the found entries by the count/priority. */
        auto compare = [](const Page a, const Page b) {
            return a.count > b.count;
        };
        std::sort(std::begin(result), std::end(result), compare);
    }

    /* Return a found page as a url, title, and section title. */
    EMSCRIPTEN_KEEPALIVE
    const char* getSearch() {
        /* Check that we don't exceed the found results. */
        if (result_index >= result.size())
            return NULL;

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

    std::cout << "Searching query:" << query << std::endl;
    performSearch(&query[0]);

    // Print the results.
    const char *result;
    while ((result = getSearch())) {
        std::cout << result << std::endl;
    }

    return 0;
}
#endif
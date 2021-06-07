#include <stdio.h>
#include <string>
#include <string.h>
#include <vector>
#include <algorithm>
#include <emscripten/emscripten.h>
#include "libstemmer.h"

#include "index.hpp"


class Stemmer {
public:
    Stemmer() {
        stemmer = sb_stemmer_new("english", "UTF_8");
    }
    ~Stemmer() {
        sb_stemmer_delete(stemmer);
    }

    const char *stem(const char *word) {
        return (const char *) sb_stemmer_stem(stemmer, (const sb_symbol *) word, strlen(word));
    }

private:
    sb_stemmer *stemmer;
};

std::vector<Entry> intersect(const std::vector<Entry>& current, const std::vector<Entry>& next) {
    std::vector<Entry> intersection;

    for (const Entry& entr1 : current) {
        for (const Entry& entr2 : next) {
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

    EMSCRIPTEN_KEEPALIVE
    void performSearch(char *input) {

        result.clear();
        result_index = 0;

        const char *word = strtok(input, " ");
        if (word == NULL)
            return;

        Stemmer stemmer;
        word = stemmer.stem(word);

        auto it = idx.find(word);
        if (it != idx.end())
            result = it->second;
        if (result.empty())
            return;

        while ((word = strtok(NULL, " ")) != NULL) {
            word = stemmer.stem(word);

            auto it = idx.find(word);
            if (it != idx.end())
                result = intersect(result, it->second);
            else
                result.clear();

            if (result.empty())
                return;
        }

        std::sort(std::begin(result), std::end(result), [](Entry a, Entry b) {return a.count > b.count;});
    }


    EMSCRIPTEN_KEEPALIVE
    const char* getSearch() {
        if (result_index >= result.size()) {
            return NULL;
        }

        Entry found = result[result_index];
        result_index++;

        return urltitles[found.page_index];
    }

}

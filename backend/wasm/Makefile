


# SOURCES := libstemmer/libstemmer/libstemmer_utf8.c libstemmer/src_c/stem_UTF_8_english.c search.cpp

SOURCES := search.cpp \
	libstemmer/src_c/stem_UTF_8_arabic.c \
	libstemmer/src_c/stem_UTF_8_armenian.c \
	libstemmer/src_c/stem_UTF_8_basque.c \
	libstemmer/src_c/stem_UTF_8_catalan.c \
	libstemmer/src_c/stem_UTF_8_danish.c \
	libstemmer/src_c/stem_UTF_8_dutch.c \
	libstemmer/src_c/stem_UTF_8_english.c \
	libstemmer/src_c/stem_UTF_8_finnish.c \
	libstemmer/src_c/stem_UTF_8_french.c \
	libstemmer/src_c/stem_UTF_8_german.c \
	libstemmer/src_c/stem_UTF_8_greek.c \
	libstemmer/src_c/stem_UTF_8_hindi.c \
	libstemmer/src_c/stem_UTF_8_hungarian.c \
	libstemmer/src_c/stem_UTF_8_indonesian.c \
	libstemmer/src_c/stem_UTF_8_irish.c \
	libstemmer/src_c/stem_UTF_8_italian.c \
	libstemmer/src_c/stem_UTF_8_lithuanian.c \
	libstemmer/src_c/stem_UTF_8_nepali.c \
	libstemmer/src_c/stem_UTF_8_norwegian.c \
	libstemmer/src_c/stem_UTF_8_porter.c \
	libstemmer/src_c/stem_UTF_8_portuguese.c \
	libstemmer/src_c/stem_UTF_8_romanian.c \
	libstemmer/src_c/stem_UTF_8_russian.c \
	libstemmer/src_c/stem_UTF_8_serbian.c \
	libstemmer/src_c/stem_UTF_8_spanish.c \
	libstemmer/src_c/stem_UTF_8_swedish.c \
	libstemmer/src_c/stem_UTF_8_tamil.c \
	libstemmer/src_c/stem_UTF_8_turkish.c \
	libstemmer/src_c/stem_UTF_8_yiddish.c \
	libstemmer/runtime/api.c \
	libstemmer/runtime/utilities.c \
	libstemmer/libstemmer/libstemmer_utf8.c

OBJS := $(SOURCES:.c=.o)
OBJS := $(OBJS:.cpp=.opp)

EM_OBJS := $(SOURCES:.c=.e)
EM_OBJS := $(EM_OBJS:.cpp=.epp)

CC_ARGS := -I"libstemmer/include"
CC := gcc $(CC_ARGS)
EM_CC := emcc -Os $(CC_ARGS) -s WASM=1 -s EXPORTED_FUNCTIONS=["_performSearch","_getSearch"] -s EXPORTED_RUNTIME_METHODS='["ccall","cwrap"]'

%.e: %.c
	$(EM_CC) -c -o $@ $<
%.epp: %.cpp
	$(EM_CC) -std=c++17 -c -o $@ $<
emscripten: emsdk $(EM_OBJS)
	@mkdir -p build
	$(EM_CC) $(EM_OBJS) -o build/search.js

%.o: %.c
	$(CC) -c -o $@ $<
%.opp: %.cpp
	$(CC) -std=c++17 -c -o $@ $<
local: $(OBJS)
	@mkdir -p build
	$(CC) -lstdc++ $(OBJS) -o build/search.out

clean:
	rm -rf build
	rm -rf $(OBJS) $(EM_OBJS)


emsdk:
	git clone https://github.com/emscripten-core/emsdk.git
	cd emsdk && ./emsdk install latest && ./emsdk activate latest

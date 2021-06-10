


# SOURCES := libstemmer/libstemmer/libstemmer_utf8.c libstemmer/src_c/stem_UTF_8_english.c search.cpp

SOURCES := search.cpp
OBJS := $(SOURCES:.cpp=.o)
EM_OBJS := $(SOURCES:.cpp=.em)

CC_ARGS := -I"libstemmer/include" -flto -Os
CC := gcc $(CC_ARGS)
EM_CC := emcc $(CC_ARGS) -s WASM=1 -s EXPORTED_FUNCTIONS=["_performSearch","_getSearch"] -s EXPORTED_RUNTIME_METHODS='["ccall","cwrap"]'

%.em: %.cpp
	$(EM_CC) -std=c++17 -c -o $@ $<
emscripten: emsdk $(EM_OBJS)
	@mkdir -p build
	$(EM_CC) $(EM_OBJS) -o build/search.js

%.o: %.cpp
	$(CC) -std=c++17 -c -o $@ $<
local: $(OBJS)
	@mkdir -p build
	$(CC) -lstdc++ $(OBJS) -o build/search.out

clean:
	rm -rf build

emsdk:
	git clone https://github.com/emscripten-core/emsdk.git
	cd emsdk && ./emsdk install latest && ./emsdk activate latest

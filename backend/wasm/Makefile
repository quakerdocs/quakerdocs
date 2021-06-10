


# SOURCES := libstemmer/libstemmer/libstemmer_utf8.c libstemmer/src_c/stem_UTF_8_english.c search.cpp

SOURCES := search.cpp

OBJS := $(SOURCES:.c=.o)
OBJS := $(OBJS:.cpp=.opp)

EM_OBJS := $(SOURCES:.c=.e)
EM_OBJS := $(EM_OBJS:.cpp=.epp)

CC_ARGS := -I"libstemmer/include"
CC := gcc $(CC_ARGS) -flto -Os
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

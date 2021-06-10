SOURCES := search.cpp
HEADERS := search.hpp
BUILD := build

OBJS := $(patsubst %.cpp, ${BUILD}/%.o, $(SOURCES))
EM_OBJS := $(patsubst %.cpp, ${BUILD}/%.em, $(SOURCES))

CC_ARGS := -Os #-flto
CC := gcc $(CC_ARGS)
EM_CC := emcc $(CC_ARGS) -s WASM=1 -s EXPORTED_FUNCTIONS=["_performSearch","_getSearch"] -s EXPORTED_RUNTIME_METHODS='["ccall","cwrap"]'

$(BUILD)/%.em: %.cpp $(HEADERS)
	$(EM_CC) -std=c++17 -c -o $@ $<
emscripten: emsdk $(EM_OBJS)
	@mkdir -p build
	$(EM_CC) $(EM_OBJS) -o build/search_data.js

$(BUILD)/%.o: %.cpp $(HEADERS)
	$(CC) -std=c++17 -c -o $@ $<
local: $(OBJS)
	@mkdir -p build
	$(CC) -lstdc++ $(OBJS) -o build/search.out

clean:
	rm -rf build

emsdk:
	git clone https://github.com/emscripten-core/emsdk.git
	cd emsdk && ./emsdk install latest && ./emsdk activate latest


CC := mingw32-gcc
SRC := $(wildcard dev/src/*.c)
OBJ := $(patsubst dev/src/%.c, output/obj/%.o, $(SRC))
INCLUDE := -Idev/include
LIBS := -Llib -l$(notdir $(basename $(wildcard lib/*)))
OUT := output/bin/main

all: $(OUT)

$(OUT): $(OBJ)
	$(CC) $(OBJ) $(LIBS) -o $(OUT)

output/obj/%.o: dev/src/%.c
	@mkdir -p $(OBJ_DIR)
	$(CC) -c $< $(INCLUDE) -o $@

clean:
	rm -rf output/obj/* output/bin/*

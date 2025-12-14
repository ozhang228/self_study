CXX := g++
CXXFLAGS := -Wall -Wextra -std=c++23

TARGET := wish
SRC := wish.cpp
TEST_SCRIPT := ./test-wish.sh

.PHONY: build run test clean

build: $(TARGET)

$(TARGET): $(SRC) 
	$(CXX) $(CXXFLAGS) -o $@ $<

run: build
	./$(TARGET)

test: build
	$(TEST_SCRIPT)

clean:
	rm -rf $(TARGET)

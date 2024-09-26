CC = g++
CXXFLAGS = -g
SRCS = $(wildcard *.cpp)
OBJS = $(SRCS:.cpp=.o)
OUTS = $(wildcard *.exe)

all : hello.exe

hello.exe :hello.cpp
	$(CC) -o $@ $<

.PHONY : clean

clean :
	del /q $(OUTS) $(OBJS)
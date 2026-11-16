SHELL     := /bin/bash
HOST      := $(shell hostname)
BUILD     := build
BIN       := $(BUILD)/bin
LOGS      := logs/$(HOST)

CXX       := g++
MPICXX    := mpicxx
CXXFLAGS  := -std=c++17 -O3 -DNDEBUG -Wall -Wextra -Wpedantic -Iinclude -isystem /usr/include/eigen3
LDFLAGS   := -lpagmo -ltbb -lpthread
MPI_RANKS ?= 4

TARGETS := \
	$(BIN)/pagmo-test \
	$(BIN)/pagmo-rosenbrock-de \
	$(BIN)/pagmo-rosenbrock-stress \
	$(BIN)/pagmo-rosenbrock-mpi \
	$(BIN)/pagmo-nsga3-zdt1 \
	$(BIN)/pagmo-zdt1-table

.PHONY: all build clean run-nsga3 run-table run-mpi

all: build

build: $(TARGETS)

$(BIN):
	@mkdir -p $(BIN)

$(BIN)/pagmo-test: src/smoke/pagmo-test.cpp | $(BIN)
	$(CXX) $(CXXFLAGS) $< $(LDFLAGS) -o $@

$(BIN)/pagmo-rosenbrock-de: src/single_obj/pagmo-rosenbrock-de.cpp | $(BIN)
	$(CXX) $(CXXFLAGS) $< $(LDFLAGS) -o $@

$(BIN)/pagmo-rosenbrock-stress: src/single_obj/pagmo-rosenbrock-stress.cpp | $(BIN)
	$(CXX) $(CXXFLAGS) $< $(LDFLAGS) -o $@

$(BIN)/pagmo-rosenbrock-mpi: src/single_obj/pagmo-rosenbrock-mpi.cpp | $(BIN)
	$(MPICXX) $(CXXFLAGS) $< $(LDFLAGS) -o $@

$(BIN)/pagmo-nsga3-zdt1: src/multi_obj/pagmo-nsga3-zdt1.cpp include/provenance.hpp | $(BIN)
	$(CXX) $(CXXFLAGS) $< $(LDFLAGS) -o $@

$(BIN)/pagmo-zdt1-table: src/multi_obj/pagmo-zdt1-table.cpp | $(BIN)
	$(CXX) $(CXXFLAGS) $< $(LDFLAGS) -o $@

run-nsga3: $(BIN)/pagmo-nsga3-zdt1
	@mkdir -p $(LOGS)
	set -o pipefail; ./$(BIN)/pagmo-nsga3-zdt1 2>&1 | tee $(LOGS)/pagmo-nsga3-zdt1_$(HOST).log

run-table: $(BIN)/pagmo-zdt1-table
	@mkdir -p $(LOGS)
	set -o pipefail; ./$(BIN)/pagmo-zdt1-table 2>&1 | tee $(LOGS)/pagmo-zdt1-table_$(HOST).log

run-mpi: $(BIN)/pagmo-rosenbrock-mpi
	@mkdir -p $(LOGS)
	set -o pipefail; HWLOC_COMPONENTS=-gl mpirun -bind-to none -np $(MPI_RANKS) ./$(BIN)/pagmo-rosenbrock-mpi 2>&1 | tee $(LOGS)/pagmo-rosenbrock-mpi_$(HOST)_np$(MPI_RANKS).log

clean:
	rm -rf $(BUILD)

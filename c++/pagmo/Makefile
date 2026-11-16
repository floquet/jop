SHELL := /bin/bash
HOST  := $(shell hostname)
NPROC := $(shell nproc)
BUILD := build
BIN   := $(BUILD)/bin
LOGS  := logs/$(HOST)
MPI_RANKS ?= 4

.PHONY: all configure build clean run-nsga3 run-table run-mpi

all: build

configure:
	cmake -S . -B $(BUILD) -DCMAKE_BUILD_TYPE=Release

build: configure
	cmake --build $(BUILD) -j $(NPROC)

run-nsga3: build
	@mkdir -p $(LOGS)
	set -o pipefail; ./$(BIN)/pagmo-nsga3-zdt1 2>&1 | tee $(LOGS)/pagmo-nsga3-zdt1_$(HOST).log

run-table: build
	@mkdir -p $(LOGS)
	set -o pipefail; ./$(BIN)/pagmo-zdt1-table 2>&1 | tee $(LOGS)/pagmo-zdt1-table_$(HOST).log

run-mpi: build
	@mkdir -p $(LOGS)
	set -o pipefail; HWLOC_COMPONENTS=-gl mpirun -bind-to none -np $(MPI_RANKS) ./$(BIN)/pagmo-rosenbrock-mpi 2>&1 | tee $(LOGS)/pagmo-rosenbrock-mpi_$(HOST)_np$(MPI_RANKS).log

clean:
	rm -rf $(BUILD)

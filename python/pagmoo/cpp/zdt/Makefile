CXX          := g++
CXXFLAGS     := -O3 -Wall -Wextra -std=c++17 -fPIC -shared
PYTHON       := python3
PY_INCLUDES  := $(shell $(PYTHON) -m pybind11 --includes)
EXT_SUFFIX   := $(shell $(PYTHON)-config --extension-suffix)
PAGMO_PREFIX ?= /usr

TARGET       := pagmo_benchmarks$(EXT_SUFFIX)
SRC          := pagmo_benchmarks.cpp

.PHONY: all clean check-deps test

all: check-deps $(TARGET)

check-deps:
	@if [ -z "$(PY_INCLUDES)" ]; then \
		echo "ERROR: pybind11 headers not found. Install via: sudo apt-get install -y python3-pybind11"; \
		exit 1; \
	fi
	@if [ ! -f "$(PAGMO_PREFIX)/include/pagmo/pagmo.hpp" ]; then \
		echo "ERROR: pagmo.hpp not found under $(PAGMO_PREFIX)/include/pagmo"; \
		exit 1; \
	fi

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(PY_INCLUDES) -I"$(PAGMO_PREFIX)/include" $< \
		-L"$(PAGMO_PREFIX)/lib" -Wl,-rpath,"$(PAGMO_PREFIX)/lib" -lpagmo -o $@

test: all
	$(PYTHON) test_deap_zdt.py 2>&1 | tee test_deap_zdt_$$(hostname).log

clean:
	rm -f pagmo_benchmarks*.so

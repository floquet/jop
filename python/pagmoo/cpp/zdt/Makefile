CXX          := g++
CXXFLAGS     := -O3 -Wall -Wextra -std=c++17 -fPIC -shared
PYTHON       := python3
PY_INCLUDES  := $(shell $(PYTHON) -m pybind11 --includes)
EXT_SUFFIX   := $(shell $(PYTHON)-config --extension-suffix)
PAGMO_PREFIX := $(shell spack location -i pagmo2)

TARGET       := pagmo_benchmarks$(EXT_SUFFIX)
SRC          := pagmo_benchmarks.cpp

.PHONY: all clean check-deps

all: check-deps $(TARGET)

check-deps:
	@if [ -z "$(PY_INCLUDES)" ]; then \
		echo "ERROR: pybind11 headers not found. Install via: sudo apt-get install -y python3-pybind11"; \
		exit 1; \
	fi
	@if [ -z "$(PAGMO_PREFIX)" ]; then \
		echo "ERROR: pagmo2 not found in Spack. Source Spack setup-env.sh first."; \
		exit 1; \
	fi

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(PY_INCLUDES) -I"$(PAGMO_PREFIX)/include" $< \
		-L"$(PAGMO_PREFIX)/lib" -Wl,-rpath,"$(PAGMO_PREFIX)/lib" -lpagmo -o $@

clean:
	rm -f pagmo_benchmarks*.so

.PHONY: test
test: all
	$(PYTHON) test_deap_zdt.py 2>&1 | tee test_deap_zdt_$$(hostname).log

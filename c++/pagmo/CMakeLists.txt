cmake_minimum_required(VERSION 3.20)
project(pagmo_benchmarks LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

find_package(Threads REQUIRED)
find_package(TBB REQUIRED)
find_package(Eigen3 REQUIRED NO_MODULE)
find_package(pagmo REQUIRED)
find_package(MPI REQUIRED)

# Helper to register standard TBB/Pagmo targets
function(add_pagmo_bench target_name src_path)
    add_executable(${target_name} ${src_path})
    target_include_directories(${target_name} PRIVATE "${CMAKE_SOURCE_DIR}/include")
    target_compile_options(${target_name} PRIVATE -Wall -Wextra -Wpedantic)
    target_link_libraries(${target_name} PRIVATE Pagmo::pagmo Eigen3::Eigen TBB::tbb Threads::Threads)
endfunction()

# Smoke & Single-Objective
add_pagmo_bench(pagmo-test              src/smoke/pagmo-test.cpp)
add_pagmo_bench(pagmo-rosenbrock-de     src/single_obj/pagmo-rosenbrock-de.cpp)
add_pagmo_bench(pagmo-rosenbrock-stress src/single_obj/pagmo-rosenbrock-stress.cpp)

# Hybrid MPI + TBB
add_pagmo_bench(pagmo-rosenbrock-mpi    src/single_obj/pagmo-rosenbrock-mpi.cpp)
target_link_libraries(pagmo-rosenbrock-mpi PRIVATE MPI::MPI_CXX)

# Multi-Objective (NSGA-III / ZDT1)
add_pagmo_bench(pagmo-nsga3-zdt1        src/multi_obj/pagmo-nsga3-zdt1.cpp)
add_pagmo_bench(pagmo-zdt1-table        src/multi_obj/pagmo-zdt1-table.cpp)

cmake_minimum_required(VERSION 3.18)
project(jop_pagmo CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pagmo REQUIRED)

add_executable(pagmo-test pagmo-test.cpp)
target_link_libraries(pagmo-test PRIVATE Pagmo::pagmo)

add_executable(pagmo-ngsa-iii-zdt1 pagmo-ngsa-iii-zdt1.cpp)
target_link_libraries(pagmo-ngsa-iii-zdt1 PRIVATE Pagmo::pagmo)

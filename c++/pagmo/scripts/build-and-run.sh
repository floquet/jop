#!/usr/bin/env bash
printf "%s\n" "$(tput bold)$(date) ${BASH_SOURCE[0]}$(tput sgr0)"

counter=0
subcounter=0
start_time=${SECONDS}

function new_step() {
    export counter=$((counter + 1))
    export subcounter=0
    echo ""
    echo "Step ${counter}: ${1}"
}

function sub_step() {
    export subcounter=$((subcounter + 1))
    echo ""
    echo "  Substep ${counter}.${subcounter}: ${1}"
}

function display_total_elapsed_time() {
    local total_elapsed_time=$((SECONDS - start_time))
    local total_minutes=$((total_elapsed_time / 60))
    local total_seconds=$((total_elapsed_time % 60))
    echo ""
    printf "Total elapsed time: %02d:%02d (MM:SS)\n" "$total_minutes" "$total_seconds"
}

# Begin steps
new_step "Ensure pagmo2 environment is loaded"
if [ -z "${CMAKE_PREFIX_PATH:-}" ]; then
    sub_step "source ./activate-pagmo.sh"
    source ./activate-pagmo.sh
else
    sub_step "Environment already active"
fi

new_step "Configure CMake"
sub_step "cmake -B build -DCMAKE_BUILD_TYPE=Release"
cmake -B build -DCMAKE_BUILD_TYPE=Release

new_step "Compile targets"
sub_step "cmake --build build -j $(nproc)"
cmake --build build -j "$(nproc)"

new_step "Run pagmo-test"
sub_step "./build/pagmo-test"
    sub_step "./build/pagmo-ngsa-iii-zdt1"
    ./build/pagmo-ngsa-iii-zdt1
./build/pagmo-test

display_total_elapsed_time

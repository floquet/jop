#!/usr/bin/env bash
printf "%s\n" "$(date), $(tput bold)${BASH_SOURCE[0]}$(tput sgr0)"

start_time=$SECONDS  # Record the start time

# Counts steps in batch process
export counter=0
function new_step() {
    counter=$((counter+1))
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Step ${counter}: ${1}"
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

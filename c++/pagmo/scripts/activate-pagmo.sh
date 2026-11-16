#!/usr/bin/env bash
printf "%s\n" "$(tput bold)$(date) ${BASH_SOURCE[0]}$(tput sgr0)"

# invocation: source activate-pagmo.sh 

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
SPACK_ROOT="$HOME/spacktivity/genesis"

new_step "Initialize Spack shell support"
if ! command -v spack >/dev/null 2>&1; then
    sub_step "source $SPACK_ROOT/share/spack/setup-env.sh"
    source "$SPACK_ROOT/share/spack/setup-env.sh"
else
    sub_step "spack already in PATH"
fi

new_step "Load pagmo2"
sub_step "spack load pagmo2"
spack load pagmo2

display_total_elapsed_time

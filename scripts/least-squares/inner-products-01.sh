#! /usr/bin/env bash
printf "%s\n" "$(date), $(tput bold)${BASH_SOURCE[0]}$(tput sgr0)"

#Initialize counters
counter=0
subcounter=0
start_time=${SECONDS}

# counts steps in batch process
export counter=0
function new_step(){
    counter=$((counter+1))
    echo ""
    echo "Step ${counter}: ${1}"
}

function sub_step() {
    export subcounter=$((subcounter + 1))
    echo ""
    echo "  Substep ${counter}.${subcounter}: ${1}"
}

for f in *.tex; do
    new_step "Processing: $f"
    [ -e "$f" ] || continue
    
    sub_step "/\\ie{ => \\innerSelf{"
    sed -i.bak 's/\\ie{/\\innerSelf{/g' "$f"

    sub_step "/\\itwo{ => \\inner{"
    sed -i.bak 's/\\itwo{/\\inner/g' "$f"
    
done

    printf 'execution time: %dh:%dm:%ds\n' $(($SECONDS/3600)) $(($SECONDS%3600/60)) $(($SECONDS%60)) 
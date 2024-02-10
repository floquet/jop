#! /usr/bin/env bash
printf "%s\n" "$(date), $(tput bold)${BASH_SOURCE[0]}$(tput sgr0)"
export SECONDS=0

# counts steps in batch process
export counter=0
function new_step(){
    counter=$((counter+1))
    echo ""
    echo "Step ${counter}: ${1}"
}

# https://stackoverflow.com/questions/20796200/how-to-loop-over-files-in-directory-and-change-path-and-add-suffix-to-filename
for filename in cfg-list.txt; do
    [ -e "$filename" ] || continue
    printf "configuration file ${filename}\n"
    # ... rest of the loop body
done

while read line; do
    # grab config file
    # launch the application 
    # pip standard and error outputs into dedicated file
    # grab next available thread
    echo "python3 ${line} 2>&1 | ./outputs/${line}.out &"
done < cfg-list.txt

    printf 'execution time: %dh:%dm:%ds\n' $(($SECONDS/3600)) $(($SECONDS%3600/60)) $(($SECONDS%60)) 
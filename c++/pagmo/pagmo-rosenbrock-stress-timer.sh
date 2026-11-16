#!/usr/bin/env bash
printf "%s\n" "$(tput bold)$(date) ${BASH_SOURCE[0]}$(tput sgr0)"

echo '/usr/bin/time -v ./pagmo-rosenbrock-stress 2>&1 | grep -E "Elapsed \(wall clock\)|User time|Percent of CPU|Maximum resident"'

/usr/bin/time -v ./pagmo-rosenbrock-stress 2>&1 | grep -E "Elapsed \(wall clock\)|User time|Percent of CPU|Maximum resident"



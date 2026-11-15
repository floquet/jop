#!/usr/bin/env bash
printf "%s\n" "$(tput bold)$(date) ${BASH_SOURCE[0]}$(tput sgr0)"

# invocation: source spack-python.sh./spack-python.sh

echo "source ~/spacktivity/genesis/share/spack/setup-env.sh"
      source ~/spacktivity/genesis/share/spack/setup-env.sh

echo "spack load py-pymoo@0.6.1.5"
      spack load py-pymoo@0.6.1.5


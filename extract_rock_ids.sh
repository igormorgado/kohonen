#!/bin/bash

cat - | sed -n '/LITOLOGIA -/,/RESUMO DAS ROCHAS/p' | grep -v -e 'TOPO' -e 'LITOLOGIA' -e 'RESUMO DAS ROCHAS' -e '------' | cut -c 38-62 | sort -nu

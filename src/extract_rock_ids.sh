#!/bin/bash

cat - \
| sed -n '/LITOLOGIA -/,/RESUMO DAS ROCHAS/p' \
| grep -v -e 'TOPO' -e 'LITOLOGIA' -e 'RESUMO DAS ROCHAS' -e '------' \
| sed 's/IGNEA NAO IDENT./IGNEA_NAO_IDENT_/g' \
| sed 's/METAMOR.NAO IDE./METAMOR_NAO_IDE_/g' \
| cut -c 38-74 \
| tr -s ' '  \
| column -t \
| sort -n \
| uniq

#!/usr/bin/env bash

# Cria arquivo com timestamp correta:

OUPUTDIR="../outputs"
TIMESTAMP=$(date +"%y%m%d%H%M%S")
USER="IGU"
FILEREF="run123"
FILENAME="${TIMESTAMP}_${USER}_${FILEREF}.log"
FILEPATH="${OUPUTDIR}/${FILENAME}"

echo "O arquivo gerado e' ${FILEPATH}"
echo "ola"  > ${FILEPATH}

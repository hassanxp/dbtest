#!/bin/bash

#
# Temp script for generating example script. For StackOverflow question.
#

schemafile=commentTest.py
output=col-example.jpg
database=hassantest
user=hassans
dburl=postgresql://localhost:5432/${database}

python3 ${schemafile} ${dburl}
schemacrawler.sh --server=postgresql --database=${database} --user=${user} -c=schema --output-format=jpg \
-o=${output} --info-level=maximum --portable-names

echo "Output in file ${output}."
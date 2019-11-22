#!/bin/bash

#
# Generates PDF of database schema based on schema file
#

schemafile=spstables.py
output=database-diagram.pdf
database=hassantest
user=hassans
dburl=postgresql://localhost:5432/${database}

python3 ${schemafile} ${dburl}
schemacrawler.sh --server=postgresql --database=${database} --user=${user} -c=schema --output-format=pdf \
-o=database-diagram.pdf --info-level=maximum --portable-names

echo "Output in file ${output}."
#!/bin/bash

function run_command {
  # psql test -c $1
  echo $1
}

run_command "drop table if exists predictions;"

columns=$(head -n1 $1 | cut -d',' -f2-)
column_names=$(echo $columns | sed 's/,/ decimal, /g')

run_command "create table predictions (id varchar, $column_names decimal);"

run_command "\copy predictions from '$(realpath $1)' header delimiter ',' csv;"
for c in $(echo $columns | sed 's/,/ /g')
do
  run_command "create index on predictions ($c);"
done

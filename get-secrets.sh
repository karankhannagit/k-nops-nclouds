#!/bin/bash

declare -a arr=("/tmp/secrets/uat" "/tmp/secrets/prod" )

for i in "${arr[@]}"
do
  for entry in $i/*
  do

          #retrieve password value from json response

    value="$(sudo aws ssm get-parameters --names "/test/initialstage/value" --with-decryption --output json)"

    while IFS= read -r line
      do
        if [[ $line = *"Value"* ]]; then
          #retrieve password value from json response
          password="${line#*:}"

          # removing whitespaces from start
          trimmed="${password## }"
          # removing whitespaces from end and eliminating any characters before starting of actual value
          trimmed="${password%% }" | sed 's/^.*"/"/'
          #remvong double quotes from value
          trimmed="${trimmed:1: -1}"
          #printf "%s\n" "$trimmed"
          export $key=$trimmed

        fi
    done < <(printf "%s\n" "$value")
  done
done


#!/usr/bin/env bash

# process each line interactively (ie line will be translated as the build occurs)
while read -r line; do
	echo $line | sed "s#@ \.#$1#"
done
#!/bin/bash

ls

for item in *; do
	if [ -d "$item" ]; then
		ls "$item"
	fi
done


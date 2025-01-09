#!/bin/bash

for subfolder in ./books/*/; do
  subfolder_name=$(basename "$subfolder")
  echo "Processing subfolder: $subfolder_name"
  rm -rf "books/$subfolder_name"
  git rm -r "books/$subfolder_name"
  git submodule add --force "git@github.com:eddieai/$subfolder_name.git" "books/$subfolder_name"
done

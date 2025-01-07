#!/bin/bash

# Navigate to the ./books folder
cd ./books || exit 1

# Loop through each subfolder inside ./books
for SUBFOLDER in */; do
  # Remove trailing slash from subfolder name
  SUBFOLDER_NAME="${SUBFOLDER%/}"

  echo "Processing subfolder: $SUBFOLDER_NAME"

  # Step 1: Run add_python_to_code_blocks.py script
  echo "Running: python scripts/add_python_to_code_blocks.py ./books/$SUBFOLDER_NAME"
  python ../scripts/add_python_to_code_blocks.py "./$SUBFOLDER_NAME"
  
  # Check if the previous command was successful
  if [ $? -ne 0 ]; then
    echo "Error while running add_python_to_code_blocks.py in $SUBFOLDER_NAME. Skipping."
    continue
  fi

  # Navigate to ./SUBFOLDER_NAME/docs
  cd "./$SUBFOLDER_NAME/docs" || { echo "Docs folder not found in $SUBFOLDER_NAME. Skipping."; continue; }

  # Step 2: Run honkit build command
  echo "Installing Honkit"
  npm init --yes
  npm install honkit --save-dev
  echo "Running: npx honkit build"
  npx honkit build

  # Check if the honkit build succeeded
  if [ $? -ne 0 ]; then
    echo "Error during 'npx honkit build' in $SUBFOLDER_NAME/docs. Skipping."
    cd ../../.. # Go back to the books directory
    continue
  fi

  # Step 3: Post-process generated book files
  echo "Running cleanup and moving files in $SUBFOLDER_NAME/docs"
  rm -rf ./gitbook && mv ./_book/* ./ && rm -rf ./_book

  # Navigate back to ./SUBFOLDER_NAME
  cd .. || { echo "Error navigating back to $SUBFOLDER_NAME. Skipping."; continue; }

  # Step 4: Create a new git commit and push the changes
  echo "Adding changes to git in $SUBFOLDER_NAME"
  git add .
  git commit -m "add python to code blocks"
  
  # Push changes
  echo "Pushing changes to remote"
  git push
  
  # Navigate back to ./books for the next subfolder
  cd .. || exit 1
done

echo "All subfolder processing complete."
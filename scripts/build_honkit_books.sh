#!/bin/bash

# Function to process a single book
process_book() {
    # Remove trailing slash from book name
    local BOOK_NAME="$(basename "$BOOK_PATH")"
    BOOK_NAME="${BOOK_NAME%/}"
    echo ""
    echo "-------------------------- Processing book: $BOOK_NAME --------------------------"

    # Step 1: Run add_python_to_code_blocks.py script
    echo ""
    cd $BOOK_PATH
    echo "Running: python scripts/add_python_to_code_blocks.py books/$BOOK_NAME"
    python $HONKITBOOKS_DIR/scripts/add_python_to_code_blocks.py $BOOK_PATH
    # Check if the previous command was successful
    if [ $? -ne 0 ]; then
        echo "Error while running add_python_to_code_blocks.py in $BOOK_NAME. Skipping."
        return 1
    fi
    sleep 1

    # Step 2: Run honkit build command
    echo ""
    # Navigate to ./BOOK_NAME/docs
    cd $BOOK_PATH/docs || {
        echo "Docs folder not found in $BOOK_NAME. Skipping."
        return 1
    }
    # Check for Git changes
    if [[ $(git status --porcelain) ]]; then
        # Git changes detected, proceed with Honkit build
        echo "Installing Honkit"
        npm init --yes > /dev/null 2>&1
        npm install honkit --save-dev > /dev/null 2>&1

        echo "Building Honkit book in $BOOK_NAME/docs"
        npx honkit build > /dev/null 2>&1
        # Check if the honkit build succeeded
        if [ $? -ne 0 ]; then
            echo "Error during 'npx honkit build' in $BOOK_NAME/docs. Skipping."
            cd ../../.. # Go back to the books directory
            return 1
        fi
        sleep 1
        # Post-process generated book files
        echo "Running cleanup and moving files in $BOOK_NAME/docs"
        rm -rf ./gitbook && mv ./_book/* ./ && rm -rf ./_book
    else
        echo "No Git changes detected. Skipping Honkit build."
    fi
    sleep 1

    # Step 3: Run enable_finger_zoom.py script
    echo ""
    cd $BOOK_PATH
    echo "Running: python scripts/enable_finger_zoom.py books/$BOOK_NAME"
    python $HONKITBOOKS_DIR/scripts/enable_finger_zoom.py $BOOK_PATH
    # Check if the previous command was successful
    if [ $? -ne 0 ]; then
        echo "Error while running enable_finger_zoom.py in $BOOK_NAME. Skipping."
        return 1
    fi
    sleep 1

    # Step 4: Check if there are any changes in the current repository, if yes git push
    if $GIT; then
        echo ""
        cd $BOOK_PATH
        echo "Preparing to commit and push changes in $BOOK_NAME"
        # Check if there are any changes in the repository
        if [[ $(git status --porcelain) ]]; then
            # There are changes, so add, commit, and push
            git add .
            git commit -m "$COMMIT_MSG"
            git push
        else
            # No changes, do nothing
            echo "No changes to commit."
        fi
        sleep 1
    fi

    return 0
}

# Main script
BOOK=""
GIT=false
COMMIT_MSG=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --BOOK)
            BOOK="$2"
            shift 2
            ;;
        --GIT)
            GIT=true
            shift 1
            ;;
        --COMMIT_MSG)
            COMMIT_MSG="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--COMMIT_MSG <commit_message>] [--BOOK <book_name>] [--GIT] [--help]"
            echo "  --COMMIT_MSG: Specify the commit message for the push."
            echo "  --BOOK: Specify the book name to push."
            echo "  --GIT: Enable Git functionality (default: false)."
            echo "  --help: Display this help message."
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Your script logic here
echo "BOOK: $BOOK"
if $GIT; then
    echo "GIT: true"
else
    echo "GIT: false"
fi
echo "COMMIT_MSG: $COMMIT_MSG"

HONKITBOOKS_DIR=$(dirname "$(dirname "$(readlink -f "$0")")")

if [ -n "$BOOK" ]; then
    # Process specific book
    BOOK_PATH="$HONKITBOOKS_DIR/books/$BOOK"
    if [ -d "$BOOK_PATH" ]; then
        process_book "$BOOK_PATH" "$COMMIT_MSG"
    else
        echo "Book '$BOOK' not found in $HONKITBOOKS_DIR/books/"
        exit 1
    fi
else
    # Process all books
    for BOOK_PATH in $HONKITBOOKS_DIR/books/*/; do
        process_book "$BOOK_PATH" "$COMMIT_MSG"
        # Navigate back to ./books for the next book
        cd .. || exit 1
    done
fi

echo ""
echo "-------------------------- All book processing complete --------------------------"

#!/bin/bash

echo "==== AI-POWERED FILE MANAGER BOT ===="
echo "How can I help you with your files today?"
read -r query

# Basic rule-based intent detection

if [[ "$query" =~ [Ll]arge\ files || "$query" =~ [Bb]ig\ files ]]; then
    echo "-> Searching for files >100MB in current directory..."
    find . -type f -size +100M -exec ls -lh {} \; | awk '{print $5, $9}'

elif [[ "$query" =~ [Tt]emporary\ files || "$query" =~ [Cc]lean\ files ]]; then
    echo "-> Looking for temp/cache files to clean..."
    find . -type f \( -name "*.tmp" -o -name "*.cache" \) -print
    echo "Run 'rm' on above files to clean."

elif [[ "$query" =~ [Dd]ocuments || "$query" =~ [Pp][Dd][Ff] ]]; then
    echo "-> Listing documents (pdf/doc/txt) in current directory..."
    find . -type f \( -name "*.pdf" -o -name "*.docx" -o -name "*.txt" \) -print

elif [[ "$query" =~ [Oo]rganize || "$query" =~ [Ss]ort ]]; then
    echo "-> Organizing files by extension into folders..."

    for file in *; do
        if [ -f "$file" ]; then
            ext="${file##*.}"
            mkdir -p "$ext"
            mv "$file" "$ext/" 2>/dev/null
        fi
    done

    echo "Files organized into folders by type."

elif [[ "$query" =~ [Hh]elp || "$query" =~ [Oo]ptions ]]; then
    echo "Supported queries:"
    echo " - Find large files"
    echo " - Clean temporary files"
    echo " - Show documents"
    echo " - Organize files"
    echo " - Help"

else
    echo "Sorry, I did not understand. Type 'help' for options."
fi

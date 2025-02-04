#!/bin/bash

# Set the directory (current directory by default)
SEARCH_DIR="${1:-.}"

# Find all Python files and replace the shebang line
find "$SEARCH_DIR" -type f -name "*.py" | while read -r file; do
    # Check if the first line contains the Python shebang
    if head -n 1 "$file" | grep -q "#!/usr/bin/env python"; then
        # Use sed to replace the line
        sed -i '1s|#!/usr/bin/env python|#!/usr/bin/env rmanpy|' "$file"
        echo "Updated: $file"
    fi
done

echo "Shebang replacement completed."
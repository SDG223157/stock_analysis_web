#!/bin/bash

# fix_structure.sh

# Create all necessary directories
mkdir -p app/{analyzer,data,analysis,visualization,config,static/{css,js},templates}

# Create __init__.py files in all directories
touch app/{__init__.py,analyzer/__init__.py,data/__init__.py,analysis/__init__.py,visualization/__init__.py,config/__init__.py}

# Copy existing code with proper module structure
if [ -d "../stock_analysis/src/data" ]; then
    cp -r ../stock_analysis/src/data/* app/data/
    cp -r ../stock_analysis/src/analysis/* app/analysis/
    cp -r ../stock_analysis/src/visualization/* app/visualization/
    cp -r ../stock_analysis/src/config/* app/config/
else
    echo "Warning: Source directories not found. Please ensure your original project is in the correct location."
fi

# Update imports in all Python files to use app prefix
find app -type f -name "*.py" -exec sed -i '' 's/from data\./from app.data./g' {} +
find app -type f -name "*.py" -exec sed -i '' 's/from analysis\./from app.analysis./g' {} +
find app -type f -name "*.py" -exec sed -i '' 's/from visualization\./from app.visualization./g' {} +
find app -type f -name "*.py" -exec sed -i '' 's/from config\./from app.config./g' {} +

echo "Project structure has been fixed and imports have been updated."
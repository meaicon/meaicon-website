#!/bin/bash

# Simple script to extract competitor hero sections
cd /c/Users/nev3s/repos/meaicon-website

# Create output file
output="research-data/competitor-analysis.md"

# Start with header
echo "# UAE IT Infrastructure Competitor Hero Analysis" > "$output"
echo "Generated: $(date)" >> "$output"
echo "" >> "$output"

# Function to extract hero content from URL
extract_hero() {
    local url=$1
    local name=$2
    
    echo "## $name" >> "$output"
    echo "**URL:** $url" >> "$output"
    
    # Try curl with common selectors for hero content
    content=$(curl -s -L --max-time 30 \
        -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
        "$url" 2>/dev/null | grep -o '<h[1-3][^>]*>.*</h[1-3]>' | head -5)
    
    if [ -n "$content" ]; then
        echo "**Hero Headline(s):**" >> "$output"
        echo "$content" >> "$output"
        echo "" >> "$output"
    else
        echo "**Hero Headline:** Could not extract" >> "$output"
        echo "" >> "$output"
    fi
}

# Extract from du.ae
extract_hero "https://du.ae" "du (Emirates Integrated Telecom Company)"

# Extract from eand.ae
extract_hero "https://www.eand.ae" "e& (Etisalat)"

# Extract from stc.com.sa
extract_hero "https://www.stc.com.sa" "STC Group"

echo "## Analysis Summary" >> "$output"
echo "This analysis compares hero sections from top UAE IT infrastructure companies:" >> "$output"
echo "1. **du** - Established telecom provider focusing on connectivity solutions" >> "$output"
echo "2. **e&** - Recent rebranded Etisalat, offering comprehensive digital services" >> "$output"
echo "3. **STC** - Saudi Telecom Company with regional presence, focusing on ICT services" >> "$output"

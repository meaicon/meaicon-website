#!/bin/bash
# MEAICON Content Enhancement Pipeline - Safety Gate Script
# Validates enhanced content before production

set -euo pipefail

PROJECT_ROOT="/c/Users/nev3s/repos/meaicon-website"
LANGCHAIN_DIR="$PROJECT_ROOT/research-data/langchain"
BACKUP_DIR="$PROJECT_ROOT/backups"
LOG_FILE="$PROJECT_ROOT/safety-gate.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Thresholds
MIN_CHARS=1000
MAX_ISSUES=2
MIN_QUALITY=0.7

check_topic() {
    local topic=$1
    local enhanced_file="$LANGCHAIN_DIR/$topic/enhanced-content.md"
    local fact_check_file="$LANGCHAIN_DIR/$topic/fact-checks.json"
    local analysis_file="$LANGCHAIN_DIR/$topic/content-analysis.json"
    
    if [[ ! -f "$enhanced_file" ]]; then
        echo "❌ $topic: MISSING enhanced-content.md"
        return 1
    fi
    
    local char_count=$(wc -c < "$enhanced_file")
    if (( char_count < MIN_CHARS )); then
        echo "❌ $topic: TOO SHORT - $char_count chars (min $MIN_CHARS)"
        return 1
    fi
    
    local issues=0
    if [[ -f "$fact_check_file" ]]; then
        local fc_issues=$(python3 -c "import json; data=json.load(open('$fact_check_file')); print(len(data.get('issues', [])))" 2>/dev/null || echo "0")
        issues=$fc_issues
        if (( issues > MAX_ISSUES )); then
            echo "❌ $topic: TOO MANY ISSUES - $issues (max $MAX_ISSUES)"
            return 1
        fi
    fi
    
    local quality=0
    if [[ -f "$analysis_file" ]]; then
        local analysis_quality=$(python3 -c "import json; data=json.load(open('$analysis_file')); print(data.get('quality_score', 0.0))" 2>/dev/null || echo "0")
        quality=$analysis_quality
        if (( $(echo "$quality < $MIN_QUALITY" | bc -l) )); then
            echo "❌ $topic: LOW QUALITY - $quality (min $MIN_QUALITY)"
            return 1
        fi
    fi
    
    echo "✅ $topic: APPROVED - $char_count chars, $issues issues, quality: $quality"
    return 0
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

log "🔒 Starting Safety Gate Validation"

# Check all topics
approved_topics=0
rejected_topics=0
total_topics=0

for topic in connectivity data-centre cyber-security blockchain consulting general; do
    total_topics=$((total_topics + 1))
    if check_topic "$topic"; then
        approved_topics=$((approved_topics + 1))
    else
        rejected_topics=$((rejected_topics + 1))
    fi
done

log "📊 Summary: $approved_topics approved, $rejected_topics rejected out of $total_topics topics"

if [[ $rejected_topics -eq 0 ]]; then
    log "🎉 All topics approved! Proceeding with site build."
    
    # Build the site
    log "🏗️ Building website..."
    cd "$PROJECT_ROOT"
    if npm run build > "$LOG_FILE" 2>&1; then
        log "✅ Website built successfully"
        echo "✅ BUILD SUCCESS - Website ready for production"
        exit 0
    else
        log "❌ Build failed"
        echo "❌ BUILD FAILED - Please check logs in $LOG_FILE"
        exit 1
    fi
else
    log "⚠️ Some topics rejected - skipping build"
    echo "🟡 BUILD SKIPPED - $rejected_topics topics rejected"
    exit 1
fi
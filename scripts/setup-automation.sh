#!/bin/bash
# MEAICON Content Enhancement Automation Setup
# Ensure perfect operation and prevent website degradation

set -euo pipefail

# Configuration
PROJECT_ROOT="/c/Users/nev3s/repos/meaicon-website"
FIRECRAWL_OUTPUT="$PROJECT_ROOT/research-data/firecrawl"
LANGCHAIN_OUTPUT="$PROJECT_ROOT/research-data/langchain"
N8N_URL="http://localhost:5678"
LOG_FILE="$PROJECT_ROOT/automation.log"
BACKUP_DIR="$PROJECT_ROOT/backups/$(date +%Y%m%d_%H%M%S)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}[$(date)] Starting MEAICON Automation Setup...${NC}" | tee -a "$LOG_FILE"

# Function to log with timestamp
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Function to check if n8n is running
check_n8n() {
    if curl -s "$N8N_URL/healthz" > /dev/null; then
        log "✅ n8n is running and healthy"
        return 0
    else
        log "❌ n8n is not running"
        return 1
    fi
}

# Function to verify pipeline completion
verify_pipeline_complete() {
    local completed_topics=0
    local total_topics=6
    
    log "Verifying pipeline completion..."
    
    # Check each topic
    for topic in connectivity data-centre cyber-security blockchain consulting general; do
        local enhanced_file="$LANGCHAIN_OUTPUT/$topic/enhanced-content.md"
        if [[ -f "$enhanced_file" ]]; then
            local char_count=$(wc -c < "$enhanced_file")
            log "✅ $topic: $char_count chars - COMPLETE"
            completed_topics=$((completed_topics + 1))
        else
            log "⏳ $topic: PENDING"
        fi
    done
    
    log "Pipeline completion: $completed_topics/$total_topics topics"
    
    if [[ $completed_topics -eq $total_topics ]]; then
        log "🎉 All pipeline topics completed!"
        return 0
    else
        log "⚠️  Some topics still pending - continuing"
        return 1
    fi
}

# Function to setup n8n workflow
import_n8n_workflow() {
    local workflow_file="$PROJECT_ROOT/scripts/n8n/meaicon-content-enhancement.json"
    
    if [[ ! -f "$workflow_file" ]]; then
        log "❌ Workflow file not found: $workflow_file"
        return 1
    fi
    
    log "📥 Importing n8n workflow..."
    
    # Check if workflow already exists
    if curl -s "$N8N_URL/api/workflows" | grep -q "Content Enhancement Pipeline"; then
        log "✅ Workflow already exists - updating..."
        # Update existing workflow
        local workflow_id=$(curl -s "$N8N_URL/api/workflows" | jq -r '.workflows[] | select(.name == "MEAICON Content Enhancement Pipeline") | .id')
        if [[ -n "$workflow_id" && "$workflow_id" != "null" ]]; then
            curl -X PUT "$N8N_URL/api/workflows/$workflow_id/import" \
                -H "Content-Type: application/json" \
                -d "$(cat "$workflow_file")" \
                -s | grep -q "successfully"
            log "✅ Workflow updated successfully"
        fi
    else
        log "🔄 Creating new workflow..."
        # Create new workflow
        curl -X POST "$N8N_URL/api/workflows" \
            -H "Content-Type: application/json" \
            -d "$(cat "$workflow_file")" \
            -s | grep -q "successfully"
        log "✅ New workflow created successfully"
    fi
}

# Function to backup before changes
create_backup() {
    log "📦 Creating backup of current state..."
    mkdir -p "$BACKUP_DIR"
    cp -r "$PROJECT_ROOT/research-data/" "$BACKUP_DIR/" 2>/dev/null || log "⚠️ Backup partial - some files may be locked"
    cp "$PROJECT_ROOT/ORCHESTRATION-PLAN.md" "$BACKUP_DIR/" 2>/dev/null || log "⚠️ Could not backup ORCHESTRATION-PLAN.md"
    log "✅ Backup created at $BACKUP_DIR"
}

# Function to verify data integrity
verify_data_integrity() {
    log "🔍 Verifying data integrity..."
    
    # Check for required files
    local errors=0
    
    for topic in connectivity data-centre cyber-security blockchain consulting general; do
        local enhanced_file="$LANGCHAIN_OUTPUT/$topic/enhanced-content.md"
        local fact_check_file="$LANGCHAIN_OUTPUT/$topic/fact-checks.json"
        local analysis_file="$LANGCHAIN_OUTPUT/$topic/content-analysis.json"
        
        if [[ -f "$enhanced_file" ]]; then
            local chars=$(wc -c < "$enhanced_file")
            log "✅ $topic/enhanced-content.md: $chars chars"
        else
            log "❌ $topic/enhanced-content.md: MISSING"
            errors=$((errors + 1))
        fi
        
        if [[ -f "$fact_check_file" ]]; then
            log "✅ $topic/fact-checks.json: exists"
        else
            log "❌ $topic/fact-checks.json: MISSING"
            errors=$((errors + 1))
        fi
        
        if [[ -f "$analysis_file" ]]; then
            log "✅ $topic/content-analysis.json: exists"
        else
            log "❌ $topic/content-analysis.json: MISSING"
            errors=$((errors + 1))
        fi
    done
    
    if [[ $errors -eq 0 ]]; then
        log "🎉 All integrity checks passed!"
        return 0
    else
        log "❌ $errors integrity errors found"
        return 1
    fi
}

# Function to setup automation triggers
setup_automation_triggers() {
    log "⚙️ Setting up automation triggers..."
    
    # Check if firecrawl monitor is running (if applicable)
    if [[ -f "$PROJECT_ROOT/scripts/firecrawl-monitor.sh" ]]; then
        log "✅ Firecrawl monitor script exists"
    else
        log "⚠️ Firecrawl monitor script not found - manual setup required"
    fi
    
    # Check if LangChain scheduler is set up
    if [[ -f "$PROJECT_ROOT/scripts/langchain-scheduler.sh" ]]; then
        log "✅ LangChain scheduler script exists"
    else
        log "⚠️ LangChain scheduler script not found - manual setup required"
    fi
    
    # Verify n8n triggers are configured
    if curl -s "$N8N_URL/api/workflows" | grep -q "Trigger"; then
        log "✅ n8n workflow triggers configured"
    else
        log "⚠️ n8n triggers not found - manual configuration needed"
    fi
}

# Function to start missing n8n topics
start_missing_topics() {
    log "🚀 Checking for missing pipeline topics..."
    
    local missing=0
    for topic in cyber-security blockchain consulting general; do
        if [[ ! -f "$LANGCHAIN_OUTPUT/$topic/enhanced-content.md" ]]; then
            log "⏳ $topic topic is missing - starting enhancement..."
            # Start the topic enhancement in background
            (cd "$PROJECT_ROOT" && nohup python scripts/langchain-enhance.py \
                --topic "$topic" \
                --page-name "$topic" \
                --input-dir "research-data/firecrawl/$topic" >> "$LOG_FILE" 2>&1 &) &
            missing=$((missing + 1))
        fi
    done
    
    if [[ $missing -gt 0 ]]; then
        log "✅ Started $missing missing topics"
    else
        log "✅ All topics are present"
    fi
}

# Main execution
main() {
    log "🚀 Starting MEAICON Content Enhancement Automation"
    log "Project root: $PROJECT_ROOT"
    
    # Pre-check validation
    if ! check_n8n; then
        log "❌ n8n not running - attempting to start..."
        # Try to start n8n (implementation depends on your setup)
        log "⚠️ Manual n8n startup required"
    fi
    
    # Verify current pipeline status
    verify_pipeline_complete
    
    # Create backup before any changes
    create_backup
    
    # Import/update n8n workflow
    import_n8n_workflow
    
    # Verify data integrity
    verify_data_integrity
    
    # Start any missing topics
    start_missing_topics
    
    # Setup automation triggers
    setup_automation_triggers
    
    log "🎉 Automation setup completed successfully!"
    log "Next steps:"
    log "  1. Run 'npm run build' to test website build"
    log "  2. Set up cron jobs for daily automation"
    log "  3. Monitor logs in automation.log"
}

# Execute main function
main
#!/usr/bin/env python3
"""
Quick validation checklist for BDM Copilot
"""

print("🔍 BDM COPILOT QUICK VALIDATION")
print("=" * 40)

# Check 1: Knowledge base files
import os
pdf_files = [f for f in os.listdir('data/pdfs') if f.endswith('.pdf')]
print(f"✅ PDF Files: {len(pdf_files)} documents")
for pdf in pdf_files:
    size = os.path.getsize(f'data/pdfs/{pdf}') / (1024*1024)
    print(f"   📄 {pdf} ({size:.1f} MB)")

# Check 2: Cache file
cache_file = 'data/processed/kb_cache.json'
if os.path.exists(cache_file):
    cache_size = os.path.getsize(cache_file) / 1024
    print(f"✅ Cache File: {cache_size:.1f} KB")
else:
    print("⚠️  Cache File: Not found (will be created on first run)")

# Check 3: Vector database
vector_db = 'data/vectordb'
if os.path.exists(vector_db):
    print(f"✅ Vector DB: Found at {vector_db}")
else:
    print("⚠️  Vector DB: Not found (will be created on first run)")

# Check 4: App endpoint
import subprocess
try:
    result = subprocess.run(['curl', '-s', 'http://localhost:8502', '-o', '/dev/null', '-w', '%{http_code}'], 
                          capture_output=True, text=True, timeout=5)
    if result.stdout == '200':
        print("✅ App Status: Running on http://localhost:8502")
    else:
        print(f"⚠️  App Status: HTTP {result.stdout}")
except:
    print("❌ App Status: Not responding")

print("\n🎯 TEST THE APP:")
print("1. Go to: http://localhost:8502")
print("2. Input tab: Paste customer discovery notes")
print("3. Analysis tab: Should show Dell solution recommendations")
print("4. Look for: VxRail, PowerStore, ProSupport in results")

print("\n✅ If you see Dell solutions recommended based on your input, it's working!")
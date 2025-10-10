#!/usr/bin/env python3
"""
Quick web app validation for BDM Copilot
"""

import requests
import time

def test_app_endpoint():
    """Test if Streamlit app is responding"""
    try:
        response = requests.get('http://localhost:8502', timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit app is running at http://localhost:8502")
            return True
        else:
            print(f"⚠️ App responding with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ App not responding: {e}")
        return False

def check_ollama_status():
    """Check if Ollama is running and model is loaded"""
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': 'llama3.2:3b', 'prompt': 'test', 'stream': False},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Ollama LLM is ready")
            return True
        else:
            print(f"⚠️ Ollama responding with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama not responding: {e}")
        return False

if __name__ == "__main__":
    print("🔍 QUICK BDM COPILOT VALIDATION")
    print("=" * 35)
    
    app_ok = test_app_endpoint()
    llm_ok = check_ollama_status()
    
    print("\n📋 TESTING INSTRUCTIONS:")
    print("1. Visit: http://localhost:8502")
    print("2. Input tab: Paste the Northern Manufacturing prompt")
    print("3. Analysis tab: Look for Adrian's 3 pillars")
    print("4. Should see: 🟢 LLM Active (not 🟡 Fallback Mode)")
    
    if app_ok and llm_ok:
        print("\n🎉 READY FOR TESTING!")
        print("✅ App running, LLM active - test the prompt now!")
    else:
        print("\n⚠️ Fix issues above before testing")
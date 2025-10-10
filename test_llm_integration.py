#!/usr/bin/env python3
"""
Test LLM integration for BDM Copilot
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.llm_engine import bdm_llm

def test_llm_connection():
    """Test LLM connection and basic functionality"""
    print("🔍 BDM COPILOT LLM INTEGRATION TEST")
    print("=" * 40)
    
    # Test 1: Connection
    print("1. Testing Ollama connection...")
    is_connected = bdm_llm.test_connection()
    if is_connected:
        print("   ✅ Ollama service is running")
    else:
        print("   ❌ Ollama service not responding")
        print("   💡 Make sure Ollama is running: brew services start ollama")
        return False
    
    # Test 2: Simple generation
    print("\n2. Testing BDM analysis generation...")
    
    test_discovery = """
    Customer: TechFlow Manufacturing
    - 50 VMs on old VMware infrastructure
    - Storage performance issues
    - Need AI-ready platform for quality control
    - Budget: $200-300k
    - Timeline: 6 months
    """
    
    test_content = [
        {"content": "VxRail provides hyper-converged infrastructure", "source": "vxrail_datasheet"},
        {"content": "PowerStore delivers high performance storage", "source": "powerstore_overview"}
    ]
    
    try:
        analysis = bdm_llm.generate_bdm_analysis(
            discovery_notes=test_discovery,
            relevant_content=test_content,
            temperature=0.7
        )
        
        print("   ✅ LLM analysis generated successfully")
        print(f"   📊 Generated {len(analysis)} analysis sections")
        
        # Show sample output
        if analysis.get('market_analysis'):
            print(f"\n   📈 Market Analysis Preview:")
            preview = analysis['market_analysis'][:200] + "..." if len(analysis['market_analysis']) > 200 else analysis['market_analysis']
            print(f"   {preview}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ LLM analysis failed: {e}")
        return False

def test_full_integration():
    """Test full knowledge base + LLM integration"""
    print("\n3. Testing full knowledge base integration...")
    
    try:
        from engine.knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        
        if not kb.is_initialized():
            print("   ⚠️  Knowledge base not initialized - building now...")
            kb.build_knowledge_base()
        
        test_notes = """
        Mid-market customer needs hyperconverged infrastructure.
        Current VMware environment with performance issues.
        Looking for AI-ready platform with enterprise support.
        """
        
        results = kb.analyze_discovery_notes_with_llm(test_notes)
        
        if 'error' not in results:
            print("   ✅ Full integration working")
            print(f"   📚 Found {results.get('chunks_found', 0)} relevant chunks")
            print(f"   🎯 LLM Available: {results.get('llm_available', False)}")
            return True
        else:
            print(f"   ⚠️  Integration issue: {results['error']}")
            return False
            
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    success1 = test_llm_connection()
    success2 = test_full_integration() if success1 else False
    
    print("\n" + "=" * 40)
    if success1 and success2:
        print("🎉 ALL LLM TESTS PASSED!")
        print("✅ BDM Copilot ready with Adrian's methodology")
        print("🚀 Visit http://localhost:8502 to test the enhanced analysis")
    else:
        print("❌ Some tests failed - check Ollama service")
        print("🔧 Troubleshooting:")
        print("   1. brew services start ollama")
        print("   2. ollama pull llama3.2:3b")
        print("   3. ollama list (to verify model)")
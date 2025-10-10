#!/usr/bin/env python3
"""
Test script to validate BDM Copilot knowledge base functionality
"""

from engine import KnowledgeBase
import os

def test_knowledge_base():
    """Test the knowledge base with various queries"""
    
    print("🧪 Testing BDM Copilot Knowledge Base\n")
    
    # Initialize knowledge base
    try:
        pdf_dir = 'data/pdfs'
        kb = KnowledgeBase(pdf_directory=pdf_dir)
        success = kb.build_knowledge_base(use_embeddings=True)
        
        if not success:
            print("❌ Failed to build knowledge base")
            return False
            
        print("✅ Knowledge base loaded successfully")
        
    except Exception as e:
        print(f"❌ Error initializing knowledge base: {e}")
        return False
    
    # Test queries
    test_cases = [
        {
            "name": "VMware + HCI Query",
            "query": "VMware hyperconverged infrastructure virtualization",
            "expected_keywords": ["vxrail", "vmware", "hci", "hyperconverged"]
        },
        {
            "name": "AI Workloads Query", 
            "query": "artificial intelligence machine learning workloads",
            "expected_keywords": ["ai", "vxrail", "gpu", "accelerator"]
        },
        {
            "name": "Storage Solution Query",
            "query": "enterprise storage powerstore performance",
            "expected_keywords": ["powerstore", "storage", "performance"]
        },
        {
            "name": "Support Services Query",
            "query": "support services proactive monitoring",
            "expected_keywords": ["prosupport", "support", "services"]
        }
    ]
    
    print("\n🔍 Running Test Queries:\n")
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. Testing: {test_case['name']}")
        print(f"   Query: '{test_case['query']}'")
        
        try:
            results = kb.find_relevant_content(test_case['query'])
            
            if not results or 'results' not in results:
                print("   ❌ No results returned")
                all_passed = False
                continue
                
            # Check if we got relevant results
            num_results = len(results['results'])
            print(f"   📊 Found {num_results} relevant chunks")
            
            if num_results == 0:
                print("   ❌ No relevant content found")
                all_passed = False
                continue
            
            # Check for expected keywords in results
            found_keywords = []
            result_text = ""
            
            for result in results['results'][:3]:  # Check top 3 results
                result_text += result.get('text', '').lower()
                result_text += result.get('source_title', '').lower()
                result_text += result.get('source_file', '').lower()
            
            for keyword in test_case['expected_keywords']:
                if keyword.lower() in result_text:
                    found_keywords.append(keyword)
            
            # Display results
            if found_keywords:
                print(f"   ✅ Found expected keywords: {', '.join(found_keywords)}")
                
                # Show top result
                top_result = results['results'][0]
                print(f"   📄 Top result: {top_result.get('source_title', 'Unknown')}")
                print(f"   🎯 Score: {top_result.get('similarity_score', 0):.3f}")
                print(f"   📝 Preview: {top_result.get('text', '')[:100]}...")
                
            else:
                print(f"   ⚠️  Expected keywords not found: {test_case['expected_keywords']}")
                print(f"   📄 Got results from: {[r.get('source_title', 'Unknown') for r in results['results'][:2]]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            all_passed = False
        
        print()
    
    return all_passed

def test_customer_scenario():
    """Test with the sample customer scenario"""
    
    print("👥 Testing Customer Scenario Analysis\n")
    
    customer_notes = """
    Customer: TechCorp Solutions Inc.
    - 300+ VMs on VMware vSphere 6.7
    - Need hyperconverged infrastructure
    - Budget: CAD 400k-550k  
    - Toronto location (data residency)
    - Planning AI/ML workloads
    - VMware compatibility required
    """
    
    try:
        pdf_dir = 'data/pdfs'
        kb = KnowledgeBase(pdf_directory=pdf_dir)
        kb.build_knowledge_base(use_embeddings=True)
        
        results = kb.find_relevant_content(customer_notes)
        
        print(f"📊 Analysis Results:")
        print(f"   • Found {len(results['results'])} relevant content chunks")
        print(f"   • Search terms identified: {results.get('search_terms', [])}")
        print(f"   • Summary: {results.get('summary', 'N/A')}")
        
        print(f"\n🎯 Top Recommendations:")
        for i, result in enumerate(results['results'][:3], 1):
            source = result.get('source_file', 'Unknown').replace('.pdf', '')
            title = result.get('source_title', 'Unknown')
            score = result.get('similarity_score', 0)
            
            print(f"   {i}. {source}")
            print(f"      Score: {score:.3f}")
            print(f"      Content: {result.get('text', '')[:120]}...")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error in customer scenario test: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 BDM COPILOT KNOWLEDGE BASE VALIDATION")
    print("=" * 60)
    
    # Test knowledge base functionality
    kb_test_passed = test_knowledge_base()
    
    print("\n" + "=" * 60)
    
    # Test customer scenario
    scenario_test_passed = test_customer_scenario()
    
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    print(f"Knowledge Base Tests: {'✅ PASSED' if kb_test_passed else '❌ FAILED'}")
    print(f"Customer Scenario Test: {'✅ PASSED' if scenario_test_passed else '❌ FAILED'}")
    
    if kb_test_passed and scenario_test_passed:
        print("\n🎉 ALL TESTS PASSED! BDM Copilot is ready for use.")
        print("\n📱 Access your app at: http://localhost:8502")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
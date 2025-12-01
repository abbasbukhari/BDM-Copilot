"""
LLM Integration module for BDM Copilot
Implements Adrian's 3 core BDM principles through Ollama
"""

import requests
import json
import logging
from typing import Dict, List, Optional
import time

logger = logging.getLogger(__name__)

class BDMLLMEngine:
    """
    Local LLM engine implementing Adrian's BDM methodology:
    1. Market Trends & Use Cases
    2. Product Portfolio & Services Mapping  
    3. Competitive Differentiation
    """
    
    def __init__(self, model_name: str = "llama3.2:3b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        
        # Adrian's BDM Core Principles Template
        self.bdm_system_prompt = """You are an expert Dell Business Development Manager assistant following Adrian's proven methodology. 

CORE PRINCIPLE: Every response must demonstrate mastery of Adrian's 3 pillars:

1. 📈 MARKET TRENDS & USE CASES
   - Identify relevant IT market trends driving customer needs
   - Connect customer scenario to broader industry patterns  
   - Explain WHY this solution matters in current market context
   - Reference specific use cases in customer's industry/segment

2. 🧰 PRODUCT PORTFOLIO & SERVICES MAPPING
   - Recommend specific Dell products that solve identified problems
   - Include complementary Dell services (ProSupport, ProDeploy, APEX, OpenManage)
   - Explain HOW each component addresses customer requirements
   - Show complete solution architecture, not just hardware

3. ⚔️ COMPETITIVE DIFFERENTIATION  
   - Compare Dell advantages vs. specific competitors (HPE, Nutanix, Cisco)
   - Highlight unique Dell benefits (support model, integration, reliability)
   - Provide concrete business advantages (deployment speed, TCO, support quality)
   - Use differentiators relevant to customer's industry and company size

RESPONSE STRUCTURE (Always use this format):

🔍 MARKET ANALYSIS
[Current IT trends relevant to customer scenario]
[Industry use cases matching customer needs]

🎯 DELL SOLUTION ARCHITECTURE  
[Specific Dell products recommended with reasoning]
[Dell services that complete the solution]
[How solution addresses each customer requirement]

🏆 COMPETITIVE ADVANTAGE
[Specific competitor comparisons with concrete advantages]
[Unique Dell differentiators for this scenario]
[Business benefits that matter to this customer]

💼 BUSINESS IMPACT
[ROI/TCO implications]
[Risk mitigation provided]
[Strategic advantages gained]

Be specific, professional, and always tie recommendations back to customer's stated needs."""

    def test_connection(self) -> bool:
        """Test if Ollama service is running and model is available"""
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": "Test",
                    "stream": False,
                    "options": {"num_predict": 10}  # Minimal response for speed
                },
                timeout=5  # Faster timeout for connection test
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"LLM connection test failed: {e}")
            return False

    def generate_bdm_analysis(self, 
                            discovery_notes: str, 
                            relevant_content: List[Dict],
                            temperature: float = 0.7) -> Dict[str, str]:
        """
        Generate BDM analysis following Adrian's methodology
        
        Args:
            discovery_notes: Customer discovery notes
            relevant_content: Retrieved content from Dell knowledge base
            temperature: Creativity level (0.0-1.0)
            
        Returns:
            Dict with analysis sections following Adrian's structure
        """
        
        # Prepare context from relevant content
        context_summary = self._prepare_knowledge_context(relevant_content)
        
        # Build the complete prompt
        full_prompt = f"""
{self.bdm_system_prompt}

CUSTOMER DISCOVERY NOTES:
{discovery_notes}

RELEVANT DELL KNOWLEDGE BASE CONTENT:
{context_summary}

TASK: Analyze this customer scenario and provide a comprehensive BDM response following Adrian's 3-pillar methodology. Focus on specific Dell solutions that match the customer's stated needs, current market trends affecting their industry, and clear competitive advantages Dell offers for their specific situation.
"""

        try:
            # Make request to Ollama
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "top_p": 0.9,
                        "top_k": 40
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis_text = result.get('response', '')
                
                # Parse the structured response
                return self._parse_bdm_response(analysis_text)
            else:
                logger.error(f"LLM API error: {response.status_code}")
                return self._fallback_analysis(discovery_notes, relevant_content)
                
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return self._fallback_analysis(discovery_notes, relevant_content)

    def _prepare_knowledge_context(self, relevant_content: List[Dict]) -> str:
        """Prepare knowledge base content for LLM context"""
        if not relevant_content:
            return "No specific Dell documentation retrieved."
        
        context_parts = []
        for i, content in enumerate(relevant_content[:8]):  # Limit to top 8 chunks
            source = content.get('source', 'Unknown')
            text = content.get('content', '')[:500]  # Limit chunk size
            context_parts.append(f"Source {i+1} ({source}):\n{text}\n")
        
        return "\n".join(context_parts)

    def _parse_bdm_response(self, response_text: str) -> Dict[str, str]:
        """Parse LLM response into structured sections"""
        
        # Default sections based on Adrian's methodology
        sections = {
            "market_analysis": "",
            "solution_architecture": "",
            "competitive_advantage": "",
            "business_impact": ""
        }
        
        # Try to extract sections using emoji markers
        current_section = None
        lines = response_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if '🔍 MARKET ANALYSIS' in line or 'MARKET ANALYSIS' in line:
                current_section = "market_analysis"
            elif '🎯 DELL SOLUTION' in line or 'SOLUTION ARCHITECTURE' in line:
                current_section = "solution_architecture"
            elif '🏆 COMPETITIVE' in line or 'COMPETITIVE ADVANTAGE' in line:
                current_section = "competitive_advantage"
            elif '💼 BUSINESS IMPACT' in line or 'BUSINESS IMPACT' in line:
                current_section = "business_impact"
            elif current_section and line:
                sections[current_section] += line + "\n"
        
        # If parsing failed, put everything in market_analysis
        if not any(sections.values()):
            sections["market_analysis"] = response_text
        
        return sections

    def _fallback_analysis(self, discovery_notes: str, relevant_content: List[Dict]) -> Dict[str, str]:
        """Fallback analysis if LLM fails"""
        return {
            "market_analysis": "🔍 MARKET ANALYSIS\nLLM service temporarily unavailable. Based on the discovery notes, we can identify key infrastructure modernization trends affecting your industry.",
            "solution_architecture": "🎯 DELL SOLUTION ARCHITECTURE\nBased on your requirements, Dell VxRail HCI, PowerStore storage, and ProSupport services align with your needs.",
            "competitive_advantage": "🏆 COMPETITIVE ADVANTAGE\nDell's integrated approach provides single-vendor simplicity compared to multi-vendor complexity of competitors.",
            "business_impact": "💼 BUSINESS IMPACT\nDell solutions typically reduce operational overhead by 40% and provide faster time-to-value for infrastructure investments."
        }

    def generate_proposal_content(self, analysis: Dict[str, str], customer_name: str = "") -> str:
        """Generate formal proposal content"""
        
        prompt = f"""
Based on this BDM analysis, write a professional executive summary for a Dell infrastructure proposal for {customer_name or 'the customer'}.

ANALYSIS:
{analysis.get('market_analysis', '')}
{analysis.get('solution_architecture', '')}
{analysis.get('competitive_advantage', '')}
{analysis.get('business_impact', '')}

Write a 2-3 paragraph executive summary that a C-level executive would find compelling. Focus on business outcomes, not technical details.
"""

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.6}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'Proposal generation failed.')
            
        except Exception as e:
            logger.error(f"Proposal generation failed: {e}")
        
        return f"Executive Summary: Based on our analysis, Dell's infrastructure solutions address {customer_name or 'your'} key requirements while providing competitive advantages in performance, support, and total cost of ownership."

# Global instance
bdm_llm = BDMLLMEngine()
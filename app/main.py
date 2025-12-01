"""
BDM Copilot - Streamlit Application

A sales enablement tool for Dell infrastructure solutions.
Converts discovery notes into structured outputs.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io
import sys
import os
import json

# Add the parent directory to path to import our engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import KnowledgeBase

# Set page config with Dell branding
st.set_page_config(
    page_title="Dell BDM Copilot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dell branding
def load_custom_css():
    st.markdown("""
    <style>
    /* Dell Brand Colors */
    :root {
        --dell-blue: #0076CE;
        --dell-dark-blue: #005A9C;
        --dell-light-blue: #4AA9E8;
        --dell-gray: #58595B;
        --dell-light-gray: #F5F5F5;
    }
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #0076CE 0%, #005A9C 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #0076CE;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #F5F5F5 0%, #FFFFFF 100%);
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        text-align: center;
    }
    
    .metric-card h3 {
        color: #0076CE;
        font-size: 2rem;
        margin: 0;
    }
    
    .metric-card p {
        color: #58595B;
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #0076CE 0%, #005A9C 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #005A9C 0%, #004275 100%);
        box-shadow: 0 4px 8px rgba(0,118,206,0.3);
        transform: translateY(-2px);
    }
    
    /* Download button styling */
    .stDownloadButton>button {
        background-color: #0076CE;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }
    
    .stDownloadButton>button:hover {
        background-color: #005A9C;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F5F5F5;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        color: #58595B;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0076CE;
        color: white;
    }
    
    /* Text input styling */
    .stTextInput>div>div>input {
        border-radius: 6px;
        border: 2px solid #E0E0E0;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #0076CE;
        box-shadow: 0 0 0 2px rgba(0,118,206,0.1);
    }
    
    /* Text area styling */
    .stTextArea>div>div>textarea {
        border-radius: 6px;
        border: 2px solid #E0E0E0;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #0076CE;
        box-shadow: 0 0 0 2px rgba(0,118,206,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #F5F5F5;
    }
    
    /* Status indicators */
    .status-success {
        background-color: #28A745;
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-warning {
        background-color: #FFC107;
        color: #333;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Section headers */
    .section-header {
        color: #0076CE;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #0076CE;
    }
    
    /* Dataframe styling */
    .dataframe {
        border: 1px solid #E0E0E0 !important;
        border-radius: 8px;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #0076CE;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize knowledge base
# Cache knowledge base initialization for performance
@st.cache_resource
def get_knowledge_base():
    """Load knowledge base once and cache it"""
    # Initialize with PDFs directory
    pdf_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'pdfs')
    kb = KnowledgeBase(pdf_directory=pdf_dir)
    
    # Build knowledge base with embeddings
    success = kb.build_knowledge_base(use_embeddings=True)
    if not success:
        raise Exception("Failed to build knowledge base from PDFs")
    
    return kb

# Load knowledge base (cached for performance)
try:
    knowledge_base = get_knowledge_base()
except Exception as e:
    st.error(f"❌ Error loading knowledge base: {e}")
    knowledge_base = None

def initialize_session_state():
    """Initialize session state variables"""
    if 'discovery_notes' not in st.session_state:
        st.session_state['discovery_notes'] = ""
    if 'customer_name' not in st.session_state:
        st.session_state['customer_name'] = ""
    if 'opportunity_value' not in st.session_state:
        st.session_state['opportunity_value'] = ""
    if 'timeline' not in st.session_state:
        st.session_state['timeline'] = ""
    if 'analysis_complete' not in st.session_state:
        st.session_state['analysis_complete'] = False

def main():
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Dell-branded header
    st.markdown("""
    <div class="main-header">
        <h1>💼 Dell BDM Copilot</h1>
        <p>AI-Powered Sales Assistant for Infrastructure Solutions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with Dell styling
    with st.sidebar:
        st.markdown("### 🎯 About BDM Copilot")
        st.markdown("""
        <div class="info-card">
        <strong>Transform discovery notes into:</strong><br><br>
        ✓ Market-aligned analysis<br>
        ✓ 3 solution options<br>
        ✓ Detailed BOM (CSV)<br>
        ✓ Ready-to-send emails<br><br>
        <strong>Powered by:</strong><br>
        • Local AI (Llama 3.2 3B)<br>
        • Dell Knowledge Base<br>
        • Adrian's 3-Pillar Method
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # System Status
        st.markdown("### 📊 System Status")
        
        # Check LLM status
        llm_status = "🟢 Active" if knowledge_base else "🟡 Loading"
        kb_status = "🟢 Ready" if knowledge_base else "🟡 Building"
        
        st.markdown(f"""
        <div class="metric-card">
            <p><strong>LLM Engine:</strong> {llm_status}</p>
            <p><strong>Knowledge Base:</strong> {kb_status}</p>
            <p><strong>Documents:</strong> 5 PDFs</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.caption("v0.1.0 • Dell Technologies")
    
    # Main content tabs with professional icons
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Input & Discovery", 
        "📊 Analysis & Insights", 
        "💼 Solutions & BOM", 
        "📧 Communications"
    ])
    
    with tab1:
        input_section()
    
    with tab2:
        analysis_section()
    
    with tab3:
        outputs_section()
    
    with tab4:
        communications_section()

def input_section():
    """Discovery notes input section - Dell branded"""
    st.markdown('<p class="section-header">📝 Customer Discovery & Input</p>', unsafe_allow_html=True)
    
    # Customer Information Row
    col1, col2 = st.columns([2, 1])
    
    with col1:
        customer_name = st.text_input(
            "Customer Name *",
            value=st.session_state.get('customer_name', ''),
            placeholder="e.g., Acme Healthcare Systems",
            help="Enter the customer or prospect name"
        )
        if customer_name:
            st.session_state['customer_name'] = customer_name
    
    with col2:
        col2a, col2b = st.columns(2)
        with col2a:
            opportunity_value = st.text_input(
                "Opportunity Value",
                value=st.session_state.get('opportunity_value', ''),
                placeholder="e.g., $800K"
            )
            if opportunity_value:
                st.session_state['opportunity_value'] = opportunity_value
        
        with col2b:
            timeline = st.text_input(
                "Timeline",
                value=st.session_state.get('timeline', ''),
                placeholder="e.g., Q2 2026"
            )
            if timeline:
                st.session_state['timeline'] = timeline
    
    st.markdown("---")
    
    # Discovery Notes Section
    st.markdown("### 📋 Discovery Notes")
    st.markdown("*Paste your customer discovery notes, requirements, pain points, and objectives below:*")
    
    discovery_notes = st.text_area(
        "",
        value=st.session_state.get('discovery_notes', ''),
        height=350,
        placeholder="""Example discovery notes:

Customer: Midwest Regional Hospital
Industry: Healthcare
Contact: Sarah Chen, Director of IT Infrastructure

Current Environment:
- 5 ESXi hosts (aging Dell servers, 4+ years old)
- Traditional SAN storage with 60TB usable capacity
- Running at 82% capacity

Pain Points:
- Running out of storage space
- Backup windows exceeding 8 hours
- No disaster recovery plan in place
- Database latency during peak hours

Growth Plans:
- Adding 2 new clinics next year
- Expecting 40% annual data growth (medical imaging)

Requirements:
- HIPAA compliance (encryption at rest/transit)
- 99.9% uptime SLA
- RPO under 1 hour, RTO under 4 hours
- Limited IT staff (3 people)
- Only 6U rack space available

Budget: $800K approved + $300K available with strong ROI case
Timeline: Must complete before Q2 2026
Preferences: Strong Dell relationship, existing ProSupport contracts

AI/Future Needs: Interested in predictive analytics, exploring AI diagnostics within 18 months"""
    )
    
    # Store in session state
    if discovery_notes:
        st.session_state['discovery_notes'] = discovery_notes
    
    st.markdown("---")
    
    # Analyze Button - Prominent Dell-styled
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_clicked = st.button(
            "🔍 Analyze Discovery Notes",
            type="primary",
            use_container_width=True,
            help="Generate AI-powered analysis using Dell knowledge base and Adrian's methodology"
        )
    
    if analyze_clicked:
        if not discovery_notes or not customer_name:
            st.error("⚠️ Please enter both customer name and discovery notes before analyzing.")
        else:
            st.session_state['analysis_complete'] = True
            st.success(f"✅ Analysis initiated for **{customer_name}**!")
            st.info("👉 Navigate to the **Analysis & Insights** tab to view results.")
    
    # Quick tips
    with st.expander("💡 Tips for Better Analysis"):
        st.markdown("""
        **Include these details for best results:**
        - Current infrastructure and pain points
        - Business objectives and growth plans
        - Budget and timeline constraints
        - Compliance or regulatory requirements
        - Technical preferences (VMware, cloud-ready, etc.)
        - Future technology needs (AI, analytics, etc.)
        
        **The more context you provide, the better the AI-generated recommendations!**
        """)

def analysis_section():
    """Analysis and summary section - Dell branded with Adrian's 3 pillars"""
    st.markdown('<p class="section-header">� Market Analysis & Insights</p>', unsafe_allow_html=True)
    
    if 'discovery_notes' not in st.session_state or not st.session_state.discovery_notes:
        st.markdown("""
        <div class="info-card">
            <h3>👈 Get Started</h3>
            <p>Please enter discovery notes in the <strong>Input & Discovery</strong> tab first, then click the <strong>Analyze</strong> button.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    discovery_notes = st.session_state.discovery_notes
    customer_name = st.session_state.get('customer_name', 'Customer')
    
    if knowledge_base is None:
        st.error("⚠️ Knowledge base not available. Please restart the application.")
        return
    
    # Header with customer context
    st.markdown(f"### Analyzing: **{customer_name}**")
    
    # **LLM-Powered BDM Analysis using Adrian's methodology**
    with st.spinner("🧠 Analyzing with AI and Dell knowledge base..."):
        try:
            # Get comprehensive BDM analysis using LLM
            analysis_results = knowledge_base.analyze_discovery_notes_with_llm(discovery_notes)
            
            # Store in session state for reuse across tabs
            st.session_state['analysis_results'] = analysis_results
            st.session_state['llm_analysis'] = analysis_results.get('llm_analysis', {})
            st.session_state['llm_available'] = analysis_results.get('llm_available', False)
            
            if 'error' in analysis_results:
                st.warning(f"⚠️ {analysis_results['error']}")
                llm_analysis = analysis_results.get('llm_analysis', {})
            else:
                llm_analysis = analysis_results.get('llm_analysis', {})
            
            # Display LLM availability status
            llm_status = analysis_results.get('llm_available', False)
            if llm_status:
                st.markdown('<span class="status-success">🟢 AI Analysis Active</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-warning">🟡 Fallback Mode</span>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # **Adrian's 3-Pillar Analysis Display** with professional cards
            
            # 1. Market Analysis & Use Cases
            if llm_analysis.get('market_analysis'):
                st.markdown("#### 📈 Market Trends & Use Cases")
                st.markdown(f"""
                <div class="info-card">
                    {llm_analysis['market_analysis']}
                </div>
                """, unsafe_allow_html=True)
            
            # 2. Dell Solution Architecture  
            if llm_analysis.get('solution_architecture'):
                st.markdown("#### 🎯 Dell Solution Architecture")
                st.markdown(f"""
                <div class="info-card">
                    {llm_analysis['solution_architecture']}
                </div>
                """, unsafe_allow_html=True)
            
            # 3. Competitive Advantage
            if llm_analysis.get('competitive_advantage'):
                st.markdown("#### 🏆 Competitive Differentiation")
                st.markdown(f"""
                <div class="info-card">
                    {llm_analysis['competitive_advantage']}
                </div>
                """, unsafe_allow_html=True)
            
            # 4. Business Impact
            if llm_analysis.get('business_impact'):
                st.markdown("#### 💼 Business Impact & ROI")
                st.markdown(f"""
                <div class="info-card">
                    {llm_analysis['business_impact']}
                </div>
                """, unsafe_allow_html=True)
            
            # Knowledge Base Statistics - Professional metrics display
            chunks_found = analysis_results.get('chunks_found', 0)
            sources_used = analysis_results.get('sources_used', 0)
            search_terms = analysis_results.get('search_terms', [])
            
            st.markdown("---")
            st.markdown("#### 📊 Analysis Metrics")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{chunks_found}</h3>
                    <p>Knowledge Chunks</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{sources_used}</h3>
                    <p>Dell Documents</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{len(search_terms)}</h3>
                    <p>Search Terms</p>
                </div>
                """, unsafe_allow_html=True)
            
            if search_terms:
                st.caption(f"**🔍 Key terms identified:** {', '.join(search_terms[:10])}")
            
            # Next steps call-to-action
            st.markdown("---")
            st.info("✅ **Analysis Complete!** → Navigate to **Solutions & BOM** tab to view tailored Dell recommendations.")
                
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            st.info("💡 **Troubleshooting:** Ensure the local AI model (Ollama) is running. Try restarting the app if the issue persists.")
            
            # Fallback to basic analysis
            with st.expander("🔧 Basic Keyword Analysis (Fallback)"):
                key_phrases = discovery_notes.lower()
                if any(word in key_phrases for word in ['vmware', 'virtualization', 'vcenter']):
                    st.markdown("- 💻 **VMware environment** detected")
                if any(word in key_phrases for word in ['ai', 'ml', 'machine learning', 'analytics']):
                    st.markdown("- 🤖 **AI/ML workload** requirements")
                if any(word in key_phrases for word in ['storage', 'capacity', 'performance', 'iops']):
                    st.markdown("- 📊 **Storage performance** needs")
                if any(word in key_phrases for word in ['backup', 'dr', 'disaster recovery', 'rpo', 'rto']):
                    st.markdown("- 🔄 **Backup/DR** requirements")
                if any(word in key_phrases for word in ['compliance', 'hipaa', 'gdpr', 'sox']):
                    st.markdown("- 🔒 **Compliance** considerations")

def outputs_section():
    """Solution options and BOM section - Dell branded"""
    st.markdown('<p class="section-header">💼 Solutions & Bill of Materials</p>', unsafe_allow_html=True)
    
    if 'discovery_notes' not in st.session_state:
        st.info("👈 Please enter discovery notes in the Input tab first.")
        return
    
    # Check if we have LLM analysis results
    discovery_notes = st.session_state.discovery_notes
    customer_name = st.session_state.get('customer_name', 'the customer')
    
    if knowledge_base is None:
        st.error("Knowledge base not available. Using fallback templates.")
        return
    
    # Get LLM analysis from session state (already computed in Analysis tab)
    llm_analysis = st.session_state.get('llm_analysis', {})
    llm_available = st.session_state.get('llm_available', False)
    
    # If analysis not yet run, show message
    if not llm_analysis and not st.session_state.get('analysis_complete', False):
        st.info("💡 Please run the analysis in the 'Market Analysis & Insights' tab first.")
        llm_available = False
    
    # Display LLM status
    status_color = "🟢" if llm_available else "🟡"
    status_text = "Dynamic Solutions" if llm_available else "Template Mode"
    st.caption(f"{status_color} {status_text}")
    
    # **Enhanced Solution Options using LLM Analysis**
    st.markdown("### 🎯 Recommended Solution Architecture")
    
    if llm_analysis.get('solution_architecture'):
        # Display LLM-generated solution architecture
        st.markdown(llm_analysis['solution_architecture'])
        
        # Generate specific solution options from LLM using direct API call
        if llm_available:
            with st.spinner("🎯 Generating specific solution options..."):
                try:
                    import requests
                    
                    solution_prompt = f"""You are a Dell Technologies sales engineer. Create 3 solution options for {customer_name} using ONLY Dell products.

CRITICAL RULES:
- Use ONLY Dell products (PowerStore, PowerScale, VxRail, PowerEdge, PowerProtect, APEX, ProSupport)
- NO HP, Cisco, NetApp, or non-Dell vendors
- Each option must have a descriptive, specific title based on the customer's industry/needs
- Follow the EXACT format shown below

Customer Industry/Context: {discovery_notes[:400]}

Key Dell Products Available:
• Storage: PowerStore (block/file), PowerScale (NAS), PowerFlex (software-defined)
• Hyperconverged: VxRail E-Series, P-Series, D-Series
• Servers: PowerEdge R650, R750, R940
• Data Protection: PowerProtect DD, PowerProtect Cyber Recovery
• Services: ProSupport Plus, ProDeploy Plus, APEX (subscription)

EXAMPLE FORMAT (follow this exactly):

**Option 1: VxRail All-Flash HCI Platform**
- **Fit:** Provides integrated compute and storage for {customer_name}'s VMware environment with simplified management for small IT team
- **Components:** VxRail E560F (4 nodes), PowerProtect DD3300, ProSupport Plus
- **Investment:** $750K - $950K

**Option 2: PowerScale + PowerEdge Hybrid Infrastructure**
- **Fit:** Scales storage independently for {customer_name}'s large file workloads while keeping compute flexible
- **Components:** PowerScale F600 (3-node cluster), PowerEdge R750 servers (6), PowerProtect DD6900, ProDeploy Plus
- **Investment:** $850K - $1.1M

**Option 3: APEX Storage as a Service**
- **Fit:** OpEx model with consumption-based pricing, ideal for {customer_name}'s budget flexibility and growth uncertainty
- **Components:** APEX Block Storage (100TB committed), APEX Data Protection, ProSupport Plus
- **Investment:** $25K/month ($300K annually)

NOW create 3 options for {customer_name} following this EXACT format:"""
                    
                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": "llama3.2:3b",
                            "prompt": solution_prompt,
                            "stream": False,
                            "options": {
                                "temperature": 0.3,
                                "num_predict": 400
                            }
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        solution_options = response.json().get('response', '').strip()
                        
                        if solution_options and len(solution_options) > 100:
                            st.markdown("---")
                            st.markdown("### 📋 Solution Options")
                            st.markdown(solution_options)
                        else:
                            _display_static_solution_options()
                    else:
                        _display_static_solution_options()
                        
                except Exception as e:
                    st.caption(f"⚠️ Dynamic generation issue, using templates")
                    _display_static_solution_options()
        else:
            _display_static_solution_options()
    else:
        _display_static_solution_options()

def _display_static_solution_options():
    """Fallback static solution options"""
    option1, option2, option3 = st.columns(3)
    
    with option1:
        st.markdown("""
        #### 🏆 Option 1: VxRail HCI
        **Fit:** Perfect VMware alignment  
        **Pros:** Integrated lifecycle, simple mgmt  
        **Risks:** Higher initial cost  
        **Source:** VxRail Overview, p.3
        """)
    
    with option2:
        st.markdown("""
        #### ⚡ Option 2: PowerFlex + Compute
        **Fit:** High performance, scalable  
        **Pros:** Better $/TB, flexible scaling  
        **Risks:** More complex management  
        **Source:** PowerFlex Datasheet, p.5
        """)
    
    with option3:
        st.markdown("""
        #### 💰 Option 3: PowerStore + vSAN
        **Fit:** Hybrid approach  
        **Pros:** Lower entry cost  
        **Risks:** Split management domains  
        **Source:** PowerStore Guide, p.8
        """)

def _generate_dynamic_bom(discovery_notes: str, llm_analysis: dict):
    """Generate dynamic BOM based on LLM analysis"""
    
    # Extract key requirements for BOM generation
    notes_lower = discovery_notes.lower()
    
    # Determine scale
    vm_count = 50  # Default
    if 'vm' in notes_lower or 'virtual machine' in notes_lower:
        import re
        vm_matches = re.findall(r'(\d+)\s*vm', notes_lower)
        if vm_matches:
            vm_count = int(vm_matches[0])
    
    # Determine node count based on VMs (rule of thumb: 10-15 VMs per node)
    node_count = max(3, min(8, (vm_count // 12) + 1))
    
    # Determine storage based on requirements
    storage_tb = 15  # Default per node
    if any(word in notes_lower for word in ['ai', 'analytics', 'data']):
        storage_tb = 25  # More storage for data-intensive workloads
    
    # Generate BOM based on analysis
    if 'vxrail' in llm_analysis.get('solution_architecture', '').lower():
        return _generate_vxrail_bom(node_count, storage_tb)
    elif 'powerstore' in llm_analysis.get('solution_architecture', '').lower():
        return _generate_powerstore_bom(node_count, storage_tb)
    else:
        return _generate_default_bom(node_count, storage_tb)

def _generate_vxrail_bom(node_count: int, storage_tb: int):
    """Generate VxRail-based BOM"""
    bom_data = {
        'Role': [
            f'VxRail E560F Node ({node_count}x)',
            'VxRail Manager',
            'Top-of-Rack Switch (2x)',
            'Backup Appliance',
            'ProSupport Services'
        ],
        'Quantity': [node_count, 1, 2, 1, 1],
        'CPU': [
            'Intel Xeon Silver 4314',
            'Embedded',
            '',
            'Intel Xeon',
            ''
        ],
        'RAM (GB)': [256, '', '', 64, ''],
        'Storage': [
            f'{storage_tb}TB NVMe',
            '1TB SSD',
            '',
            '96TB Dedup',
            ''
        ],
        'Network': [
            '25GbE',
            '10GbE',
            '100GbE',
            '10GbE',
            ''
        ],
        'License': [
            'VMware vSAN Enterprise',
            'VxRail Manager',
            '',
            'DD OS',
            ''
        ],
        'Services': [
            'ProSupport Plus 3yr',
            'ProSupport Plus 3yr',
            'ProSupport 3yr',
            'ProSupport Plus 3yr',
            '24x7 Support'
        ],
        'Notes': [
            'Hyper-converged infrastructure',
            'Centralized lifecycle management',
            'Redundant switching fabric',
            'Integrated backup solution',
            'Mission-critical support'
        ]
    }
    return bom_data

def _generate_powerstore_bom(node_count: int, storage_tb: int):
    """Generate PowerStore-based BOM"""
    bom_data = {
        'Role': [
            f'PowerEdge R750 ({node_count}x)',
            'PowerStore 1000T',
            'PowerSwitch S5248F (2x)',
            'Management Server',
            'ProSupport Services'
        ],
        'Quantity': [node_count, 1, 2, 1, 1],
        'CPU': [
            'Intel Xeon Gold 6338',
            'Embedded Controller',
            '',
            'Intel Xeon Silver',
            ''
        ],
        'RAM (GB)': [512, '', '', 128, ''],
        'Storage': [
            '1TB NVMe Boot',
            f'{storage_tb * node_count}TB NVMe',
            '',
            '2TB SSD',
            ''
        ],
        'Network': [
            '25GbE',
            '32Gb FC',
            '100GbE',
            '10GbE',
            ''
        ],
        'License': [
            'VMware vSphere Ent+',
            'PowerStore OS',
            '',
            'VMware vCenter',
            ''
        ],
        'Services': [
            'ProSupport Plus 3yr',
            'ProSupport Mission Critical',
            'ProSupport 3yr',
            'ProSupport Plus 3yr',
            '24x7 Support'
        ],
        'Notes': [
            'Compute cluster nodes',
            'All-flash storage array',
            'High-performance switching',
            'Infrastructure management',
            'Enterprise-grade support'
        ]
    }
    return bom_data

def _generate_default_bom(node_count: int, storage_tb: int):
    """Generate default BOM when solution type unclear"""
    bom_data = {
        'Role': [
            f'PowerEdge R750 ({node_count}x)',
            'Storage System',
            'Network Switches (2x)',
            'Management/Backup'
        ],
        'Quantity': [node_count, 1, 2, 1],
        'CPU': ['Intel Xeon Gold', 'Embedded', '', 'Intel Xeon'],
        'RAM (GB)': [384, '', '', 128],
        'Storage': [
            '2TB NVMe',
            f'{storage_tb * node_count}TB',
            '',
            '10TB'
        ],
        'Network': ['25GbE', '25GbE', '100GbE', '10GbE'],
        'License': ['VMware', 'Storage OS', '', 'Management'],
        'Services': ['ProSupport Plus', 'ProSupport', 'ProSupport', 'ProSupport'],
        'Notes': [
            'Compute infrastructure',
            'Primary storage',
            'Network fabric',
            'Management & backup'
        ]
    }
    return bom_data

    # **Enhanced BOM Section using Dynamic Generation**
    st.markdown("### 💼 Draft Bill of Materials")
    
    if llm_analysis:
        # Generate dynamic BOM based on LLM analysis
        bom_data = _generate_dynamic_bom(discovery_notes, llm_analysis)
    else:
        # Fallback to default BOM
        bom_data = _generate_default_bom(4, 15)
    
    df = pd.DataFrame(bom_data)
    st.dataframe(df, use_container_width=True)
    
    # Export BOM
    if st.button("📥 Download BOM as CSV"):
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name=f"bom_draft_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

def communications_section():
    """Email templates section - Dell branded"""
    st.markdown('<p class="section-header">📧 Professional Communications</p>', unsafe_allow_html=True)
    
    if 'discovery_notes' not in st.session_state or not st.session_state.discovery_notes:
        st.markdown("""
        <div class="info-card">
            <h3>👈 Get Started</h3>
            <p>Please complete the analysis in the <strong>Analysis & Insights</strong> tab first to generate personalized communications.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Get customer info and LLM analysis from session state
    discovery_notes = st.session_state.discovery_notes
    customer_name = st.session_state.get('customer_name', '[Customer Name]')
    llm_analysis = st.session_state.get('llm_analysis', {})
    llm_available = st.session_state.get('llm_available', False)
    
    # If analysis not yet run, show message
    if not llm_analysis and not st.session_state.get('analysis_complete', False):
        st.info("💡 Please run the analysis in the 'Market Analysis & Insights' tab first.")
        llm_available = False
    
    # Display LLM status for communications
    status_color = "🟢" if llm_available else "🟡"
    status_text = "Personalized Content" if llm_available else "Template Mode"
    st.caption(f"{status_color} {status_text}")
    
    email1, email2, email3 = st.columns(3)
    
    with email1:
        st.markdown("### 📧 Customer Recap")
        
        if llm_available and llm_analysis:
            # Generate dynamic customer recap email using direct LLM call
            try:
                from engine.llm_engine import bdm_llm
                import requests
                
                recap_prompt = f"""Write a professional customer follow-up email after a discovery meeting with {customer_name}.

Format the email with these sections:
- Subject line (start with "Subject: ")
- Greeting
- Brief thank you for the meeting
- Summary of 2-3 key requirements/challenges discussed
- Recommended Dell solutions (mention specific products like VxRail, PowerStore, or ProSupport)
- Next steps (schedule technical deep-dive, share architecture proposal)
- Closing

Keep it concise (under 300 words), professional, and action-oriented.

CUSTOMER DISCOVERY NOTES:
{discovery_notes[:400]}

DELL SOLUTION RECOMMENDATIONS:
{llm_analysis.get('solution_architecture', 'VxRail HCI and ProSupport services')[:300]}

Write the complete email now:"""
                
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama3.2:3b",
                        "prompt": recap_prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,
                            "num_predict": 350
                        }
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    recap_email = response.json().get('response', '').strip()
                    
                    # Ensure it has a subject line
                    if not recap_email.startswith('Subject:') and 'Subject:' not in recap_email[:100]:
                        recap_email = f"Subject: Follow-up: {customer_name} Infrastructure Discussion\n\n{recap_email}"
                else:
                    recap_email = _generate_fallback_recap_email(customer_name, discovery_notes)
                    
            except Exception as e:
                st.caption(f"⚠️ LLM generation issue, using template")
                recap_email = _generate_fallback_recap_email(customer_name, discovery_notes)
        else:
            recap_email = _generate_fallback_recap_email(customer_name, discovery_notes)
        
        st.text_area("", value=recap_email, height=400, key="recap")
        
        # Download options: .eml (Outlook) and Salesforce JSON
        eml_recap = f"Subject: {recap_email.splitlines()[0].replace('**Subject:** ', '')}\n\n" + "\n".join(recap_email.splitlines()[2:])
        sf_recap = {
            "subject": recap_email.splitlines()[0].replace('**Subject:** ', ''),
            "body": recap_email,
            "to": "[Customer Contact]",
            "related_to": customer_name
        }

        st.download_button(
            label="⬇️ Download Recap (.eml)",
            data=eml_recap,
            file_name=f"recap_{customer_name.replace(' ', '_')}.eml",
            mime="message/rfc822",
            key="download_recap_eml"
        )

        st.download_button(
            label="⬇️ Download Recap (Salesforce JSON)",
            data=json.dumps(sf_recap, indent=2),
            file_name=f"recap_{customer_name.replace(' ', '_')}_sf.json",
            mime="application/json",
            key="download_recap_json"
        )

        if st.button("📋 Copy Recap Email", key="copy_recap"):
            st.success("Email content ready to copy!")
    
    with email2:
        st.markdown("### 🤝 Partner Request")
        
        # Generate dynamic partner email based on recommended solutions
        if llm_analysis.get('solution_architecture'):
            solutions_text = llm_analysis['solution_architecture']
            
            # Extract Dell products mentioned
            dell_products = []
            if 'vxrail' in solutions_text.lower():
                dell_products.append("VxRail nodes")
            if 'powerstore' in solutions_text.lower():
                dell_products.append("PowerStore arrays")
            if 'powerswitch' in solutions_text.lower() or 'switch' in solutions_text.lower():
                dell_products.append("PowerSwitch networking")
            if 'poweredge' in solutions_text.lower():
                dell_products.append("PowerEdge servers")
            
            products_list = ", ".join(dell_products) if dell_products else "Dell infrastructure components"
        else:
            # Fallback based on discovery notes
            notes_lower = discovery_notes.lower()
            if any(word in notes_lower for word in ['startup', 'small', 'budget']):
                products_list = "PowerEdge T-series, basic networking"
            else:
                products_list = "VxRail nodes, switches"
        
        partner_email = f"""**Subject:** Lead-time check — {customer_name} Dell Infrastructure Opportunity

Hi [Partner Rep],

We're scoping Dell infrastructure for {customer_name}. Could you confirm current promos, bundle SKUs, and lead times for:

- {products_list}
- VMware licensing bundles (if applicable)
- ProSupport services

Goal: Optimize margin and timeline for this opportunity. Draft BOM will be shared separately.

Customer timeline: {st.session_state.get('timeline', '90 days')}
Opportunity value: {st.session_state.get('opportunity_value', 'TBD')}

Thanks,
[Your Name]
        """
        st.text_area("", value=partner_email, height=400, key="partner")
        
        # Partner email download options
        eml_partner = f"Subject: {partner_email.splitlines()[0].replace('**Subject:** ', '')}\n\n" + "\n".join(partner_email.splitlines()[2:])
        sf_partner = {
            "subject": partner_email.splitlines()[0].replace('**Subject:** ', ''),
            "body": partner_email,
            "to": "[Partner Rep]",
            "related_to": customer_name
        }

        st.download_button(
            label="⬇️ Download Partner Email (.eml)",
            data=eml_partner,
            file_name=f"partner_{customer_name.replace(' ', '_')}.eml",
            mime="message/rfc822",
            key="download_partner_eml"
        )

        st.download_button(
            label="⬇️ Download Partner (Salesforce JSON)",
            data=json.dumps(sf_partner, indent=2),
            file_name=f"partner_{customer_name.replace(' ', '_')}_sf.json",
            mime="application/json",
            key="download_partner_json"
        )

        if st.button("📋 Copy Partner Email", key="copy_partner"):
            st.success("Partner email ready to copy!")
    
    with email3:
        st.markdown("### 📊 Executive Summary")
        
        if llm_available and llm_analysis:
            # Generate executive summary email using direct LLM call
            try:
                import requests
                
                exec_prompt = f"""Write a professional executive summary email FROM a Dell BDM TO the executive leadership team at {customer_name}.

This email is being sent BY the Dell sales representative TO the customer's C-level executives (CEO, CFO, CIO) to present a business case for Dell infrastructure modernization.

Format the email with these sections:
- Subject line (start with "Subject: ")
- Greeting to executive team ("Dear {customer_name} Executive Team," or similar)
- 2-3 sentence business context (what challenges they face)
- Strategic benefits Dell solutions provide (business outcomes, not technical specs)
- Investment overview (mention budget of $800K-$1.1M range)
- Risk mitigation and competitive advantages
- Call to action / next steps (propose meeting, technical review)
- Professional closing from Dell representative

Key points to include:
- This is FROM Dell TO the customer (not from their IT director)
- Focus on business outcomes: uptime, efficiency, growth enablement, risk reduction
- Mention specific challenges: storage capacity, backup windows, HIPAA compliance, small IT team
- Highlight Dell differentiators: single vendor simplicity, ProSupport, proven healthcare track record
- Keep executive-level (avoid technical jargon)
- Under 300 words total

CUSTOMER BUSINESS CONTEXT:
{discovery_notes[:500]}

BUSINESS IMPACT ANALYSIS:
{llm_analysis.get('business_impact', 'Dell infrastructure modernization will reduce operational complexity, improve uptime, and enable future growth')[:400]}

COMPETITIVE ADVANTAGES:
{llm_analysis.get('competitive_advantage', 'Dell provides superior integration, support, and total cost of ownership')[:300]}

Write the complete executive summary email FROM Dell TO {customer_name} executives now:"""
                
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama3.2:3b",
                        "prompt": exec_prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,
                            "num_predict": 350
                        }
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    exec_email = response.json().get('response', '').strip()
                    
                    # Ensure it has a subject line
                    if not exec_email.startswith('Subject:') and 'Subject:' not in exec_email[:100]:
                        exec_email = f"Subject: {customer_name} Infrastructure Modernization - Executive Summary\n\n{exec_email}"
                else:
                    exec_email = _generate_fallback_exec_email(customer_name, discovery_notes)
                    
            except Exception as e:
                st.caption(f"⚠️ LLM generation issue, using template")
                exec_email = _generate_fallback_exec_email(customer_name, discovery_notes)
        else:
            exec_email = _generate_fallback_exec_email(customer_name, discovery_notes)
        
        st.text_area("", value=exec_email, height=400, key="executive")
        
        # Executive email download options
        eml_exec = f"Subject: {exec_email.splitlines()[0].replace('**Subject:** ', '')}\n\n" + "\n".join(exec_email.splitlines()[2:])
        sf_exec = {
            "subject": exec_email.splitlines()[0].replace('**Subject:** ', ''),
            "body": exec_email,
            "to": "[Executive Team]",
            "related_to": customer_name
        }

        st.download_button(
            label="⬇️ Download Executive (.eml)",
            data=eml_exec,
            file_name=f"exec_{customer_name.replace(' ', '_')}.eml",
            mime="message/rfc822",
            key="download_exec_eml"
        )

        st.download_button(
            label="⬇️ Download Executive (Salesforce JSON)",
            data=json.dumps(sf_exec, indent=2),
            file_name=f"exec_{customer_name.replace(' ', '_')}_sf.json",
            mime="application/json",
            key="download_exec_json"
        )

        if st.button("📋 Copy Executive Email", key="copy_exec"):
            st.success("Executive summary ready to copy!")

def _generate_fallback_recap_email(customer_name: str, discovery_notes: str) -> str:
    """Fallback customer recap email with some intelligence"""
    
    # Extract some key points from discovery notes
    notes_lower = discovery_notes.lower()
    
    # Detect budget
    budget_context = ""
    if any(word in notes_lower for word in ['$', 'budget', 'cost']):
        budget_context = "- Budget considerations discussed"
    
    # Detect technology preferences
    tech_context = ""
    if 'vmware' in notes_lower:
        tech_context = "- VMware environment modernization"
    elif any(word in notes_lower for word in ['startup', 'small']):
        tech_context = "- Small business infrastructure needs"
    
    # Detect timeline
    timeline_context = ""
    if any(word in notes_lower for word in ['week', 'month', 'urgent', 'quick']):
        timeline_context = "- Accelerated timeline requirements"
    
    return f"""**Subject:** {customer_name} Infrastructure Discussion - Next Steps

Hi [Customer Contact],

Thank you for the productive discussion about {customer_name}'s infrastructure modernization plans.

**Key Requirements Understood:**
{budget_context}
{tech_context}
{timeline_context}
- Performance and scalability improvements needed
- Future-ready platform for emerging technologies

**Dell Solutions Recommended:**
1) VxRail HCI — Integrated VMware platform with lifecycle automation
2) PowerStore — High-performance all-flash storage  
3) ProSupport — Enterprise-grade support services

**Next Steps:**
- Technical deep-dive session (next week)
- Draft solution architecture review
- Reference customer introductions

**Open Questions:** Specific compliance requirements, backup strategy preferences

Best regards,
[Your Name]"""

def _generate_fallback_exec_email(customer_name: str, discovery_notes: str) -> str:
    """Fallback executive summary email with context awareness"""
    
    notes_lower = discovery_notes.lower()
    
    # Adapt messaging based on company type
    if 'startup' in notes_lower:
        context = "startup growth and investor confidence"
        investment_msg = "Scalable infrastructure that grows with your business"
    elif any(word in notes_lower for word in ['manufacturing', 'automotive']):
        context = "operational efficiency and competitive advantage"
        investment_msg = "Reduced downtime and improved production capabilities"
    else:
        context = "business transformation and competitive positioning"
        investment_msg = "Improved operational efficiency and future readiness"
    
    return f"""**Subject:** {customer_name} Infrastructure Modernization - Executive Summary

Dear [Executive Team],

Dell Technologies can help {customer_name} achieve your infrastructure modernization goals while delivering measurable business value.

**Strategic Benefits:**
- Reduced operational complexity and IT overhead
- Improved application performance and user experience
- Future-ready platform for AI/ML and emerging workloads
- Enhanced {context}

**Investment Considerations:**
- {investment_msg}
- Competitive total cost of ownership vs. status quo
- Faster time-to-value compared to DIY approaches
- Proven ROI in similar organizations

**Recommended Next Steps:**
1. Technical validation and proof-of-concept
2. Detailed business case development
3. Implementation planning and timeline

We're committed to your success and look forward to partnering with {customer_name}.

Best regards,
[Your Name]
Dell Technologies"""

if __name__ == "__main__":
    main()
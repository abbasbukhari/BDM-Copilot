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

# Add the parent directory to path to import our engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import KnowledgeBase

# Set page config
st.set_page_config(
    page_title="BDM Copilot",
    page_icon="🤖",
    layout="wide"
)

# Initialize knowledge base
@st.cache_resource
def load_knowledge_base():
    """Load and cache the knowledge base"""
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
    knowledge_base = load_knowledge_base()
    st.success("🧠 Knowledge base loaded successfully with Dell documentation!")
except Exception as e:
    st.error(f"❌ Error loading knowledge base: {e}")
    knowledge_base = None

import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Page configuration
import streamlit as st
import pandas as pd
from io import StringIO
import sys
import os

# Add the parent directory to path to import our engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import KnowledgeBase

# Set page config
st.set_page_config(
    page_title="BDM Copilot",
    page_icon="�",
    layout="wide"
)

def main():
    st.title("🤝 BDM Copilot")
    st.subheader("Dell Infrastructure Solutions Assistant")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### About")
        st.markdown("""
        Transform discovery notes into:
        - Market-aligned summary
        - 3 solution options
        - Draft BOM (CSV)
        - Ready-to-send emails
        """)
        
        st.markdown("### Status")
        st.info("v0.1 - Manual template mode")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Input", "📊 Analysis", "💼 Outputs", "📧 Communications"])
    
    with tab1:
        input_section()
    
    with tab2:
        analysis_section()
    
    with tab3:
        outputs_section()
    
    with tab4:
        communications_section()

def input_section():
    """Discovery notes input section"""
    st.header("Discovery Notes Input")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Customer Discovery Notes")
        discovery_notes = st.text_area(
            "Paste your discovery notes here:",
            height=300,
            placeholder="""Example:
Customer: BigFinance Co.
Notes: Consolidate ~250–300 VMs across 2 sites to HCI. Prefers VMware. Needs simple mgmt, 25GbE roadmap, DR plan, AI POC later.
Budget: CAD 350–450k. Compliance: Data residency in Ontario."""
        )
        
        # Store in session state
        if discovery_notes:
            st.session_state['discovery_notes'] = discovery_notes
    
    with col2:
        st.markdown("### Quick Info")
        customer_name = st.text_input("Customer Name", placeholder="e.g., BigFinance Co.")
        opportunity_value = st.text_input("Opportunity Value", placeholder="e.g., CAD 350-450k")
        timeline = st.text_input("Timeline", placeholder="e.g., 90 days")
        
        if st.button("🔄 Process Notes", type="primary"):
            if discovery_notes:
                st.success("Notes processed! Check other tabs for outputs.")
                # Store additional info
                st.session_state['customer_name'] = customer_name
                st.session_state['opportunity_value'] = opportunity_value
                st.session_state['timeline'] = timeline
            else:
                st.error("Please enter discovery notes first.")

def analysis_section():
    """Analysis and summary section"""
    st.header("🔍 Market Analysis & Summary")
    
    if 'discovery_notes' not in st.session_state:
        st.info("👈 Please enter discovery notes in the Input tab first.")
        return
    
    discovery_notes = st.session_state.discovery_notes
    
    if knowledge_base is None:
        st.error("Knowledge base not available. Analysis will be limited.")
        return
    
    # Analyze discovery notes using knowledge base
    with st.spinner("🧠 Analyzing discovery notes against Dell knowledge base..."):
        try:
            # Find relevant content from knowledge base
            search_results = knowledge_base.find_relevant_content(discovery_notes)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📋 Key Requirements Identified")
                
                # Extract key requirements from notes
                key_phrases = discovery_notes.lower()
                requirements = []
                
                # Budget detection
                if any(word in key_phrases for word in ['budget', 'cost', '$', 'price']):
                    requirements.append("💰 Budget considerations identified")
                
                # Scale detection
                if any(word in key_phrases for word in ['vm', 'virtual machine', 'workload', 'server']):
                    requirements.append("📊 Scale requirements noted")
                
                # Technology preferences
                if any(word in key_phrases for word in ['vmware', 'hyper-v', 'kvm']):
                    requirements.append("💻 Virtualization platform preferences")
                
                # Compliance
                if any(word in key_phrases for word in ['compliance', 'regulation', 'security']):
                    requirements.append("🔒 Compliance requirements")
                
                if requirements:
                    for req in requirements:
                        st.markdown(f"- {req}")
                else:
                    st.markdown("- 📝 Requirements being analyzed...")
            
            with col2:
                st.markdown("### 🎯 Relevant Dell Solutions")
                
                if search_results and search_results.get('results'):
                    # Show top relevant solutions
                    solutions_found = set()
                    for result in search_results['results'][:5]:
                        source_title = result.get('source_title', '')
                        if 'vxrail' in source_title.lower():
                            solutions_found.add("Dell VxRail HCI")
                        elif 'powerstore' in source_title.lower():
                            solutions_found.add("Dell PowerStore")
                        elif 'prosupport' in source_title.lower():
                            solutions_found.add("Dell ProSupport Services")
                    
                    if solutions_found:
                        st.markdown("**Recommended Solutions:**")
                        for solution in solutions_found:
                            st.markdown(f"- ✅ {solution}")
                    
                    # Show search summary
                    if 'summary' in search_results:
                        st.markdown(f"**Knowledge Base:** {search_results['summary']}")
                else:
                    st.markdown("- 🔍 Analyzing against Dell product portfolio...")
                    
            # Store analysis results in session state
            st.session_state.analysis_results = {
                'search_results': search_results,
                'requirements': requirements,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            st.error(f"Error during analysis: {e}")
            
            # Fallback to static analysis
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Key Requirements")
                st.markdown("*Analysis in progress...*")
            with col2:
                st.markdown("### Market Insight")
                st.markdown("*Dell solution matching in progress...*")

def outputs_section():
    """Solution options and BOM section"""
    st.header("Solution Options & BOM")
    
    if 'discovery_notes' not in st.session_state:
        st.info("👈 Please enter discovery notes in the Input tab first.")
        return
    
    # Solution options
    st.markdown("### Solution Options")
    
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
    
    # BOM Section
    st.markdown("### Draft Bill of Materials")
    
    # Sample BOM data based on your template
    bom_data = {
        'Role': [
            'Compute Node (VxRail R760)',
            'Top-of-Rack Switch',
            'Storage Expansion Node',
            'Management Server'
        ],
        'Quantity': [4, 2, 2, 1],
        'CPU': [
            'Intel Xeon',
            '',
            'Intel Xeon', 
            'Intel Xeon'
        ],
        'RAM (GB)': [512, '', 256, 128],
        'Storage': [
            '15TB NVMe',
            '',
            '30TB SSD',
            '2TB SSD'
        ],
        'Network': [
            '25GbE',
            '100GbE',
            '25GbE',
            '10GbE'
        ],
        'License': [
            'VMware vSAN',
            '',
            '',
            'VMware vCenter'
        ],
        'Services': [
            'ProSupport 3yr',
            '',
            'ProSupport 3yr',
            'ProSupport Plus 3yr'
        ],
        'Notes': [
            'Core virtualization cluster',
            'Redundant switching; 25GbE downlinks',
            'Optional capacity scaling',
            'Centralized management'
        ]
    }
    
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
    """Email templates section"""
    st.header("Ready-to-Send Communications")
    
    if 'discovery_notes' not in st.session_state:
        st.info("👈 Please enter discovery notes in the Input tab first.")
        return
    
    # Get customer name from session state
    customer_name = st.session_state.get('customer_name', '[Customer Name]')
    
    email1, email2, email3 = st.columns(3)
    
    with email1:
        st.markdown("### 📧 Customer Recap")
        recap_email = f"""
**Subject:** {customer_name} Infrastructure Discussion - Next Steps

Hi [Customer Contact],

Thanks for the productive discussion about your infrastructure modernization needs.

**Context & Goals:** Consolidate 250-300 VMs to HCI for operational simplicity
**Constraints:** Budget CAD 350-450k, timeline 90 days, Ontario data residency, VMware preference

**Market Insight:** HCI adoption accelerating due to virtualization sprawl and operational complexity.

**Options (3) with citations:**
1) VxRail HCI — Perfect VMware fit & integrated lifecycle. [Source: VxRail Overview, p.3]
2) PowerFlex + Compute — High performance, better $/TB. [Source: PowerFlex Datasheet, p.5]  
3) PowerStore + vSAN — Lower entry cost hybrid approach. [Source: PowerStore Guide, p.8]

**Next Steps:**
- Technical deep-dive session (next week)
- Draft BOM review 
- Reference customer introductions

**Assumptions:** Current VMware licensing transferable
**Open Questions:** Specific compliance requirements, backup strategy

Best regards,
[Your Name]
        """
        st.text_area("", value=recap_email, height=400, key="recap")
        
        if st.button("📋 Copy Recap Email", key="copy_recap"):
            st.success("Email copied to clipboard!")
    
    with email2:
        st.markdown("### 🤝 Partner Request")
        partner_email = f"""
**Subject:** Promo/lead-time check — {customer_name}/VxRail Opportunity

Hi [Partner Rep],

We're scoping VxRail HCI solution for {customer_name}. Could you confirm current promos/spiffs, bundle SKUs, and lead times for:
- VxRail R760 nodes (4x)
- Top-of-rack switches (2x)  
- VMware licensing bundles

Goal: Improve margin and timeline for {customer_name}. Draft BOM attached (CSV).

Thanks,
Abbas
        """
        st.text_area("", value=partner_email, height=400, key="partner")
        
        if st.button("📋 Copy Partner Email", key="copy_partner"):
            st.success("Email copied to clipboard!")
    
    with email3:
        st.markdown("### ⚙️ SA Handoff")
        sa_email = f"""
**Opportunity:** {customer_name} HCI Modernization  
**Target close:** {st.session_state.get('timeline', '[Timeline]')}  
**Owner:** Abbas

**Constraints:** Budget CAD 350-450k, timeline 90 days, Ontario compliance, VMware preference

**Recommended path:** VxRail HCI — VMware alignment and operational simplicity

**Draft BOM attached:** bom_draft.csv

**Questions for SA:**
- Sizing validation for 250-300 VMs
- DR architecture options
- Migration timeline and approach
- ProSupport vs ProSupport Plus recommendation
        """
        st.text_area("", value=sa_email, height=400, key="sa")
        
        if st.button("📋 Copy SA Handoff", key="copy_sa"):
            st.success("Email copied to clipboard!")

if __name__ == "__main__":
    main()
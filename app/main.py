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
    
    # **NEW: LLM-Powered BDM Analysis using Adrian's methodology**
    with st.spinner("🧠 Analyzing discovery notes with Dell BDM intelligence..."):
        try:
            # Get comprehensive BDM analysis using LLM
            analysis_results = knowledge_base.analyze_discovery_notes_with_llm(discovery_notes)
            
            if 'error' in analysis_results:
                st.warning(f"⚠️ {analysis_results['error']}")
                # Show fallback analysis
                llm_analysis = analysis_results.get('llm_analysis', {})
            else:
                llm_analysis = analysis_results.get('llm_analysis', {})
            
            # Display LLM availability status
            llm_status = analysis_results.get('llm_available', False)
            status_color = "🟢" if llm_status else "🟡"
            status_text = "LLM Active" if llm_status else "LLM Fallback Mode"
            st.caption(f"{status_color} {status_text}")
            
            # **Adrian's 3-Pillar Analysis Display**
            
            # 1. Market Analysis & Use Cases
            if llm_analysis.get('market_analysis'):
                st.markdown("---")
                st.markdown(llm_analysis['market_analysis'])
            
            # 2. Dell Solution Architecture  
            if llm_analysis.get('solution_architecture'):
                st.markdown("---")
                st.markdown(llm_analysis['solution_architecture'])
            
            # 3. Competitive Advantage
            if llm_analysis.get('competitive_advantage'):
                st.markdown("---")
                st.markdown(llm_analysis['competitive_advantage'])
            
            # 4. Business Impact
            if llm_analysis.get('business_impact'):
                st.markdown("---")
                st.markdown(llm_analysis['business_impact'])
            
            # Knowledge Base Statistics
            chunks_found = analysis_results.get('chunks_found', 0)
            sources_used = analysis_results.get('sources_used', 0)
            search_terms = analysis_results.get('search_terms', [])
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📚 Knowledge Chunks", chunks_found)
            with col2:
                st.metric("📄 Dell Documents", sources_used) 
            with col3:
                st.metric("🔍 Search Terms", len(search_terms))
            
            if search_terms:
                st.caption(f"**Search terms identified:** {', '.join(search_terms[:8])}")
                
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            
            # Fallback to basic analysis
            st.markdown("### 📋 Basic Analysis")
            st.markdown("Using fallback analysis mode...")
            
            # Simple keyword extraction fallback
            key_phrases = discovery_notes.lower()
            if any(word in key_phrases for word in ['vmware', 'virtualization']):
                st.markdown("- 💻 VMware environment detected")
            if any(word in key_phrases for word in ['ai', 'ml', 'machine learning']):
                st.markdown("- 🤖 AI/ML workload requirements")
            if any(word in key_phrases for word in ['storage', 'performance']):
                st.markdown("- 📊 Storage performance needs")

def outputs_section():
    """Solution options and BOM section - Enhanced with LLM analysis"""
    st.header("Solution Options & BOM")
    
    if 'discovery_notes' not in st.session_state:
        st.info("👈 Please enter discovery notes in the Input tab first.")
        return
    
    # Check if we have LLM analysis results
    discovery_notes = st.session_state.discovery_notes
    
    if knowledge_base is None:
        st.error("Knowledge base not available. Using fallback templates.")
        return
    
    # Get LLM analysis for dynamic solution generation
    with st.spinner("🔧 Generating solution options..."):
        try:
            analysis_results = knowledge_base.analyze_discovery_notes_with_llm(discovery_notes)
            
            if 'error' not in analysis_results:
                llm_analysis = analysis_results.get('llm_analysis', {})
                llm_available = analysis_results.get('llm_available', False)
            else:
                st.warning(f"⚠️ {analysis_results['error']}")
                llm_analysis = analysis_results.get('llm_analysis', {})
                llm_available = False
                
        except Exception as e:
            st.error(f"Failed to generate dynamic solutions: {e}")
            llm_analysis = {}
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
        
        # Generate specific solution options from LLM
        solution_prompt = f"""
        Based on this customer analysis, provide 3 specific Dell solution options in this format:
        
        **Option 1: [Primary Recommendation]**
        - Fit: [Why it fits customer needs]
        - Components: [Specific Dell products]
        - Investment: [Estimated range]
        
        **Option 2: [Alternative Approach]**
        - Fit: [Different approach rationale]
        - Components: [Alternative Dell products]
        - Investment: [Estimated range]
        
        **Option 3: [Budget/Phased Option]**
        - Fit: [Cost-conscious approach]
        - Components: [Entry-level Dell products]
        - Investment: [Lower cost range]
        
        Customer Requirements: {discovery_notes[:500]}
        Solution Analysis: {llm_analysis.get('solution_architecture', '')[:500]}
        """
        
        if llm_available:
            with st.spinner("🎯 Generating specific solution options..."):
                try:
                    from engine.llm_engine import bdm_llm
                    solution_options = bdm_llm.generate_proposal_content(
                        analysis={"solution_analysis": solution_prompt},
                        customer_name=st.session_state.get('customer_name', 'the customer')
                    )
                    
                    if solution_options and len(solution_options) > 50:
                        st.markdown("---")
                        st.markdown("### 📋 Solution Options")
                        st.markdown(solution_options)
                    else:
                        # Fallback to static templates
                        _display_static_solution_options()
                        
                except Exception as e:
                    st.warning(f"Dynamic solution generation failed: {e}")
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
    """Email templates section - Enhanced with LLM content"""
    st.header("Ready-to-Send Communications")
    
    if 'discovery_notes' not in st.session_state:
        st.info("👈 Please enter discovery notes in the Input tab first.")
        return
    
    # Get customer info and LLM analysis
    discovery_notes = st.session_state.discovery_notes
    customer_name = st.session_state.get('customer_name', '[Customer Name]')
    
    # Get LLM analysis for dynamic email generation
    if knowledge_base:
        with st.spinner("✉️ Generating personalized communications..."):
            try:
                analysis_results = knowledge_base.analyze_discovery_notes_with_llm(discovery_notes)
                llm_analysis = analysis_results.get('llm_analysis', {})
                llm_available = analysis_results.get('llm_available', False)
            except:
                llm_analysis = {}
                llm_available = False
    else:
        llm_analysis = {}
        llm_available = False
    
    # Display LLM status for communications
    status_color = "🟢" if llm_available else "🟡"
    status_text = "Personalized Content" if llm_available else "Template Mode"
    st.caption(f"{status_color} {status_text}")
    
    email1, email2, email3 = st.columns(3)
    
    with email1:
        st.markdown("### 📧 Customer Recap")
        
        if llm_available and llm_analysis:
            # Generate dynamic customer recap email
            recap_prompt = f"""
            Write a professional follow-up email to {customer_name} after a discovery meeting. Include:
            
            1. Summary of their key requirements and challenges
            2. Top 2-3 Dell solution recommendations with brief rationale
            3. Next steps for technical evaluation
            4. Any assumptions or open questions
            
            Keep it concise, professional, and action-oriented.
            
            Customer Context: {discovery_notes[:300]}
            Dell Solutions: {llm_analysis.get('solution_architecture', '')[:300]}
            Competitive Context: {llm_analysis.get('competitive_advantage', '')[:200]}
            """
            
            try:
                from engine.llm_engine import bdm_llm
                recap_email = bdm_llm.generate_proposal_content(
                    analysis={"email_content": recap_prompt},
                    customer_name=customer_name
                )
                
                if not recap_email or len(recap_email) < 50:
                    recap_email = _generate_fallback_recap_email(customer_name, discovery_notes)
                    
            except:
                recap_email = _generate_fallback_recap_email(customer_name, discovery_notes)
        else:
            recap_email = _generate_fallback_recap_email(customer_name, discovery_notes)
        
        st.text_area("", value=recap_email, height=400, key="recap")
        
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
        
        if st.button("📋 Copy Partner Email", key="copy_partner"):
            st.success("Partner email ready to copy!")
    
    with email3:
        st.markdown("### 📊 Executive Summary")
        
        if llm_available and llm_analysis:
            # Generate executive summary email
            exec_prompt = f"""
            Write a concise executive summary email for {customer_name}'s leadership team. Focus on:
            
            1. Business impact and strategic advantages
            2. Risk mitigation and competitive positioning
            3. Investment summary and ROI considerations
            4. Recommended next steps
            
            Write for C-level audience, focus on business outcomes not technical details.
            
            Business Context: {discovery_notes[:400]}
            Business Impact: {llm_analysis.get('business_impact', '')[:400]}
            """
            
            try:
                from engine.llm_engine import bdm_llm
                exec_email = bdm_llm.generate_proposal_content(
                    analysis={"executive_summary": exec_prompt},
                    customer_name=customer_name
                )
                
                if not exec_email or len(exec_email) < 50:
                    exec_email = _generate_fallback_exec_email(customer_name, discovery_notes)
                    
            except:
                exec_email = _generate_fallback_exec_email(customer_name, discovery_notes)
        else:
            exec_email = _generate_fallback_exec_email(customer_name, discovery_notes)
        
        st.text_area("", value=exec_email, height=400, key="executive")
        
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
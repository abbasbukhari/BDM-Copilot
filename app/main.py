"""
BDM Copilot - Streamlit Application

A sales enablement tool for Dell infrastructure solutions.
Converts discovery notes into structured outputs.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="BDM Copilot",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
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
    st.header("Market Analysis & Summary")
    
    if 'discovery_notes' not in st.session_state:
        st.info("👈 Please enter discovery notes in the Input tab first.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Key Requirements")
        st.markdown("""
        *This will be auto-generated from your notes*
        
        **Identified Constraints:**
        - Budget: CAD 350-450k
        - Timeline: Quick deployment preferred
        - Scale: 250-300 VMs
        - Compliance: Data residency in Ontario
        - Preferences: VMware alignment
        """)
    
    with col2:
        st.markdown("### Market Insight")
        st.markdown("""
        *Market trend analysis*
        
        **Why Now:**
        HCI adoption accelerating due to virtualization sprawl and operational complexity. VMware licensing changes driving infrastructure refresh cycles.
        """)

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
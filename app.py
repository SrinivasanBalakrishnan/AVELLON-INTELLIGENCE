import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import graphviz
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import random
import time

# -----------------------------------------------------------------------------
# 1. CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AVELLON INTELLIGENCE",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Enterprise/Military Aesthetic
st.markdown("""
<style>
    /* Global Background & Font */
    .stApp {
        background-color: #0b0d10;
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #f0f2f6;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    h1 { font-size: 2.5rem; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
    h2 { font-size: 1.8rem; color: #aab; margin-top: 30px; }
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] {
        font-family: 'Roboto Mono', monospace;
        font-size: 1.8rem !important;
        color: #e0e0e0;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #666;
    }
    
    /* Cards/Panels */
    .css-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Navigation Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #30363d;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 4px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Alert Badges */
    .badge-critical { background-color: #7f1d1d; color: #fecaca; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; border: 1px solid #991b1b; }
    .badge-high { background-color: #7c2d12; color: #fed7aa; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; border: 1px solid #c2410c; }
    .badge-medium { background-color: #713f12; color: #fef08a; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; border: 1px solid #a16207; }
    .badge-low { background-color: #14532d; color: #bbf7d0; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; border: 1px solid #166534; }
    
    /* Footer */
    .footer {
        text-align: center;
        font-size: 0.75rem;
        color: #444;
        margin-top: 50px;
        border-top: 1px solid #222;
        padding-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. STATE MANAGEMENT & BACKEND MOCK
# -----------------------------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

class AvellonBackend:
    @staticmethod
    def get_risk_metrics():
        return {
            "global_index": 72.4,
            "critical_assets": 4,
            "watchlist": 12,
            "uptime": "99.998%",
            "last_scan": datetime.now().strftime("%H:%M:%S UTC")
        }

    @staticmethod
    def get_assets():
        return [
            {"name": "Strait of Malacca", "lat": 4.2105, "lon": 101.9758, "type": "Choke Point", "risk": "CRITICAL", "conf": 98},
            {"name": "Taiwan Strait", "lat": 23.9037, "lon": 119.6763, "type": "Conflict Zone", "risk": "HIGH", "conf": 92},
            {"name": "Suez Canal", "lat": 30.5852, "lon": 32.3999, "type": "Choke Point", "risk": "MEDIUM", "conf": 89},
            {"name": "Rotterdam Hub", "lat": 51.9225, "lon": 4.47917, "type": "Port", "risk": "LOW", "conf": 99},
            {"name": "Panama Canal", "lat": 9.1012, "lon": -79.6955, "type": "Chokepoint", "risk": "LOW", "conf": 95},
             {"name": "Gulf of Aden", "lat": 12.8, "lon": 45.0, "type": "Trade Route", "risk": "HIGH", "conf": 88},
        ]

    @staticmethod
    def get_intel_feed():
        return [
            {"id": "EVT-902", "title": "Unverified Drone Activity", "loc": "Red Sea Sector 4", "severity": "CRITICAL", "cat": "Conflict", "time": "14m ago", "conf": 94},
            {"id": "EVT-901", "title": "Typhoon Beryl Formation", "loc": "Philippine Sea", "severity": "HIGH", "cat": "Weather", "time": "42m ago", "conf": 88},
            {"id": "EVT-899", "title": "Port Labor Strike Notice", "loc": "Hamburg Terminal", "severity": "MEDIUM", "cat": "Labor", "time": "2h ago", "conf": 76},
            {"id": "EVT-898", "title": "New Sanctions List Issued", "loc": "Global / OFAC", "severity": "LOW", "cat": "Regulatory", "time": "5h ago", "conf": 100},
        ]

    @staticmethod
    def get_logs():
        return pd.DataFrame([
            {"Timestamp": "14:12:01", "User": "ADMIN_SEC", "Action": "ACCESS_WAR_ROOM", "IP": "10.2.4.12"},
            {"Timestamp": "14:08:45", "User": "SYSTEM", "Action": "AUTO_SCALING_EVENT", "IP": "INTERNAL"},
            {"Timestamp": "13:55:22", "User": "ANALYST_04", "Action": "OVERRIDE_CONFIDENCE", "IP": "10.2.5.99"},
        ])

# -----------------------------------------------------------------------------
# 3. NAVIGATION CONTROLLER
# -----------------------------------------------------------------------------
def sidebar_nav():
    st.sidebar.title("AVELLON")
    st.sidebar.caption("The Architecture of Dominion")
    st.sidebar.markdown("---")

    # Public Navigation
    nav_options = ["Home", "Platform", "Solutions", "Services", "Insights", "About", "Contact"]
    
    # Secure Navigation (Only if authenticated)
    if st.session_state['authenticated']:
        st.sidebar.markdown("### SECURE CONSOLE")
        secure_options = ["War Room", "Analytics", "Simulation", "System Logs"]
        selected_secure = st.sidebar.radio("Command", secure_options, label_visibility="collapsed")
        
        st.sidebar.markdown("---")
        if st.sidebar.button("Log Out"):
            st.session_state['authenticated'] = False
            st.session_state['page'] = 'Home'
            st.rerun()
            
        # If a secure option is selected in radio, update page state
        # Logic fix: Use a callback or direct assignment if this were complex. 
        # For simplicity, we assume user clicks logic below.
        if selected_secure != st.session_state.get('last_secure', None):
            st.session_state['page'] = selected_secure
            st.session_state['last_secure'] = selected_secure

    else:
        st.sidebar.markdown("### NAVIGATION")
        selected_public = st.sidebar.radio("Menu", nav_options, label_visibility="collapsed")
        
        if selected_public != st.session_state.get('last_public', None):
            st.session_state['page'] = selected_public
            st.session_state['last_public'] = selected_public
        
        st.sidebar.markdown("---")
        if st.sidebar.button("Secure Login"):
            st.session_state['page'] = "Login"
            st.rerun()

    # Footer in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 AVELLON INTELLIGENCE\nVer: 21.4.0-ENT\nStatus: OPERATIONAL")

# -----------------------------------------------------------------------------
# 4. PAGE RENDERERS
# -----------------------------------------------------------------------------

# --- PUBLIC PAGES ---

def render_home():
    st.title("The Geometry of Risk.")
    st.markdown("""
    <div style='background-color: #161b22; padding: 30px; border-left: 5px solid #00d4ff; margin-bottom: 40px;'>
        <h3 style='margin-top:0;'>Operational Pre-cognition for the Fortune 500.</h3>
        <p style='font-size: 1.1rem; color: #ccc;'>
            Traditional intelligence reacts to headlines. AVELLON models the structural integrity of global stability.
            We provide an autonomous, generative operating system for risk that sees, understands, and mitigates threats before they materialize.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 01. PREDICTIVE")
        st.info("Don't just monitor. Forecast.")
        st.caption("Our probabilistic engines model risk velocity, calculating the financial blast radius of geopolitical friction days in advance.")
    with c2:
        st.markdown("### 02. OMNISCIENT")
        st.info("Total informational dominance.")
        st.caption("Fusing satellite reconnaissance, dark web signals, and proprietary sensor networks into a single, unified truth.")
    with c3:
        st.markdown("### 03. AUTONOMOUS")
        st.info("Self-healing supply chains.")
        st.caption("The system doesn't just alert; it suggests mitigation pathways, auditing suppliers and routing alternatives in real-time.")

    st.markdown("---")
    st.markdown("### WHO WE SERVE")
    cols = st.columns(4)
    cols[0].metric("Governments", "Sovereign")
    cols[1].metric("Defense", "Strategic")
    cols[2].metric("Finance", "Institutional")
    cols[3].metric("Energy", "Critical")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Request Strategic Briefing →"):
        st.session_state['page'] = "Contact"
        st.rerun()

def render_platform():
    st.title("Generative Risk Operating System")
    st.markdown("AVELLON is not a dashboard. It is a computational engine for global stability.")
    
    st.markdown("### CORE MODULES")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🌍 Global War Room")
        st.caption("A geospatial command interface providing real-time situational awareness across physical, cyber, and cognitive domains.")
        st.markdown("#### 🧠 Predictive Risk Engine")
        st.caption("Utilizing graph neural networks to map hidden dependencies between assets, suppliers, and geopolitical actors.")
    
    with c2:
        st.markdown("#### 🕸️ Digital Twin")
        st.caption("Create a high-fidelity simulation of your entire value chain to test resilience against kinetic and non-kinetic shocks.")
        st.markdown("#### ⚖️ Regulatory Sentinel")
        st.caption("Automated compliance monitoring against 450+ global sanctions lists, trade restrictions, and export controls.")

    st.markdown("---")
    st.markdown("### ENTERPRISE READINESS")
    st.table(pd.DataFrame({
        "Feature": ["Security", "Deployment", "Auditability", "Latency"],
        "Standard": ["FEDRAMP High / IL5 Ready", "On-Prem / Air-Gapped / Hybrid Cloud", "Immutable Blockchain Logs", "< 50ms Global Edge"]
    }).set_index("Feature"))

def render_solutions():
    st.title("Strategic Solutions")
    
    tab1, tab2, tab3 = st.tabs(["CORPORATE", "GOVERNMENT", "FINANCE"])
    
    with tab1:
        st.subheader("Fortune 500 Enterprises")
        st.markdown("**The Challenge:** Supply chain opacity and kinetic disruption.")
        st.markdown("**The AVELLON Approach:** We transform supply chains from fragile linear sequences into resilient, self-healing mesh networks.")
        st.markdown("**Outcome:** 40% reduction in downtime costs; 100% visibility into Tier-N suppliers.")
        
    with tab2:
        st.subheader("Defense & Intelligence")
        st.markdown("**The Challenge:** Cognitive overload and signal-to-noise ratio.")
        st.markdown("**The AVELLON Approach:** AI-driven sensor fusion that prioritizes threats based on strategic intent and capability.")
        st.markdown("**Outcome:** Faster OODA loops; enhanced sovereign decision-making.")

    with tab3:
        st.subheader("Institutional Finance")
        st.markdown("**The Challenge:** Pricing geopolitical risk into asset models.")
        st.markdown("**The AVELLON Approach:** Real-time quantification of macro-risk factors mapped to specific tickers and commodities.")
        st.markdown("**Outcome:** Alpha generation through superior information asymmetry.")

def render_services():
    st.title("Advisory & Engagement")
    st.write("Beyond the platform, AVELLON provides high-touch strategic services for our most critical partners.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Strategic Risk Intelligence")
        st.caption("Bespoke intelligence products delivered by our team of former agency analysts and sector experts.")
        st.markdown("#### Custom Platform Deployment")
        st.caption("Tailoring the AVELLON OS to integrate with proprietary internal data lakes and legacy ERP systems.")
    with c2:
        st.markdown("#### Crisis Response & Simulation")
        st.caption("Live 'Red Teaming' and table-top exercises to stress-test executive decision-making.")
        st.markdown("#### Sovereign Advisory")
        st.caption("Confidential consultation for heads of state and ministries on national resilience architecture.")

def render_about():
    st.title("About AVELLON")
    st.markdown("""
    AVELLON was founded on a singular premise: **Complexity is the new threat vector.**
    
    In a hyper-connected world, a butterfly effect in a remote strait can collapse industries on the other side of the planet. Traditional intelligence agencies are built for a slower, more predictable era.
    
    We are engineers, mathematicians, and strategists building the immunity system for the global economy. We do not predict the future; we calculate the probabilities of survival.
    
    **Headquarters:** London | Washington D.C. | Singapore
    """)

def render_contact():
    st.title("Secure Engagement")
    st.write("For strategic inquiries, please utilize the channels below. All communications are encrypted.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Institutional Email")
        st.text_input("Organization / Agency")
        st.selectbox("Inquiry Type", ["Platform Demo", "Strategic Partnership", "Media / Press", "Sovereign Liaison"])
        st.button("Initiate Handshake")
    
    with c2:
        st.markdown("#### Global Offices")
        st.markdown("10 Downing Street, London\n\n1600 Pennsylvania Ave, Washington D.C.\n\n1 Raffles Quay, Singapore")
        st.caption("PGP Key available upon request.")

def render_insights():
    st.title("Strategic Insights")
    st.write("Briefings for the decision-making elite.")
    
    st.markdown("### LATEST BRIEFS")
    
    with st.expander("The Kinetic Pivot: Maritime Chokepoints in 2026", expanded=True):
        st.caption("Classification: PUBLIC | Date: Jan 02, 2026")
        st.write("An analysis of shifting naval doctrines in the Indo-Pacific and the implications for commercial semiconductor transit.")
    
    with st.expander("Generative Disinformation and Market Stability"):
        st.caption("Classification: PUBLIC | Date: Dec 15, 2025")
        st.write("How synthetic media is being weaponized to trigger algorithmic trading flash crashes.")
        
    with st.expander("The Rare Earth Decoupling"):
        st.caption("Classification: RESTRICTED (Summary Only)")
        st.write("Projecting the 5-year timeline of critical mineral supply chain bifurcation.")

# --- PRIVATE / SECURE PAGES ---

def render_login():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown("## AVELLON SECURE CONSOLE")
        st.markdown("Access Restricted to Authorized Personnel.")
        user = st.text_input("Identity")
        pwd = st.text_input("Keycode", type="password")
        
        if st.button("Authenticate", use_container_width=True):
            if user and pwd: # Mock auth
                st.session_state['authenticated'] = True
                st.session_state['user_role'] = "COMMANDER"
                st.session_state['page'] = "War Room"
                st.rerun()
            else:
                st.error("Invalid Credentials. Attempt Logged.")

def render_war_room():
    # Header Metrics
    metrics = AvellonBackend.get_risk_metrics()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Global Risk Index", metrics['global_index'], "+1.2%")
    c2.metric("Critical Assets", metrics['critical_assets'], "Active")
    c3.metric("System Uptime", metrics['uptime'])
    c4.metric("Last Scan", metrics['last_scan'])
    
    st.markdown("---")
    
    # Map & Feed
    col_map, col_feed = st.columns([2, 1])
    
    with col_map:
        st.subheader("OPERATIONAL THEATER")
        assets = AvellonBackend.get_assets()
        m = folium.Map(location=[20, 10], zoom_start=2, tiles="CartoDB dark_matter")
        
        risk_colors = {"CRITICAL": "red", "HIGH": "orange", "MEDIUM": "yellow", "LOW": "green"}
        
        for a in assets:
            color = risk_colors.get(a['risk'], 'blue')
            # Pulse for critical
            if a['risk'] == "CRITICAL":
                folium.CircleMarker(
                    location=[a['lat'], a['lon']], radius=20, color=color, fill=True, fill_opacity=0.2
                ).add_to(m)
            
            folium.CircleMarker(
                location=[a['lat'], a['lon']],
                radius=6,
                popup=f"<b>{a['name']}</b><br>Risk: {a['risk']}<br>Conf: {a['conf']}%",
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=1
            ).add_to(m)
            
        st_folium(m, height=500, use_container_width=True)
        
    with col_feed:
        st.subheader("INTELLIGENCE STREAM")
        feed = AvellonBackend.get_intel_feed()
        for item in feed:
            badge_class = f"badge-{item['severity'].lower()}"
            with st.container():
                st.markdown(f"""
                <div class='css-card' style='padding: 10px; margin-bottom:10px;'>
                    <div style='display:flex; justify-content:space-between;'>
                        <span class='{badge_class}'>{item['severity']}</span>
                        <span style='color:#666; font-size:0.8rem;'>{item['time']}</span>
                    </div>
                    <div style='font-weight:bold; margin-top:5px;'>{item['title']}</div>
                    <div style='font-size:0.8rem; color:#aaa;'>{item['loc']} • {item['cat']}</div>
                    <div style='font-size:0.7rem; color:#444; margin-top:5px;'>Conf: {item['conf']}% | ID: {item['id']}</div>
                </div>
                """, unsafe_allow_html=True)

def render_analytics():
    st.title("Strategic Analytics")
    
    tab1, tab2 = st.tabs(["RISK VELOCITY", "DEPENDENCY GRAPH"])
    
    with tab1:
        st.markdown("#### 30-Day Risk Trend Analysis")
        # Mock Data
        data = pd.DataFrame({
            'Date': pd.date_range(start='2024-01-01', periods=30),
            'Risk Score': np.random.normal(70, 5, 30).cumsum() + 50
        })
        chart = alt.Chart(data).mark_area(
            line={'color':'#00d4ff'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='#00d4ff', offset=0),
                       alt.GradientStop(color='rgba(0, 212, 255, 0)', offset=1)],
                x1=1, x2=1, y1=1, y2=0
            )
        ).encode(
            x='Date',
            y=alt.Y('Risk Score', scale=alt.Scale(domain=[40, 100]))
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
        
    with tab2:
        st.markdown("#### Supply Chain Critical Path")
        graph = graphviz.Digraph()
        graph.attr(bgcolor='transparent', rankdir='LR')
        graph.attr('node', shape='box', style='filled', color='black', fontcolor='white')
        graph.node('A', 'Rare Earth Mine (Source)', fillcolor='#444')
        graph.node('B', 'Refining Facility (Processing)', fillcolor='#444')
        graph.node('C', 'Choke Point (Logistics)', fillcolor='#7f1d1d') # Critical
        graph.node('D', 'Component Fab (Mfg)', fillcolor='#444')
        graph.node('E', 'Assembly Plant (Final)', fillcolor='#444')
        
        graph.edge('A', 'B')
        graph.edge('B', 'C', label='Delay risk', color='red')
        graph.edge('C', 'D')
        graph.edge('D', 'E')
        
        st.graphviz_chart(graph)
        st.caption("CRITICAL FAILURE POINT DETECTED: Node C (Logistics Choke Point)")

def render_simulation():
    st.title("Scenario Modeling")
    st.markdown("### Monte Carlo Risk Simulation")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("#### Input Parameters")
        st.selectbox("Scenario Type", ["Strait Closure", "Pandemic Event", "Cyber Grid Down", "Sanctions Escalation"])
        days = st.slider("Duration (Days)", 1, 90, 14)
        severity = st.select_slider("Severity Level", options=["Localized", "Regional", "Global Systemic"])
        st.button("Run Simulation", type="primary")
        
    with c2:
        st.markdown("#### Projected Impact")
        m1, m2 = st.columns(2)
        m1.metric("Revenue at Risk", f"${days * 12.5}M", "High Confidence")
        m2.metric("Inventory Burn", f"{days * 2.4}%", "Critical")
        
        st.progress(min(100, days * 2))
        st.caption("Probability of cascading failure: 68%")
        
        st.info("AI RECOMMENDATION: Initiate buffer stock release in EMEA region immediately to mitigate Day 14 stockout.")

def render_logs():
    st.title("System Audit Logs")
    logs = AvellonBackend.get_logs()
    st.dataframe(logs, use_container_width=True)

# -----------------------------------------------------------------------------
# 5. MAIN APP ROUTER
# -----------------------------------------------------------------------------
def main():
    # Sidebar Navigation
    sidebar_nav()
    
    # Page Routing
    page = st.session_state['page']
    
    # Public Routes
    if page == "Home": render_home()
    elif page == "Platform": render_platform()
    elif page == "Solutions": render_solutions()
    elif page == "Services": render_services()
    elif page == "Insights": render_insights()
    elif page == "About": render_about()
    elif page == "Contact": render_contact()
    elif page == "Login": render_login()
    
    # Secure Routes (Protected)
    elif page == "War Room": 
        if st.session_state['authenticated']: render_war_room()
        else: render_login()
    elif page == "Analytics":
        if st.session_state['authenticated']: render_analytics()
        else: render_login()
    elif page == "Simulation":
        if st.session_state['authenticated']: render_simulation()
        else: render_login()
    elif page == "System Logs":
        if st.session_state['authenticated']: render_logs()
        else: render_login()

    # Footer
    st.markdown("""
    <div class='footer'>
        <p>AVELLON INTELLIGENCE &copy; 2026. All Rights Reserved.</p>
        <p>Restricted Access. Unauthorized use is a violation of federal law.</p>
        <p>Operating under ISO 27001 Information Security Standards.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

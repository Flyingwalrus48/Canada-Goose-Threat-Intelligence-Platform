# app_enterprise.py - Ultra-Advanced Canada Goose Global Security Intelligence Platform
# Next-Level Enterprise Features with GitHub Add-ons

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import networkx as nx
import numpy as np

# Advanced Streamlit Components
try:
    from streamlit_autorefresh import st_autorefresh
    AUTOREFRESH_AVAILABLE = True
except ImportError:
    AUTOREFRESH_AVAILABLE = False

try:
    from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
    AGGRID_AVAILABLE = True
except ImportError:
    AGGRID_AVAILABLE = False

try:
    from streamlit_option_menu import option_menu
    OPTION_MENU_AVAILABLE = True
except ImportError:
    OPTION_MENU_AVAILABLE = False

try:
    import streamlit_lottie as st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

# --- ENHANCED CONFIGURATION ---
BRAND_COLORS = {
    "primary_black": "#000000",
    "primary_white": "#FFFFFF", 
    "accent_red": "#DC143C",
    "critical_red": "#FF4444",
    "high_orange": "#FF8C00",
    "medium_yellow": "#FFD700",
    "low_green": "#32CD32",
    "background_gray": "#F8F9FA",
    "card_gray": "#FFFFFF",
    "text_dark": "#2C3E50",
    "text_light": "#6C757D",
    "dark_bg": "#1E1E1E",
    "dark_card": "#2D2D2D"
}

ENHANCED_RISK_MATRIX = {
    "Activism / Physical Security": {"likelihood": 4, "impact": 3, "primary_impact": "Store Operations & Reputation"},
    "Geopolitical / Market Risk": {"likelihood": 3, "impact": 5, "primary_impact": "Revenue & Market Access"},
    "Legal / Financial": {"likelihood": 2, "impact": 4, "primary_impact": "Financial Performance"},
    "Organized Retail Crime": {"likelihood": 4, "impact": 3, "primary_impact": "Inventory Loss & Staff Safety"},
    "Cyber / Dark Web": {"likelihood": 3, "impact": 4, "primary_impact": "Customer Data & Brand Trust"},
    "General Intelligence": {"likelihood": 2, "impact": 2, "primary_impact": "General Awareness"}
}

# --- ADVANCED UTILITY FUNCTIONS ---
def load_custom_css_with_theme(dark_mode=False):
    """Enhanced CSS loading with dark/light theme support."""
    theme_colors = BRAND_COLORS.copy()
    if dark_mode:
        theme_colors.update({
            "background_gray": "#1E1E1E",
            "card_gray": "#2D2D2D",
            "text_dark": "#FFFFFF",
            "text_light": "#CCCCCC"
        })
    
    try:
        with open('style.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Dynamic theme replacement
        for key, color in theme_colors.items():
            css_content = css_content.replace(f"#{key.upper()}", color)
        
        # Additional dark mode styles
        if dark_mode:
            css_content += """
            /* Dark Mode Enhancements */
            .main { background-color: #1E1E1E !important; }
            .stApp { background-color: #1E1E1E !important; }
            .css-18e3th9 { background-color: #2D2D2D !important; }
            """
        
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        
        # Add advanced animations
        st.markdown("""
        <style>
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes slideIn {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .animated-metric {
            animation: pulse 2s infinite;
        }
        
        .slide-in {
            animation: slideIn 0.5s ease-out;
        }
        
        .threat-network-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .real-time-indicator {
            animation: pulse 1s infinite;
            background: #32CD32;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        </style>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.warning("⚠️ style.css file not found. Using enhanced built-in styling.")
        load_fallback_css()

def load_fallback_css():
    """Fallback CSS with enhanced features."""
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }
    
    .metric-card-advanced {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card-advanced:hover {
        transform: translateY(-10px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def create_animated_counter(value, label, duration=2000):
    """Create animated counter component."""
    st.markdown(f"""
    <div class="animated-metric">
        <div style="text-align: center; padding: 1rem;">
            <div id="counter-{label.replace(' ', '-')}" style="font-size: 3rem; font-weight: bold; color: #DC143C;">0</div>
            <div style="font-size: 1rem; color: #6C757D; text-transform: uppercase;">{label}</div>
        </div>
    </div>
    <script>
    function animateCounter(elementId, endValue, duration) {{
        const element = document.getElementById(elementId);
        const startValue = 0;
        const startTime = performance.now();
        
        function updateCounter(currentTime) {{
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const currentValue = Math.floor(startValue + (endValue - startValue) * progress);
            
            element.textContent = currentValue;
            
            if (progress < 1) {{
                requestAnimationFrame(updateCounter);
            }}
        }}
        
        requestAnimationFrame(updateCounter);
    }}
    
    animateCounter('counter-{label.replace(' ', '-')}', {value}, {duration});
    </script>
    """, unsafe_allow_html=True)

def create_threat_network_graph(events_data):
    """Create advanced threat relationship network using NetworkX."""
    # Create network graph
    G = nx.Graph()
    
    # Add nodes for locations and threat types
    locations = set(event['location'] for event in events_data)
    threat_types = set(event['analysis']['threat_type'] for event in events_data)
    
    # Add location nodes
    for location in locations:
        location_events = [e for e in events_data if e['location'] == location]
        avg_risk = np.mean([e['analysis']['risk_assessment']['risk_score'] for e in location_events])
        G.add_node(location, 
                  node_type='location', 
                  risk_score=avg_risk,
                  size=max(10, avg_risk * 2))
    
    # Add threat type nodes
    for threat_type in threat_types:
        threat_events = [e for e in events_data if e['analysis']['threat_type'] == threat_type]
        avg_risk = np.mean([e['analysis']['risk_assessment']['risk_score'] for e in threat_events])
        G.add_node(threat_type, 
                  node_type='threat', 
                  risk_score=avg_risk,
                  size=max(15, avg_risk * 1.5))
    
    # Add edges between locations and threat types
    for event in events_data:
        location = event['location']
        threat_type = event['analysis']['threat_type']
        risk_score = event['analysis']['risk_assessment']['risk_score']
        
        if G.has_edge(location, threat_type):
            G[location][threat_type]['weight'] += risk_score
        else:
            G.add_edge(location, threat_type, weight=risk_score)
    
    # Create Plotly network visualization
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Extract node and edge information
    node_x = []
    node_y = []
    node_info = []
    node_colors = []
    node_sizes = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        node_data = G.nodes[node]
        node_type = node_data.get('node_type', 'unknown')
        risk_score = node_data.get('risk_score', 0)
        
        node_info.append(f"{node}<br>Type: {node_type}<br>Avg Risk: {risk_score:.1f}")
        
        # Color based on node type
        if node_type == 'location':
            if risk_score >= 15:
                node_colors.append(BRAND_COLORS['critical_red'])
            elif risk_score >= 10:
                node_colors.append(BRAND_COLORS['high_orange'])
            else:
                node_colors.append(BRAND_COLORS['medium_yellow'])
        else:
            node_colors.append(BRAND_COLORS['accent_red'])
        
        node_sizes.append(node_data.get('size', 15))
    
    # Extract edge information
    edge_x = []
    edge_y = []
    edge_weights = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_weights.append(G[edge[0]][edge[1]]['weight'])
    
    # Create the plot
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y,
                            line=dict(width=2, color='rgba(50,50,50,0.5)'),
                            hoverinfo='none',
                            mode='lines'))
    
    # Add nodes
    fig.add_trace(go.Scatter(x=node_x, y=node_y,
                            mode='markers+text',
                            marker=dict(size=node_sizes,
                                       color=node_colors,
                                       line=dict(width=2, color='white')),
                            text=[node for node in G.nodes()],
                            textposition="middle center",
                            textfont=dict(size=10, color='white'),
                            hoverinfo='text',
                            hovertext=node_info))
    
    fig.update_layout(title="Threat Intelligence Network Analysis",
                     showlegend=False,
                     hovermode='closest',
                     margin=dict(b=20,l=5,r=5,t=40),
                     annotations=[ dict(
                         text="Interactive network showing relationships between locations and threat types",
                         showarrow=False,
                         xref="paper", yref="paper",
                         x=0.005, y=-0.002 ) ],
                     xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                     yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                     plot_bgcolor='rgba(0,0,0,0)',
                     paper_bgcolor='rgba(0,0,0,0)')
    
    return fig

def create_advanced_data_table(events_data):
    """Create advanced interactive data table with AgGrid."""
    if not AGGRID_AVAILABLE:
        st.warning("AgGrid not available. Using standard table.")
        return st.dataframe(pd.DataFrame(events_data))
    
    # Prepare data for AgGrid
    df_events = pd.DataFrame([{
        'Date': event['date'],
        'Title': event['title'][:50] + '...' if len(event['title']) > 50 else event['title'],
        'Location': event['location'],
        'Threat Type': event['analysis']['threat_type'],
        'Risk Level': event['analysis']['risk_assessment']['risk_level'],
        'Risk Score': event['analysis']['risk_assessment']['risk_score'],
        'Details': event['details'][:100] + '...' if len(event['details']) > 100 else event['details']
    } for event in events_data])
    
    # Configure AgGrid
    gb = GridOptionsBuilder.from_dataframe(df_events)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    
    # Color coding for risk levels
    cell_style_jscode = """
    function(params) {
        if (params.data.RiskLevel == 'CRITICAL') {
            return {'background-color': '#FF4444', 'color': 'white'}
        } else if (params.data.RiskLevel == 'HIGH') {
            return {'background-color': '#FF8C00', 'color': 'white'}
        } else if (params.data.RiskLevel == 'MEDIUM') {
            return {'background-color': '#FFD700', 'color': 'black'}
        } else {
            return {'background-color': '#32CD32', 'color': 'white'}
        }
    }
    """
    
    gb.configure_column("Risk Level", cellStyle=cell_style_jscode)
    gridOptions = gb.build()
    
    # Display the grid
    grid_response = AgGrid(
        df_events,
        gridOptions=gridOptions,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=False,
        theme='alpine',
        enable_enterprise_modules=True,
        height=400,
        reload_data=False
    )
    
    return grid_response

def render_real_time_dashboard():
    """Render real-time auto-refreshing dashboard components."""
    if AUTOREFRESH_AVAILABLE:
        # Auto-refresh every 30 seconds
        count = st_autorefresh(interval=30000, limit=1000, key="threat_refresh")
        
        if count > 0:
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem; background: #32CD32; color: white; border-radius: 5px; margin-bottom: 1rem;">
                <span class="real-time-indicator"></span>
                <strong>Live Feed Active</strong> - Auto-refreshed {count} times | Last update: {datetime.now().strftime('%H:%M:%S')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 Install streamlit-autorefresh for real-time updates: `pip install streamlit-autorefresh`")

def render_advanced_sidebar_menu():
    """Render advanced sidebar navigation with option-menu."""
    if OPTION_MENU_AVAILABLE:
        with st.sidebar:
            selected = option_menu(
                menu_title="🛡️ Security Console",
                options=["Dashboard", "LAV Intelligence", "Risk Analysis", "Travel Brief", "Network Graph", "Data Tables"],
                icons=["speedometer2", "eye", "graph-up", "airplane", "diagram-3", "table"],
                menu_icon="shield-check",
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "#1E1E1E"},
                    "icon": {"color": "#DC143C", "font-size": "18px"},
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#2D2D2D"},
                    "nav-link-selected": {"background-color": "#DC143C"},
                }
            )
        return selected
    else:
        with st.sidebar:
            return st.selectbox("Navigation", ["Dashboard", "LAV Intelligence", "Risk Analysis", "Travel Brief", "Network Graph", "Data Tables"])

# --- ENHANCED MAIN APPLICATION ---
def main():
    """Ultra-advanced main application with next-level features."""
    # Page Configuration
    st.set_page_config(
        page_title="🛡️ CG Enterprise Security", 
        page_icon="🛡️", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize theme state
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    # Load advanced styling
    load_custom_css_with_theme(st.session_state.dark_mode)
    
    # Load data
    @st.cache_data
    def load_application_data():
        try:
            with open('corporate_data.json', 'r', encoding='utf-8') as f:
                corporate = json.load(f)
            
            # Enhanced event analysis
            with open('events.json', 'r', encoding='utf-8') as f:
                events = json.load(f)
            
            analyzed_events = []
            for event in events:
                threat_type = classify_threat_type(event['title'], event['details'])
                risk_assessment = calculate_enhanced_risk_score(event, threat_type)
                event['analysis'] = {'threat_type': threat_type, 'risk_assessment': risk_assessment}
                analyzed_events.append(event)
            
            with open('indicators.json', 'r', encoding='utf-8') as f:
                indicators = json.load(f)
                
            return corporate, analyzed_events, indicators
        except Exception as e:
            st.error(f"Critical data loading error: {e}")
            st.stop()
    
    corporate_data, events_data, indicators_data = load_application_data()
    
    # Advanced Navigation
    selected_page = render_advanced_sidebar_menu()
    
    # Theme toggle in sidebar
    with st.sidebar:
        st.markdown("---")
        if st.button("🌙 Toggle Dark Mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Real-time dashboard
    render_real_time_dashboard()
    
    # Main Header with enhanced styling
    st.markdown(f"""
    <div class="main-header slide-in">
        <h1>🛡️ Canada Goose Enterprise Security Intelligence</h1>
        <p>Ultra-Advanced LAV Counter-Intelligence • Real-Time Threat Monitoring • Predictive Analytics</p>
        <small>Theme: {'🌙 Dark Mode' if st.session_state.dark_mode else '☀️ Light Mode'}</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Page routing based on selection
    if selected_page == "Dashboard":
        render_enhanced_dashboard(events_data, corporate_data)
    elif selected_page == "LAV Intelligence":
        render_lav_deep_dive(indicators_data)
    elif selected_page == "Risk Analysis":
        render_advanced_risk_analysis(events_data)
    elif selected_page == "Travel Brief":
        render_enhanced_travel_section(events_data)
    elif selected_page == "Network Graph":
        render_network_analysis(events_data)
    elif selected_page == "Data Tables":
        render_data_explorer(events_data)

def render_enhanced_dashboard(events_data, corporate_data):
    """Enhanced dashboard with animated metrics."""
    st.markdown("## 📊 Executive Command Dashboard")
    
    # Animated metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_animated_counter(corporate_data['store_locations']['total_stores'], "Stores Monitored")
    
    with col2:
        high_risk_events = sum(1 for e in events_data if e['analysis']['risk_assessment']['risk_level'] in ["HIGH", "CRITICAL"])
        create_animated_counter(high_risk_events, "High-Risk Events")
    
    with col3:
        total_risk_score = sum(e['analysis']['risk_assessment']['risk_score'] for e in events_data)
        create_animated_counter(total_risk_score, "Total Risk Score")
    
    with col4:
        lav_events = sum(1 for e in events_data if "peta" in e['details'].lower() or "activist" in e['title'].lower())
        create_animated_counter(lav_events, "LAV Incidents")

def render_network_analysis(events_data):
    """Render threat network analysis."""
    st.markdown("## 🕸️ Threat Intelligence Network")
    
    st.markdown("""
    <div class="threat-network-container">
        <h3 style="color: white; text-align: center;">Interactive Threat Relationship Mapping</h3>
        <p style="color: white; text-align: center;">Visualizing connections between locations and threat types</p>
    </div>
    """, unsafe_allow_html=True)
    
    network_fig = create_threat_network_graph(events_data)
    st.plotly_chart(network_fig, use_container_width=True)

def render_data_explorer(events_data):
    """Render advanced data exploration interface."""
    st.markdown("## 📈 Advanced Data Explorer")
    
    st.markdown("### Interactive Intelligence Data Grid")
    grid_response = create_advanced_data_table(events_data)
    
    if grid_response and 'selected_rows' in grid_response:
        if grid_response['selected_rows']:
            st.markdown("### Selected Events Analysis")
            selected_df = pd.DataFrame(grid_response['selected_rows'])
            st.dataframe(selected_df)

# Helper functions (keeping the core logic from previous versions)
def classify_threat_type(event_title, event_details):
    """Classify threats using NLP-like pattern matching."""
    title_lower = event_title.lower()
    details_lower = event_details.lower()
    
    if "peta" in details_lower or "activist" in title_lower or "protest" in details_lower:
        return "Activism / Physical Security"
    if "trade" in title_lower or "geopolitical" in title_lower or "china" in title_lower or "diplomatic" in details_lower:
        return "Geopolitical / Market Risk"
    if "arbitration" in title_lower or "financial" in title_lower or "charge" in details_lower:
        return "Legal / Financial"
    if "orc" in title_lower or "organized retail crime" in title_lower or "thefts" in details_lower:
        return "Organized Retail Crime"
    if "dark web" in title_lower or "cyber" in title_lower or "data" in details_lower:
        return "Cyber / Dark Web"
    return "General Intelligence"

def calculate_enhanced_risk_score(event: dict, threat_type: str) -> dict:
    """Calculate sophisticated risk scores with location-based adjustments."""
    baseline = ENHANCED_RISK_MATRIX.get(threat_type, ENHANCED_RISK_MATRIX["General Intelligence"])
    likelihood = baseline["likelihood"]
    impact = baseline["impact"]
    
    location = event.get('location', '')
    location_multiplier = 1.0
    
    business_critical_locations = {
        "China": {"revenue_impact": 17.7, "criticality": "CRITICAL"},
        "Shanghai": {"revenue_impact": 8.8, "criticality": "HIGH"},
        "Beijing": {"revenue_impact": 5.0, "criticality": "HIGH"},
        "London": {"revenue_impact": 12.0, "criticality": "HIGH"},
        "Paris": {"revenue_impact": 8.0, "criticality": "HIGH"},
        "New York": {"revenue_impact": 15.0, "criticality": "HIGH"},
        "Toronto": {"revenue_impact": 25.0, "criticality": "CRITICAL"}
    }
    
    for critical_loc, data in business_critical_locations.items():
        if critical_loc.lower() in location.lower():
            if data["criticality"] == "CRITICAL":
                location_multiplier = 1.3
            elif data["criticality"] == "HIGH":
                location_multiplier = 1.2
            break
    
    if "peta" in event.get('details', '').lower():
        likelihood = min(5, likelihood + 1)
    
    final_impact = min(5, impact * location_multiplier)
    risk_score = likelihood * final_impact
    
    if risk_score >= 20:
        risk_level = "CRITICAL"
    elif risk_score >= 15:
        risk_level = "HIGH"
    elif risk_score >= 10:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return {
        "risk_score": int(risk_score),
        "risk_level": risk_level,
        "likelihood": likelihood,
        "impact": int(final_impact),
        "primary_impact": baseline["primary_impact"]
    }

# Placeholder functions for modular structure
def render_lav_deep_dive(indicators_data):
    st.markdown("## 🕵️ LAV Deep Intelligence Analysis")
    st.info("LAV counter-intelligence module - Enhanced analysis coming soon")

def render_advanced_risk_analysis(events_data):
    st.markdown("## ⚡ Advanced Risk Analytics")
    st.info("Advanced risk modeling and prediction algorithms")

def render_enhanced_travel_section(events_data):
    st.markdown("## ✈️ Enhanced Travel Intelligence")
    st.info("Advanced travel risk assessment with ML predictions")

if __name__ == "__main__":
    main()

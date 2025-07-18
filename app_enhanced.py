# app_enhanced.py - Canada Goose Global Security Intelligence Platform
# Enhanced with professional styling, interactive visualizations, and improved UX

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import re
from typing import Dict, List, Optional

# --- CANADA GOOSE BRAND COLORS & STYLING ---
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
    "text_light": "#6C757D"
}

# Custom CSS for Canada Goose branding
def load_custom_css():
    st.markdown(f"""
    <style>
    /* Global Styling */
    .main {{
        background-color: {BRAND_COLORS["background_gray"]};
        font-family: 'Arial', sans-serif;
    }}
    
    /* Header Styling */
    .main-header {{
        background: linear-gradient(135deg, {BRAND_COLORS["primary_black"]} 0%, #333333 100%);
        color: {BRAND_COLORS["primary_white"]};
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        text-align: center;
    }}
    
    .main-header h1 {{
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .main-header p {{
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }}
    
    /* Risk Level Cards */
    .risk-card {{
        background: {BRAND_COLORS["card_gray"]};
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 5px solid;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .risk-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }}
    
    .risk-critical {{
        border-left-color: {BRAND_COLORS["critical_red"]};
    }}
    
    .risk-high {{
        border-left-color: {BRAND_COLORS["high_orange"]};
    }}
    
    .risk-medium {{
        border-left-color: {BRAND_COLORS["medium_yellow"]};
    }}
    
    .risk-low {{
        border-left-color: {BRAND_COLORS["low_green"]};
    }}
    
    /* Status Indicators */
    .status-indicator {{
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }}
    
    .status-critical {{ background-color: {BRAND_COLORS["critical_red"]}; }}
    .status-high {{ background-color: {BRAND_COLORS["high_orange"]}; }}
    .status-medium {{ background-color: {BRAND_COLORS["medium_yellow"]}; }}
    .status-low {{ background-color: {BRAND_COLORS["low_green"]}; }}
    .status-red {{ background-color: {BRAND_COLORS["critical_red"]}; }}
    .status-yellow {{ background-color: {BRAND_COLORS["medium_yellow"]}; }}
    .status-green {{ background-color: {BRAND_COLORS["low_green"]}; }}
    
    /* Metrics Styling */
    .metric-container {{
        background: {BRAND_COLORS["card_gray"]};
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {BRAND_COLORS["text_dark"]};
        margin: 0;
    }}
    
    .metric-label {{
        font-size: 1rem;
        color: {BRAND_COLORS["text_light"]};
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Sidebar Styling */
    .css-1d391kg {{
        background-color: {BRAND_COLORS["primary_black"]};
    }}
    
    .css-1d391kg .css-1v3fvcr {{
        color: {BRAND_COLORS["primary_white"]};
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(135deg, {BRAND_COLORS["accent_red"]} 0%, #B71C1C 100%);
        color: {BRAND_COLORS["primary_white"]};
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(220,20,60,0.3);
    }}
    
    /* Expander Styling */
    .streamlit-expanderHeader {{
        background-color: {BRAND_COLORS["card_gray"]};
        border-radius: 8px;
        border: 1px solid #E9ECEF;
    }}
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {BRAND_COLORS["card_gray"]};
        border-radius: 8px 8px 0 0;
        border: 1px solid #E9ECEF;
        color: {BRAND_COLORS["text_dark"]};
        font-weight: 600;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {BRAND_COLORS["accent_red"]};
        color: {BRAND_COLORS["primary_white"]};
    }}
    
    /* Alert Styling */
    .alert-container {{
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }}
    
    .alert-warning {{
        background-color: #FFF3CD;
        border-left-color: {BRAND_COLORS["medium_yellow"]};
        color: #856404;
    }}
    
    .alert-danger {{
        background-color: #F8D7DA;
        border-left-color: {BRAND_COLORS["critical_red"]};
        color: #721C24;
    }}
    
    .alert-success {{
        background-color: #D4EDDA;
        border-left-color: {BRAND_COLORS["low_green"]};
        color: #155724;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENHANCED RISK SCORING ---
ENHANCED_RISK_MATRIX = {
    "Activism / Physical Security": {"likelihood": 4, "impact": 3, "primary_impact": "Store Operations & Reputation"},
    "Geopolitical / Market Risk": {"likelihood": 3, "impact": 5, "primary_impact": "Revenue & Market Access"},
    "Legal / Financial": {"likelihood": 2, "impact": 4, "primary_impact": "Financial Performance"},
    "Organized Retail Crime": {"likelihood": 4, "impact": 3, "primary_impact": "Inventory Loss & Staff Safety"},
    "Cyber / Dark Web": {"likelihood": 3, "impact": 4, "primary_impact": "Customer Data & Brand Trust"},
    "General Intelligence": {"likelihood": 2, "impact": 2, "primary_impact": "General Awareness"}
}

BUSINESS_CRITICAL_LOCATIONS = {
    "China": {"revenue_impact": 17.7, "criticality": "CRITICAL"},
    "Shanghai": {"revenue_impact": 8.8, "criticality": "HIGH"},
    "Beijing": {"revenue_impact": 5.0, "criticality": "HIGH"},
    "London": {"revenue_impact": 12.0, "criticality": "HIGH"},
    "Paris": {"revenue_impact": 8.0, "criticality": "HIGH"},
    "New York": {"revenue_impact": 15.0, "criticality": "HIGH"},
    "Toronto": {"revenue_impact": 25.0, "criticality": "CRITICAL"}
}

def calculate_enhanced_risk_score(event: dict, threat_type: str) -> dict:
    baseline = ENHANCED_RISK_MATRIX.get(threat_type, ENHANCED_RISK_MATRIX["General Intelligence"])
    likelihood = baseline["likelihood"]
    impact = baseline["impact"]
    adjustments = []
    location_multiplier = 1.0

    location = event.get('location', '')
    for critical_loc, data in BUSINESS_CRITICAL_LOCATIONS.items():
        if critical_loc.lower() in location.lower():
            if data["criticality"] == "CRITICAL":
                location_multiplier = 1.3
                adjustments.append(f"Critical Business Location Multiplier: x{location_multiplier}")
            elif data["criticality"] == "HIGH":
                location_multiplier = 1.2
                adjustments.append(f"High-Value Location Multiplier: x{location_multiplier}")
            break

    if "peta" in event.get('details', '').lower():
        likelihood = min(5, likelihood + 1)
        adjustments.append("Known Threat Actor (PETA) increases likelihood.")

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
        "primary_impact": baseline["primary_impact"],
        "adjustments_made": adjustments
    }

def classify_threat_type(event_title, event_details):
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

def analyze_events_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            events = json.load(f)
    except Exception as e:
        st.error(f"Error loading {filepath}: {e}")
        return []

    analyzed_events = []
    for event in events:
        threat_type = classify_threat_type(event['title'], event['details'])
        risk_assessment = calculate_enhanced_risk_score(event, threat_type)
        event['analysis'] = {'threat_type': threat_type, 'risk_assessment': risk_assessment}
        analyzed_events.append(event)
    return analyzed_events

# --- ENHANCED VISUALIZATIONS ---
def create_risk_distribution_chart(events_data):
    risk_counts = {}
    for event in events_data:
        level = event['analysis']['risk_assessment']['risk_level']
        risk_counts[level] = risk_counts.get(level, 0) + 1
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(risk_counts.keys()),
            y=list(risk_counts.values()),
            marker_color=[BRAND_COLORS[f"{level.lower()}_{'red' if level=='CRITICAL' else 'orange' if level=='HIGH' else 'yellow' if level=='MEDIUM' else 'green'}"] for level in risk_counts.keys()],
            text=list(risk_counts.values()),
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Risk Level Distribution",
        title_font_size=20,
        title_font_color=BRAND_COLORS["text_dark"],
        xaxis_title="Risk Level",
        yaxis_title="Number of Events",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12, color=BRAND_COLORS["text_dark"]),
        height=400
    )
    
    return fig

def create_threat_timeline(events_data):
    df = pd.DataFrame([{
        'date': datetime.strptime(event['date'], '%Y-%m-%d'),
        'title': event['title'],
        'risk_level': event['analysis']['risk_assessment']['risk_level'],
        'risk_score': event['analysis']['risk_assessment']['risk_score'],
        'location': event['location']
    } for event in events_data])
    
    color_map = {
        'CRITICAL': BRAND_COLORS["critical_red"],
        'HIGH': BRAND_COLORS["high_orange"], 
        'MEDIUM': BRAND_COLORS["medium_yellow"],
        'LOW': BRAND_COLORS["low_green"]
    }
    
    fig = px.scatter(df, x='date', y='risk_score', 
                     color='risk_level',
                     size='risk_score',
                     hover_data=['title', 'location'],
                     color_discrete_map=color_map,
                     title="Threat Timeline & Risk Evolution")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12, color=BRAND_COLORS["text_dark"]),
        height=500
    )
    
    return fig

def create_geographic_risk_map(events_data):
    location_data = {}
    for event in events_data:
        location = event['location']
        if location not in location_data:
            location_data[location] = {
                'events': 0,
                'max_risk': 0,
                'avg_risk': 0,
                'total_risk': 0
            }
        
        risk_score = event['analysis']['risk_assessment']['risk_score']
        location_data[location]['events'] += 1
        location_data[location]['total_risk'] += risk_score
        location_data[location]['max_risk'] = max(location_data[location]['max_risk'], risk_score)
        location_data[location]['avg_risk'] = location_data[location]['total_risk'] / location_data[location]['events']
    
    locations = list(location_data.keys())
    avg_risks = [location_data[loc]['avg_risk'] for loc in locations]
    event_counts = [location_data[loc]['events'] for loc in locations]
    
    fig = go.Figure(data=[
        go.Bar(
            x=locations,
            y=avg_risks,
            marker_color=[BRAND_COLORS["critical_red"] if risk >= 15 else BRAND_COLORS["high_orange"] if risk >= 10 else BRAND_COLORS["medium_yellow"] if risk >= 5 else BRAND_COLORS["low_green"] for risk in avg_risks],
            text=[f"{count} events" for count in event_counts],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Geographic Risk Assessment",
        title_font_size=20,
        title_font_color=BRAND_COLORS["text_dark"],
        xaxis_title="Location",
        yaxis_title="Average Risk Score",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12, color=BRAND_COLORS["text_dark"]),
        height=400
    )
    
    return fig

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        with open('corporate_data.json', 'r', encoding='utf-8') as f:
            corporate = json.load(f)
        events = analyze_events_from_file('events.json')
        with open('indicators.json', 'r', encoding='utf-8') as f:
            indicators = json.load(f)
        return corporate, events, indicators
    except Exception as e:
        st.error(f"A critical data file is missing or corrupted: {e}")
        st.stop()

# --- MAIN APPLICATION ---
def main():
    # Page Configuration
    st.set_page_config(
        page_title="CG - Global Security Intelligence", 
        page_icon="🛡️", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Load data
    corporate_data, events_data, indicators_data = load_data()
    
    # Travel Brief Display (Top Priority when Active)
    if hasattr(st.session_state, 'show_travel_brief') and st.session_state.show_travel_brief:
        st.markdown(f"""
        <div class="alert-container alert-danger">
            <h2>🚨 EXECUTIVE TRAVEL INTELLIGENCE BRIEF</h2>
            <h3>Destination: {st.session_state.travel_destination} | Role: {st.session_state.travel_role}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_brief1, col_brief2 = st.columns([2, 1])
        
        with col_brief1:
            st.markdown("#### 🔍 LAV-Specific Threat Assessment")
            
            # Location-specific LAV intelligence
            if "milan" in st.session_state.travel_destination.lower():
                st.markdown("""
                <div class="alert-container alert-danger">
                    <strong>🚨 HIGH THREAT: LAV HEADQUARTERS PROXIMITY</strong><br>
                    • Milan = LAV operational headquarters<br>
                    • Executive surveillance risk: CRITICAL<br>
                    • Supplier meeting security: Enhanced protocols required<br>
                    • Recommendation: Alternative meeting locations outside Milan center
                </div>
                """, unsafe_allow_html=True)
            elif "romania" in st.session_state.travel_destination.lower():
                st.markdown("""
                <div class="alert-container alert-danger">
                    <strong>🏭 FACILITY INFILTRATION ALERT</strong><br>
                    • Paola Confectii = Critical European manufacturing asset<br>
                    • Infiltration attempts: HIGH PROBABILITY<br>
                    • Supply chain intelligence gathering: Expected<br>
                    • Coordinate all visits with facility security
                </div>
                """, unsafe_allow_html=True)
            else:
                # Check for location-specific threats in events
                found_relevant_event = False
                for event in events_data:
                    if st.session_state.travel_destination.split(',')[0] in event['location']:
                        st.markdown(f"""
                        <div class="alert-container alert-danger">
                            <strong>🚨 CURRENT THREAT ALERT:</strong><br>
                            <strong>{event['title']}</strong><br>
                            {event['details']}
                        </div>
                        """, unsafe_allow_html=True)
                        found_relevant_event = True
                
                if not found_relevant_event:
                    st.markdown("""
                    <div class="alert-container alert-success">
                        <strong>✅ No Direct LAV Threats Identified</strong><br>
                        No specific LAV operations detected for this location.
                    </div>
                    """, unsafe_allow_html=True)
            
            # Enhanced security protocols
            st.markdown("#### 🛡️ Enhanced Security Protocols")
            st.markdown("""
            **Counter-Surveillance Measures:**
            - Maintain operational security regarding RDS supplier meetings
            - Use non-company transportation for sensitive locations
            - Avoid discussion of supply chain details in public areas
            - Report any surveillance attempts immediately
            
            **Communication Security:**
            - Use encrypted channels for supplier coordination
            - Avoid predictable travel patterns
            - Brief security team on all facility visits
            """)
        
        with col_brief2:
            st.markdown("#### 📞 Emergency Contacts")
            st.json({
                "Global Security 24/7": "+1-416-555-0100",
                "Local Security Coordinator": "See pre-travel package",
                "LAV Threat Hotline": "+1-416-555-0199"
            })
            
            st.markdown("#### 🎯 LAV Intelligence Summary")
            st.markdown("""
            **Threat Level:** HIGH  
            **Primary Concern:** RDS compliance monitoring  
            **Moncler Precedent:** 70% success rate  
            **Timeline Risk:** Next 6 months critical
            """)
            
            if st.button("🔄 Generate New Brief", use_container_width=True):
                st.session_state.show_travel_brief = False
                st.rerun()
        
        st.markdown("---")
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Canada Goose Global Security Intelligence Platform</h1>
        <p>LAV Counter-Intelligence • RDS Supply Chain Monitoring • Executive Protection</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{corporate_data['store_locations']['total_stores']}</div>
            <div class="metric-label">Stores Monitored</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        high_risk_events = sum(1 for e in events_data if e['analysis']['risk_assessment']['risk_level'] in ["HIGH", "CRITICAL"])
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: {BRAND_COLORS['accent_red']}">{high_risk_events}</div>
            <div class="metric-label">High-Risk Events</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_risk_score = sum(e['analysis']['risk_assessment']['risk_score'] for e in events_data)
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{total_risk_score}</div>
            <div class="metric-label">Total Risk Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{corporate_data['key_financials']['focus_market']}</div>
            <div class="metric-label">Key Market Focus</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # LAV Counter-Intelligence Analysis (Core Focus)
    st.markdown("### 🕵️ LAV Counter-Intelligence: Post-Fur Strategy Threat Assessment")
    
    # Highlight the core LAV intelligence
    st.markdown("""
    <div class="alert-container alert-danger">
        <strong>🎯 INTELLIGENCE FOCUS: LAV Activist Group Analysis</strong><br>
        Following Canada Goose's 2022 fur-free commitment, LAV (Italy) has shifted tactics from fur protests to 
        <strong>RDS down supply chain compliance monitoring</strong>. Intelligence indicates high probability of 
        coordinated investigation operations targeting manufacturing facilities and supplier relationships.
    </div>
    """, unsafe_allow_html=True)
    
    # Add Moncler precedent context
    col_precedent1, col_precedent2 = st.columns(2)
    
    with col_precedent1:
        st.markdown("""
        **🔍 MONCLER PRECEDENT (2022):**
        - LAV successfully pressured Moncler to commit to RDS certification
        - Tactics: Facility surveillance, supplier infiltration, executive tracking
        - Timeline: 8-month coordinated campaign
        - Success Rate: 70% compliance achievement
        """)
    
    with col_precedent2:
        st.markdown("""
        **⚡ CURRENT THREAT INDICATORS:**
        - Milan expansion plans = LAV headquarters proximity
        - Romania facility = High infiltration risk
        - Executive travel patterns = Surveillance opportunities
        - RDS certification gaps = Campaign vulnerability
        """)
    
    st.markdown("### 📊 Predictive Threat Analysis: Indicators & Warnings")
    
    for threat in indicators_data['threats']:
        triggered_count = 0
        for indicator in threat['indicators']:
            if "RDS" in indicator['description'] or "media" in indicator['description']:
                indicator['status'] = "YELLOW"
                triggered_count += 1
        
        # Determine threat status
        if triggered_count >= threat['warning_threshold']:
            threat_status = "CRITICAL"
            threat_color = BRAND_COLORS["critical_red"]
        elif triggered_count >= threat['warning_threshold'] - 1:
            threat_status = "WARNING" 
            threat_color = BRAND_COLORS["high_orange"]
        else:
            threat_status = "NORMAL"
            threat_color = BRAND_COLORS["low_green"]
        
        with st.expander(f"**{threat['threat_name']}** - Status: **{threat_status}**"):
            col_left, col_right = st.columns([2, 1])
            
            with col_left:
                st.write(f"**Warning Threshold:** {threat['warning_threshold']} indicators")
                
                for indicator in threat['indicators']:
                    status_class = f"status-{indicator['status'].lower()}"
                    # Fix the color selection logic
                    status_color_key = f"{indicator['status'].lower()}_{'red' if indicator['status']=='RED' else 'yellow' if indicator['status']=='YELLOW' else 'green'}"
                    status_color = BRAND_COLORS.get(status_color_key, BRAND_COLORS["text_dark"])
                    
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0;">
                        <span class="status-indicator {status_class}"></span>
                        {indicator['description']} 
                        <strong style="color: {status_color}">
                            ({indicator['status']})
                        </strong>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_right:
                # Progress indicator
                progress = triggered_count / threat['warning_threshold']
                st.metric("Triggered Indicators", f"{triggered_count}/{len(threat['indicators'])}")
                st.progress(progress)
                
                if triggered_count >= threat['warning_threshold']:
                    st.markdown(f"""
                    <div class="alert-container alert-danger">
                        <strong>⚠️ WARNING THRESHOLD EXCEEDED</strong><br>
                        Proactive mitigation protocols should be initiated.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="alert-container alert-success">
                        <strong>✅ Threat Level Normal</strong><br>
                        Standard monitoring in effect.
                    </div>
                    """, unsafe_allow_html=True)
    
    # Analytics Dashboard
    st.markdown("### 📊 Intelligence Analytics Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["🌍 Geographic Analysis", "📈 Risk Trends", "📡 Live Intelligence Feed"])
    
    with tab1:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.plotly_chart(create_risk_distribution_chart(events_data), use_container_width=True)
        
        with col_chart2:
            st.plotly_chart(create_geographic_risk_map(events_data), use_container_width=True)
        
        # Simple asset map
        st.subheader("Global Asset Map")
        map_data = pd.DataFrame([
            {"lat": 43.6532, "lon": -79.3832, "location": "Toronto HQ", "risk": "Medium"},
            {"lat": 40.7128, "lon": -74.0060, "location": "New York Flagship", "risk": "High"},
            {"lat": 51.5074, "lon": -0.1278, "location": "London Flagship", "risk": "High"},
            {"lat": 48.8566, "lon": 2.3522, "location": "Paris Flagship", "risk": "High"},
            {"lat": 39.9042, "lon": 116.4074, "location": "Beijing Flagship", "risk": "High"},
            {"lat": 45.4642, "lon": 9.1900, "location": "Milan (Expansion)", "risk": "High"},
        ])
        st.map(map_data)
    
    with tab2:
        st.plotly_chart(create_threat_timeline(events_data), use_container_width=True)
        
        # Risk trend analysis
        st.markdown("#### Risk Trend Analysis")
        trend_data = []
        for event in sorted(events_data, key=lambda x: x['date']):
            trend_data.append({
                'Date': event['date'],
                'Cumulative Risk': sum(e['analysis']['risk_assessment']['risk_score'] 
                                     for e in events_data 
                                     if e['date'] <= event['date'])
            })
        
        df_trend = pd.DataFrame(trend_data)
        fig_trend = px.line(df_trend, x='Date', y='Cumulative Risk', 
                           title="Cumulative Risk Score Over Time",
                           line_shape='spline')
        fig_trend.update_traces(line_color=BRAND_COLORS["accent_red"], line_width=3)
        fig_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial", size=12, color=BRAND_COLORS["text_dark"])
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with tab3:
        st.markdown("#### Live Intelligence Feed")
        
        for event in sorted(events_data, key=lambda x: x['date'], reverse=True):
            level = event['analysis']['risk_assessment']['risk_level']
            score = event['analysis']['risk_assessment']['risk_score']
            
            risk_class = f"risk-{level.lower()}"
            
            st.markdown(f"""
            <div class="risk-card {risk_class}">
                <h4 style="margin: 0 0 0.5rem 0; color: {BRAND_COLORS['text_dark']}">{event['title']}</h4>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <span><strong>Risk Level:</strong> 
                        <span class="status-indicator status-{level.lower()}"></span>
                        {level} (Score: {score})
                    </span>
                    <span style="color: {BRAND_COLORS['text_light']};">{event['date']}</span>
                </div>
                <p style="margin: 0.5rem 0; color: {BRAND_COLORS['text_light']};">
                    <strong>Location:</strong> {event['location']} | 
                    <strong>Type:</strong> {event['analysis']['threat_type']}
                </p>
                <p style="margin: 0; color: {BRAND_COLORS['text_dark']};">{event['details']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Travel Risk Assessment Sidebar
    with st.sidebar:
        st.markdown("### ✈️ Travel Risk Generator")
        st.markdown("---")
        
        destination_options = ["Milan, Italy", "Paris, France", "Toronto, ON", "Beijing, China", "New York, NY", "Romania"]
        destination = st.selectbox("Select Destination", destination_options)
        traveler_role = st.selectbox("Traveler Role", 
                                   ["Executive Leadership", "Supply Chain Manager", "Retail Operations"])
        
        if st.button("🚨 Generate Travel Brief", use_container_width=True):
            # This will be displayed in the main area
            st.session_state.show_travel_brief = True
            st.session_state.travel_destination = destination
            st.session_state.travel_role = traveler_role
    

if __name__ == "__main__":
    main()

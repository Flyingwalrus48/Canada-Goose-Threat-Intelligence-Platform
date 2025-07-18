# app_professional.py - Canada Goose Global Security Intelligence Platform
# Professional Enterprise-Grade Application with Modular Architecture

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

# --- CONFIGURATION & CONSTANTS ---
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

# --- UTILITY FUNCTIONS ---
def load_custom_css():
    """Load CSS from external file for cleaner code structure."""
    try:
        with open('style.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ style.css file not found. Using basic styling.")

def calculate_enhanced_risk_score(event: dict, threat_type: str) -> dict:
    """Calculate sophisticated risk scores with location-based adjustments."""
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

def analyze_events_from_file(filepath):
    """Load and analyze events with enhanced risk scoring."""
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

# --- REUSABLE UI COMPONENTS ---
def display_metric(label: str, value: str, color: str = "#2C3E50") -> None:
    """Reusable metric card component."""
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value" style="color: {color}">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def display_intelligence_card(event: dict) -> None:
    """Reusable intelligence feed card component."""
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

def display_alert(message: str, alert_type: str = "warning") -> None:
    """Reusable alert component."""
    st.markdown(f"""
    <div class="alert-container alert-{alert_type}">
        {message}
    </div>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_application_data():
    """Centralized data loading with error handling."""
    try:
        with open('corporate_data.json', 'r', encoding='utf-8') as f:
            corporate = json.load(f)
        events = analyze_events_from_file('events.json')
        with open('indicators.json', 'r', encoding='utf-8') as f:
            indicators = json.load(f)
        return corporate, events, indicators
    except Exception as e:
        st.error(f"Critical data loading error: {e}")
        st.stop()

# --- VISUALIZATION FUNCTIONS ---
def create_professional_map(events_data):
    """Create an enhanced Plotly Scattermapbox with professional styling."""
    # Prepare map data
    map_locations = [
        {"name": "Toronto HQ", "lat": 43.6532, "lon": -79.3832, "risk": "MEDIUM", "type": "Headquarters"},
        {"name": "New York Flagship", "lat": 40.7128, "lon": -74.0060, "risk": "HIGH", "type": "Flagship Store"},
        {"name": "London Flagship", "lat": 51.5074, "lon": -0.1278, "risk": "HIGH", "type": "Flagship Store"},
        {"name": "Paris Flagship", "lat": 48.8566, "lon": 2.3522, "risk": "HIGH", "type": "Flagship Store"},
        {"name": "Beijing Flagship", "lat": 39.9042, "lon": 116.4074, "risk": "HIGH", "type": "High Revenue Market"},
        {"name": "Milan (LAV HQ)", "lat": 45.4642, "lon": 9.1900, "risk": "CRITICAL", "type": "Threat Zone"},
        {"name": "Romania Facility", "lat": 44.8833, "lon": 25.8000, "risk": "HIGH", "type": "Manufacturing"}
    ]
    
    # Color mapping for risk levels
    color_map = {
        "CRITICAL": BRAND_COLORS["critical_red"],
        "HIGH": BRAND_COLORS["high_orange"],
        "MEDIUM": BRAND_COLORS["medium_yellow"],
        "LOW": BRAND_COLORS["low_green"]
    }
    
    # Size mapping for risk levels
    size_map = {"CRITICAL": 20, "HIGH": 15, "MEDIUM": 12, "LOW": 10}
    
    fig = go.Figure()
    
    for location in map_locations:
        fig.add_trace(go.Scattermapbox(
            lat=[location["lat"]],
            lon=[location["lon"]],
            mode='markers',
            marker=dict(
                size=size_map[location["risk"]],
                color=color_map[location["risk"]],
                opacity=0.8,
                sizemode='diameter'
            ),
            text=f"{location['name']}<br>Risk: {location['risk']}<br>Type: {location['type']}",
            hovertemplate="<b>%{text}</b><extra></extra>",
            name=location["risk"]
        ))
    
    fig.update_layout(
        mapbox=dict(
            accesstoken="pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A",
            style="carto-darkmatter",
            center=dict(lat=45, lon=10),
            zoom=1.5
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255,255,255,0.8)"
        ),
        height=500,
        title=dict(
            text="Canada Goose Global Security Asset Map",
            font=dict(size=18, color=BRAND_COLORS["text_dark"])
        )
    )
    
    return fig

def create_risk_distribution_chart(events_data):
    """Enhanced risk distribution visualization."""
    risk_counts = {}
    for event in events_data:
        level = event['analysis']['risk_assessment']['risk_level']
        risk_counts[level] = risk_counts.get(level, 0) + 1
    
    colors = [BRAND_COLORS[f"{level.lower()}_{'red' if level=='CRITICAL' else 'orange' if level=='HIGH' else 'yellow' if level=='MEDIUM' else 'green'}"] 
              for level in risk_counts.keys()]
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(risk_counts.keys()),
            y=list(risk_counts.values()),
            marker_color=colors,
            text=list(risk_counts.values()),
            textposition='auto',
            hovertemplate="<b>%{x}</b><br>Events: %{y}<extra></extra>"
        )
    ])
    
    fig.update_layout(
        title="Risk Level Distribution",
        title_font_size=18,
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
    """Interactive threat timeline with enhanced hover data."""
    df = pd.DataFrame([{
        'date': datetime.strptime(event['date'], '%Y-%m-%d'),
        'title': event['title'],
        'risk_level': event['analysis']['risk_assessment']['risk_level'],
        'risk_score': event['analysis']['risk_assessment']['risk_score'],
        'location': event['location'],
        'threat_type': event['analysis']['threat_type']
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
                     hover_data={'title': True, 'location': True, 'threat_type': True},
                     color_discrete_map=color_map,
                     title="Threat Evolution Timeline")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12, color=BRAND_COLORS["text_dark"]),
        height=500
    )
    
    return fig

# --- SECTION RENDERING FUNCTIONS ---
def render_header():
    """Render the main application header."""
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Canada Goose Global Security Intelligence Platform</h1>
        <p>LAV Counter-Intelligence • RDS Supply Chain Monitoring • Executive Protection</p>
    </div>
    """, unsafe_allow_html=True)

def render_travel_brief():
    """Render travel brief section if active."""
    if hasattr(st.session_state, 'show_travel_brief') and st.session_state.show_travel_brief:
        st.markdown(f"""
        <div class="travel-brief-header">
            <h2>🚨 EXECUTIVE TRAVEL INTELLIGENCE BRIEF</h2>
            <h3>Destination: {st.session_state.travel_destination} | Role: {st.session_state.travel_role}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_brief1, col_brief2 = st.columns([2, 1])
        
        with col_brief1:
            st.markdown("#### 🔍 LAV-Specific Threat Assessment")
            
            if "milan" in st.session_state.travel_destination.lower():
                display_alert("""
                <strong>🚨 HIGH THREAT: LAV HEADQUARTERS PROXIMITY</strong><br>
                • Milan = LAV operational headquarters<br>
                • Executive surveillance risk: CRITICAL<br>
                • Supplier meeting security: Enhanced protocols required<br>
                • Recommendation: Alternative meeting locations outside Milan center
                """, "danger")
            elif "romania" in st.session_state.travel_destination.lower():
                display_alert("""
                <strong>🏭 FACILITY INFILTRATION ALERT</strong><br>
                • Paola Confectii = Critical European manufacturing asset<br>
                • Infiltration attempts: HIGH PROBABILITY<br>
                • Supply chain intelligence gathering: Expected<br>
                • Coordinate all visits with facility security
                """, "danger")
            else:
                display_alert("""
                <strong>✅ No Direct LAV Threats Identified</strong><br>
                No specific LAV operations detected for this location.
                """, "success")
            
            st.markdown("""
            #### 🛡️ Enhanced Security Protocols
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
            
            st.markdown("""
            <div class="intelligence-summary">
                <h4>🎯 LAV Intelligence Summary</h4>
                <strong>Threat Level:</strong> HIGH<br>
                <strong>Primary Concern:</strong> RDS compliance monitoring<br>
                <strong>Moncler Precedent:</strong> 70% success rate<br>
                <strong>Timeline Risk:</strong> Next 6 months critical
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Generate New Brief", use_container_width=True):
                st.session_state.show_travel_brief = False
                st.rerun()
        
        st.markdown("---")

def render_key_metrics(events_data, corporate_data):
    """Render key performance metrics."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        display_metric("Stores Monitored", str(corporate_data['store_locations']['total_stores']))
    
    with col2:
        high_risk_events = sum(1 for e in events_data if e['analysis']['risk_assessment']['risk_level'] in ["HIGH", "CRITICAL"])
        display_metric("High-Risk Events", str(high_risk_events), BRAND_COLORS['accent_red'])
    
    with col3:
        total_risk_score = sum(e['analysis']['risk_assessment']['risk_score'] for e in events_data)
        display_metric("Total Risk Score", str(total_risk_score))
    
    with col4:
        display_metric("Key Market Focus", corporate_data['key_financials']['focus_market'])

def render_lav_analysis(indicators_data):
    """Render LAV counter-intelligence analysis."""
    st.markdown("### 🕵️ LAV Counter-Intelligence: Post-Fur Strategy Threat Assessment")
    
    display_alert("""
    <strong>🎯 INTELLIGENCE FOCUS: LAV Activist Group Analysis</strong><br>
    Following Canada Goose's 2022 fur-free commitment, LAV (Italy) has shifted tactics from fur protests to 
    <strong>RDS down supply chain compliance monitoring</strong>. Intelligence indicates high probability of 
    coordinated investigation operations targeting manufacturing facilities and supplier relationships.
    """, "danger")
    
    col_precedent1, col_precedent2 = st.columns(2)
    
    with col_precedent1:
        st.markdown("""
        <div class="precedent-card">
            <h4>🔍 MONCLER PRECEDENT (2022):</h4>
            <ul>
                <li>LAV successfully pressured Moncler to commit to RDS certification</li>
                <li>Tactics: Facility surveillance, supplier infiltration, executive tracking</li>
                <li>Timeline: 8-month coordinated campaign</li>
                <li>Success Rate: 70% compliance achievement</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_precedent2:
        st.markdown("""
        <div class="lav-intelligence-card">
            <h4>⚡ CURRENT THREAT INDICATORS:</h4>
            <ul>
                <li>Milan expansion plans = LAV headquarters proximity</li>
                <li>Romania facility = High infiltration risk</li>
                <li>Executive travel patterns = Surveillance opportunities</li>
                <li>RDS certification gaps = Campaign vulnerability</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def render_predictive_analysis(indicators_data):
    """Render predictive threat analysis section."""
    st.markdown("### 📊 Predictive Threat Analysis: Indicators & Warnings")
    
    for threat in indicators_data['threats']:
        triggered_count = 0
        for indicator in threat['indicators']:
            if "RDS" in indicator['description'] or "media" in indicator['description']:
                indicator['status'] = "YELLOW"
                triggered_count += 1
        
        threat_status = "CRITICAL" if triggered_count >= threat['warning_threshold'] else "WARNING" if triggered_count >= threat['warning_threshold'] - 1 else "NORMAL"
        
        with st.expander(f"**{threat['threat_name']}** - Status: **{threat_status}**"):
            col_left, col_right = st.columns([2, 1])
            
            with col_left:
                st.write(f"**Warning Threshold:** {threat['warning_threshold']} indicators")
                
                for indicator in threat['indicators']:
                    status_class = f"status-{indicator['status'].lower()}"
                    status_color_key = f"{indicator['status'].lower()}_{'red' if indicator['status']=='RED' else 'yellow' if indicator['status']=='YELLOW' else 'green'}"
                    status_color = BRAND_COLORS.get(status_color_key, BRAND_COLORS["text_dark"])
                    
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0;">
                        <span class="status-indicator {status_class}"></span>
                        {indicator['description']} 
                        <strong style="color: {status_color}">({indicator['status']})</strong>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_right:
                progress = triggered_count / threat['warning_threshold']
                st.metric("Triggered Indicators", f"{triggered_count}/{len(threat['indicators'])}")
                st.progress(progress)
                
                if triggered_count >= threat['warning_threshold']:
                    display_alert("<strong>⚠️ WARNING THRESHOLD EXCEEDED</strong><br>Proactive mitigation protocols should be initiated.", "danger")
                else:
                    display_alert("<strong>✅ Threat Level Normal</strong><br>Standard monitoring in effect.", "success")

def render_analytics_dashboard(events_data):
    """Render interactive analytics dashboard."""
    st.markdown("### 📊 Intelligence Analytics Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["🌍 Geographic Analysis", "📈 Risk Trends", "📡 Live Intelligence Feed"])
    
    with tab1:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.plotly_chart(create_risk_distribution_chart(events_data), use_container_width=True)
        
        with col_chart2:
            # Professional map
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            st.plotly_chart(create_professional_map(events_data), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.plotly_chart(create_threat_timeline(events_data), use_container_width=True)
        
        # Risk trend analysis
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
        render_enhanced_intelligence_feed(events_data)

def render_enhanced_intelligence_feed(events_data):
    """Render enhanced intelligence feed with filters."""
    st.markdown("#### Live Intelligence Feed")
    
    # Filter controls
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        risk_filter = st.multiselect(
            "Filter by Risk Level",
            options=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            default=["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        )
    
    with col_filter2:
        search_term = st.text_input("Search in title/details", placeholder="Enter search term...")
    
    with col_filter3:
        location_filter = st.selectbox(
            "Filter by Location",
            options=["All Locations"] + list(set(event['location'] for event in events_data))
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_events = events_data
    
    # Risk level filter
    if risk_filter:
        filtered_events = [e for e in filtered_events if e['analysis']['risk_assessment']['risk_level'] in risk_filter]
    
    # Search filter
    if search_term:
        filtered_events = [e for e in filtered_events if 
                          search_term.lower() in e['title'].lower() or 
                          search_term.lower() in e['details'].lower()]
    
    # Location filter
    if location_filter != "All Locations":
        filtered_events = [e for e in filtered_events if e['location'] == location_filter]
    
    # Display filtered results
    st.write(f"**Showing {len(filtered_events)} of {len(events_data)} events**")
    
    for event in sorted(filtered_events, key=lambda x: x['date'], reverse=True):
        display_intelligence_card(event)

def render_travel_controls():
    """Render travel risk assessment controls in sidebar."""
    with st.sidebar:
        st.markdown("### ✈️ Travel Risk Generator")
        st.markdown("---")
        
        destination_options = ["Milan, Italy", "Paris, France", "Toronto, ON", "Beijing, China", "New York, NY", "Romania"]
        destination = st.selectbox("Select Destination", destination_options)
        traveler_role = st.selectbox("Traveler Role", 
                                   ["Executive Leadership", "Supply Chain Manager", "Retail Operations"])
        
        if st.button("🚨 Generate Travel Brief", use_container_width=True):
            st.session_state.show_travel_brief = True
            st.session_state.travel_destination = destination
            st.session_state.travel_role = traveler_role
            st.rerun()

# --- MAIN APPLICATION ---
def main():
    """Main application orchestrator with clean, modular structure."""
    # Page Configuration
    st.set_page_config(
        page_title="CG - Global Security Intelligence", 
        page_icon="🛡️", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load styling and data
    load_custom_css()
    corporate_data, events_data, indicators_data = load_application_data()
    
    # Render application sections
    render_travel_brief()  # Top priority when active
    render_header()
    render_key_metrics(events_data, corporate_data)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    render_lav_analysis(indicators_data)
    render_predictive_analysis(indicators_data)
    render_analytics_dashboard(events_data)
    render_travel_controls()

if __name__ == "__main__":
    main()

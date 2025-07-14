# app_enhanced.py - Complete Enhanced Canada Goose Global Security Intelligence Platform
# Now with Activist Counter-Intelligence Prediction

import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta

# Import our enhanced backend modules
from nlp_engine import analyze_events_from_file
from travel_risk_analyzer import TravelRiskAnalyzer, predict_travel_impacts
from geopolitical_intelligence import GeopoliticalIntelligenceMonitor, get_geopolitical_context

# Import the new counter-intelligence predictor
try:
    from activist_counter_intelligence_predictor import (
        ActivistCounterIntelligencePredictor,
        get_activist_intelligence_summary,
        get_travel_security_enhancements
    )

    COUNTER_INTEL_AVAILABLE = True
except ImportError:
    COUNTER_INTEL_AVAILABLE = False
    st.error(
        "⚠️ Counter-Intelligence module not found. Please ensure activist_counter_intelligence_predictor.py is in your project folder.")

# --- Page Configuration ---
st.set_page_config(
    page_title="CG - Global Security Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# --- Enhanced Custom Styling ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 8px solid #E6332A;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .main-header h1, .main-header p { color: white; }

    .metric-card {
        background: #2c3e50;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #E6332A;
        color: white;
        text-align: center;
    }

    .travel-risk-card {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        color: white;
        margin: 1rem 0;
    }

    .counter-intel-card {
        background: linear-gradient(135deg, #8e44ad, #9b59b6);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #e74c3c;
        color: white;
        margin: 1rem 0;
    }

    .geopolitical-alert {
        background: rgba(231, 76, 60, 0.1);
        border-left: 4px solid #e74c3c;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }

    .business-critical {
        background: rgba(52, 152, 219, 0.1);
        border-left: 4px solid #3498db;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }

    .executive-brief {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }

    .prediction-alert {
        background: rgba(142, 68, 173, 0.1);
        border-left: 4px solid #8e44ad;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }

    .risk-critical { background-color: rgba(220, 53, 69, 0.1); border-left-color: #dc3545; }
    .risk-high { background-color: rgba(255, 193, 7, 0.1); border-left-color: #ffc107; }
    .risk-medium { background-color: rgba(255, 193, 7, 0.1); border-left-color: #fd7e14; }
    .risk-low { background-color: rgba(40, 167, 69, 0.1); border-left-color: #28a745; }
</style>
""", unsafe_allow_html=True)


# --- Data Loading (Enhanced) ---
@st.cache_data
def load_all_data():
    """Load all necessary data and initialize intelligence systems"""
    try:
        # Load existing data files
        with open('corporate_data.json', 'r') as f:
            corporate_data = json.load(f)
        with open('emergency_action_plans.json', 'r') as f:
            eaps = json.load(f)

        # Analyze events with enhanced NLP
        analyzed_events = analyze_events_from_file('events.json')

        # Initialize travel risk analyzer
        travel_analyzer = TravelRiskAnalyzer()

        # Initialize geopolitical monitor
        geopolitical_monitor = GeopoliticalIntelligenceMonitor()

        return corporate_data, analyzed_events, eaps, travel_analyzer, geopolitical_monitor

    except FileNotFoundError as e:
        st.error(f"FATAL ERROR: Missing data file - {e}. Please ensure all .json files exist.")
        st.stop()


# --- Enhanced Data Loading ---
corporate_data, analyzed_events, eaps, travel_analyzer, geo_monitor = load_all_data()

# --- Enhanced Header ---
st.markdown("""
<div class="main-header">
    <h1>🛡️ Canada Goose Global Security Intelligence Platform</h1>
    <p>Travel Risk Management • Geopolitical Intelligence • Business-Critical Location Monitoring • Predictive Threat Analysis</p>
    <small style="color: #cccccc;">Advanced Travel Intelligence & Counter-Intelligence Threat Assessment System</small>
</div>
""", unsafe_allow_html=True)

# --- Executive Summary with Enhanced Intelligence ---
st.subheader("📊 Executive Intelligence Dashboard")

# Enhanced metrics with counter-intelligence data
total_stores = corporate_data['store_locations']['total_stores']
high_risk_events_count = sum(1 for event in analyzed_events if event['analysis']['risk_assessment']['risk_score'] >= 15)
market_focus = corporate_data['key_financials']['focus_market']
china_revenue_pct = corporate_data['key_financials']['revenue_from_greater_china_pct']

# Get travel risk overview
travel_overview = travel_analyzer.get_global_risk_overview()
high_risk_locations = len(travel_overview["high_risk_locations"])

# Get geopolitical intelligence summary
geo_summary = geo_monitor.get_current_intelligence_summary()
geopolitical_alerts = geo_summary["alert_counts"]["high_priority"]

# Get counter-intelligence summary if available
counter_intel_alerts = 0
if COUNTER_INTEL_AVAILABLE:
    activist_summary = get_activist_intelligence_summary()
    counter_intel_alerts = activist_summary["indicators_triggered"]

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(
        f'<div class="metric-card">Global Locations<br><strong style="font-size: 2em;">{total_stores}</strong><br><small>Business-Critical Sites</small></div>',
        unsafe_allow_html=True)

with col2:
    st.markdown(
        f'<div class="metric-card">High-Risk Locations<br><strong style="font-size: 2em; color: #E6332A;">{high_risk_locations}</strong><br><small>Travel Risk ≥ 6.0</small></div>',
        unsafe_allow_html=True)

with col3:
    st.markdown(
        f'<div class="metric-card">Geopolitical Alerts<br><strong style="font-size: 2em; color: #f39c12;">{geopolitical_alerts}</strong><br><small>High Priority</small></div>',
        unsafe_allow_html=True)

with col4:
    st.markdown(
        f'<div class="metric-card">Counter-Intel Alerts<br><strong style="font-size: 2em; color: #8e44ad;">{counter_intel_alerts}</strong><br><small>I&W Indicators</small></div>',
        unsafe_allow_html=True)

with col5:
    st.markdown(
        f'<div class="metric-card">China Market<br><strong style="font-size: 2em;">{china_revenue_pct}%</strong><br><small>Revenue at Risk</small></div>',
        unsafe_allow_html=True)

with col6:
    st.markdown(
        f'<div class="metric-card">Active Events<br><strong style="font-size: 2em;">{high_risk_events_count}</strong><br><small>Security Incidents</small></div>',
        unsafe_allow_html=True)

# --- Enhanced Business Context Section ---
st.markdown("---")
st.subheader("🎯 Business Context & Geopolitical Intelligence")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="business-critical">', unsafe_allow_html=True)
    st.write("**Business-Critical Risk Factors (SEC Filings):**")
    for risk in corporate_data['stated_risk_factors']:
        st.write(f"• {risk}")

    st.write(f"\n**Key Financial Exposure:**")
    st.write(f"• Greater China Revenue: **{china_revenue_pct}%**")
    st.write(f"• Direct-to-Consumer: **{corporate_data['key_financials']['DTC_revenue_pct']}%**")
    st.info("🎯 Strategic Focus: Protecting high-value operations and China market access")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="business-critical">', unsafe_allow_html=True)
    st.write("**Current Geopolitical Intelligence:**")

    # Display high-priority geopolitical alerts
    if geo_summary["recent_high_impact_events"]:
        for event in geo_summary["recent_high_impact_events"]:
            priority_color = "#e74c3c" if event["priority"] == "HIGH" else "#f39c12"
            st.markdown(f"""
            <div style="background: rgba(231, 76, 60, 0.1); padding: 0.5rem; border-radius: 5px; margin: 0.3rem 0; border-left: 3px solid {priority_color};">
                <strong>{event['headline'][:60]}...</strong><br>
                <small>{event['region']} | {event['priority']} Priority</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No high-priority geopolitical alerts")

    st.markdown('</div>', unsafe_allow_html=True)

# --- NEW: Predictive Threat Analysis Section ---
if COUNTER_INTEL_AVAILABLE:
    st.markdown("---")
    st.subheader("🔮 Predictive Threat Analysis: Activist Counter-Intelligence")

    # Initialize the counter-intelligence predictor
    try:
        counter_intel_predictor = ActivistCounterIntelligencePredictor()
        activist_summary = get_activist_intelligence_summary()

        # Display current threat status
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown('<div class="counter-intel-card">', unsafe_allow_html=True)
            st.write("**🎯 INTELLIGENCE ASSESSMENT: Post-Fur Strategy Analysis**")

            # Threat level display with color coding
            threat_level = activist_summary["threat_level"]
            if threat_level == "HIGH":
                threat_color = "#e74c3c"
                threat_icon = "🔴"
            elif threat_level == "MEDIUM":
                threat_color = "#f39c12"
                threat_icon = "🟡"
            else:
                threat_color = "#27ae60"
                threat_icon = "🟢"

            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid {threat_color}; margin: 1rem 0;">
                <strong>{threat_icon} Current Threat Level: {threat_level}</strong><br>
                <small>Activist groups have shifted from fur protests to sophisticated RDS supply chain investigations</small>
            </div>
            """, unsafe_allow_html=True)

            st.write("**🔍 KEY INTELLIGENCE FINDINGS:**")
            st.write(
                "• **Moncler Precedent Confirmed**: LAV successfully pressured Moncler (2022) using identical tactics")
            st.write("• **Target Evolution**: Focus shifted from fur protests to down supply chain credibility")
            st.write("• **New TTPs**: Professional investigations, executive surveillance, facility infiltration")
            st.write("• **Geographic Focus**: Milan expansion and Romania manufacturing facility")

            st.write(
                f"**⚠️ High-Probability Operations Predicted**: {len(activist_summary['high_probability_operations'])}")
            for operation in activist_summary["high_probability_operations"]:
                st.write(f"  • {operation.replace('_', ' ').title()}")

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="travel-risk-card">', unsafe_allow_html=True)
            st.write("**📊 Indicators & Warnings Status**")

            # Get current indicators status
            current_assessment = counter_intel_predictor.assess_current_threat_level()
            indicator_summary = current_assessment["indicator_summary"]

            # Display indicator counts with visual elements
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <div style="margin: 0.5rem 0;">
                    <span style="color: #e74c3c; font-size: 1.2em;">🔴 RED: {indicator_summary["RED"]}</span>
                </div>
                <div style="margin: 0.5rem 0;">
                    <span style="color: #f39c12; font-size: 1.2em;">🟡 YELLOW: {indicator_summary["YELLOW"]}</span>
                </div>
                <div style="margin: 0.5rem 0;">
                    <span style="color: #27ae60; font-size: 1.2em;">🟢 GREEN: {indicator_summary["GREEN"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if current_assessment["executive_attention_required"]:
                st.error("🚨 EXECUTIVE ATTENTION REQUIRED")
            else:
                st.success("✅ Standard monitoring protocols")

            st.markdown('</div>', unsafe_allow_html=True)

        # Enhanced Indicators & Warnings Display
        st.write("#### 📈 Indicators & Warnings (I&W) Framework")

        # Create expandable sections for each indicator
        for indicator_id, indicator in counter_intel_predictor.counter_intel_indicators.items():

            # Color coding for status
            if indicator.current_status == "RED":
                status_color = "#e74c3c"
                status_icon = "🔴"
            elif indicator.current_status == "YELLOW":
                status_color = "#f39c12"
                status_icon = "🟡"
            else:
                status_color = "#27ae60"
                status_icon = "🟢"

            # Trend arrows
            if indicator.trend == "INCREASING":
                trend_icon = "📈"
            elif indicator.trend == "DECREASING":
                trend_icon = "📉"
            else:
                trend_icon = "➡️"

            with st.expander(f"{status_icon} {indicator.description} ({indicator.current_status})"):
                col_a, col_b = st.columns(2)

                with col_a:
                    st.write(f"**Status:** {indicator.current_status}")
                    st.write(f"**Trend:** {trend_icon} {indicator.trend}")
                    st.write(f"**Confidence:** {indicator.confidence_level}%")
                    st.write(f"**Last Updated:** {indicator.last_updated.strftime('%Y-%m-%d %H:%M')}")

                with col_b:
                    st.write(f"**Trigger Threshold:**")
                    st.write(f"{indicator.trigger_threshold}")
                    st.write(f"**Impact Assessment:**")
                    st.write(f"{indicator.impact_assessment}")

        # Operation Predictions Section
        st.write("#### 🎯 High-Probability Operation Predictions")

        # Milan RDS Investigation Prediction
        milan_prediction = counter_intel_predictor.generate_operation_prediction("MILAN_RDS_INVESTIGATION")

        st.markdown(f"""
        <div class="prediction-alert">
            <h5>🇮🇹 MILAN RDS INVESTIGATION OPERATION</h5>
            <strong>Prediction Confidence:</strong> {int(milan_prediction['prediction_confidence'] * 100)}%<br>
            <strong>Moncler Precedent Similarity:</strong> {int(milan_prediction['moncler_precedent_similarity'] * 100)}%<br>
            <strong>Timeline:</strong> {milan_prediction['predicted_timeline']['predicted_start']} to {milan_prediction['predicted_timeline']['predicted_end']}<br>
            <strong>Days Until Start:</strong> {milan_prediction['predicted_timeline']['days_until_start']} days
        </div>
        """, unsafe_allow_html=True)

        col_x, col_y = st.columns(2)

        with col_x:
            st.write("**Predicted Tactics:**")
            for ttp in milan_prediction['operation_details']['likely_ttps']:
                st.write(f"• {ttp}")

        with col_y:
            st.write("**Warning Indicators:**")
            for indicator in milan_prediction['operation_details']['indicators']:
                st.write(f"• {indicator}")

        # Romania Facility Threat Assessment
        romania_prediction = counter_intel_predictor.generate_operation_prediction("ROMANIA_INFILTRATION_ATTEMPT")

        st.markdown(f"""
        <div class="business-critical">
            <h5>🇷🇴 ROMANIA FACILITY INFILTRATION THREAT</h5>
            <strong>Prediction Confidence:</strong> {int(romania_prediction['prediction_confidence'] * 100)}%<br>
            <strong>Target:</strong> Paola Confectii Manufacturing Facility (Titu)<br>
            <strong>Business Impact:</strong> {romania_prediction['operation_details']['business_impact']}<br>
            <strong>Primary Objective:</strong> {romania_prediction['operation_details']['objectives'][0]}
        </div>
        """, unsafe_allow_html=True)

        # Immediate Action Recommendations
        st.write("#### ⚡ Immediate Action Recommendations")

        priority_actions = [
            "🛡️ **Enhanced Executive Travel Security**: Implement counter-surveillance protocols for supply chain personnel traveling to Milan and Romania",
            "🔒 **Facility Security Upgrade**: Review and enhance access controls at Romania facility with focus on infiltration prevention",
            "📱 **Secure Communications**: Establish encrypted communication protocols for all supplier-related discussions",
            "👥 **Personnel Security Awareness**: Conduct counter-surveillance training for executives involved in supply chain operations",
            "🌐 **Alternative Meeting Protocols**: Develop secure, off-site meeting procedures for sensitive supplier engagements"
        ]

        for action in priority_actions:
            st.markdown(f"• {action}")

    except Exception as e:
        st.error(f"Counter-Intelligence Module Error: {e}")
        st.info("💡 Ensure activist_counter_intelligence_predictor.py is in the same directory as your main app.")

# Continue with existing sections...
st.markdown("---")

# --- Enhanced Global Situational Awareness ---
st.subheader("🌍 Global Travel Risk & Threat Landscape")

col1, col2 = st.columns([2, 1])

# Enhanced Global Map Section - Replace the existing map section in your app_enhanced.py

with col1:
    st.write("#### 🗺️ Business-Critical Location Risk Assessment")

    # Enhanced map with comprehensive global locations
    m = folium.Map(location=[45, 10], zoom_start=2, tiles="CartoDB positron")

    # COMPREHENSIVE Canada Goose global locations with accurate coordinates
    business_locations = {
        # --- GREATER CHINA (High Revenue Impact) ---
        "Shanghai, China": [31.2304, 121.4737],
        "Beijing, China": [39.9042, 116.4074],
        "Hong Kong": [22.3193, 114.1694],

        # --- NORTH AMERICA (HQ & Manufacturing) ---
        "Toronto, ON (HQ)": [43.6532, -79.3832],
        "Winnipeg, MB (Manufacturing)": [49.8951, -97.1384],
        "Montreal, QC (Manufacturing)": [45.5017, -73.5673],
        "New York, NY (Flagship)": [40.7589, -73.9851],
        "Chicago, IL": [41.8781, -87.6298],
        "Vancouver, BC": [49.2827, -123.1207],
        "Boston, MA": [42.3601, -71.0589],

        # --- EUROPE (Expansion Focus) ---
        "London, UK (Flagship)": [51.5074, -0.1278],
        "Paris, France (Flagship)": [48.8566, 2.3522],
        "Milan, Italy (Expansion)": [45.4642, 9.1900],  # NEW - Expansion target
        "Titu, Romania (Manufacturing)": [44.8833, 25.8000],  # NEW - Paola Confectii facility
        "Stockholm, Sweden": [59.3293, 18.0686],
        "Berlin, Germany": [52.5200, 13.4050],
        "Dublin, Ireland": [53.3498, -6.2603],
        "Zurich, Switzerland": [47.3769, 8.5417],

        # --- ASIA PACIFIC ---
        "Tokyo, Japan": [35.6762, 139.6503],
        "Seoul, South Korea": [37.5665, 126.9780],
        "Singapore": [1.3521, 103.8198],
        "Sydney, Australia": [33.8688, 151.2093],

        # --- ADDITIONAL MANUFACTURING LOCATIONS (Research these) ---
        "Scarborough, ON (Manufacturing)": [43.7764, -79.2318],
        "Boisbriand, QC (Manufacturing)": [45.6167, -73.8333],
    }

    # Enhanced location categorization for visual distinction
    location_categories = {
        # Critical business locations (red markers)
        "headquarters": ["Toronto, ON (HQ)"],
        "manufacturing": [
            "Winnipeg, MB (Manufacturing)",
            "Montreal, QC (Manufacturing)",
            "Titu, Romania (Manufacturing)",
            "Scarborough, ON (Manufacturing)",
            "Boisbriand, QC (Manufacturing)"
        ],
        "flagship_stores": [
            "New York, NY (Flagship)",
            "London, UK (Flagship)",
            "Paris, France (Flagship)"
        ],
        "expansion_targets": ["Milan, Italy (Expansion)"],
        "high_revenue_markets": ["Shanghai, China", "Beijing, China", "Hong Kong"],
        "standard_retail": [
            "Chicago, IL", "Vancouver, BC", "Boston, MA", "Stockholm, Sweden",
            "Berlin, Germany", "Dublin, Ireland", "Zurich, Switzerland",
            "Tokyo, Japan", "Seoul, South Korea", "Singapore", "Sydney, Australia"
        ]
    }

    # Color and icon mapping for different location types
    location_styling = {
        "headquarters": {"color": "darkred", "icon": "home", "size": "large"},
        "manufacturing": {"color": "red", "icon": "cog", "size": "medium"},
        "flagship_stores": {"color": "orange", "icon": "shopping-bag", "size": "medium"},
        "expansion_targets": {"color": "purple", "icon": "star", "size": "medium"},
        "high_revenue_markets": {"color": "darkblue", "icon": "usd", "size": "medium"},
        "standard_retail": {"color": "blue", "icon": "shopping-cart", "size": "small"}
    }

    # Add markers for each location
    for location, coords in business_locations.items():
        # Determine location category
        location_category = "standard_retail"  # default
        for category, locations in location_categories.items():
            if location in locations:
                location_category = category
                break

        # Get styling for this category
        styling = location_styling[location_category]

        # Get travel risk assessment for this location
        # Handle locations that might not be in travel analyzer
        location_name_clean = location.split(" (")[0]  # Remove parenthetical descriptions

        try:
            risk_assessment = travel_analyzer.assess_location_risk(location_name_clean)

            if "error" not in risk_assessment:
                risk_score = risk_assessment["overall_risk_score"]
                risk_level = risk_assessment["risk_level"]
                business_function = risk_assessment["business_function"]
                specific_threats = risk_assessment["specific_threats"]
                revenue_impact = risk_assessment["revenue_impact"]
            else:
                # Fallback data for locations not in travel analyzer
                risk_score = 4.0
                risk_level = "MEDIUM"
                business_function = "Business Operations"
                specific_threats = ["Standard business risks"]
                revenue_impact = "Regional market presence"
        except:
            # Fallback for any errors
            risk_score = 4.0
            risk_level = "MEDIUM"
            business_function = "Business Operations"
            specific_threats = ["Standard business risks"]
            revenue_impact = "Regional market presence"

        # Enhanced popup with comprehensive information
        popup_html = f"""
        <div style="width: 280px;">
            <h4 style="color: {styling['color']};">{location}</h4>
            <strong>Category:</strong> {location_category.replace('_', ' ').title()}<br>
            <strong>Business Function:</strong> {business_function}<br>
            <strong>Travel Risk Score:</strong> {risk_score:.1f}/10<br>
            <strong>Risk Level:</strong> {risk_level}<br>
            <strong>Revenue Impact:</strong> {revenue_impact}<br>
            <hr>
            <strong>Key Threats:</strong><br>
            {'<br>'.join(f"• {threat}" for threat in specific_threats[:2])}<br>
        """

        # Add special intelligence for key locations
        if "Milan" in location:
            popup_html += """
            <hr style="border-color: purple;">
            <strong style="color: purple;">🎯 EXPANSION INTELLIGENCE:</strong><br>
            • LAV headquarters location<br>
            • High activist surveillance risk<br>
            • Moncler precedent applies<br>
            """
        elif "Romania" in location:
            popup_html += """
            <hr style="border-color: red;">
            <strong style="color: red;">🏭 FACILITY INTELLIGENCE:</strong><br>
            • Paola Confectii acquisition (2023)<br>
            • Key European manufacturing asset<br>
            • Infiltration risk elevated<br>
            """
        elif "Shanghai" in location or "Beijing" in location:
            popup_html += """
            <hr style="border-color: darkblue;">
            <strong style="color: darkblue;">💰 REVENUE INTELLIGENCE:</strong><br>
            • 17.7% total revenue exposure<br>
            • Geopolitical tensions active<br>
            • Diplomatic risk monitoring<br>
            """

        popup_html += "</div>"

        # Determine marker size based on importance
        if location_category in ["headquarters", "manufacturing", "flagship_stores"]:
            marker_size = 12
        elif location_category in ["expansion_targets", "high_revenue_markets"]:
            marker_size = 10
        else:
            marker_size = 8

        # Create marker with enhanced styling
        folium.Marker(
            location=coords,
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(
                color=styling["color"],
                icon=styling["icon"],
                prefix='fa'
            ),
            tooltip=f"{location}: {risk_level} Risk | {location_category.replace('_', ' ').title()}"
        ).add_to(m)

    # Add special threat zones with circles
    # China tension zone
    folium.Circle(
        location=[35, 115],
        radius=800000,  # 800km radius
        popup="Greater China Market - 17.7% Revenue Exposure",
        color="red",
        fill=True,
        fillColor="red",
        fillOpacity=0.1,
        opacity=0.3
    ).add_to(m)

    # European activist zone
    folium.Circle(
        location=[45.4642, 9.1900],  # Milan center
        radius=300000,  # 300km radius
        popup="European Activist Activity Zone - LAV/PETA Focus",
        color="purple",
        fill=True,
        fillColor="purple",
        fillOpacity=0.1,
        opacity=0.3
    ).add_to(m)

    # Add legend using HTML
    legend_html = '''
    <div style="position: fixed; 
                top: 10px; right: 10px; width: 200px; height: 160px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px">
    <h4>Location Categories</h4>
    <p><i class="fa fa-home" style="color:darkred"></i> Headquarters</p>
    <p><i class="fa fa-cog" style="color:red"></i> Manufacturing</p>
    <p><i class="fa fa-shopping-bag" style="color:orange"></i> Flagship Stores</p>
    <p><i class="fa fa-star" style="color:purple"></i> Expansion Targets</p>
    <p><i class="fa fa-usd" style="color:darkblue"></i> High Revenue Markets</p>
    <p><i class="fa fa-shopping-cart" style="color:blue"></i> Standard Retail</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Display the enhanced map
    st_folium(m, height=500, use_container_width=True)

    # Add map insights below
    st.write("#### 📊 Global Footprint Intelligence Summary")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.write("**🏭 Manufacturing Locations:**")
        st.write("• Canada: 5 facilities (Winnipeg, Montreal, Toronto area)")
        st.write("• Europe: 1 facility (Romania - Paola Confectii)")
        st.write("• **Risk Focus**: Romania facility infiltration")

    with col_b:
        st.write("**🎯 Expansion Targets:**")
        st.write("• Milan, Italy (2025 priority)")
        st.write("• **Intelligence**: LAV headquarters location")
        st.write("• **Moncler Precedent**: 70% campaign success probability")

    with col_c:
        st.write("**💰 Revenue Concentration:**")
        st.write("• Greater China: 17.7% total revenue")
        st.write("• North America: Primary market")
        st.write("• **Risk Focus**: Geopolitical market access")

    for location, coords in business_locations.items():
        # Get travel risk assessment for this location
        risk_assessment = travel_analyzer.assess_location_risk(location)

        if "error" not in risk_assessment:
            risk_score = risk_assessment["overall_risk_score"]
            risk_level = risk_assessment["risk_level"]
            business_function = risk_assessment["business_function"]

            # Color coding based on risk level
            if risk_score >= 8:
                color, icon = "darkred", "exclamation-sign"
            elif risk_score >= 6:
                color, icon = "red", "warning-sign"
            elif risk_score >= 4:
                color, icon = "orange", "info-sign"
            else:
                color, icon = "green", "ok-sign"

            # Enhanced popup with travel intelligence
            popup_html = f"""
            <div style="width: 250px;">
                <h4>{location}</h4>
                <strong>Business Function:</strong> {business_function}<br>
                <strong>Travel Risk Score:</strong> {risk_score:.1f}/10<br>
                <strong>Risk Level:</strong> {risk_level}<br>
                <strong>Revenue Impact:</strong> {risk_assessment['revenue_impact']}<br>
                <hr>
                <strong>Top Threats:</strong><br>
                {'<br>'.join(f"• {threat}" for threat in risk_assessment['specific_threats'][:2])}
            </div>
            """

            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=color, icon=icon),
                tooltip=f"{location}: {risk_level} Risk"
            ).add_to(m)

    st_folium(m, height=450, use_container_width=True)

with col2:
    st.write("#### 📡 Integrated Intelligence Feed")

    # Combine security events and geopolitical intelligence
    all_intelligence = []

    # Add security events
    for event in analyzed_events:
        risk_score = event['analysis']['risk_assessment']['risk_score']
        all_intelligence.append({
            "type": "Security Event",
            "title": event['title'],
            "date": event['date'],
            "location": event['location'],
            "priority": "HIGH" if risk_score >= 20 else "MEDIUM" if risk_score >= 15 else "LOW",
            "score": risk_score,
            "source": event['source']
        })

    # Add geopolitical intelligence
    for alert in geo_monitor.intelligence_feeds:
        all_intelligence.append({
            "type": "Geopolitical Intel",
            "title": alert['headline'],
            "date": alert['timestamp'].strftime("%Y-%m-%d"),
            "location": alert['region'].title(),
            "priority": alert['priority'],
            "score": alert['confidence_level'],
            "source": "Geopolitical Monitor"
        })

    # Add counter-intelligence alerts if available
    if COUNTER_INTEL_AVAILABLE:
        all_intelligence.append({
            "type": "Counter-Intel",
            "title": "Predictive Alert: Milan RDS Investigation Operation",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "location": "Milan, Italy",
            "priority": "HIGH",
            "score": 85,
            "source": "Predictive Analysis"
        })

    # Sort by priority and date
    priority_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    all_intelligence.sort(key=lambda x: (priority_order.get(x["priority"], 0), x["date"]), reverse=True)

    # Display integrated intelligence feed
    for intel in all_intelligence[:8]:  # Show top 8
        priority_colors = {"HIGH": "#e74c3c", "MEDIUM": "#f39c12", "LOW": "#3498db"}
        color = priority_colors.get(intel["priority"], "#6c757d")

        # Special styling for counter-intel
        if intel["type"] == "Counter-Intel":
            color = "#8e44ad"

        st.markdown(f"""
        <div style="background: #2c3e50; padding: 1rem; border-radius: 5px; margin: 0.5rem 0; border-left: 4px solid {color}; color: white;">
            <strong>{intel['title'][:45]}...</strong><br>
            <small>📅 {intel['date']} | 📍 {intel['location']} | 🔍 {intel['type']}</small><br>
            <small>🎯 {intel['priority']} Priority | Score: {intel['score']}</small>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# --- Enhanced Executive Travel Risk Assessment ---
st.subheader("✈️ Executive Travel Risk Assessment & Security Planning")

# Travel destination selection with business context
business_critical_destinations = [
    "Shanghai, China", "Beijing, China", "London, UK", "Paris, France",
    "Toronto, ON", "New York, NY", "Winnipeg, MB", "Milan, Italy", "Titu, Romania"
]

col1, col2 = st.columns([1, 2])

with col1:
    st.write("#### 🎯 Travel Destination Selection")

    selected_destination = st.selectbox(
        "Select Business-Critical Destination:",
        [""] + business_critical_destinations
    )

    travel_purpose = st.selectbox(
        "Travel Purpose:",
        ["Business Operations", "Executive Meetings", "Store Inspection", "Crisis Response", "Board Meeting",
         "Supply Chain Management"]
    )

    executive_level = st.selectbox(
        "Executive Level:",
        ["Senior Leadership", "C-Suite", "Board Member", "Regional Director", "Supply Chain Executive"]
    )

    if st.button("🔍 Generate Travel Risk Assessment", type="primary"):
        st.session_state.generate_travel_brief = True
        st.session_state.travel_destination = selected_destination
        st.session_state.travel_purpose = travel_purpose
        st.session_state.executive_level = executive_level

with col2:
    if hasattr(st.session_state,
               'generate_travel_brief') and st.session_state.generate_travel_brief and selected_destination:

        st.write(f"#### 📋 Executive Travel Security Brief: {selected_destination}")

        # Generate comprehensive travel brief
        with st.spinner("🔍 Analyzing travel risks and generating security protocols..."):
            travel_brief = travel_analyzer.generate_executive_travel_brief(
                st.session_state.travel_destination,
                st.session_state.travel_purpose,
                st.session_state.executive_level
            )

            if "error" not in travel_brief:
                # Display executive summary
                st.markdown('<div class="travel-risk-card">', unsafe_allow_html=True)

                st.write(f"**Classification:** {travel_brief['classification']}")
                st.write(f"**Assessment Date:** {travel_brief['assessment_date']}")
                st.write(f"**Executive Level:** {travel_brief['executive_level']}")
                st.write(f"**Travel Purpose:** {travel_brief['travel_purpose']}")

                # Executive Summary (BLUF)
                summary = travel_brief["executive_summary"]
                st.markdown("---")
                st.write("#### Executive Summary (BLUF)")
                st.write(f"**Overall Risk Level:** {summary['overall_risk']}")
                st.write(f"**Business Context:** {summary['business_context']}")
                st.write(f"**Recommendation:** {summary['recommendation']}")

                if summary["key_concerns"]:
                    st.write("**Key Concerns:**")
                    for concern in summary["key_concerns"]:
                        st.write(f"• {concern}")

                st.markdown('</div>', unsafe_allow_html=True)

                # Enhanced Travel Security if Counter-Intel available
                if COUNTER_INTEL_AVAILABLE and selected_destination:
                    enhanced_recommendations = get_travel_security_enhancements(selected_destination)

                    with st.expander("🕵️ Enhanced Counter-Intelligence Travel Protocols"):
                        st.write("**Counter-Surveillance Recommendations:**")
                        for recommendation in enhanced_recommendations:
                            st.write(f"• {recommendation}")

                        # Location-specific intelligence
                        if "milan" in selected_destination.lower():
                            st.warning(
                                "🔍 **Milan-Specific Intelligence**: LAV headquarters located in Milan. Heightened risk of executive surveillance during supplier meetings. Recommend alternative meeting locations outside Milan city center.")

                        elif "romania" in selected_destination.lower():
                            st.error(
                                "⚠️ **Romania Facility Alert**: Paola Confectii facility represents critical European supply chain asset. Infiltration attempts highly likely. Coordinate all visits with facility security.")

            else:
                st.error(f"Could not generate travel brief: {travel_brief['error']}")

# --- Generate Professional Intelligence Brief ---
st.markdown("---")
if st.button("📊 Generate Executive Intelligence Brief", type="primary"):
    with st.expander("📈 Executive Intelligence Brief", expanded=True):
        st.markdown('<div class="executive-brief">', unsafe_allow_html=True)

        st.write(f"**Intelligence Brief for Week Ending:** {datetime.now().strftime('%Y-%m-%d')}")
        st.write(f"**Classification:** FOR OFFICIAL USE ONLY")
        st.markdown("---")

        # Enhanced BLUF with counter-intelligence context
        st.write("#### Bottom Line Up Front (BLUF):")

        # Construct comprehensive BLUF
        bluf_components = []

        # Counter-intelligence threats if available
        if COUNTER_INTEL_AVAILABLE:
            activist_summary = get_activist_intelligence_summary()
            if activist_summary["executive_attention_required"]:
                bluf_components.append(
                    f"HIGH-PRIORITY: Activist counter-intelligence operations predicted with {len(activist_summary['high_probability_operations'])} high-probability scenarios")

        # Geopolitical threats
        high_geo_alerts = [alert for alert in geo_monitor.intelligence_feeds if alert["priority"] == "HIGH"]
        if high_geo_alerts:
            bluf_components.append(
                f"{len(high_geo_alerts)} high-priority geopolitical events affecting business operations")

        # Travel risk status
        high_risk_travel_locations = len(travel_overview["high_risk_locations"])
        if high_risk_travel_locations > 0:
            bluf_components.append(f"{high_risk_travel_locations} business-critical locations at elevated travel risk")

        # China market specific
        china_threats = [threat for threat in geo_monitor.threat_indicators if "china" in threat]
        if china_threats:
            bluf_components.append(f"Greater China market tensions threatening {china_revenue_pct}% revenue exposure")

        # Security events
        critical_events = [e for e in analyzed_events if e['analysis']['risk_assessment']['risk_score'] >= 20]
        if critical_events:
            bluf_components.append(f"{len(critical_events)} critical security incidents requiring executive attention")

        if bluf_components:
            bluf_text = "Primary concerns: " + "; ".join(
                bluf_components) + ". Enhanced monitoring and executive briefings recommended."
        else:
            bluf_text = "No critical threats identified this period. Standard monitoring protocols maintained across all regions."

        st.info(bluf_text)

        # Intelligence Summary Sections
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.write("#### 🌍 Geopolitical Intelligence Summary")
            geo_brief = geo_monitor.generate_executive_geopolitical_brief()

            st.write(f"**Total Alerts:** {geo_brief['executive_summary']['total_alerts']}")
            st.write(f"**High Priority:** {geo_brief['executive_summary']['high_priority_issues']}")

            if geo_brief["priority_concerns"]:
                st.write("**Priority Concerns:**")
                for concern in geo_brief["priority_concerns"][:3]:
                    st.write(f"• {concern['concern']}")

            st.write("#### ✈️ Travel Risk Assessment")
            st.write(f"**Locations Monitored:** {travel_overview['total_locations']}")
            st.write(f"**High-Risk Locations:** {len(travel_overview['high_risk_locations'])}")

            if travel_overview["high_risk_locations"]:
                st.write("**Elevated Risk Destinations:**")
                for location in travel_overview["high_risk_locations"][:3]:
                    st.write(f"• {location['location']} ({location['risk_level']})")

        with col_b:
            if COUNTER_INTEL_AVAILABLE:
                st.write("#### 🕵️ Counter-Intelligence Assessment")
                counter_intel_predictor = ActivistCounterIntelligencePredictor()
                current_assessment = counter_intel_predictor.assess_current_threat_level()

                st.write(f"**Threat Level:** {current_assessment['overall_threat_level']}")
                st.write(
                    f"**Active Indicators:** {current_assessment['indicator_summary']['YELLOW'] + current_assessment['indicator_summary']['RED']}")

                if current_assessment["high_probability_operations"]:
                    st.write("**Predicted Operations:**")
                    for op in current_assessment["high_probability_operations"]:
                        st.write(f"• {op.replace('_', ' ').title()}")

                st.write("**Key Assessments:**")
                st.write("• Moncler precedent indicates 70% probability of similar campaign success")
                st.write("• LAV focus has shifted to RDS certification challenges")
                st.write("• Executive surveillance risk elevated in Milan and Romania")

        with col_c:
            st.write("#### 🚨 Security Incident Summary")

            # Event analysis
            event_by_risk = {"CRITICAL": [], "HIGH": [], "MEDIUM": []}
            for event in analyzed_events:
                score = event['analysis']['risk_assessment']['risk_score']
                if score >= 20:
                    event_by_risk["CRITICAL"].append(event)
                elif score >= 15:
                    event_by_risk["HIGH"].append(event)
                elif score >= 10:
                    event_by_risk["MEDIUM"].append(event)

            st.write(f"**Critical Events:** {len(event_by_risk['CRITICAL'])}")
            st.write(f"**High-Risk Events:** {len(event_by_risk['HIGH'])}")
            st.write(f"**Medium-Risk Events:** {len(event_by_risk['MEDIUM'])}")

            if event_by_risk["CRITICAL"] or event_by_risk["HIGH"]:
                st.write("**Executive Attention Required:**")
                for event in (event_by_risk["CRITICAL"] + event_by_risk["HIGH"])[:3]:
                    st.write(f"• {event['title']} (Score: {event['analysis']['risk_assessment']['risk_score']})")

            st.write("#### 💼 Business Impact Assessment")
            if "greater_china_risk" in travel_overview.get("business_impact_summary", {}):
                china_data = travel_overview["business_impact_summary"]["greater_china_risk"]
                st.write(f"**Greater China Risk Score:** {china_data['average_risk_score']}/10")
                st.write(f"**Revenue at Risk:** {china_data['revenue_at_risk']}")
                st.write(f"**Status:** {china_data['status']}")

        # Strategic Recommendations
        st.write("#### 🎯 Strategic Recommendations")

        strategic_recommendations = [
            "**IMMEDIATE**: Implement enhanced counter-surveillance protocols for supply chain executives traveling to Milan and Romania",
            "**STRATEGIC**: Develop proactive RDS transparency initiatives to prevent activist certification challenges",
            "**OPERATIONAL**: Enhance facility security at Romania manufacturing location with focus on infiltration prevention",
            "**INTELLIGENCE**: Increase monitoring of LAV and PETA operational planning and coordination activities",
            "**COMMUNICATIONS**: Prepare crisis communication strategies for potential supply chain exposé scenarios"
        ]

        if COUNTER_INTEL_AVAILABLE:
            for recommendation in strategic_recommendations:
                st.write(f"• {recommendation}")
        else:
            st.write("• Continue standard security monitoring across all regions")
            st.write("• Review and update threat assessment protocols")
            st.write("• Conduct routine executive travel security briefings")

        st.markdown('</div>', unsafe_allow_html=True)

# --- Generate Counter-Intelligence Brief (if available) ---
if COUNTER_INTEL_AVAILABLE:
    if st.button("🕵️ Generate Executive Counter-Intelligence Brief", type="primary"):
        with st.expander("🕵️ Executive Counter-Intelligence Assessment", expanded=True):
            st.markdown('<div class="executive-brief">', unsafe_allow_html=True)

            # Generate the brief
            counter_intel_predictor = ActivistCounterIntelligencePredictor()
            intel_brief = counter_intel_predictor.generate_intelligence_brief()

            # Display with proper formatting
            st.text(intel_brief)

            st.markdown('</div>', unsafe_allow_html=True)

            # Add download option
            st.download_button(
                label="📥 Download Counter-Intelligence Brief",
                data=intel_brief,
                file_name=f"CG_Counter_Intelligence_Brief_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

# --- Footer ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <small>Canada Goose Global Security Intelligence Platform | Enhanced Travel Risk & Geopolitical Intelligence | Predictive Threat Analysis | 
    Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
    Business-Critical Location Monitoring Active | Counter-Intelligence Prediction System {"ACTIVE" if COUNTER_INTEL_AVAILABLE else "OFFLINE"}</small>
</div>
""", unsafe_allow_html=True)
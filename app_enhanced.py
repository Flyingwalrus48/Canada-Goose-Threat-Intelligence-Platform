# app_enhanced.py - Canada Goose Global Security Intelligence Platform
# Working version with basic Streamlit components only

import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Try to import plotly for 3D globe - fallback gracefully if not available
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

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

# --- ENHANCED CSS STYLING ---
def load_custom_css():
    """Professional CSS styling for Canada Goose branding."""
    st.markdown(f"""
    <style>
    /* Professional Canada Goose Styling */
    .main {{
        background-color: {BRAND_COLORS["background_gray"]};
        font-family: 'Arial', 'Segoe UI', sans-serif;
    }}
    
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
    
    .risk-critical {{ border-left-color: {BRAND_COLORS["critical_red"]}; }}
    .risk-high {{ border-left-color: {BRAND_COLORS["high_orange"]}; }}
    .risk-medium {{ border-left-color: {BRAND_COLORS["medium_yellow"]}; }}
    .risk-low {{ border-left-color: {BRAND_COLORS["low_green"]}; }}
    
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
    
    .metric-container {{
        background: {BRAND_COLORS["card_gray"]};
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }}
    
    .metric-container:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
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
    
    .lav-intelligence-card {{
        background: linear-gradient(135deg, #8e44ad 0%, #9b59b6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(142, 68, 173, 0.3);
    }}
    
    .precedent-card {{
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(231, 76, 60, 0.3);
    }}
    
    .travel-brief-header {{
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        text-align: center;
    }}
    
    .intelligence-summary {{
        background: #2c3e50;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }}
    
    .real-time-indicator {{
        background: {BRAND_COLORS["low_green"]};
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        animation: pulse 1s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
        100% {{ opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CORE FUNCTIONS ---
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
    """Classify threats using pattern matching."""
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
    """Load and analyze events with risk scoring."""
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

# --- 3D GLOBE VISUALIZATION ---
def create_true_3d_globe():
    """Create a genuine 3D globe using 3D scatter plot with sphere mapping."""
    if not PLOTLY_AVAILABLE:
        st.warning("🌍 True 3D Globe requires plotly. Add 'plotly>=5.0.0' to requirements.txt for the full experience!")
        return None
    
    import numpy as np
    
    # Create sphere coordinates for Earth
    def sphere_coords(lat, lon, radius=1):
        lat_rad = np.radians(lat)
        lon_rad = np.radians(lon)
        x = radius * np.cos(lat_rad) * np.cos(lon_rad)
        y = radius * np.cos(lat_rad) * np.sin(lon_rad)
        z = radius * np.sin(lat_rad)
        return x, y, z
    
    # Create Earth surface
    phi = np.linspace(0, 2*np.pi, 50)
    theta = np.linspace(0, np.pi, 50)
    phi_grid, theta_grid = np.meshgrid(phi, theta)
    
    x_sphere = np.cos(phi_grid) * np.sin(theta_grid)
    y_sphere = np.sin(phi_grid) * np.sin(theta_grid)
    z_sphere = np.cos(theta_grid)
    
    # Canada Goose locations with enhanced Romanian facility details
    locations_data = [
        {"name": "Toronto HQ", "lat": 43.6532, "lon": -79.3832, "risk": "MEDIUM", "size": 15},
        {"name": "New York Flagship", "lat": 40.7589, "lon": -73.9851, "risk": "HIGH", "size": 12},
        {"name": "London Flagship", "lat": 51.5074, "lon": -0.1278, "risk": "HIGH", "size": 12},
        {"name": "Paris Flagship", "lat": 48.8566, "lon": 2.3522, "risk": "HIGH", "size": 11},
        {"name": "Milan (LAV HQ)", "lat": 45.4642, "lon": 9.1900, "risk": "CRITICAL", "size": 18},
        {"name": "🏭 Titu, Romania\n(Paola Confectii)", "lat": 44.8833, "lon": 25.8000, "risk": "HIGH", "size": 20},
        {"name": "Beijing Flagship", "lat": 39.9042, "lon": 116.4074, "risk": "HIGH", "size": 12},
        {"name": "Shanghai Store", "lat": 31.2304, "lon": 121.4737, "risk": "HIGH", "size": 14},
    ]
    
    # Color mapping
    color_map = {"CRITICAL": "#FF4444", "HIGH": "#FF8C00", "MEDIUM": "#FFD700", "LOW": "#32CD32"}
    
    fig = go.Figure()
    
    # Add Earth surface
    fig.add_trace(go.Surface(
        x=x_sphere, y=y_sphere, z=z_sphere,
        colorscale=[[0, 'lightblue'], [0.5, 'lightgreen'], [1, 'brown']],
        opacity=0.7,
        showscale=False,
        name='Earth'
    ))
    
    # Add location markers
    for loc in locations_data:
        x, y, z = sphere_coords(loc['lat'], loc['lon'], 1.02)  # Slightly above surface
        
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers+text',
            marker=dict(
                size=loc['size'],
                color=color_map[loc['risk']],
                opacity=0.9,
                line=dict(width=2, color='white')
            ),
            text=[loc['name']],
            textposition="top center",
            name=loc['risk'],
            hovertemplate=f"<b>{loc['name']}</b><br>Risk: {loc['risk']}<extra></extra>"
        ))
    
    # Add threat vectors (3D lines)
    milan_x, milan_y, milan_z = sphere_coords(45.4642, 9.1900, 1.02)
    titu_x, titu_y, titu_z = sphere_coords(44.8833, 25.8000, 1.02)
    
    fig.add_trace(go.Scatter3d(
        x=[milan_x, titu_x], y=[milan_y, titu_y], z=[milan_z, titu_z],
        mode='lines',
        line=dict(color='red', width=8, dash='dash'),
        name='LAV Threat Vector',
        hoverinfo='none'
    ))
    
    fig.update_layout(
        title="🌍 True 3D Globe - Canada Goose Global Security Intelligence",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False), 
            zaxis=dict(visible=False),
            bgcolor='black',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        height=600,
        showlegend=True
    )
    
    return fig

def create_stunning_3d_globe():
    """Create a high-resolution 3D interactive globe with Canada Goose locations."""
    if not PLOTLY_AVAILABLE:
        st.warning("🌍 Enhanced 3D Globe requires plotly. Add 'plotly>=5.0.0' to requirements.txt for the full experience!")
        return None
    
    # Canada Goose global locations with enhanced data
    locations_data = [
        # North America - Corporate Hub
        {"name": "Toronto HQ", "lat": 43.6532, "lon": -79.3832, "risk": "MEDIUM", "type": "Headquarters", 
         "revenue": 25.0, "threat_level": 3, "size": 30, "description": "Global Headquarters & Command Center"},
        {"name": "New York Flagship", "lat": 40.7589, "lon": -73.9851, "risk": "HIGH", "type": "Flagship Store", 
         "revenue": 15.0, "threat_level": 4, "size": 25, "description": "Premier North American Flagship"},
        {"name": "Winnipeg Manufacturing", "lat": 49.8951, "lon": -97.1384, "risk": "LOW", "type": "Manufacturing", 
         "revenue": 10.0, "threat_level": 2, "size": 20, "description": "Primary Manufacturing Facility"},
        
        # Europe - Expansion & Risk Zone
        {"name": "London Flagship", "lat": 51.5074, "lon": -0.1278, "risk": "HIGH", "type": "Flagship Store", 
         "revenue": 12.0, "threat_level": 4, "size": 25, "description": "European Market Leader"},
        {"name": "Paris Flagship", "lat": 48.8566, "lon": 2.3522, "risk": "HIGH", "type": "Flagship Store", 
         "revenue": 8.0, "threat_level": 4, "size": 22, "description": "European Luxury Market"},
        {"name": "Milan (LAV HQ)", "lat": 45.4642, "lon": 9.1900, "risk": "CRITICAL", "type": "Threat Zone", 
         "revenue": 5.0, "threat_level": 5, "size": 35, "description": "⚠️ LAV Headquarters - High Surveillance Risk"},
        {"name": "Titu, Romania (Paola Confectii)", "lat": 44.8833, "lon": 25.8000, "risk": "HIGH", "type": "Manufacturing", 
         "revenue": 6.0, "threat_level": 4, "size": 28, "description": "🏭 Paola Confectii Warehouse, Titu City | European Down Sourcing Hub | Acquired 2023 | LAV Infiltration Target"},
        
        # Asia-Pacific - Revenue Critical
        {"name": "Beijing Flagship", "lat": 39.9042, "lon": 116.4074, "risk": "HIGH", "type": "High Revenue", 
         "revenue": 5.0, "threat_level": 4, "size": 25, "description": "China Market Access Point"},
        {"name": "Shanghai Store", "lat": 31.2304, "lon": 121.4737, "risk": "HIGH", "type": "High Revenue", 
         "revenue": 8.8, "threat_level": 4, "size": 28, "description": "Primary China Revenue Center"},
        {"name": "Hong Kong", "lat": 22.3193, "lon": 114.1694, "risk": "MEDIUM", "type": "Regional Hub", 
         "revenue": 4.0, "threat_level": 3, "size": 20, "description": "Asia-Pacific Gateway"},
        {"name": "Tokyo Store", "lat": 35.6762, "lon": 139.6503, "risk": "LOW", "type": "Standard Retail", 
         "revenue": 3.0, "threat_level": 2, "size": 18, "description": "Japan Market Presence"},
    ]
    
    # Color mapping for risk levels with Canada Goose brand colors
    color_map = {
        "CRITICAL": "#FF4444",  # Bright Red
        "HIGH": "#FF8C00",      # Orange
        "MEDIUM": "#FFD700",    # Gold
        "LOW": "#32CD32"        # Green
    }
    
    # Create the 3D globe
    fig = go.Figure()
    
    # Add location markers
    for loc in locations_data:
        # Custom hover text with intelligence data
        hover_text = f"""
        <b>{loc['name']}</b><br>
        🏢 Type: {loc['type']}<br>
        ⚠️ Risk Level: {loc['risk']}<br>
        💰 Revenue Impact: ${loc['revenue']}M<br>
        🎯 Threat Level: {loc['threat_level']}/5<br>
        📍 Details: {loc['description']}
        """
        
        fig.add_trace(go.Scattergeo(
            lon=[loc['lon']],
            lat=[loc['lat']],
            text=[loc['name']],
            mode='markers+text',
            marker=dict(
                size=loc['size'],
                color=color_map[loc['risk']],
                opacity=0.8,
                line=dict(width=2, color='white'),
                symbol='circle'
            ),
            textposition="top center",
            textfont=dict(size=10, color='white'),
            hovertemplate=hover_text + "<extra></extra>",
            name=loc['risk'],
            showlegend=True if loc == locations_data[0] else False
        ))
    
    # Add threat connection lines for LAV operations
    lav_center = {"lat": 45.4642, "lon": 9.1900}  # Milan
    
    # Connect LAV to key targets
    target_locations = [
        {"lat": 44.8833, "lon": 25.8000, "name": "Titu Warehouse (Paola Confectii)"},  # Romania Manufacturing
        {"lat": 43.6532, "lon": -79.3832, "name": "Toronto HQ"},        # Toronto
        {"lat": 40.7589, "lon": -73.9851, "name": "New York Flagship"}  # New York
    ]
    
    for target in target_locations:
        fig.add_trace(go.Scattergeo(
            lon=[lav_center['lon'], target['lon']],
            lat=[lav_center['lat'], target['lat']],
            mode='lines',
            line=dict(width=2, color='rgba(220, 20, 60, 0.6)', dash='dash'),
            hoverinfo='none',
            showlegend=False,
            name='LAV Threat Vectors'
        ))
    
    # Enhanced 3D globe styling
    fig.update_layout(
        title=dict(
            text="🌍 Canada Goose Global Security Intelligence Globe",
            font=dict(size=20, color="#2C3E50", family="Arial"),
            x=0.5
        ),
        geo=dict(
            projection_type='orthographic',  # 3D globe projection
            showland=True,
            landcolor='rgba(243, 243, 243, 0.8)',
            coastlinecolor='rgba(204, 204, 204, 0.8)',
            showocean=True,
            oceancolor='rgba(0, 100, 200, 0.3)',
            showlakes=True,
            lakecolor='rgba(0, 100, 200, 0.2)',
            showcountries=True,
            countrycolor='rgba(204, 204, 204, 0.5)',
            projection_rotation=dict(
                lon=0,
                lat=0,
                roll=0
            ),
            center=dict(
                lon=0,
                lat=20
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        height=600,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=60, b=0)
    )
    
    return fig

def create_threat_radar_globe():
    """Create an enhanced threat radar visualization on 3D globe."""
    if not PLOTLY_AVAILABLE:
        return None
    
    # Threat zones data
    threat_zones = [
        {"name": "LAV Activity Zone (Milan HQ)", "lat": 45.4642, "lon": 9.1900, "radius": 800, "threat": "Activist Surveillance & Coordination"},
        {"name": "Romania Facility Risk Zone", "lat": 44.8833, "lon": 25.8000, "radius": 400, "threat": "Manufacturing Infiltration Risk"},
        {"name": "China Geopolitical Risk", "lat": 35, "lon": 110, "radius": 1200, "threat": "Market Access Risk"},
        {"name": "North America Secure", "lat": 45, "lon": -75, "radius": 600, "threat": "Operational Security"}
    ]
    
    fig = go.Figure()
    
    # Add threat zone circles
    for zone in threat_zones:
        # Create circle around threat zone
        angles = [i * 360 / 50 for i in range(51)]  # 50 points for smooth circle
        lats = []
        lons = []
        
        import math
        for angle in angles:
            # Convert radius from km to degrees (rough approximation)
            radius_deg = zone['radius'] / 111.32  # km to degrees
            lat_rad = math.radians(zone['lat'])
            lon_rad = math.radians(zone['lon'])
            angle_rad = math.radians(angle)
            
            new_lat = math.asin(math.sin(lat_rad) * math.cos(radius_deg/111.32) + 
                               math.cos(lat_rad) * math.sin(radius_deg/111.32) * math.cos(angle_rad))
            new_lon = lon_rad + math.atan2(math.sin(angle_rad) * math.sin(radius_deg/111.32) * math.cos(lat_rad),
                                          math.cos(radius_deg/111.32) - math.sin(lat_rad) * math.sin(new_lat))
            
            lats.append(math.degrees(new_lat))
            lons.append(math.degrees(new_lon))
        
        if "LAV" in zone['name']:
            color = "#FF4444"  # Red for LAV
        elif "Romania" in zone['name']:
            color = "#FF8C00"  # Orange for Romania facility risk
        elif "China" in zone['name']:
            color = "#FFD700"  # Yellow for China
        else:
            color = "#32CD32"  # Green for secure zones
        
        fig.add_trace(go.Scattergeo(
            lon=lons,
            lat=lats,
            mode='lines',
            line=dict(width=3, color=color),
            fill='tonext' if zone != threat_zones[0] else None,
            fillcolor=f"rgba{tuple(int(color[i:i+2], 16) for i in (1, 3, 5)) + (0.1,)}",
            name=zone['name'],
            hovertemplate=f"<b>{zone['name']}</b><br>Threat: {zone['threat']}<extra></extra>"
        ))
    
    fig.update_layout(
        title="🎯 Global Threat Radar - Live Intelligence Zones",
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            showocean=True,
            oceancolor='rgb(255, 255, 255)',
            projection_rotation=dict(lon=0, lat=0, roll=0)
        ),
        height=500
    )
    
    return fig

# --- UI COMPONENTS ---
def display_metric(label: str, value: str, color: str = "#2C3E50") -> None:
    """Professional metric card component."""
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value" style="color: {color}">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def display_intelligence_card(event: dict) -> None:
    """Professional intelligence card component."""
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
    """Professional alert component."""
    st.markdown(f"""
    <div class="alert-container alert-{alert_type}">
        {message}
    </div>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_application_data():
    """Load all application data with error handling."""
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

# --- MAIN APPLICATION ---
def main():
    """Main application function."""
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
    
    # Travel Brief (if active)
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
                <strong>🏭 TITU FACILITY INFILTRATION ALERT</strong><br>
                • Location: Paola Confectii Warehouse, Titu City, Romania<br>
                • Status: Critical European Down Sourcing Hub (Acquired 2023)<br>
                • Threat: LAV infiltration attempts - HIGH PROBABILITY<br>
                • Intelligence: Supply chain documentation/RDS compliance targeting<br>
                • Distance from Milan LAV HQ: ~1,100km (manageable for operations)<br>
                • Security Protocol: Coordinate ALL visits with facility security team
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
    
    # Real-time header
    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem; background: {BRAND_COLORS['low_green']}; color: white; border-radius: 5px; margin-bottom: 1rem;">
        <span class="real-time-indicator"></span>
        <strong>Live Intelligence Feed Active</strong> | Last update: {datetime.now().strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Canada Goose Global Security Intelligence Platform</h1>
        <p>LAV Counter-Intelligence • RDS Supply Chain Monitoring • Executive Protection</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
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
        lav_events = sum(1 for e in events_data if "peta" in e['details'].lower() or "activist" in e['title'].lower())
        display_metric("LAV Incidents", str(lav_events), BRAND_COLORS['accent_red'])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # LAV Intelligence Analysis
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
    
    # Predictive Analysis
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
    
    # Analytics Dashboard
    st.markdown("### 📊 Intelligence Analytics Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["🌍 Geographic Analysis", "📈 Risk Trends", "📡 Live Intelligence Feed"])
    
    with tab1:
        # Check if we can display the stunning 3D globe
        if PLOTLY_AVAILABLE:
            st.markdown("### 🌍 Interactive 3D Globe - Global Security Intelligence")
            
            # Toggle between different globe views
            globe_view = st.radio(
                "Select Globe View:",
                ["🌎 True 3D Globe", "🌍 Geographic Projection", "🎯 Threat Radar Zones", "📊 Risk Distribution"],
                horizontal=True
            )
            
            if globe_view == "🌎 True 3D Globe":
                globe_fig = create_true_3d_globe()
                if globe_fig:
                    st.plotly_chart(globe_fig, use_container_width=True)
                    
                    # Add interactive controls
                    st.markdown("""
                    **🎮 Interactive 3D Globe Controls:**
                    - **Click & Drag** to rotate the true 3D globe
                    - **Scroll** to zoom in/out  
                    - **Hover** over locations for detailed intelligence
                    - **Red dashed line** shows LAV threat vector: Milan → Titu, Romania facility
                    - **Romania (Titu)** = Paola Confectii warehouse - Critical Down Sourcing Hub
                    """)
                    
                    # Enhanced Romania facility info
                    st.info("🏭 **Titu, Romania Facility Focus:** Paola Confectii warehouse is a critical European down sourcing hub acquired in 2023. High LAV infiltration risk due to RDS compliance monitoring operations.")
                    
            elif globe_view == "🌍 Geographic Projection":
                globe_fig = create_stunning_3d_globe()
                if globe_fig:
                    st.plotly_chart(globe_fig, use_container_width=True)
                    
                    # Add interactive controls
                    st.markdown("""
                    **🎮 Interactive Controls:**
                    - **Click & Drag** to rotate the globe
                    - **Scroll** to zoom in/out  
                    - **Hover** over locations for detailed intelligence
                    - **Red dashed lines** show LAV threat vectors from Milan
                    """)
                    
            elif globe_view == "🎯 Threat Radar Zones":
                radar_fig = create_threat_radar_globe()
                if radar_fig:
                    st.plotly_chart(radar_fig, use_container_width=True)
                    st.info("🎯 **Threat Zones:** Red = LAV Activity (Milan), Orange = Romania Facility Risk, Yellow = China Geopolitical Risk, Green = Secure Operations")
                    
            else:  # Risk Distribution
                # Enhanced risk distribution with plotly
                risk_counts = {}
                for event in events_data:
                    level = event['analysis']['risk_assessment']['risk_level']
                    risk_counts[level] = risk_counts.get(level, 0) + 1
                
                import plotly.express as px
                chart_data = pd.DataFrame({
                    'Risk Level': list(risk_counts.keys()),
                    'Count': list(risk_counts.values())
                })
                
                fig = px.bar(chart_data, x='Risk Level', y='Count', 
                           title="Risk Level Distribution",
                           color='Risk Level',
                           color_discrete_map={
                               'CRITICAL': '#FF4444',
                               'HIGH': '#FF8C00', 
                               'MEDIUM': '#FFD700',
                               'LOW': '#32CD32'
                           })
                
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            # Fallback to basic charts if plotly not available
            st.subheader("Risk Level Distribution")
            
            risk_counts = {}
            for event in events_data:
                level = event['analysis']['risk_assessment']['risk_level']
                risk_counts[level] = risk_counts.get(level, 0) + 1
            
            # Use built-in bar chart
            chart_data = pd.DataFrame({
                'Risk Level': list(risk_counts.keys()),
                'Count': list(risk_counts.values())
            })
            st.bar_chart(chart_data.set_index('Risk Level'))
            
            # Simple map using built-in map
            st.subheader("Global Asset Map")
            st.info("💡 Add 'plotly>=5.0.0' to requirements.txt to unlock the stunning 3D globe!")
            map_data = pd.DataFrame([
                {"lat": 43.6532, "lon": -79.3832},
                {"lat": 40.7128, "lon": -74.0060},
                {"lat": 51.5074, "lon": -0.1278},
                {"lat": 48.8566, "lon": 2.3522},
                {"lat": 39.9042, "lon": 116.4074},
                {"lat": 45.4642, "lon": 9.1900},
            ])
            st.map(map_data)
    
    with tab2:
        st.subheader("Risk Score Timeline")
        
        # Create timeline chart
        timeline_data = []
        for event in sorted(events_data, key=lambda x: x['date']):
            timeline_data.append({
                'Date': event['date'],
                'Risk Score': event['analysis']['risk_assessment']['risk_score']
            })
        
        df_timeline = pd.DataFrame(timeline_data)
        st.line_chart(df_timeline.set_index('Date'))
    
    with tab3:
        st.subheader("Live Intelligence Feed")
        
        # Filter controls
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            risk_filter = st.multiselect(
                "Filter by Risk Level",
                options=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                default=["CRITICAL", "HIGH", "MEDIUM", "LOW"]
            )
        
        with col_filter2:
            search_term = st.text_input("Search in title/details", placeholder="Enter search term...")
        
        # Apply filters
        filtered_events = events_data
        
        if risk_filter:
            filtered_events = [e for e in filtered_events if e['analysis']['risk_assessment']['risk_level'] in risk_filter]
        
        if search_term:
            filtered_events = [e for e in filtered_events if 
                              search_term.lower() in e['title'].lower() or 
                              search_term.lower() in e['details'].lower()]
        
        # Display results
        st.write(f"**Showing {len(filtered_events)} of {len(events_data)} events**")
        
        for event in sorted(filtered_events, key=lambda x: x['date'], reverse=True):
            display_intelligence_card(event)
    
    # Travel Controls Sidebar
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

if __name__ == "__main__":
    main()

# risk_scorer.py - Enhanced Risk Assessment with Travel Intelligence Integration

import re
from datetime import datetime
from typing import Dict, List, Optional

# Enhanced risk matrix with travel and geopolitical considerations
ENHANCED_RISK_MATRIX = {
    "Activism / Physical Security": {
        "likelihood": 4,
        "impact": 3,
        "primary_impact": "Store Operations & Reputation",
        "travel_impact": "Medium - Enhanced security for store visits"
    },
    "Geopolitical / Market Risk": {
        "likelihood": 3,
        "impact": 5,
        "primary_impact": "Revenue & Market Access",
        "travel_impact": "High - Executive travel restrictions possible"
    },
    "Legal / Financial": {
        "likelihood": 5,
        "impact": 4,
        "primary_impact": "Financial Performance",
        "travel_impact": "Low - Standard travel precautions"
    },
    "Organized Retail Crime": {
        "likelihood": 4,
        "impact": 3,
        "primary_impact": "Inventory Loss & Staff Safety",
        "travel_impact": "Medium - Enhanced security in retail districts"
    },
    "Cyber / Dark Web": {
        "likelihood": 3,
        "impact": 4,
        "primary_impact": "Customer Data & Brand Trust",
        "travel_impact": "Medium - Secure communications required"
    },
    "Travel Security": {
        "likelihood": 3,
        "impact": 4,
        "primary_impact": "Executive Safety & Business Continuity",
        "travel_impact": "High - Direct travel safety implications"
    },
    "Supply Chain Disruption": {
        "likelihood": 4,
        "impact": 3,
        "primary_impact": "Manufacturing & Operations",
        "travel_impact": "Medium - Supplier location travel risks"
    },
    "General Intelligence": {
        "likelihood": 2,
        "impact": 2,
        "primary_impact": "General Awareness",
        "travel_impact": "Low - Standard precautions"
    }
}

# Business-critical locations for enhanced risk assessment
BUSINESS_CRITICAL_LOCATIONS = {
    "China": {
        "revenue_impact": 17.7,
        "business_criticality": "CRITICAL",
        "geopolitical_sensitivity": "HIGH"
    },
    "Shanghai": {
        "revenue_impact": 8.8,  # Estimated portion of China revenue
        "business_criticality": "CRITICAL",
        "geopolitical_sensitivity": "HIGH"
    },
    "Beijing": {
        "revenue_impact": 5.0,
        "business_criticality": "HIGH",
        "geopolitical_sensitivity": "CRITICAL"  # Government relations
    },
    "London": {
        "revenue_impact": 12.0,  # Estimated EMEA flagship
        "business_criticality": "HIGH",
        "geopolitical_sensitivity": "MEDIUM"
    },
    "Paris": {
        "revenue_impact": 8.0,
        "business_criticality": "HIGH",
        "geopolitical_sensitivity": "MEDIUM"
    },
    "Toronto": {
        "revenue_impact": 25.0,  # HQ and Canada operations
        "business_criticality": "CRITICAL",
        "geopolitical_sensitivity": "LOW"
    },
    "New York": {
        "revenue_impact": 15.0,  # US flagship market
        "business_criticality": "HIGH",
        "geopolitical_sensitivity": "LOW"
    }
}

# Travel risk multipliers by threat type
TRAVEL_RISK_MULTIPLIERS = {
    "Geopolitical / Market Risk": 1.5,  # Higher impact on travel
    "Travel Security": 2.0,  # Direct travel impact
    "Activism / Physical Security": 1.3,  # Store visit risks
    "Cyber / Dark Web": 1.2,  # Communication security
    "Supply Chain Disruption": 1.1,  # Supplier travel
    "General Intelligence": 1.0
}


def calculate_enhanced_risk_score(analyzed_event: dict, threat_type: str,
                                  include_travel_assessment: bool = True) -> dict:
    """
    Enhanced risk calculation with travel intelligence and business impact modeling.

    Args:
        analyzed_event (dict): Event data including location, details, source
        threat_type (str): Classified threat category
        include_travel_assessment (bool): Whether to include travel risk assessment

    Returns:
        dict: Comprehensive risk assessment with travel intelligence
    """

    # Get baseline scores from enhanced matrix
    baseline_scores = ENHANCED_RISK_MATRIX.get(threat_type, ENHANCED_RISK_MATRIX["General Intelligence"])
    likelihood = baseline_scores["likelihood"]
    impact = baseline_scores["impact"]
    primary_impact = baseline_scores["primary_impact"]
    travel_impact = baseline_scores["travel_impact"]

    # Track all adjustments for transparency
    adjustments = []
    travel_considerations = []
    business_impact_factors = []

    # --- ENHANCED CAUSAL LOGIC RULES ---

    # Rule 1: Business-critical location adjustments
    location = analyzed_event.get('location', '')
    location_multiplier = 1.0

    for critical_location, location_data in BUSINESS_CRITICAL_LOCATIONS.items():
        if critical_location.lower() in location.lower():
            # Revenue-based impact adjustment
            revenue_impact = location_data["revenue_impact"]
            if revenue_impact >= 15:  # High revenue impact
                impact = min(5, impact + 1)
                adjustments.append(f"High revenue impact location: {revenue_impact}% revenue exposure")

            # Geopolitical sensitivity adjustment
            geo_sensitivity = location_data["geopolitical_sensitivity"]
            if geo_sensitivity == "CRITICAL" and threat_type == "Geopolitical / Market Risk":
                likelihood = min(5, likelihood + 1)
                impact = min(5, impact + 1)
                adjustments.append(f"Critical geopolitical sensitivity: {critical_location}")

            # Business criticality multiplier
            if location_data["business_criticality"] == "CRITICAL":
                location_multiplier = 1.3
                business_impact_factors.append(f"Critical business location: {critical_location}")
            elif location_data["business_criticality"] == "HIGH":
                location_multiplier = 1.2
                business_impact_factors.append(f"High-value business location: {critical_location}")

            break

    # Rule 2: Enhanced geopolitical risk assessment
    if threat_type == "Geopolitical / Market Risk":
        details = analyzed_event.get('details', '').lower()

        # China-specific risks (17.7% revenue exposure)
        if any(term in location.lower() for term in ["china", "shanghai", "beijing"]):
            impact = 5  # Maximum impact due to revenue exposure
            primary_impact = f"Revenue & Market Access (China - {BUSINESS_CRITICAL_LOCATIONS.get('China', {}).get('revenue_impact', 17.7)}% revenue)"
            adjustments.append("China market risk: Maximum impact due to revenue concentration")

            # Travel-specific considerations for China
            if include_travel_assessment:
                travel_considerations.extend([
                    "Executive travel to China requires enhanced security protocols",
                    "Government relations meetings need diplomatic coordination",
                    "Communication security critical due to surveillance concerns",
                    "Alternative meeting locations outside China may be advisable"
                ])

        # Trade-related escalation
        if any(term in details for term in ["trade", "tariff", "diplomatic", "sanctions"]):
            likelihood = min(5, likelihood + 1)
            adjustments.append("Trade/diplomatic tension indicators increase likelihood")

    # Rule 3: Enhanced activism and physical security
    if threat_type == "Activism / Physical Security":
        details = analyzed_event.get('details', '').lower()

        # Known activist groups
        activist_groups = ["peta", "humane society", "animal justice"]
        for group in activist_groups:
            if group in details:
                likelihood = 5  # Known groups have high execution capability
                adjustments.append(f"Known activist organization identified: {group.upper()}")
                break

        # Multi-location campaigns
        if any(connector in location.lower() for connector in ["and", "&", "emea", "north america", "europe"]):
            impact = min(5, impact + 1)
            likelihood = min(5, likelihood + 1)
            adjustments.append("Multi-location campaign increases coordination and impact")

            # Travel considerations for activism
            if include_travel_assessment:
                travel_considerations.extend([
                    "Store visits during protest periods require enhanced security",
                    "Alternative entrances and timing for retail location access",
                    "Executive protection recommended for high-profile visits",
                    "Monitor social media for specific targeting of executives"
                ])

        # Seasonal timing (October-February peak for animal rights campaigns)
        event_date = analyzed_event.get('date', '')
        if event_date:
            try:
                month = int(event_date.split('-')[1])
                if month in [10, 11, 12, 1, 2]:  # Peak season
                    impact = min(5, impact + 1)
                    adjustments.append("Peak protest season increases operational impact")
            except:
                pass

    # Rule 4: Enhanced organized retail crime assessment
    if threat_type == "Organized Retail Crime":
        details = analyzed_event.get('details', '').lower()

        # High-value retail districts
        luxury_districts = ["soho", "fifth avenue", "rodeo drive", "bond street", "champs-elysees"]
        for district in luxury_districts:
            if district in location.lower():
                likelihood = 5
                impact = min(5, impact + 1)
                adjustments.append(f"High-value retail district: {district}")

                # Travel considerations for ORC
                if include_travel_assessment:
                    travel_considerations.extend([
                        f"Enhanced security required when visiting {district} area",
                        "Coordinate with local law enforcement for store visits",
                        "Avoid displaying company identification in high-crime areas"
                    ])
                break

        # Coordinated group tactics
        if any(term in details for term in ["organized", "coordinated", "group", "ring"]):
            likelihood = min(5, likelihood + 1)
            impact = min(5, impact + 1)
            adjustments.append("Organized criminal tactics increase success probability and impact")

    # Rule 5: Travel security threat assessment
    if threat_type == "Travel Security" or include_travel_assessment:
        travel_risk_multiplier = TRAVEL_RISK_MULTIPLIERS.get(threat_type, 1.0)

        if travel_risk_multiplier > 1.0:
            impact = min(5, int(impact * travel_risk_multiplier))
            adjustments.append(f"Travel risk multiplier applied: {travel_risk_multiplier}x")

        # Location-specific travel risks
        if any(high_risk in location.lower() for high_risk in ["china", "beijing", "shanghai"]):
            travel_considerations.extend([
                "Geopolitical tensions may affect executive travel",
                "Enhanced diplomatic protocols required",
                "Secure communication methods essential",
                "Emergency evacuation procedures should be briefed"
            ])

        # Add general travel considerations based on threat type
        if threat_type not in ["Travel Security"]:
            if likelihood >= 4 or impact >= 4:
                travel_considerations.append(f"Enhanced travel security recommended due to {threat_type.lower()} risk")

    # Rule 6: Supply chain and business continuity
    if threat_type == "Supply Chain Disruption":
        # Manufacturing location risks
        if any(loc in location.lower() for loc in ["winnipeg", "toronto", "canada"]):
            impact = min(5, impact + 1)
            adjustments.append("Manufacturing hub disruption increases business impact")

            if include_travel_assessment:
                travel_considerations.extend([
                    "Supplier facility visits may require enhanced security",
                    "Alternative meeting locations if facilities affected",
                    "Business continuity planning for extended disruptions"
                ])

    # Apply location multiplier
    final_impact = min(5, impact * location_multiplier)
    if location_multiplier > 1.0:
        adjustments.append(f"Business location multiplier: {location_multiplier}x")

    # Calculate final risk score
    risk_score = likelihood * final_impact

    # Determine risk level category
    if risk_score >= 20:
        risk_level = "CRITICAL"
    elif risk_score >= 15:
        risk_level = "HIGH"
    elif risk_score >= 10:
        risk_level = "MEDIUM"
    elif risk_score >= 5:
        risk_level = "LOW"
    else:
        risk_level = "MINIMAL"

    # Enhanced business impact assessment
    business_impact = _assess_enhanced_business_impact(
        threat_type, risk_score, analyzed_event, location_multiplier
    )

    # Travel risk assessment
    travel_risk_assessment = None
    if include_travel_assessment:
        travel_risk_assessment = _assess_travel_risk_impact(
            threat_type, risk_score, location, travel_considerations
        )

    # Executive notification requirements
    executive_notifications = _determine_executive_notifications(
        risk_score, threat_type, location, business_impact_factors
    )

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "likelihood": likelihood,
        "impact": int(final_impact),
        "primary_impact": primary_impact,
        "business_impact": business_impact,
        "travel_impact": travel_impact,
        "travel_risk_assessment": travel_risk_assessment,
        "location_multiplier": location_multiplier,
        "adjustments_made": adjustments,
        "business_impact_factors": business_impact_factors,
        "travel_considerations": travel_considerations,
        "executive_notifications": executive_notifications,
        "assessment_rationale": f"Risk Score {risk_score} = Likelihood {likelihood}/5 × Impact {int(final_impact)}/5 × Location Factor {location_multiplier:.1f}"
    }


def _assess_enhanced_business_impact(threat_type: str, risk_score: int,
                                     event: dict, location_multiplier: float) -> dict:
    """Enhanced business impact assessment with location and revenue considerations"""

    impact_analysis = {
        "financial_impact": "Low",
        "operational_impact": "Low",
        "reputational_impact": "Low",
        "revenue_exposure": "Minimal",
        "recommendations": [],
        "stakeholders_to_notify": [],
        "business_continuity_risk": "Low"
    }

    # High-risk events require executive attention
    if risk_score >= 15:
        impact_analysis["stakeholders_to_notify"].extend([
            "Global Security Director",
            "Chief Risk Officer",
            "Executive Leadership Team"
        ])

    if risk_score >= 20:
        impact_analysis["stakeholders_to_notify"].extend([
            "CEO", "Board Risk Committee"
        ])

    # Location-based impact assessment
    location = event.get('location', '')

    # China market specific impacts
    if any(china_loc in location.lower() for china_loc in ["china", "shanghai", "beijing"]):
        if threat_type == "Geopolitical / Market Risk":
            impact_analysis.update({
                "financial_impact": "Critical",
                "revenue_exposure": "17.7% of total revenue",
                "business_continuity_risk": "High",
                "recommendations": [
                    "Activate China market contingency planning",
                    "Brief investor relations on potential revenue impact",
                    "Engage Canadian embassy for diplomatic support",
                    "Assess alternative Asian market strategies",
                    "Monitor competitor responses to similar risks"
                ]
            })

    # European market impacts (activism focus)
    elif any(eu_loc in location.lower() for eu_loc in ["london", "paris", "europe", "emea"]):
        if threat_type == "Activism / Physical Security":
            impact_analysis.update({
                "operational_impact": "High",
                "reputational_impact": "High",
                "recommendations": [
                    "Enhance European store security protocols",
                    "Activate crisis communications for EMEA region",
                    "Coordinate with local law enforcement",
                    "Brief European retail teams on response procedures",
                    "Monitor social media sentiment in affected markets"
                ]
            })

    # North American operations
    elif any(na_loc in location.lower() for na_loc in ["toronto", "canada", "new york", "north america"]):
        if location_multiplier > 1.2:  # Critical locations
            impact_analysis.update({
                "operational_impact": "High",
                "business_continuity_risk": "Medium",
                "recommendations": [
                    "Review business continuity protocols",
                    "Assess backup operational capabilities",
                    "Brief North American leadership team",
                    "Monitor supply chain implications"
                ]
            })

    # Threat-specific enhancements
    if threat_type == "Supply Chain Disruption":
        impact_analysis.update({
            "operational_impact": "High",
            "financial_impact": "Medium",
            "recommendations": [
                "Activate supplier contingency plans",
                "Assess inventory buffer adequacy",
                "Review alternative sourcing options",
                "Brief manufacturing and procurement teams"
            ]
        })

    elif threat_type == "Cyber / Dark Web":
        impact_analysis.update({
            "reputational_impact": "High",
            "recommendations": [
                "Alert cybersecurity team to heightened threat",
                "Review customer data protection measures",
                "Prepare incident response communications",
                "Monitor for suspicious network activity",
                "Brief legal team on potential exposure"
            ]
        })

    return impact_analysis


def _assess_travel_risk_impact(threat_type: str, risk_score: int,
                               location: str, travel_considerations: List[str]) -> dict:
    """Assess specific travel risk implications"""

    travel_assessment = {
        "travel_risk_level": "Standard",
        "executive_travel_impact": "Low",
        "recommended_protocols": [],
        "restricted_activities": [],
        "enhanced_security_required": False,
        "alternative_arrangements": []
    }

    # Risk-based travel assessment
    if risk_score >= 20:
        travel_assessment.update({
            "travel_risk_level": "Critical",
            "executive_travel_impact": "High",
            "enhanced_security_required": True,
            "recommended_protocols": [
                "Executive protection team required",
                "Advance security assessment mandatory",
                "Emergency evacuation procedures briefed",
                "24/7 security monitoring active"
            ]
        })

        # Consider travel restrictions for critical risks
        if threat_type == "Geopolitical / Market Risk":
            travel_assessment["restricted_activities"].extend([
                "Non-essential travel postponed",
                "Government meetings require diplomatic coordination",
                "Media appearances avoided"
            ])

    elif risk_score >= 15:
        travel_assessment.update({
            "travel_risk_level": "High",
            "executive_travel_impact": "Medium",
            "enhanced_security_required": True,
            "recommended_protocols": [
                "Enhanced security briefing required",
                "Secure transportation arranged",
                "Local security contractor on standby",
                "Regular check-in protocols active"
            ]
        })

    elif risk_score >= 10:
        travel_assessment.update({
            "travel_risk_level": "Medium",
            "executive_travel_impact": "Low-Medium",
            "recommended_protocols": [
                "Security awareness briefing",
                "Enhanced situational awareness",
                "Secure communications recommended"
            ]
        })

    # Location-specific travel considerations
    if any(china_loc in location.lower() for china_loc in ["china", "shanghai", "beijing"]):
        travel_assessment["alternative_arrangements"].extend([
            "Virtual meeting capabilities as backup",
            "Third-country meeting locations identified",
            "Diplomatic protocol consultation available"
        ])

    # Include provided travel considerations
    if travel_considerations:
        travel_assessment["specific_considerations"] = travel_considerations

    return travel_assessment


def _determine_executive_notifications(risk_score: int, threat_type: str,
                                       location: str, business_factors: List[str]) -> dict:
    """Determine executive notification requirements"""

    notifications = {
        "immediate_notification_required": False,
        "notification_level": "Standard",
        "recipients": [],
        "escalation_criteria": [],
        "reporting_frequency": "Standard"
    }

    # Critical risk notifications
    if risk_score >= 20:
        notifications.update({
            "immediate_notification_required": True,
            "notification_level": "Critical",
            "recipients": [
                "CEO", "Global Security Director", "Chief Risk Officer",
                "Board Risk Committee", "Executive Leadership Team"
            ],
            "reporting_frequency": "Immediate + Hourly updates",
            "escalation_criteria": [
                "CEO notification within 1 hour",
                "Board notification within 4 hours",
                "Media response team activation"
            ]
        })

    # High risk notifications
    elif risk_score >= 15:
        notifications.update({
            "immediate_notification_required": True,
            "notification_level": "High",
            "recipients": [
                "Global Security Director", "Chief Risk Officer",
                "Regional Leadership", "Executive Leadership Team"
            ],
            "reporting_frequency": "Immediate + Daily updates",
            "escalation_criteria": [
                "Security Director notification within 2 hours",
                "Executive team briefing within 8 hours"
            ]
        })

    # Business-critical location notifications
    if any(factor for factor in business_factors if "Critical" in factor):
        if "CEO" not in notifications["recipients"]:
            notifications["recipients"].append("Regional CEO")
        notifications["escalation_criteria"].append("Business continuity assessment required")

    # China-specific notifications (revenue impact)
    if any(china_loc in location.lower() for china_loc in ["china", "shanghai", "beijing"]):
        notifications["recipients"].extend([
            "Asia Pacific Regional Director",
            "Investor Relations Team",
            "Government Relations Team"
        ])
        notifications["escalation_criteria"].append("Revenue impact assessment required")

    return notifications


# Legacy compatibility function
def calculate_risk_score(analyzed_event: dict, threat_type: str) -> dict:
    """
    Legacy compatibility wrapper for existing dashboard code
    """
    enhanced_result = calculate_enhanced_risk_score(analyzed_event, threat_type, include_travel_assessment=False)

    # Return simplified format for compatibility
    return {
        "risk_score": enhanced_result["risk_score"],
        "likelihood": enhanced_result["likelihood"],
        "impact": enhanced_result["impact"],
        "primary_impact": enhanced_result["primary_impact"],
        "risk_level": enhanced_result["risk_level"],
        "business_impact": enhanced_result["business_impact"],
        "adjustments_made": enhanced_result["adjustments_made"],
        "assessment_rationale": enhanced_result["assessment_rationale"]
    }


# Test function for the enhanced risk scorer
def test_enhanced_risk_calculations():
    """Test enhanced risk calculations with travel intelligence"""

    print("🧪 Testing Enhanced Risk Calculator with Travel Intelligence")
    print("=" * 65)

    test_events = [
        {
            "date": "2025-07-15",
            "type": "Activism/Physical Security",
            "title": "PETA Announces 'Winter of Discontent' Campaign",
            "details": "Activist group PETA announces planned protests targeting Canada Goose flagship stores in London, Paris, and New York, starting in October. TTPs likely include store entrance blockades.",
            "location": "EMEA/North America",
            "source": "Simulated OSINT"
        },
        {
            "date": "2025-07-20",
            "type": "Geopolitical/Market Risk",
            "title": "Canada-China Trade Tensions Escalate",
            "details": "New Canadian policy on luxury goods trade with China has sparked nationalist backlash on Weibo. Mentions of #BoycottCanadaGoose are trending.",
            "location": "China",
            "source": "Simulated SOCMINT"
        },
        {
            "date": "2025-08-01",
            "type": "Organized Retail Crime",
            "title": "ORC Ring Targets Luxury Retail in NYC SoHo",
            "details": "NYPD reports coordinated smash-and-grab thefts targeting luxury apparel stores in SoHo district by organized groups.",
            "location": "New York, NY - SoHo",
            "source": "Law Enforcement Bulletin"
        }
    ]

    for i, event in enumerate(test_events, 1):
        print(f"\n{i}. Testing: {event['title']}")
        print("-" * 50)

        # Determine threat type
        if "PETA" in event["details"] or "activist" in event["details"].lower():
            threat_type = "Activism / Physical Security"
        elif "trade" in event["details"].lower() or "China" in event["location"]:
            threat_type = "Geopolitical / Market Risk"
        elif "crime" in event["type"].lower():
            threat_type = "Organized Retail Crime"
        else:
            threat_type = "General Intelligence"

        # Calculate enhanced risk
        result = calculate_enhanced_risk_score(event, threat_type, include_travel_assessment=True)

        print(f"📊 Risk Assessment:")
        print(f"   Risk Score: {result['risk_score']} ({result['risk_level']})")
        print(f"   Likelihood: {result['likelihood']}/5, Impact: {result['impact']}/5")
        print(f"   Primary Impact: {result['primary_impact']}")
        print(f"   Location Multiplier: {result['location_multiplier']:.1f}x")

        if result['adjustments_made']:
            print(f"📈 Risk Adjustments:")
            for adjustment in result['adjustments_made']:
                print(f"   • {adjustment}")

        if result['travel_risk_assessment']:
            travel_risk = result['travel_risk_assessment']
            print(f"✈️ Travel Risk Assessment:")
            print(f"   Travel Risk Level: {travel_risk['travel_risk_level']}")
            print(f"   Executive Travel Impact: {travel_risk['executive_travel_impact']}")
            if travel_risk['enhanced_security_required']:
                print(f"   🛡️ Enhanced Security Required")

        if result['executive_notifications']['immediate_notification_required']:
            print(f"🚨 Executive Notifications:")
            notifications = result['executive_notifications']
            print(f"   Level: {notifications['notification_level']}")
            print(f"   Recipients: {', '.join(notifications['recipients'][:3])}...")

    print(f"\n✅ Enhanced risk calculation testing complete")
    print("Integration with travel intelligence and business impact modeling validated")


if __name__ == "__main__":
    test_enhanced_risk_calculations()
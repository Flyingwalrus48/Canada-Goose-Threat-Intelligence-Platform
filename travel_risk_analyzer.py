# travel_risk_analyzer.py - Advanced Travel Risk Intelligence for Canada Goose

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random


class TravelRiskAnalyzer:
    """
    Advanced travel risk analysis engine specifically designed for Canada Goose's
    business-critical locations and executive travel requirements.

    Integrates SEC filing risks with real-world travel intelligence.
    """

    def __init__(self):
        self.business_critical_locations = self._init_business_locations()
        self.geopolitical_events = self._init_geopolitical_events()
        self.travel_risk_matrix = self._init_risk_matrix()
        self.executive_protocols = self._init_executive_protocols()

    def _init_business_locations(self):
        """Initialize Canada Goose business-critical locations with specific risks"""
        return {
            # Greater China Market (17.7% revenue at risk)
            "Shanghai, China": {
                "business_function": "Greater China Regional Hub",
                "revenue_impact": "17.7% of total revenue",
                "sec_filing_risk": "Geopolitical tensions affecting market access",
                "critical_assets": ["flagship store", "regional office", "distribution center"],
                "risk_factors": {
                    "geopolitical": 9,  # High due to trade tensions
                    "regulatory": 8,  # Government restrictions possible
                    "civil_unrest": 3,  # Generally stable
                    "crime": 4,  # Moderate urban crime
                    "health": 6,  # Post-COVID monitoring
                    "infrastructure": 7  # Generally good but restrictions possible
                },
                "specific_threats": [
                    "Nationalist backlash against Canadian brands",
                    "Government restrictions on luxury goods",
                    "Social media campaign boycotts",
                    "Regulatory compliance changes"
                ]
            },

            "Beijing, China": {
                "business_function": "Government Relations & Market Access",
                "revenue_impact": "Critical for China market retention",
                "sec_filing_risk": "Trade policy changes affecting operations",
                "critical_assets": ["government liaison office", "key partnerships"],
                "risk_factors": {
                    "geopolitical": 9,
                    "regulatory": 9,  # Capital city - high regulatory risk
                    "civil_unrest": 2,  # Heavily controlled
                    "crime": 3,
                    "health": 6,
                    "infrastructure": 8
                },
                "specific_threats": [
                    "Diplomatic incidents affecting business",
                    "Regulatory crackdowns on foreign brands",
                    "Executive detention risk during tensions",
                    "Restricted movement during political events"
                ]
            },

            # European Flagship Operations
            "London, UK": {
                "business_function": "European Flagship & Regional Hub",
                "revenue_impact": "Key EMEA market revenue",
                "sec_filing_risk": "Activist protests disrupting operations",
                "critical_assets": ["Regent Street flagship", "European office"],
                "risk_factors": {
                    "geopolitical": 4,
                    "regulatory": 5,
                    "civil_unrest": 6,  # Protest activity
                    "crime": 5,
                    "health": 3,
                    "infrastructure": 8
                },
                "specific_threats": [
                    "PETA protests at flagship stores",
                    "Animal rights activism campaigns",
                    "Store blockades during peak seasons",
                    "Negative media coverage from protests"
                ]
            },

            "Paris, France": {
                "business_function": "European Luxury Market",
                "revenue_impact": "High-value European sales",
                "sec_filing_risk": "Activist protests and civil unrest",
                "critical_assets": ["Champs-Élysées store", "luxury partnerships"],
                "risk_factors": {
                    "geopolitical": 4,
                    "regulatory": 6,
                    "civil_unrest": 7,  # Higher protest activity
                    "crime": 6,
                    "health": 3,
                    "infrastructure": 7
                },
                "specific_threats": [
                    "French animal rights group coordination",
                    "General strike disruptions",
                    "Yellow vest movement spillover",
                    "Luxury goods targeting by activists"
                ]
            },

            # North American Operations
            "Toronto, ON": {
                "business_function": "Global Headquarters",
                "revenue_impact": "Corporate operations center",
                "sec_filing_risk": "Concentration of business functions",
                "critical_assets": ["HQ", "design center", "executive team"],
                "risk_factors": {
                    "geopolitical": 3,
                    "regulatory": 4,
                    "civil_unrest": 4,
                    "crime": 4,
                    "health": 3,
                    "infrastructure": 8
                },
                "specific_threats": [
                    "Executive targeting by activists",
                    "Corporate espionage attempts",
                    "Headquarters security breaches",
                    "Business continuity disruptions"
                ]
            },

            "New York, NY": {
                "business_function": "US Market Flagship",
                "revenue_impact": "Key North American revenue",
                "sec_filing_risk": "Activist protests at retail locations",
                "critical_assets": ["SoHo flagship", "US operations"],
                "risk_factors": {
                    "geopolitical": 3,
                    "regulatory": 5,
                    "civil_unrest": 6,
                    "crime": 7,
                    "health": 4,
                    "infrastructure": 7
                },
                "specific_threats": [
                    "Organized retail crime targeting luxury goods",
                    "PETA headquarters proximity - higher protest risk",
                    "Social media-coordinated flash protests",
                    "High-value theft targeting winter inventory"
                ]
            },

            # Supply Chain Critical Locations
            "Winnipeg, MB": {
                "business_function": "Manufacturing Hub",
                "revenue_impact": "Core production capacity",
                "sec_filing_risk": "Unionized workforce disruptions",
                "critical_assets": ["manufacturing facilities", "down processing"],
                "risk_factors": {
                    "geopolitical": 2,
                    "regulatory": 4,
                    "civil_unrest": 5,  # Labor disputes
                    "crime": 3,
                    "health": 3,
                    "infrastructure": 7
                },
                "specific_threats": [
                    "Labor strikes during peak production",
                    "Supply chain disruptions affecting manufacturing",
                    "Quality control issues under pressure",
                    "Union negotiations impacting operations"
                ]
            }
        }

    def _init_geopolitical_events(self):
        """Current geopolitical events affecting Canada Goose operations"""
        return [
            {
                "event": "Canada-China Diplomatic Tensions",
                "impact_level": "HIGH",
                "affected_locations": ["Shanghai, China", "Beijing, China"],
                "description": "Ongoing diplomatic tensions affecting Canadian business operations",
                "business_impact": "17.7% of revenue at risk from Greater China market access restrictions",
                "monitoring_indicators": [
                    "Chinese social media sentiment toward Canadian brands",
                    "Government policy announcements on foreign luxury goods",
                    "Customs and regulatory enforcement changes",
                    "Nationalist campaign organization online"
                ],
                "duration": "Ongoing",
                "escalation_risk": "MEDIUM"
            },
            {
                "event": "European Animal Rights Activism Surge",
                "impact_level": "MEDIUM",
                "affected_locations": ["London, UK", "Paris, France"],
                "description": "Coordinated European animal rights campaigns targeting fur and down products",
                "business_impact": "Store operations disruption, brand reputation risk",
                "monitoring_indicators": [
                    "PETA campaign announcements",
                    "Social media activism coordination",
                    "Local animal rights group activities",
                    "Seasonal protest pattern analysis"
                ],
                "duration": "Seasonal (October-February)",
                "escalation_risk": "MEDIUM"
            },
            {
                "event": "Global Supply Chain Disruptions",
                "impact_level": "MEDIUM",
                "affected_locations": ["All locations"],
                "description": "Ongoing global logistics and material sourcing challenges",
                "business_impact": "Manufacturing delays, cost increases, inventory management",
                "monitoring_indicators": [
                    "Shipping route disruptions",
                    "Raw material price volatility",
                    "Supplier facility closures",
                    "Transportation strikes"
                ],
                "duration": "Ongoing",
                "escalation_risk": "LOW"
            }
        ]

    def _init_risk_matrix(self):
        """Travel risk assessment matrix for Canada Goose executives"""
        return {
            "risk_categories": {
                "geopolitical": {
                    "weight": 0.25,
                    "description": "Government relations, diplomatic tensions, policy changes"
                },
                "regulatory": {
                    "weight": 0.20,
                    "description": "Business compliance, regulatory changes, legal risks"
                },
                "civil_unrest": {
                    "weight": 0.15,
                    "description": "Protests, demonstrations, activist activities"
                },
                "crime": {
                    "weight": 0.15,
                    "description": "Personal security, theft, organized crime"
                },
                "health": {
                    "weight": 0.15,
                    "description": "Disease outbreaks, medical infrastructure, health emergencies"
                },
                "infrastructure": {
                    "weight": 0.10,
                    "description": "Transportation, communications, utilities reliability"
                }
            },
            "risk_levels": {
                1: {"level": "MINIMAL", "color": "green", "action": "Standard precautions"},
                2: {"level": "LOW", "color": "green", "action": "Standard precautions"},
                3: {"level": "LOW-MEDIUM", "color": "yellow", "action": "Enhanced awareness"},
                4: {"level": "MEDIUM", "color": "yellow", "action": "Enhanced awareness"},
                5: {"level": "MEDIUM", "color": "orange", "action": "Enhanced security measures"},
                6: {"level": "MEDIUM-HIGH", "color": "orange", "action": "Enhanced security measures"},
                7: {"level": "HIGH", "color": "red", "action": "Executive protection required"},
                8: {"level": "HIGH", "color": "red", "action": "Executive protection required"},
                9: {"level": "CRITICAL", "color": "darkred", "action": "Travel not recommended"},
                10: {"level": "CRITICAL", "color": "darkred", "action": "Travel prohibited"}
            }
        }

    def _init_executive_protocols(self):
        """Executive travel security protocols by risk level"""
        return {
            "MINIMAL": {
                "pre_travel": ["Standard travel booking", "Basic itinerary review"],
                "during_travel": ["Check-in protocols", "Standard communications"],
                "security_measures": ["Corporate credit cards", "Travel insurance"],
                "reporting": ["Standard trip reports"]
            },
            "LOW": {
                "pre_travel": ["Enhanced itinerary review", "Local contact verification"],
                "during_travel": ["Enhanced check-in protocols", "Local security awareness"],
                "security_measures": ["Secure transportation booking", "Emergency contacts"],
                "reporting": ["Enhanced trip reports", "Incident reporting"]
            },
            "MEDIUM": {
                "pre_travel": ["Security briefing", "Threat assessment review", "Alternative plans"],
                "during_travel": ["Regular check-ins", "Secure communications", "Situational awareness"],
                "security_measures": ["Executive protection consultation", "Secure accommodations"],
                "reporting": ["Daily situation reports", "Immediate incident reporting"]
            },
            "HIGH": {
                "pre_travel": ["Comprehensive security briefing", "Executive protection planning"],
                "during_travel": ["Continuous monitoring", "Executive protection team", "Secure transport"],
                "security_measures": ["24/7 security support", "Emergency evacuation plans"],
                "reporting": ["Real-time monitoring", "Immediate escalation protocols"]
            },
            "CRITICAL": {
                "pre_travel": ["Travel not recommended"],
                "during_travel": ["Emergency procedures only"],
                "security_measures": ["Maximum security protocols"],
                "reporting": ["Crisis management protocols"]
            }
        }

    def assess_location_risk(self, location: str) -> Dict:
        """Comprehensive risk assessment for specific business location"""
        if location not in self.business_critical_locations:
            return {"error": f"Location {location} not in business-critical database"}

        location_data = self.business_critical_locations[location]
        risk_factors = location_data["risk_factors"]

        # Calculate weighted risk score
        weighted_score = 0
        risk_breakdown = {}

        for category, score in risk_factors.items():
            if category in self.travel_risk_matrix["risk_categories"]:
                weight = self.travel_risk_matrix["risk_categories"][category]["weight"]
                weighted_score += score * weight
                risk_breakdown[category] = {
                    "score": score,
                    "weight": weight,
                    "weighted_contribution": score * weight
                }

        # Determine overall risk level
        overall_risk_level = min(10, max(1, int(weighted_score)))
        risk_level_info = self.travel_risk_matrix["risk_levels"][overall_risk_level]

        # Get current events affecting this location
        relevant_events = [
            event for event in self.geopolitical_events
            if location in event["affected_locations"] or "All locations" in event["affected_locations"]
        ]

        return {
            "location": location,
            "business_function": location_data["business_function"],
            "revenue_impact": location_data["revenue_impact"],
            "overall_risk_score": round(weighted_score, 2),
            "risk_level": risk_level_info["level"],
            "risk_color": risk_level_info["color"],
            "recommended_action": risk_level_info["action"],
            "risk_breakdown": risk_breakdown,
            "specific_threats": location_data["specific_threats"],
            "current_events": relevant_events,
            "sec_filing_context": location_data["sec_filing_risk"],
            "executive_protocols": self.executive_protocols.get(risk_level_info["level"], {}),
            "assessment_timestamp": datetime.now().isoformat()
        }

    def generate_executive_travel_brief(self, destination: str, travel_purpose: str = "Business Operations",
                                        executive_level: str = "Senior Leadership") -> Dict:
        """Generate comprehensive executive travel security brief"""

        # Get base risk assessment
        risk_assessment = self.assess_location_risk(destination)

        if "error" in risk_assessment:
            return risk_assessment

        # Enhanced briefing for executives
        brief = {
            "classification": "FOR OFFICIAL USE ONLY",
            "briefing_type": "Executive Travel Security Assessment",
            "destination": destination,
            "executive_level": executive_level,
            "travel_purpose": travel_purpose,
            "assessment_date": datetime.now().strftime("%Y-%m-%d"),
            "validity_period": f"{datetime.now().strftime('%Y-%m-%d')} to {(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')}",

            # Executive Summary (BLUF)
            "executive_summary": {
                "overall_risk": risk_assessment["risk_level"],
                "key_concerns": self._generate_key_concerns(risk_assessment),
                "business_context": risk_assessment["revenue_impact"],
                "recommendation": risk_assessment["recommended_action"]
            },

            # Detailed Risk Analysis
            "threat_analysis": {
                "primary_risks": self._prioritize_risks(risk_assessment["risk_breakdown"]),
                "specific_threats": risk_assessment["specific_threats"],
                "current_events": risk_assessment["current_events"],
                "sec_filing_context": risk_assessment["sec_filing_context"]
            },

            # Security Protocols
            "security_protocols": {
                "pre_travel_requirements": risk_assessment["executive_protocols"].get("pre_travel", []),
                "travel_procedures": risk_assessment["executive_protocols"].get("during_travel", []),
                "security_measures": risk_assessment["executive_protocols"].get("security_measures", []),
                "communication_protocols": self._generate_communication_protocols(risk_assessment["risk_level"])
            },

            # Operational Considerations
            "operational_intelligence": {
                "business_function_risks": risk_assessment["business_function"],
                "local_considerations": self._generate_local_considerations(destination),
                "contingency_plans": self._generate_contingency_plans(risk_assessment["risk_level"]),
                "emergency_contacts": self._generate_emergency_contacts(destination)
            },

            # Recommendations
            "recommendations": {
                "immediate_actions": self._generate_immediate_actions(risk_assessment),
                "risk_mitigation": self._generate_mitigation_strategies(risk_assessment),
                "monitoring_requirements": self._generate_monitoring_requirements(destination)
            }
        }

        return brief

    def _generate_key_concerns(self, assessment: Dict) -> List[str]:
        """Generate key executive concerns based on risk assessment"""
        concerns = []

        # High-risk categories become key concerns
        for category, data in assessment["risk_breakdown"].items():
            if data["score"] >= 7:
                concerns.append(f"HIGH {category.upper()} RISK: {data['score']}/10")

        # Add business-specific concerns
        if "China" in assessment["location"]:
            concerns.append("GEOPOLITICAL: 17.7% revenue exposure from China market tensions")

        if assessment["risk_level"] in ["HIGH", "CRITICAL"]:
            concerns.append("EXECUTIVE PROTECTION: Enhanced security measures required")

        return concerns[:5]  # Top 5 concerns

    def _prioritize_risks(self, risk_breakdown: Dict) -> List[Dict]:
        """Prioritize risks by weighted impact"""
        risks = []
        for category, data in risk_breakdown.items():
            risks.append({
                "category": category.title(),
                "score": data["score"],
                "impact": data["weighted_contribution"],
                "priority": "HIGH" if data["score"] >= 7 else "MEDIUM" if data["score"] >= 5 else "LOW"
            })

        return sorted(risks, key=lambda x: x["impact"], reverse=True)

    def _generate_communication_protocols(self, risk_level: str) -> List[str]:
        """Generate communication protocols based on risk level"""
        base_protocols = [
            "Secure smartphone with VPN capability",
            "Emergency contact verification before travel",
            "Daily check-in with Global Security"
        ]

        if risk_level in ["HIGH", "CRITICAL"]:
            base_protocols.extend([
                "Encrypted communication apps only",
                "Hourly check-ins during high-risk periods",
                "24/7 security operations center monitoring",
                "Emergency satellite communication backup"
            ])
        elif risk_level == "MEDIUM":
            base_protocols.extend([
                "Enhanced check-in frequency (twice daily)",
                "Secure communication during sensitive meetings"
            ])

        return base_protocols

    def _generate_local_considerations(self, destination: str) -> List[str]:
        """Generate location-specific operational considerations"""
        considerations = []

        if "China" in destination:
            considerations = [
                "VPN access may be restricted - prepare alternative communication methods",
                "Sensitive business discussions should occur in secure locations only",
                "Social media activity should be minimal and non-political",
                "Government liaison protocols required for official meetings",
                "Customs declarations must be meticulous to avoid delays"
            ]
        elif "London" in destination or "Paris" in destination:
            considerations = [
                "Monitor animal rights group activity before flagship store visits",
                "Avoid public identification with Canada Goose during protest seasons",
                "Use alternative entrances for retail location visits if protests active",
                "Coordinate with local security for store visit timing"
            ]
        elif "Toronto" in destination:
            considerations = [
                "Headquarters security protocols in effect",
                "Executive parking and entrance procedures",
                "Visitor management and screening processes",
                "Conference room security for sensitive discussions"
            ]

        return considerations

    def _generate_contingency_plans(self, risk_level: str) -> List[str]:
        """Generate contingency plans based on risk level"""
        base_plans = [
            "Alternative transportation routes identified",
            "Emergency contact list with local authorities",
            "Medical emergency response procedures"
        ]

        if risk_level in ["HIGH", "CRITICAL"]:
            base_plans.extend([
                "Emergency evacuation procedures and rally points",
                "Safe house locations identified",
                "Emergency cash and documentation storage",
                "Immediate extraction protocols available"
            ])
        elif risk_level == "MEDIUM":
            base_plans.extend([
                "Alternative meeting locations prepared",
                "Local security contractor on standby"
            ])

        return base_plans

    def _generate_emergency_contacts(self, destination: str) -> Dict:
        """Generate relevant emergency contacts for destination"""
        return {
            "canada_goose_global_security": "+1-416-555-0100",
            "local_emergency_services": "911" if "Canada" in destination or "United States" in destination else "112",
            "canadian_embassy": "+1-613-996-8885 (Global Affairs Canada 24/7)",
            "local_security_contractor": f"+{random.randint(100, 999)}-555-{random.randint(1000, 9999)}",
            "executive_protection_team": "+1-416-555-0150",
            "crisis_management_center": "+1-416-555-0200"
        }

    def _generate_immediate_actions(self, assessment: Dict) -> List[str]:
        """Generate immediate pre-travel actions"""
        actions = [
            "Review and approve detailed itinerary with Global Security",
            "Confirm secure transportation arrangements",
            "Verify emergency contact information and communication protocols"
        ]

        if assessment["risk_level"] in ["HIGH", "CRITICAL"]:
            actions.extend([
                "Schedule executive protection briefing",
                "Coordinate with local security contractors",
                "Establish emergency evacuation procedures",
                "Prepare crisis communication protocols"
            ])

        return actions

    def _generate_mitigation_strategies(self, assessment: Dict) -> List[str]:
        """Generate risk mitigation strategies"""
        strategies = []

        # Risk-specific mitigation
        for category, data in assessment["risk_breakdown"].items():
            if data["score"] >= 6:
                if category == "geopolitical":
                    strategies.append("Maintain low profile and avoid political discussions")
                elif category == "civil_unrest":
                    strategies.append("Monitor protest activities and avoid demonstration areas")
                elif category == "crime":
                    strategies.append("Use secure transportation and avoid displaying valuable items")

        # General high-risk mitigation
        if assessment["risk_level"] in ["HIGH", "CRITICAL"]:
            strategies.append("Consider virtual meeting alternatives if operationally feasible")

        return strategies

    def _generate_monitoring_requirements(self, destination: str) -> List[str]:
        """Generate ongoing monitoring requirements"""
        return [
            "Real-time security situation monitoring",
            "Local news and social media sentiment tracking",
            "Weather and transportation disruption alerts",
            "Government travel advisory updates",
            f"Canada Goose-specific threat monitoring for {destination}"
        ]

    def get_global_risk_overview(self) -> Dict:
        """Get overview of risks across all business-critical locations"""
        overview = {
            "assessment_timestamp": datetime.now().isoformat(),
            "total_locations": len(self.business_critical_locations),
            "risk_summary": {},
            "high_risk_locations": [],
            "active_events": len(self.geopolitical_events),
            "business_impact_summary": {}
        }

        # Assess all locations
        risk_levels = {"MINIMAL": 0, "LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}

        for location in self.business_critical_locations:
            assessment = self.assess_location_risk(location)
            risk_level = assessment["risk_level"]

            # Count risk levels
            for level in risk_levels:
                if level in risk_level:
                    risk_levels[level] += 1
                    break

            # Identify high-risk locations
            if assessment["overall_risk_score"] >= 6:
                overview["high_risk_locations"].append({
                    "location": location,
                    "risk_level": risk_level,
                    "risk_score": assessment["overall_risk_score"],
                    "business_function": assessment["business_function"]
                })

        overview["risk_summary"] = risk_levels

        # Business impact summary
        china_locations = [loc for loc in self.business_critical_locations if "China" in loc]
        if china_locations:
            avg_china_risk = sum(self.assess_location_risk(loc)["overall_risk_score"] for loc in china_locations) / len(
                china_locations)
            overview["business_impact_summary"]["greater_china_risk"] = {
                "average_risk_score": round(avg_china_risk, 2),
                "revenue_at_risk": "17.7%",
                "status": "HIGH PRIORITY MONITORING"
            }

        return overview


def predict_travel_impacts(destination: str, current_events: List[Dict]) -> Dict:
    """
    Predict potential travel impacts based on current intelligence
    Legacy function for compatibility with existing dashboard
    """
    analyzer = TravelRiskAnalyzer()

    # Generate travel brief
    brief = analyzer.generate_executive_travel_brief(destination)

    if "error" in brief:
        return {
            "destination": destination,
            "overall_risk": "UNKNOWN",
            "predicted_impacts": ["Location not in business-critical database"],
            "recommendations": ["Use general travel risk assessment procedures"]
        }

    return {
        "destination": destination,
        "overall_risk": brief["executive_summary"]["overall_risk"],
        "predicted_impacts": brief["executive_summary"]["key_concerns"],
        "recommendations": brief["recommendations"]["immediate_actions"][:3],
        "business_context": brief["executive_summary"]["business_context"]
    }
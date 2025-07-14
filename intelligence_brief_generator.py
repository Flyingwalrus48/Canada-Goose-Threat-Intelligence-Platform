# intelligence_brief_generator.py - Professional Intelligence Brief for Canada Goose

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class IntelligenceBriefGenerator:
    """
    Generate professional intelligence briefs for Canada Goose executive leadership
    following standard intelligence community formats and protocols.
    """

    def __init__(self, travel_analyzer, geo_monitor, analyzed_events, corporate_data):
        self.travel_analyzer = travel_analyzer
        self.geo_monitor = geo_monitor
        self.analyzed_events = analyzed_events
        self.corporate_data = corporate_data

    def generate_executive_intelligence_brief(self, brief_type: str = "weekly") -> str:
        """Generate comprehensive executive intelligence brief"""

        current_date = datetime.now()

        # Collect intelligence data
        geo_summary = self.geo_monitor.get_current_intelligence_summary()
        travel_overview = self.travel_analyzer.get_global_risk_overview()
        high_risk_events = [e for e in self.analyzed_events if e['analysis']['risk_assessment']['risk_score'] >= 15]

        # Generate brief content
        brief = self._generate_brief_header(brief_type, current_date)
        brief += self._generate_executive_summary(geo_summary, travel_overview, high_risk_events)
        brief += self._generate_threat_analysis(high_risk_events, geo_summary)
        brief += self._generate_travel_intelligence(travel_overview)
        brief += self._generate_business_impact_assessment()
        brief += self._generate_recommendations_and_actions()
        brief += self._generate_brief_footer()

        return brief

    def _generate_brief_header(self, brief_type: str, date: datetime) -> str:
        """Generate professional intelligence brief header"""

        classification = "FOR OFFICIAL USE ONLY (FOUO)"

        header = f"""
{classification}

CANADA GOOSE HOLDINGS INC.
GLOBAL SECURITY INTELLIGENCE BRIEF

TO:         Executive Leadership Team
FROM:       Global Security Intelligence & Travel Risk Analyst  
DATE:       {date.strftime('%d %B %Y')}
SUBJECT:    {brief_type.title()} Global Security Intelligence Assessment

CLASSIFICATION: {classification}
HANDLING: This brief contains proprietary business intelligence. Distribution limited to authorized personnel only.

"""
        return header

    def _generate_executive_summary(self, geo_summary: Dict, travel_overview: Dict, high_risk_events: List) -> str:
        """Generate executive summary with BLUF format"""

        # Calculate key metrics
        total_high_priority_geo = geo_summary["alert_counts"]["high_priority"]
        high_risk_locations = len(travel_overview["high_risk_locations"])
        critical_security_events = len(
            [e for e in high_risk_events if e['analysis']['risk_assessment']['risk_score'] >= 20])
        china_revenue_exposure = self.corporate_data['key_financials']['revenue_from_greater_china_pct']

        # Construct BLUF
        bluf_components = []

        if critical_security_events > 0:
            bluf_components.append(
                f"{critical_security_events} critical security incidents requiring immediate executive attention")

        if total_high_priority_geo > 0:
            bluf_components.append(
                f"{total_high_priority_geo} high-priority geopolitical events affecting business operations")

        if high_risk_locations > 0:
            bluf_components.append(f"{high_risk_locations} business-critical locations at elevated travel risk")

        # China-specific concerns
        china_threats = [threat for threat in self.geo_monitor.threat_indicators if "china" in threat.lower()]
        if china_threats:
            bluf_components.append(
                f"geopolitical tensions threatening {china_revenue_exposure}% revenue from Greater China market")

        if bluf_components:
            bluf_statement = f"BOTTOM LINE UP FRONT: {'; '.join(bluf_components)}. Enhanced monitoring and executive engagement recommended."
        else:
            bluf_statement = "BOTTOM LINE UP FRONT: No critical threats identified this assessment period. Standard security posture maintained across all global operations."

        summary = f"""
1. EXECUTIVE SUMMARY

{bluf_statement}

KEY METRICS:
• Global Locations Monitored: {travel_overview['total_locations']} business-critical sites
• High-Risk Travel Destinations: {high_risk_locations}
• Critical Security Events: {critical_security_events}
• High-Priority Geopolitical Alerts: {total_high_priority_geo}
• Revenue at Risk (Greater China): {china_revenue_exposure}%

EXECUTIVE ATTENTION REQUIRED: {'YES' if geo_summary['executive_attention_required'] or critical_security_events > 0 else 'NO'}

"""
        return summary

    def _generate_threat_analysis(self, high_risk_events: List, geo_summary: Dict) -> str:
        """Generate detailed threat analysis section"""

        analysis = """
2. THREAT ANALYSIS

2.1 SECURITY INCIDENT ASSESSMENT

"""

        if high_risk_events:
            # Categorize events by type
            event_categories = {}
            for event in high_risk_events:
                event_type = event.get('type', 'General')
                if event_type not in event_categories:
                    event_categories[event_type] = []
                event_categories[event_type].append(event)

            for category, events in event_categories.items():
                analysis += f"   {category.upper()}:\n"

                for event in events[:2]:  # Top 2 per category
                    risk_score = event['analysis']['risk_assessment']['risk_score']
                    risk_level = event['analysis']['risk_assessment']['risk_level']

                    analysis += f"   • {event['title']} (Risk Score: {risk_score} - {risk_level})\n"
                    analysis += f"     Location: {event['location']}\n"
                    analysis += f"     Business Impact: {event['analysis']['risk_assessment']['primary_impact']}\n"

                    # Add key risk factors if available
                    if 'adjustments_made' in event['analysis']['risk_assessment']:
                        key_factors = event['analysis']['risk_assessment']['adjustments_made'][:2]
                        for factor in key_factors:
                            analysis += f"     Risk Factor: {factor}\n"

                    analysis += "\n"
        else:
            analysis += "   No high-risk security incidents identified in current assessment period.\n\n"

        # Geopolitical intelligence section
        analysis += "2.2 GEOPOLITICAL INTELLIGENCE\n\n"

        if geo_summary["recent_high_impact_events"]:
            for event in geo_summary["recent_high_impact_events"]:
                analysis += f"   • {event['headline']}\n"
                analysis += f"     Region: {event['region'].title()}\n"
                analysis += f"     Priority: {event['priority']}\n"
                analysis += f"     Business Impact: {event['business_impact']}\n\n"
        else:
            analysis += "   Current geopolitical environment stable with no high-impact events affecting operations.\n\n"

        return analysis

    def _generate_travel_intelligence(self, travel_overview: Dict) -> str:
        """Generate travel intelligence and executive protection guidance"""

        intelligence = """
3. TRAVEL INTELLIGENCE & EXECUTIVE PROTECTION

3.1 GLOBAL TRAVEL RISK ASSESSMENT

"""

        # Overall risk status
        high_risk_count = len(travel_overview["high_risk_locations"])
        total_locations = travel_overview["total_locations"]

        intelligence += f"   Risk Status: {high_risk_count}/{total_locations} business-critical locations at elevated risk\n\n"

        # High-risk destinations
        if travel_overview["high_risk_locations"]:
            intelligence += "   HIGH-RISK DESTINATIONS:\n"

            for location in travel_overview["high_risk_locations"]:
                intelligence += f"   • {location['location']}: {location['risk_level']} Risk (Score: {location['risk_score']:.1f}/10)\n"
                intelligence += f"     Business Function: {location['business_function']}\n"

                # Get specific travel recommendations
                if location['location'] in ["Shanghai, China", "Beijing, China"]:
                    intelligence += "     Travel Considerations: Enhanced diplomatic protocols, secure communications required\n"
                elif location['location'] in ["London, UK", "Paris, France"]:
                    intelligence += "     Travel Considerations: Monitor activist activity, enhanced store visit security\n"
                elif location['location'] in ["New York, NY"]:
                    intelligence += "     Travel Considerations: Organized retail crime awareness, enhanced urban security\n"

                intelligence += "\n"
        else:
            intelligence += "   All monitored destinations within acceptable risk parameters.\n\n"

        # Executive travel protocols
        intelligence += "3.2 EXECUTIVE TRAVEL PROTOCOLS\n\n"
        intelligence += "   STANDARD REQUIREMENTS:\n"
        intelligence += "   • Pre-travel security briefings for all business-critical destinations\n"
        intelligence += "   • Secure transportation and accommodation arrangements\n"
        intelligence += "   • Regular check-in protocols with Global Security\n"
        intelligence += "   • Emergency contact verification and communication procedures\n\n"

        if high_risk_count > 0:
            intelligence += "   ENHANCED PROTOCOLS (High-Risk Destinations):\n"
            intelligence += "   • Executive protection assessment required\n"
            intelligence += "   • Advanced security briefings with threat-specific guidance\n"
            intelligence += "   • 24/7 security monitoring and support\n"
            intelligence += "   • Emergency evacuation procedures briefed\n\n"

        return intelligence

    def _generate_business_impact_assessment(self) -> str:
        """Generate business impact and revenue risk assessment"""

        assessment = """
4. BUSINESS IMPACT ASSESSMENT

4.1 REVENUE EXPOSURE ANALYSIS

"""

        # China market analysis
        china_revenue = self.corporate_data['key_financials']['revenue_from_greater_china_pct']
        assessment += f"   GREATER CHINA MARKET ({china_revenue}% of revenue):\n"

        # Check for China-related threats
        china_threats = []
        for alert in self.geo_monitor.intelligence_feeds:
            if "china" in alert['region'].lower() and alert['priority'] in ["HIGH", "MEDIUM"]:
                china_threats.append(alert)

        if china_threats:
            assessment += f"     Status: ELEVATED RISK - {len(china_threats)} active geopolitical concerns\n"
            assessment += "     Impact: Potential market access restrictions could affect revenue\n"
            assessment += "     Mitigation: Enhanced diplomatic engagement, alternative market strategies\n\n"
        else:
            assessment += "     Status: STABLE - No immediate threats to market access\n"
            assessment += "     Impact: Revenue stream secure under current conditions\n\n"

        # Operational impact analysis
        assessment += "4.2 OPERATIONAL IMPACT SUMMARY\n\n"

        # Store operations
        flagship_threats = [e for e in self.analyzed_events
                            if any(city in e.get('location', '') for city in ['London', 'Paris', 'New York'])
                            and e['analysis']['risk_assessment']['risk_score'] >= 10]

        if flagship_threats:
            assessment += f"   RETAIL OPERATIONS: {len(flagship_threats)} threats affecting flagship store operations\n"
            assessment += "     Impact: Potential store disruptions, enhanced security costs\n"
            assessment += "     Mitigation: Crisis response protocols, enhanced store security\n\n"
        else:
            assessment += "   RETAIL OPERATIONS: No significant threats to store operations\n\n"

        # Supply chain assessment
        supply_threats = [e for e in self.analyzed_events
                          if 'supply' in e.get('details', '').lower()
                          and e['analysis']['risk_assessment']['risk_score'] >= 10]

        if supply_threats:
            assessment += f"   SUPPLY CHAIN: {len(supply_threats)} potential disruptions identified\n"
            assessment += "     Impact: Manufacturing delays, cost increases possible\n"
            assessment += "     Mitigation: Supplier diversification, inventory buffering\n\n"
        else:
            assessment += "   SUPPLY CHAIN: Operations within normal parameters\n\n"

        return assessment

    def _generate_recommendations_and_actions(self) -> str:
        """Generate strategic recommendations and immediate actions"""

        recommendations = """
5. STRATEGIC RECOMMENDATIONS & IMMEDIATE ACTIONS

5.1 IMMEDIATE EXECUTIVE ACTIONS (Next 7 Days)

"""

        # Generate specific recommendations based on current threats
        immediate_actions = []
        strategic_actions = []

        # High-priority geopolitical alerts
        high_geo_alerts = [alert for alert in self.geo_monitor.intelligence_feeds if alert["priority"] == "HIGH"]
        if high_geo_alerts:
            immediate_actions.append("Review high-priority geopolitical alerts with Government Relations team")
            strategic_actions.append("Develop enhanced diplomatic engagement strategy for affected regions")

        # China market risks
        china_alerts = [alert for alert in self.geo_monitor.intelligence_feeds
                        if "china" in alert['region'].lower() and alert['priority'] in ["HIGH", "MEDIUM"]]
        if china_alerts:
            immediate_actions.append("Assess Greater China market contingency plans")
            strategic_actions.append("Diversify Asian market presence to reduce China dependency")

        # High-risk travel locations
        travel_overview = self.travel_analyzer.get_global_risk_overview()
        if travel_overview["high_risk_locations"]:
            immediate_actions.append("Brief executives on enhanced travel security protocols")
            strategic_actions.append("Review and update executive protection procedures")

        # Critical security events
        critical_events = [e for e in self.analyzed_events if e['analysis']['risk_assessment']['risk_score'] >= 20]
        if critical_events:
            immediate_actions.append("Convene emergency security briefing for critical incidents")
            strategic_actions.append("Enhance crisis communication and response capabilities")

        # Default actions if no major threats
        if not (high_geo_alerts or china_alerts or critical_events):
            immediate_actions.extend([
                "Continue standard security monitoring across all regions",
                "Review and update threat assessment protocols",
                "Conduct routine executive travel security briefings"
            ])
            strategic_actions.extend([
                "Enhance intelligence collection capabilities",
                "Strengthen relationships with local security partners",
                "Invest in predictive threat analysis systems"
            ])

        # Format recommendations
        for i, action in enumerate(immediate_actions, 1):
            recommendations += f"   {i}. {action}\n"

        recommendations += "\n5.2 STRATEGIC INITIATIVES (Next 30 Days)\n\n"

        for i, action in enumerate(strategic_actions, 1):
            recommendations += f"   {i}. {action}\n"

        recommendations += "\n5.3 MONITORING AND ASSESSMENT\n\n"
        recommendations += "   • Continue daily geopolitical intelligence monitoring\n"
        recommendations += "   • Maintain weekly executive travel risk assessments\n"
        recommendations += "   • Conduct monthly business impact reviews\n"
        recommendations += "   • Update threat indicators and risk models quarterly\n\n"

        return recommendations

    def _generate_brief_footer(self) -> str:
        """Generate professional brief footer"""

        next_assessment = (datetime.now() + timedelta(days=7)).strftime('%d %B %Y')

        footer = f"""
6. NEXT ASSESSMENT

Next scheduled intelligence brief: {next_assessment}

DISTRIBUTION:
• CEO and Executive Leadership Team
• Global Security Director
• Chief Risk Officer
• Regional Leadership (As Applicable)

CLASSIFICATION: FOR OFFICIAL USE ONLY (FOUO)

This brief is prepared by the Global Security Intelligence & Travel Risk Analyst and represents 
current threat assessments based on available intelligence. Threat levels and recommendations 
may change based on evolving conditions.

For questions or additional intelligence requirements, contact Global Security at ext.
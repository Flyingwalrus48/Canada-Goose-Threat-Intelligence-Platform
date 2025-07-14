# activist_counter_intelligence_predictor.py - Advanced Counter-Intelligence for Canada Goose

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ThreatLevel(Enum):
    """Threat assessment levels for counter-intelligence"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class OperationType(Enum):
    """Types of activist operations"""
    SURVEILLANCE = "SURVEILLANCE"
    INFILTRATION = "INFILTRATION"
    INVESTIGATION = "INVESTIGATION"
    MEDIA_CAMPAIGN = "MEDIA_CAMPAIGN"
    CERTIFICATION_CHALLENGE = "CERTIFICATION_CHALLENGE"


@dataclass
class ThreatActor:
    """Enhanced threat actor profile"""
    name: str
    organization: str
    location: str
    capabilities: List[str]
    known_ttps: List[str]
    success_record: List[str]
    current_focus: str
    threat_level: ThreatLevel


@dataclass
class CounterIntelIndicator:
    """Counter-intelligence indicator for I&W system"""
    indicator_id: str
    description: str
    current_status: str  # GREEN, YELLOW, RED
    trend: str  # STABLE, INCREASING, DECREASING
    confidence_level: int  # 1-100
    last_updated: datetime
    trigger_threshold: str
    impact_assessment: str


class ActivistCounterIntelligencePredictor:
    """
    Advanced counter-intelligence predictor for activist operations targeting
    Canada Goose's post-fur supply chain integrity and RDS certification.

    Focus: Sophisticated activist espionage operations, not basic protests.
    """

    def __init__(self):
        self.threat_actors = self._init_threat_actors()
        self.counter_intel_indicators = self._init_indicators()
        self.operation_predictions = self._init_operation_predictions()
        self.moncler_precedent_analysis = self._init_moncler_analysis()

    def _init_threat_actors(self) -> Dict[str, ThreatActor]:
        """Initialize sophisticated threat actor profiles"""
        return {
            "LAV_ITALY": ThreatActor(
                name="Lega Anti Vivisezione (LAV)",
                organization="Italian Animal Rights Organization",
                location="Milan, Italy",
                capabilities=[
                    "Professional undercover investigations",
                    "Media campaign coordination",
                    "Corporate pressure campaigns",
                    "Legal advocacy and litigation",
                    "European activist network coordination"
                ],
                known_ttps=[
                    "Long-term corporate engagement campaigns",
                    "Supply chain investigation and exposure",
                    "Certification standard challenges",
                    "Executive and supplier targeting",
                    "Media-ready evidence documentation"
                ],
                success_record=[
                    "Moncler fur-free policy (2022)",
                    "Multiple Italian fashion brand policy changes",
                    "EU-wide animal welfare advocacy victories"
                ],
                current_focus="Post-fur strategy: Challenging RDS certification integrity and investigating down supply chains",
                threat_level=ThreatLevel.HIGH
            ),

            "PETA_GLOBAL": ThreatActor(
                name="People for the Ethical Treatment of Animals",
                organization="Global Animal Rights Organization",
                location="Multiple (HQ: Norfolk, VA)",
                capabilities=[
                    "Global campaign coordination",
                    "Celebrity and influencer engagement",
                    "Professional investigative operations",
                    "Legal and regulatory pressure",
                    "Social media amplification networks"
                ],
                known_ttps=[
                    "Undercover facility investigations",
                    "Executive personal targeting campaigns",
                    "Shareholder pressure tactics",
                    "Supply chain infiltration attempts",
                    "Certification body pressure campaigns"
                ],
                success_record=[
                    "Canada Goose fur-free commitment (influenced)",
                    "Multiple luxury brand policy changes",
                    "Fashion Week disruption campaigns"
                ],
                current_focus="Escalated RDS challenge campaign following fur-free victory",
                threat_level=ThreatLevel.HIGH
            ),

            "COALITION_EUROPEAN": ThreatActor(
                name="European Animal Rights Coalition",
                organization="Coordinated European Activist Network",
                location="Multiple European Cities",
                capabilities=[
                    "Multi-country operation coordination",
                    "Resource and intelligence sharing",
                    "Synchronized campaign execution",
                    "Regulatory influence operations",
                    "Supply chain mapping capabilities"
                ],
                known_ttps=[
                    "Simultaneous multi-city operations",
                    "Supply chain personnel tracking",
                    "Facility location identification",
                    "Coordinated media releases",
                    "Regulatory complaint filing"
                ],
                success_record=[
                    "Coordinated EU-wide campaigns",
                    "Multiple supply chain exposures",
                    "Policy influence operations"
                ],
                current_focus="Coordinated investigation of luxury brand down sourcing across Europe",
                threat_level=ThreatLevel.MEDIUM
            )
        }

    def _init_indicators(self) -> Dict[str, CounterIntelIndicator]:
        """Initialize Indicators & Warnings (I&W) system"""
        return {
            "SUPPLY_CHAIN_SURVEILLANCE": CounterIntelIndicator(
                indicator_id="SCS-001",
                description="Unusual interest in Canada Goose supply chain personnel or facilities",
                current_status="YELLOW",
                trend="INCREASING",
                confidence_level=75,
                last_updated=datetime.now(),
                trigger_threshold="Evidence of personnel being followed or photographed",
                impact_assessment="Could lead to supplier identification and targeting"
            ),

            "RDS_CERTIFICATION_CHALLENGE": CounterIntelIndicator(
                indicator_id="RCC-002",
                description="Public challenges to RDS certification credibility or methodology",
                current_status="YELLOW",
                trend="INCREASING",
                confidence_level=80,
                last_updated=datetime.now(),
                trigger_threshold="Published reports questioning RDS standards",
                impact_assessment="Could undermine consumer trust in ethical sourcing claims"
            ),

            "MILAN_OPERATIONAL_ACTIVITY": CounterIntelIndicator(
                indicator_id="MOA-003",
                description="LAV operational activity increase in Milan during expansion period",
                current_status="YELLOW",
                trend="STABLE",
                confidence_level=70,
                last_updated=datetime.now(),
                trigger_threshold="Increased LAV communications or resource allocation",
                impact_assessment="Could target Milan expansion with supply chain focus"
            ),

            "ROMANIA_FACILITY_INTEREST": CounterIntelIndicator(
                indicator_id="RFI-004",
                description="Activist interest in European supply chain operations (Romania focus)",
                current_status="GREEN",
                trend="STABLE",
                confidence_level=60,
                last_updated=datetime.now(),
                trigger_threshold="Unusual activity near Titu facility or personnel tracking",
                impact_assessment="Could expose key European supply chain relationships"
            ),

            "EXECUTIVE_TARGETING": CounterIntelIndicator(
                indicator_id="EXT-005",
                description="Activist attempts to identify and track supply chain executives",
                current_status="YELLOW",
                trend="INCREASING",
                confidence_level=85,
                last_updated=datetime.now(),
                trigger_threshold="Social media or professional network reconnaissance of executives",
                impact_assessment="Could lead to surveillance during business travel"
            )
        }

    def _init_operation_predictions(self) -> Dict[str, Dict]:
        """Initialize operation predictions based on intelligence analysis"""
        return {
            "MILAN_RDS_INVESTIGATION": {
                "operation_type": OperationType.INVESTIGATION,
                "predicted_timeframe": "Q4 2025 - Q1 2026",
                "probability": 0.75,
                "threat_actors": ["LAV_ITALY", "COALITION_EUROPEAN"],
                "target": "Milan retail expansion and European supply chain",
                "objectives": [
                    "Identify European down suppliers",
                    "Document supply chain practices",
                    "Challenge RDS certification credibility",
                    "Generate media exposé content"
                ],
                "likely_ttps": [
                    "Executive surveillance during business travel",
                    "Facility location identification",
                    "Supply chain personnel tracking",
                    "Undercover supplier investigations"
                ],
                "indicators": [
                    "Increased LAV activity in Milan area",
                    "Unusual interest in Canada Goose business travel",
                    "Social media reconnaissance of supply chain executives",
                    "Coordination with other European activist groups"
                ],
                "business_impact": "HIGH - Could force supply chain changes and damage RDS credibility",
                "recommended_countermeasures": [
                    "Enhanced executive travel security protocols",
                    "Counter-surveillance training for supply chain personnel",
                    "Secure communications for sensitive business discussions",
                    "Alternative meeting locations for supplier engagements"
                ]
            },

            "ROMANIA_INFILTRATION_ATTEMPT": {
                "operation_type": OperationType.INFILTRATION,
                "predicted_timeframe": "Q1 2026",
                "probability": 0.60,
                "threat_actors": ["COALITION_EUROPEAN"],
                "target": "Paola Confectii facility and operations",
                "objectives": [
                    "Document manufacturing practices",
                    "Identify key suppliers and relationships",
                    "Gather evidence for RDS challenge",
                    "Create viral content exposing operations"
                ],
                "likely_ttps": [
                    "Employment infiltration attempts",
                    "Facility perimeter surveillance",
                    "Personnel relationship exploitation",
                    "Documentation and video evidence gathering"
                ],
                "indicators": [
                    "Unusual job applications from activist-affiliated individuals",
                    "Increased surveillance activity near Titu facility",
                    "Attempts to cultivate relationships with facility personnel",
                    "Suspicious photography or mapping activity"
                ],
                "business_impact": "CRITICAL - Could expose key supplier relationships and damage certification integrity",
                "recommended_countermeasures": [
                    "Enhanced facility security and access controls",
                    "Background screening for new personnel",
                    "Counter-surveillance detection systems",
                    "Employee awareness and reporting protocols"
                ]
            },

            "GLOBAL_RDS_DELEGITIMIZATION": {
                "operation_type": OperationType.CERTIFICATION_CHALLENGE,
                "predicted_timeframe": "Ongoing - Q2 2026 peak",
                "probability": 0.85,
                "threat_actors": ["PETA_GLOBAL", "LAV_ITALY", "COALITION_EUROPEAN"],
                "target": "RDS certification system and credibility",
                "objectives": [
                    "Frame RDS as industry 'humane-washing'",
                    "Pressure RDS certifying bodies",
                    "Generate consumer doubt about ethical claims",
                    "Force stricter standards or abandonment"
                ],
                "likely_ttps": [
                    "Academic and scientific criticism campaigns",
                    "Media investigations of RDS facilities",
                    "Celebrity and influencer engagement",
                    "Regulatory pressure and complaint filing"
                ],
                "indicators": [
                    "Published critiques of RDS methodology",
                    "Pressure campaigns against RDS certifying bodies",
                    "Media investigations of RDS-certified facilities",
                    "Academic papers questioning RDS effectiveness"
                ],
                "business_impact": "CRITICAL - Could undermine entire ethical sourcing foundation",
                "recommended_countermeasures": [
                    "Proactive RDS transparency initiatives",
                    "Third-party validation of practices",
                    "Academic and scientific engagement",
                    "Alternative certification strategy development"
                ]
            }
        }

    def _init_moncler_analysis(self) -> Dict:
        """Initialize Moncler precedent analysis for tactical prediction"""
        return {
            "campaign_timeline": {
                "initial_pressure": "2018-2019",
                "escalation_phase": "2020-2021",
                "victory_achievement": "January 2022",
                "total_duration": "3-4 years"
            },
            "tactical_progression": [
                "Public awareness campaigns about fur use",
                "Direct corporate engagement and dialogue",
                "Media pressure and negative coverage",
                "Consumer pressure and social media campaigns",
                "Long-term sustained pressure until policy change"
            ],
            "key_success_factors": [
                "LAV's local presence and credibility in Italy",
                "Sustained, professional campaign execution",
                "Focus on corporate engagement rather than just protests",
                "Strategic timing during corporate sustainability focus",
                "Coordination with international activist networks"
            ],
            "canada_goose_adaptation": {
                "target_shift": "From fur to down supply chain",
                "tactical_evolution": "From corporate pressure to supply chain investigation",
                "new_vulnerabilities": [
                    "RDS certification credibility",
                    "Supply chain transparency gaps",
                    "Executive travel exposure during supplier meetings",
                    "Facility and supplier location exposure"
                ],
                "predicted_campaign_duration": "2-3 years (2025-2027)",
                "critical_decision_points": [
                    "First major supply chain exposé",
                    "RDS certification challenge success",
                    "Consumer sentiment tipping point",
                    "Corporate policy response decision"
                ]
            },
            "intelligence_assessment": {
                "probability_of_similar_success": 0.70,
                "most_likely_victory_condition": "RDS policy strengthening or alternative certification adoption",
                "business_impact_timeline": "Significant impact within 18-24 months",
                "recommended_preemptive_actions": [
                    "Proactive supply chain transparency initiatives",
                    "Enhanced RDS compliance verification",
                    "Stakeholder engagement and communication strategy",
                    "Alternative certification pathway development"
                ]
            }
        }

    def assess_current_threat_level(self) -> Dict:
        """Assess current overall threat level from activist operations"""

        # Calculate indicator-based threat level
        indicator_scores = []
        for indicator in self.counter_intel_indicators.values():
            if indicator.current_status == "RED":
                indicator_scores.append(3)
            elif indicator.current_status == "YELLOW":
                indicator_scores.append(2)
            else:
                indicator_scores.append(1)

        avg_indicator_score = sum(indicator_scores) / len(indicator_scores)

        # Determine overall threat level
        if avg_indicator_score >= 2.5:
            overall_threat = ThreatLevel.HIGH
        elif avg_indicator_score >= 2.0:
            overall_threat = ThreatLevel.MEDIUM
        else:
            overall_threat = ThreatLevel.LOW

        # Count indicators by status
        status_counts = {"GREEN": 0, "YELLOW": 0, "RED": 0}
        for indicator in self.counter_intel_indicators.values():
            status_counts[indicator.current_status] += 1

        # High-probability operations
        high_prob_ops = [
            op_name for op_name, op_data in self.operation_predictions.items()
            if op_data["probability"] >= 0.7
        ]

        return {
            "overall_threat_level": overall_threat.value,
            "indicator_summary": status_counts,
            "average_indicator_score": round(avg_indicator_score, 2),
            "high_probability_operations": high_prob_ops,
            "assessment_timestamp": datetime.now().isoformat(),
            "executive_attention_required": overall_threat in [ThreatLevel.HIGH, ThreatLevel.CRITICAL],
            "immediate_actions_needed": len(
                [i for i in self.counter_intel_indicators.values() if i.current_status == "RED"]) > 0
        }

    def generate_operation_prediction(self, operation_name: str) -> Dict:
        """Generate detailed prediction for specific operation"""

        if operation_name not in self.operation_predictions:
            return {"error": f"Operation {operation_name} not found"}

        operation = self.operation_predictions[operation_name]

        # Calculate tactical confidence based on Moncler precedent
        moncler_similarity = self._calculate_moncler_similarity(operation)

        # Generate timeline prediction
        timeline = self._generate_operation_timeline(operation)

        # Assess countermeasures effectiveness
        countermeasure_assessment = self._assess_countermeasures(operation)

        return {
            "operation_name": operation_name,
            "prediction_confidence": operation["probability"],
            "moncler_precedent_similarity": moncler_similarity,
            "operation_details": operation,
            "predicted_timeline": timeline,
            "countermeasure_effectiveness": countermeasure_assessment,
            "business_impact_forecast": self._forecast_business_impact(operation),
            "recommended_immediate_actions": operation["recommended_countermeasures"][:3],
            "monitoring_priorities": self._generate_monitoring_priorities(operation)
        }

    def _calculate_moncler_similarity(self, operation: Dict) -> float:
        """Calculate similarity to Moncler campaign for tactical prediction"""

        # Key similarity factors
        factors = {
            "italian_location": 0.8 if "LAV_ITALY" in operation["threat_actors"] else 0.0,
            "supply_chain_focus": 0.9 if operation["operation_type"] == OperationType.INVESTIGATION else 0.3,
            "certification_challenge": 0.9 if "RDS" in str(operation["objectives"]) else 0.2,
            "long_term_campaign": 0.8 if operation["predicted_timeframe"] and "Q" in operation[
                "predicted_timeframe"] else 0.4
        }

        # Weighted average similarity
        weights = {"italian_location": 0.3, "supply_chain_focus": 0.3, "certification_challenge": 0.3,
                   "long_term_campaign": 0.1}

        similarity = sum(factors[factor] * weights[factor] for factor in factors)
        return round(similarity, 2)

    def _generate_operation_timeline(self, operation: Dict) -> Dict:
        """Generate predicted timeline for operation"""

        current_date = datetime.now()

        # Parse timeframe
        timeframe = operation["predicted_timeframe"]
        if "Q4 2025" in timeframe:
            start_date = datetime(2025, 10, 1)
            end_date = datetime(2026, 3, 31)
        elif "Q1 2026" in timeframe:
            start_date = datetime(2026, 1, 1)
            end_date = datetime(2026, 6, 30)
        else:
            start_date = current_date + timedelta(days=30)
            end_date = current_date + timedelta(days=365)

        # Generate phase breakdown
        phases = []
        if operation["operation_type"] == OperationType.INVESTIGATION:
            phases = [
                {"phase": "Reconnaissance", "duration": "30-60 days",
                 "activities": ["Target identification", "Personnel tracking"]},
                {"phase": "Intelligence Gathering", "duration": "60-120 days",
                 "activities": ["Surveillance operations", "Source cultivation"]},
                {"phase": "Documentation", "duration": "30-90 days",
                 "activities": ["Evidence collection", "Media preparation"]},
                {"phase": "Publication", "duration": "7-30 days", "activities": ["Media release", "Campaign launch"]}
            ]

        return {
            "predicted_start": start_date.strftime("%Y-%m-%d"),
            "predicted_end": end_date.strftime("%Y-%m-%d"),
            "days_until_start": (start_date - current_date).days if start_date > current_date else 0,
            "total_duration_days": (end_date - start_date).days,
            "operation_phases": phases,
            "critical_windows": [
                "Milan fashion week periods (high visibility)",
                "Quarterly earnings periods (maximum business impact)",
                "Winter season (peak product relevance)"
            ]
        }

    def _assess_countermeasures(self, operation: Dict) -> Dict:
        """Assess effectiveness of recommended countermeasures"""

        countermeasures = operation["recommended_countermeasures"]

        effectiveness_scores = []
        for countermeasure in countermeasures:
            if "surveillance" in countermeasure.lower():
                effectiveness_scores.append(0.8)  # High effectiveness against surveillance
            elif "security" in countermeasure.lower():
                effectiveness_scores.append(0.7)  # Good effectiveness for security measures
            elif "communication" in countermeasure.lower():
                effectiveness_scores.append(0.6)  # Moderate effectiveness for communications
            else:
                effectiveness_scores.append(0.5)  # Default moderate effectiveness

        avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else 0.5

        return {
            "overall_effectiveness": round(avg_effectiveness, 2),
            "high_impact_measures": [cm for cm in countermeasures if
                                     "surveillance" in cm.lower() or "security" in cm.lower()],
            "implementation_priority": "HIGH" if avg_effectiveness < 0.6 else "MEDIUM",
            "estimated_risk_reduction": f"{int(avg_effectiveness * 100)}%",
            "additional_recommendations": [
                "Proactive stakeholder engagement",
                "Enhanced threat intelligence collection",
                "Legal preparedness for activist challenges",
                "Crisis communication strategy development"
            ]
        }

    def _forecast_business_impact(self, operation: Dict) -> Dict:
        """Forecast business impact of predicted operation"""

        impact_level = operation["business_impact"]

        # Define impact scenarios
        scenarios = {
            "HIGH": {
                "revenue_risk": "5-15% of affected market segment",
                "reputation_impact": "Significant negative media coverage",
                "operational_disruption": "Supply chain modifications required",
                "recovery_timeline": "6-18 months"
            },
            "CRITICAL": {
                "revenue_risk": "15-30% of affected market segment",
                "reputation_impact": "Major brand credibility challenge",
                "operational_disruption": "Major supply chain restructuring",
                "recovery_timeline": "12-36 months"
            }
        }

        scenario = scenarios.get(impact_level.replace("HIGH", "HIGH").replace("CRITICAL", "CRITICAL"),
                                 scenarios["HIGH"])

        return {
            "impact_level": impact_level,
            "scenario_details": scenario,
            "most_likely_outcome": "Forced enhancement of RDS compliance and transparency",
            "worst_case_scenario": "Abandonment of RDS certification for alternative standards",
            "mitigation_opportunities": [
                "Proactive transparency initiatives",
                "Stakeholder engagement programs",
                "Enhanced certification standards",
                "Supply chain diversification"
            ]
        }

    def _generate_monitoring_priorities(self, operation: Dict) -> List[str]:
        """Generate monitoring priorities for predicted operation"""

        base_priorities = [
            "Social media monitoring for activist coordination",
            "Executive travel pattern analysis",
            "Supply chain personnel security awareness",
            "Facility perimeter security assessments"
        ]

        # Add operation-specific priorities
        if operation["operation_type"] == OperationType.INVESTIGATION:
            base_priorities.extend([
                "Unusual interest in company personnel on professional networks",
                "Photography or surveillance activity near facilities",
                "Background check alerts for new hires or contractor applications"
            ])

        if "MILAN" in operation.get("target", "").upper():
            base_priorities.extend([
                "LAV organization activity and communications monitoring",
                "Milan area security situation awareness",
                "European activist coordination intelligence"
            ])

        return base_priorities[:7]  # Return top 7 priorities

    def generate_intelligence_brief(self) -> str:
        """Generate executive intelligence brief on activist counter-intelligence"""

        threat_assessment = self.assess_current_threat_level()

        brief = f"""
CLASSIFICATION: FOR OFFICIAL USE ONLY (FOUO)

CANADA GOOSE HOLDINGS INC.
ACTIVIST COUNTER-INTELLIGENCE ASSESSMENT

TO:         Executive Leadership Team
FROM:       Global Security Intelligence & Travel Risk Analyst
DATE:       {datetime.now().strftime('%d %B %Y')}
SUBJECT:    Activist Counter-Intelligence Threat Assessment - Post-Fur Strategy Analysis

1. EXECUTIVE SUMMARY (BLUF)

Current Threat Level: {threat_assessment['overall_threat_level']}

Following Canada Goose's 2022 fur-free commitment, activist groups have strategically shifted focus to challenging the Responsible Down Standard (RDS) certification integrity. Intelligence indicates high probability of sophisticated counter-intelligence operations targeting supply chain personnel and facilities, particularly in Europe.

Key Assessment: Activist groups are evolving from public protests to professional investigative operations designed to expose supply chain vulnerabilities and challenge corporate integrity claims.

2. THREAT EVOLUTION ANALYSIS

The Moncler Precedent indicates a clear tactical evolution:
- Previous Focus: Fur use and animal welfare protests
- Current Focus: Supply chain investigation and certification credibility
- New Threat Vectors: Executive surveillance, facility infiltration, supplier targeting

Primary Threat Actors:
- LAV (Italy): {self.threat_actors['LAV_ITALY'].current_focus}
- PETA (Global): {self.threat_actors['PETA_GLOBAL'].current_focus}

3. HIGH-PROBABILITY OPERATION PREDICTIONS

"""

        # Add high-probability operations
        for op_name, op_data in self.operation_predictions.items():
            if op_data["probability"] >= 0.7:
                brief += f"""
{op_name.replace('_', ' ').title()}:
- Probability: {int(op_data['probability'] * 100)}%
- Timeframe: {op_data['predicted_timeframe']}
- Business Impact: {op_data['business_impact']}
- Primary Objective: {op_data['objectives'][0]}
"""

        brief += f"""

4. INDICATORS & WARNINGS STATUS

Current Alert Status:
- RED Indicators: {threat_assessment['indicator_summary']['RED']}
- YELLOW Indicators: {threat_assessment['indicator_summary']['YELLOW']}
- GREEN Indicators: {threat_assessment['indicator_summary']['GREEN']}

Executive Attention Required: {'YES' if threat_assessment['executive_attention_required'] else 'NO'}

5. IMMEDIATE RECOMMENDATIONS

Priority Actions (Next 30 Days):
1. Implement enhanced executive travel security protocols for supply chain personnel
2. Conduct counter-surveillance training for Romania facility operations
3. Establish secure communications protocols for supplier engagement discussions
4. Review and enhance facility access controls and visitor screening procedures

Strategic Initiatives (Next 90 Days):
1. Develop proactive RDS transparency and verification program
2. Establish alternative supplier engagement protocols to reduce exposure
3. Create crisis communication strategy for potential supply chain exposés
4. Enhance threat intelligence collection on activist operational planning

6. ASSESSMENT CONFIDENCE

This assessment is based on:
- Moncler precedent tactical analysis (High Confidence)
- Known activist organization capabilities (High Confidence)  
- Supply chain vulnerability assessment (Medium-High Confidence)
- Timeline predictions (Medium Confidence)

Next Assessment: {(datetime.now() + timedelta(days=30)).strftime('%d %B %Y')}

CLASSIFICATION: FOR OFFICIAL USE ONLY (FOUO)
        """

        return brief.strip()


# Integration functions for existing platform
def get_activist_intelligence_summary() -> Dict:
    """Get summary for integration with existing geopolitical intelligence"""

    predictor = ActivistCounterIntelligencePredictor()
    threat_assessment = predictor.assess_current_threat_level()

    return {
        "threat_level": threat_assessment["overall_threat_level"],
        "high_probability_operations": threat_assessment["high_probability_operations"],
        "indicators_triggered": threat_assessment["indicator_summary"]["YELLOW"] +
                                threat_assessment["indicator_summary"]["RED"],
        "executive_attention_required": threat_assessment["executive_attention_required"],
        "assessment_type": "Activist Counter-Intelligence",
        "primary_concerns": [
            "RDS certification integrity challenges",
            "Supply chain personnel surveillance",
            "European facility infiltration attempts",
            "Executive travel security during supplier meetings"
        ]
    }


def get_travel_security_enhancements(destination: str) -> List[str]:
    """Get enhanced travel security recommendations for supply chain personnel"""

    predictor = ActivistCounterIntelligencePredictor()

    enhancements = [
        "Maintain operational security (OPSEC) regarding travel purpose and meetings",
        "Use non-company transportation and accommodation booking",
        "Avoid company-branded materials during supplier meetings",
        "Conduct counter-surveillance awareness before and during travel"
    ]

    # Location-specific enhancements
    if "milan" in destination.lower() or "italy" in destination.lower():
        enhancements.extend([
            "Enhanced awareness of LAV operational activity in Milan area",
            "Use alternative meeting locations away from company facilities",
            "Report any unusual interest or surveillance activity immediately"
        ])

    if "romania" in destination.lower():
        enhancements.extend([
            "Coordinate with facility security before arrival",
            "Use secure communications for all business discussions",
            "Vary travel routes and timing to facility visits"
        ])

    return enhancements


# Test function
def test_activist_counter_intelligence():
    """Test the activist counter-intelligence predictor"""

    print("🕵️ Testing Activist Counter-Intelligence Predictor...")

    predictor = ActivistCounterIntelligencePredictor()

    # Test threat assessment
    assessment = predictor.assess_current_threat_level()
    print(f"✅ Current Threat Level: {assessment['overall_threat_level']}")

    # Test operation prediction
    milan_prediction = predictor.generate_operation_prediction("MILAN_RDS_INVESTIGATION")
    print(f"✅ Milan Operation Confidence: {milan_prediction['prediction_confidence']}")

    # Test intelligence brief generation
    brief = predictor.generate_intelligence_brief()
    print(f"✅ Generated intelligence brief ({len(brief)} characters)")

    print("🎯 Activist Counter-Intelligence Predictor ready for integration!")

    return True


if __name__ == "__main__":
    test_activist_counter_intelligence()
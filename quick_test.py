# quick_test.py
print("🧪 Testing Canada Goose Intelligence Platform...")

try:
    from travel_risk_analyzer import TravelRiskAnalyzer

    print("✅ TravelRiskAnalyzer imported successfully")

    analyzer = TravelRiskAnalyzer()
    result = analyzer.assess_location_risk("Shanghai, China")
    print(f"✅ Shanghai Risk Score: {result.get('overall_risk_score', 'Error')}")

except Exception as e:
    print(f"❌ Error: {e}")

try:
    from geopolitical_intelligence import GeopoliticalIntelligenceMonitor

    print("✅ GeopoliticalIntelligenceMonitor imported successfully")

    monitor = GeopoliticalIntelligenceMonitor()
    summary = monitor.get_current_intelligence_summary()
    print(f"✅ Geopolitical alerts: {summary.get('alert_counts', {}).get('total', 'Error')}")

except Exception as e:
    print(f"❌ Geopolitical Error: {e}")

print("🎯 Test complete!")
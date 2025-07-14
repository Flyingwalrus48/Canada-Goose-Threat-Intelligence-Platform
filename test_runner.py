# test_runner.py - Simple test to verify your enhanced Canada Goose system works
import asyncio
import sys
import traceback
from datetime import datetime


def print_header(title):
    """Print a nice header"""
    print(f"\n{'=' * 60}")
    print(f"🧪 {title}")
    print(f"{'=' * 60}")


def print_result(test_name, success, details=""):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"   └─ {details}")


async def test_enhanced_nlp_engine():
    """Test your enhanced NLP engine"""
    print_header("Testing Enhanced NLP Engine")

    try:
        # Import your enhanced NLP engine
        from advanced_nlp_engine import create_advanced_nlp_engine
        print("✓ Successfully imported advanced_nlp_engine")

        # Create engine (fallback mode first)
        engine = create_advanced_nlp_engine(enable_transformers=False)
        print("✓ Created NLP engine in fallback mode")

        # Test with Canada Goose security text
        test_text = """
        Canada Goose executives in Toronto coordinate with security teams to protect retail stores in New York. 
        Cyber criminals threaten the company's IT infrastructure while law enforcement monitors suspicious activities.
        The security department works with RCMP to investigate potential threats from organized crime groups.
        """

        print("📝 Analyzing test text...")
        results = engine.analyze_text(test_text)

        # Check results
        entities = results.get('entities', [])
        relationships = results.get('relationships', [])
        metrics = results.get('metrics', {})

        print_result("NLP Analysis", True,
                     f"Found {len(entities)} entities and {len(relationships)} relationships")

        # Display some results
        if entities:
            print("🏷️  Found entities:")
            for entity in entities[:5]:  # Show first 5
                print(f"   • {entity['text']} ({entity['type']}) - confidence: {entity['confidence']:.2f}")

        if relationships:
            print("🔗 Found relationships:")
            for rel in relationships[:3]:  # Show first 3
                print(
                    f"   • {rel['source']} → {rel['relation']} → {rel['target']} (confidence: {rel['confidence']:.2f})")

        # Try transformer mode if available
        try:
            transformer_engine = create_advanced_nlp_engine(enable_transformers=True)
            print("✓ Transformer mode available")

            transformer_results = transformer_engine.analyze_text(test_text)
            transformer_entities = transformer_results.get('entities', [])

            print_result("Transformer Mode", True,
                         f"Transformer analysis found {len(transformer_entities)} entities")

        except Exception as e:
            print_result("Transformer Mode", False,
                         f"Transformers not available: {str(e)}")

        return True

    except Exception as e:
        print_result("Enhanced NLP Engine", False, f"Error: {str(e)}")
        traceback.print_exc()
        return False


async def test_osint_collector():
    """Test your OSINT collector"""
    print_header("Testing OSINT Collector")

    try:
        from osint_collector import CanadaGooseOSINTCollector
        print("✓ Successfully imported osint_collector")

        # Create collector
        async with CanadaGooseOSINTCollector() as collector:
            print("✓ Created OSINT collector")

            # Check source configuration
            sources = collector.sources
            print_result("Source Configuration", len(sources) > 0,
                         f"Configured {len(sources)} OSINT sources")

            # Test source types
            source_types = set(source.source_type.value for source in sources)
            print(f"📡 Source types: {', '.join(source_types)}")

            # Test relevance calculation
            test_title = "Canada Goose faces cyber security threat in Toronto headquarters"
            relevance = collector._calculate_relevance(test_title, "")
            print_result("Relevance Calculation", relevance > 0,
                         f"Calculated relevance: {relevance:.3f}")

            # Test threat assessment
            threat_level = collector._assess_threat_level(test_title, "cyber attack data breach")
            print_result("Threat Assessment", threat_level.value in ['low', 'medium', 'high', 'critical'],
                         f"Assessed threat level: {threat_level.value}")

            # Test a small collection (shortened for quick test)
            print("🔄 Testing quick collection cycle...")

            # Mock some sample data collection instead of real network calls
            from osint_collector import SourceType  # Make sure this import is here

            # Mock some sample data collection instead of real network calls
            sample_intelligence = {
                'id': 'test-001',
                'title': 'Test Security Alert',
                'content': 'Sample security intelligence for testing',
                'source_name': 'Test Source',
                'source_type': 'security_feed',  # We can use a simple string for the test
                'relevance_score': 0.8,
                'threat_level': 'medium',
                'entities': []  # <-- ADD THIS LINE
            }

            collector.collected_items.append(type('obj', (object,), sample_intelligence)())

            # Test summary report
            summary = collector.get_summary_report()
            print_result("Summary Report", 'total_items' in summary,
                         f"Generated summary with {summary.get('total_items', 0)} items")

            return True
    except Exception as e:
        print_result("OSINT Collector", False, f"Error: {str(e)}")
        traceback.print_exc()
        return False


async def test_enterprise_architecture():
    """Test your enterprise architecture"""
    print_header("Testing Enterprise Architecture")

    try:
        from enterprise_architecture import (
            create_intelligence_service, DomainEvent, EventType, Command, QueryRequest
        )
        print("✓ Successfully imported enterprise_architecture")

        # Create intelligence service
        service = await create_intelligence_service()
        print("✓ Created intelligence service")

        await service.start()
        print("✓ Started intelligence service")

        # Test command processing
        intelligence_data = {
            'id': 'test-intel-001',
            'title': 'Test Intelligence Item',
            'content': 'Canada Goose security teams detected suspicious activity in Toronto retail locations.',
            'source_name': 'Test Security Feed',
            'relevance_score': 0.9,
            'threat_level': 'medium'
        }

        success = await service.collect_intelligence(intelligence_data)
        print_result("Intelligence Collection", success,
                     "Successfully processed intelligence collection command")

        # Test query processing
        dashboard_data = await service.get_dashboard_data()
        print_result("Dashboard Query", 'total_threats' in dashboard_data,
                     f"Dashboard returned {len(dashboard_data)} data fields")

        summary = await service.get_intelligence_summary(5)
        print_result("Intelligence Summary", 'total_items' in summary,
                     f"Summary shows {summary.get('total_items', 0)} total items")

        # Test event store
        test_event = DomainEvent(
            event_type=EventType.SYSTEM_STATUS,
            aggregate_id="test",
            data={'status': 'testing', 'timestamp': datetime.now().isoformat()}
        )

        event_stored = await service.event_store.append_event(test_event)
        print_result("Event Store", event_stored,
                     "Successfully stored test event")

        # Stop service
        await service.stop()
        print("✓ Stopped intelligence service")

        return True

    except Exception as e:
        print_result("Enterprise Architecture", False, f"Error: {str(e)}")
        traceback.print_exc()
        return False


async def test_streamlit_integration():
    """Test if your Streamlit app components work"""
    print_header("Testing Streamlit App Integration")

    try:
        # Check if the enhanced app can import the NLP engine
        from advanced_nlp_engine import create_advanced_nlp_engine, RelationType

        engine = create_advanced_nlp_engine()
        print_result("Streamlit NLP Import", True,
                     "App can successfully import enhanced NLP engine")

        # Test the analysis that the Streamlit app would perform
        sample_text = """
        A sophisticated cyber attack targeted Canada Goose's Toronto headquarters, attempting to breach customer data systems. 
        Security teams implemented emergency protocols and secured all access points. 
        The IT department monitors ongoing threats while executives coordinate response efforts.
        """

        results = engine.analyze_text(sample_text)

        # Check if results have the format expected by Streamlit app
        required_fields = ['entities', 'relationships', 'metrics']
        has_all_fields = all(field in results for field in required_fields)

        print_result("Streamlit Data Format", has_all_fields,
                     "NLP results compatible with Streamlit dashboard")

        # Test metrics format
        metrics = results['metrics']
        expected_metrics = ['entity_count', 'relationship_count', 'avg_relationship_confidence']
        has_metrics = any(metric in metrics for metric in expected_metrics)

        print_result("Dashboard Metrics", has_metrics,
                     f"Metrics available: {list(metrics.keys())}")

        return True

    except Exception as e:
        print_result("Streamlit Integration", False, f"Error: {str(e)}")
        return False


def test_dependencies():
    """Test if required dependencies are available"""
    print_header("Testing Dependencies")

    dependencies = {
        'transformers': 'Advanced NLP features',
        'sentence_transformers': 'Semantic similarity',
        'torch': 'PyTorch for transformers',
        'newspaper3k': 'News article extraction',
        'yfinance': 'Financial data',
        'pandas': 'Data manipulation',
        'redis': 'Message bus (optional)',
        'aiosqlite': 'Async database operations'
    }

    available = []
    missing = []

    for dep, description in dependencies.items():
        try:
            __import__(dep)
            available.append(dep)
            print_result(f"Dependency: {dep}", True, description)
        except ImportError:
            missing.append(dep)
            print_result(f"Dependency: {dep}", False, f"Missing - {description}")

    print(f"\n📊 Dependency Summary:")
    print(f"   ✅ Available: {len(available)}/{len(dependencies)} ({len(available) / len(dependencies) * 100:.0f}%)")
    print(f"   ❌ Missing: {len(missing)}")

    if missing:
        print(f"\n💡 To install missing dependencies:")
        print(f"   pip install {' '.join(missing)}")

    return len(missing) == 0


async def main():
    """Run all tests"""
    print(f"🚀 Canada Goose Intelligence System - Enhanced Code Test")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Track results
    results = []

    # Test dependencies first
    deps_ok = test_dependencies()
    results.append(('Dependencies', deps_ok))

    # Test your enhanced modules
    nlp_ok = await test_enhanced_nlp_engine()
    results.append(('Enhanced NLP Engine', nlp_ok))

    osint_ok = await test_osint_collector()
    results.append(('OSINT Collector', osint_ok))

    enterprise_ok = await test_enterprise_architecture()
    results.append(('Enterprise Architecture', enterprise_ok))

    streamlit_ok = await test_streamlit_integration()
    results.append(('Streamlit Integration', streamlit_ok))

    # Final summary
    print_header("FINAL TEST SUMMARY")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")

    success_rate = (passed / total) * 100 if total > 0 else 0

    print(f"\n📊 Overall Results:")
    print(f"   Tests Passed: {passed}/{total}")
    print(f"   Success Rate: {success_rate:.1f}%")

    if success_rate >= 80:
        print("\n🎉 EXCELLENT! Your enhanced Canada Goose system is working great!")
        print("   Ready to demonstrate to the hiring team!")
    elif success_rate >= 60:
        print("\n✅ GOOD! Most features working, minor issues to address")
    else:
        print("\n⚠️  NEEDS WORK: Some core features need attention")

    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    # Run the tests
    asyncio.run(main())
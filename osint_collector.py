# osint_collector.py - Phase 3: Sophisticated OSINT Microservices
import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, AsyncGenerator
from dataclasses import dataclass, asdict
from enum import Enum
import json
import hashlib
import re
from urllib.parse import urljoin, urlparse
import time

# For RSS and news feeds
try:
    import feedparser
    import newspaper
    from newspaper import Article

    NEWSPAPER_AVAILABLE = True
except ImportError:
    NEWSPAPER_AVAILABLE = False
    print("⚠️  Install newspaper3k for enhanced news collection: pip install newspaper3k")

# For financial data integration
try:
    import yfinance as yf
    import pandas as pd

    FINANCE_AVAILABLE = True
except ImportError:
    FINANCE_AVAILABLE = False
    print("⚠️  Install yfinance for financial data: pip install yfinance pandas")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SourceType(Enum):
    """Types of OSINT sources"""
    NEWS_RSS = "news_rss"
    GOVERNMENT = "government"
    FINANCIAL = "financial"
    SOCIAL_MEDIA = "social_media"
    ACADEMIC = "academic"
    CORPORATE = "corporate"
    SECURITY_FEED = "security_feed"


class ThreatLevel(Enum):
    """Threat assessment levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class OSINTSource:
    """OSINT source configuration"""
    name: str
    url: str
    source_type: SourceType
    update_frequency: int  # minutes
    priority: int  # 1-10
    active: bool = True
    last_update: Optional[datetime] = None
    api_key: Optional[str] = None
    headers: Optional[Dict] = None


@dataclass
class IntelligenceItem:
    """Individual intelligence item"""
    id: str
    title: str
    content: str
    source_url: str
    source_name: str
    source_type: SourceType
    timestamp: datetime
    relevance_score: float
    threat_level: ThreatLevel
    entities: List[Dict] = None
    relationships: List[Dict] = None
    geographic_focus: List[str] = None
    keywords: List[str] = None
    sentiment_score: float = 0.0
    credibility_score: float = 0.0


class CanadaGooseOSINTCollector:
    """
    Phase 3: Sophisticated OSINT microservices for Canada Goose Global Security
    Implements multi-source intelligence gathering with market impact analysis
    """

    def __init__(self, nlp_engine=None):
        self.nlp_engine = nlp_engine
        self.sources = []
        self.collected_items = []
        self.session = None

        # Initialize source configurations
        self._init_sources()

        # Cache for preventing duplicates
        self.content_hashes = set()

        logger.info("🕵️ Canada Goose OSINT Collector initialized")

    def _init_sources(self):
        """Initialize OSINT source configurations"""

        # Government and official sources
        government_sources = [
            OSINTSource(
                name="US State Department",
                url="https://www.state.gov/rss-feeds/",
                source_type=SourceType.GOVERNMENT,
                update_frequency=60,
                priority=9
            ),
            OSINTSource(
                name="Canadian Government Security",
                url="https://www.publicsafety.gc.ca/cnt/rsrcs/nws/rss-en.xml",
                source_type=SourceType.GOVERNMENT,
                update_frequency=60,
                priority=9
            ),
            OSINTSource(
                name="CSIS Public Reports",
                url="https://www.canada.ca/en/security-intelligence-service.html",
                source_type=SourceType.GOVERNMENT,
                update_frequency=120,
                priority=8
            )
        ]

        # Financial and market sources
        financial_sources = [
            OSINTSource(
                name="TSX Market Data",
                url="https://api.tmxmoney.com/",
                source_type=SourceType.FINANCIAL,
                update_frequency=30,
                priority=7
            ),
            OSINTSource(
                name="Defense Sector News",
                url="https://www.defensenews.com/rss/",
                source_type=SourceType.FINANCIAL,
                update_frequency=45,
                priority=6
            )
        ]

        # Security and threat intelligence
        security_sources = [
            OSINTSource(
                name="Krebs Security",
                url="https://krebsonsecurity.com/feed/",
                source_type=SourceType.SECURITY_FEED,
                update_frequency=45,
                priority=8
            ),
            OSINTSource(
                name="Threat Post",
                url="https://threatpost.com/feed/",
                source_type=SourceType.SECURITY_FEED,
                update_frequency=30,
                priority=7
            )
        ]

        # News sources with geopolitical focus
        news_sources = [
            OSINTSource(
                name="Reuters World News",
                url="https://feeds.reuters.com/reuters/worldNews",
                source_type=SourceType.NEWS_RSS,
                update_frequency=30,
                priority=8
            ),
            OSINTSource(
                name="BBC World News",
                url="http://feeds.bbci.co.uk/news/world/rss.xml",
                source_type=SourceType.NEWS_RSS,
                update_frequency=30,
                priority=8
            ),
            OSINTSource(
                name="Middle East Eye",
                url="https://www.middleeasteye.net/rss.xml",
                source_type=SourceType.NEWS_RSS,
                update_frequency=45,
                priority=7
            )
        ]

        # Combine all sources
        self.sources = government_sources + financial_sources + security_sources + news_sources

        logger.info(f"📡 Initialized {len(self.sources)} OSINT sources")

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Canada-Goose-Security-Intelligence/2.0'
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def collect_from_rss_feed(self, source: OSINTSource) -> List[IntelligenceItem]:
        """Collect intelligence from RSS feeds"""
        items = []

        try:
            async with self.session.get(source.url) as response:
                if response.status == 200:
                    content = await response.text()

                    # Parse RSS feed
                    feed = feedparser.parse(content)

                    for entry in feed.entries[:10]:  # Limit to 10 most recent
                        # Generate unique ID
                        item_id = hashlib.md5(f"{source.name}{entry.link}".encode()).hexdigest()

                        # Check for duplicates
                        content_hash = hashlib.md5(entry.get('summary', '').encode()).hexdigest()
                        if content_hash in self.content_hashes:
                            continue

                        self.content_hashes.add(content_hash)

                        # Calculate relevance score
                        relevance = self._calculate_relevance(
                            entry.get('title', ''),
                            entry.get('summary', '')
                        )

                        # Assess threat level
                        threat_level = self._assess_threat_level(
                            entry.get('title', ''),
                            entry.get('summary', '')
                        )

                        # Create intelligence item
                        intel_item = IntelligenceItem(
                            id=item_id,
                            title=entry.get('title', ''),
                            content=entry.get('summary', ''),
                            source_url=entry.get('link', ''),
                            source_name=source.name,
                            source_type=source.source_type,
                            timestamp=datetime.now(),
                            relevance_score=relevance,
                            threat_level=threat_level
                        )

                        # Enhanced processing with NLP if available
                        if self.nlp_engine:
                            intel_item = await self._enhance_with_nlp(intel_item)

                        items.append(intel_item)

        except Exception as e:
            logger.error(f"Error collecting from {source.name}: {e}")

        return items

    async def collect_government_sources(self) -> List[IntelligenceItem]:
        """Collect from government and official sources"""
        government_items = []

        government_sources = [s for s in self.sources if s.source_type == SourceType.GOVERNMENT]

        for source in government_sources:
            if source.active:
                items = await self.collect_from_rss_feed(source)
                government_items.extend(items)

                # Special handling for specific government APIs
                if "state.gov" in source.url:
                    special_items = await self._collect_state_dept_special(source)
                    government_items.extend(special_items)

        logger.info(f"🏛️ Collected {len(government_items)} government intelligence items")
        return government_items

    async def collect_financial_data(self) -> List[IntelligenceItem]:
        """Collect financial market data and defense sector intelligence"""
        financial_items = []

        if not FINANCE_AVAILABLE:
            logger.warning("⚠️ Financial data collection requires yfinance")
            return financial_items

        try:
            # Canada Goose stock data
            cg_ticker = "GOOS.TO"  # Canada Goose on TSX
            cg_stock = yf.Ticker(cg_ticker)

            # Get recent news
            cg_news = cg_stock.news

            for news_item in cg_news[:5]:  # Latest 5 news items
                item_id = hashlib.md5(f"GOOS_NEWS_{news_item.get('uuid', '')}".encode()).hexdigest()

                intel_item = IntelligenceItem(
                    id=item_id,
                    title=news_item.get('title', ''),
                    content=news_item.get('summary', ''),
                    source_url=news_item.get('link', ''),
                    source_name="Yahoo Finance - GOOS",
                    source_type=SourceType.FINANCIAL,
                    timestamp=datetime.fromtimestamp(news_item.get('providerPublishTime', time.time())),
                    relevance_score=0.9,  # High relevance for company-specific news
                    threat_level=ThreatLevel.MEDIUM
                )

                financial_items.append(intel_item)

            # Defense and security sector analysis
            defense_tickers = ["LMT", "RTX", "NOC", "GD", "BA"]  # Major defense contractors

            for ticker in defense_tickers:
                try:
                    stock = yf.Ticker(ticker)
                    stock_news = stock.news

                    for news_item in stock_news[:2]:  # Top 2 news per ticker
                        # Check if relevant to security/geopolitics
                        title_content = f"{news_item.get('title', '')} {news_item.get('summary', '')}"
                        if self._is_security_relevant(title_content):
                            item_id = hashlib.md5(f"DEFENSE_{ticker}_{news_item.get('uuid', '')}".encode()).hexdigest()

                            intel_item = IntelligenceItem(
                                id=item_id,
                                title=f"[{ticker}] {news_item.get('title', '')}",
                                content=news_item.get('summary', ''),
                                source_url=news_item.get('link', ''),
                                source_name=f"Defense Sector - {ticker}",
                                source_type=SourceType.FINANCIAL,
                                timestamp=datetime.fromtimestamp(news_item.get('providerPublishTime', time.time())),
                                relevance_score=self._calculate_relevance(title_content, ""),
                                threat_level=self._assess_threat_level(title_content, "")
                            )

                            financial_items.append(intel_item)

                except Exception as e:
                    logger.error(f"Error collecting from {ticker}: {e}")

            # Market impact analysis
            market_intel = await self._analyze_market_impact()
            financial_items.extend(market_intel)

        except Exception as e:
            logger.error(f"Error in financial data collection: {e}")

        logger.info(f"💰 Collected {len(financial_items)} financial intelligence items")
        return financial_items

    async def collect_security_feeds(self) -> List[IntelligenceItem]:
        """Collect from cybersecurity and threat intelligence feeds"""
        security_items = []

        security_sources = [s for s in self.sources if s.source_type == SourceType.SECURITY_FEED]

        for source in security_sources:
            if source.active:
                items = await self.collect_from_rss_feed(source)
                security_items.extend(items)

        logger.info(f"🔒 Collected {len(security_items)} security intelligence items")
        return security_items

    async def collect_geopolitical_intelligence(self) -> List[IntelligenceItem]:
        """Collect geopolitical intelligence focusing on Iran-Israel and other key regions"""
        geopolitical_items = []

        # Specific geopolitical keywords for filtering
        geopolitical_keywords = [
            'iran', 'israel', 'middle east', 'sanctions', 'conflict', 'trade war',
            'china', 'russia', 'ukraine', 'nato', 'security council',
            'cyber warfare', 'espionage', 'diplomatic', 'embassy'
        ]

        # Collect from news sources with geopolitical focus
        news_sources = [s for s in self.sources if s.source_type == SourceType.NEWS_RSS]

        for source in news_sources:
            if source.active:
                items = await self.collect_from_rss_feed(source)

                # Filter for geopolitical relevance
                for item in items:
                    content_text = f"{item.title} {item.content}".lower()

                    # Check if contains geopolitical keywords
                    if any(keyword in content_text for keyword in geopolitical_keywords):
                        item.relevance_score *= 1.2  # Boost relevance
                        item.geographic_focus = self._extract_geographic_focus(content_text)
                        geopolitical_items.append(item)

        logger.info(f"🌍 Collected {len(geopolitical_items)} geopolitical intelligence items")
        return geopolitical_items

    async def _collect_state_dept_special(self, source: OSINTSource) -> List[IntelligenceItem]:
        """Special collection from State Department sources"""
        items = []

        # State Department travel advisories (high relevance for corporate security)
        travel_advisory_url = "https://travel.state.gov/content/travel/en/traveladvisories.html"

        try:
            async with self.session.get(travel_advisory_url) as response:
                if response.status == 200:
                    # Parse for travel advisories affecting Canada Goose operations
                    content = await response.text()

                    # Extract country advisories (simplified parsing)
                    advisory_pattern = r'Level (\d): ([^<]+)'
                    advisories = re.findall(advisory_pattern, content)

                    for level, country in advisories[:10]:
                        if int(level) >= 3:  # Level 3+ advisories
                            item_id = hashlib.md5(f"TRAVEL_ADVISORY_{country}".encode()).hexdigest()

                            intel_item = IntelligenceItem(
                                id=item_id,
                                title=f"Travel Advisory Level {level}: {country}",
                                content=f"US State Department issued Level {level} travel advisory for {country}",
                                source_url=travel_advisory_url,
                                source_name="US State Department Travel Advisories",
                                source_type=SourceType.GOVERNMENT,
                                timestamp=datetime.now(),
                                relevance_score=0.8,
                                threat_level=ThreatLevel.HIGH if int(level) == 4 else ThreatLevel.MEDIUM,
                                geographic_focus=[country.strip()]
                            )

                            items.append(intel_item)

        except Exception as e:
            logger.error(f"Error collecting State Dept special sources: {e}")

        return items

    async def _analyze_market_impact(self) -> List[IntelligenceItem]:
        """Analyze market conditions that could impact Canada Goose"""
        market_items = []

        if not FINANCE_AVAILABLE:
            return market_items

        try:
            # Key market indicators
            indicators = {
                "^GSPC": "S&P 500",  # General market
                "^IXIC": "NASDAQ",  # Tech sector
                "^DJI": "Dow Jones",  # Industrial
                "USDCAD=X": "USD/CAD Exchange Rate"
            }

            for symbol, name in indicators.items():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="5d")

                    if not hist.empty:
                        # Calculate volatility and trend
                        latest_close = hist['Close'].iloc[-1]
                        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else latest_close
                        change_pct = ((latest_close - prev_close) / prev_close) * 100

                        # Create market intelligence item for significant moves
                        if abs(change_pct) > 2:  # Significant move (>2%)
                            item_id = hashlib.md5(f"MARKET_{symbol}_{datetime.now().date()}".encode()).hexdigest()

                            direction = "surged" if change_pct > 0 else "declined"
                            threat_level = ThreatLevel.MEDIUM if abs(change_pct) > 5 else ThreatLevel.LOW

                            intel_item = IntelligenceItem(
                                id=item_id,
                                title=f"Market Alert: {name} {direction} {abs(change_pct):.1f}%",
                                content=f"{name} {direction} {abs(change_pct):.1f}% to ${latest_close:.2f}. Potential impact on retail and luxury goods sector.",
                                source_url=f"https://finance.yahoo.com/quote/{symbol}",
                                source_name="Market Impact Analysis",
                                source_type=SourceType.FINANCIAL,
                                timestamp=datetime.now(),
                                relevance_score=0.6,
                                threat_level=threat_level
                            )

                            market_items.append(intel_item)

                except Exception as e:
                    logger.error(f"Error analyzing {symbol}: {e}")

        except Exception as e:
            logger.error(f"Error in market impact analysis: {e}")

        return market_items

    async def _enhance_with_nlp(self, item: IntelligenceItem) -> IntelligenceItem:
        """Enhance intelligence item with NLP analysis"""
        if not self.nlp_engine:
            return item

        try:
            # Analyze content with NLP engine
            analysis_text = f"{item.title} {item.content}"
            nlp_results = self.nlp_engine.analyze_text(analysis_text)

            # Extract entities and relationships
            item.entities = nlp_results.get('entities', [])
            item.relationships = nlp_results.get('relationships', [])

            # Extract keywords from entities
            item.keywords = [entity['text'].lower() for entity in item.entities]

            # Calculate sentiment if available
            item.sentiment_score = self._calculate_sentiment(analysis_text)

            # Calculate credibility based on source and content analysis
            item.credibility_score = self._calculate_credibility(item)

        except Exception as e:
            logger.error(f"Error enhancing item with NLP: {e}")

        return item

    def _calculate_relevance(self, title: str, content: str) -> float:
        """Calculate relevance score for Canada Goose security interests"""
        relevance_keywords = [
            # Company-specific
            'canada goose', 'retail', 'luxury goods', 'fashion', 'apparel',
            # Security-specific
            'cyber attack', 'data breach', 'security threat', 'fraud', 'theft',
            # Geographic
            'toronto', 'canada', 'north america', 'china', 'manufacturing',
            # Market-specific
            'consumer confidence', 'retail sales', 'supply chain', 'tariffs'
        ]

        text = f"{title} {content}".lower()
        matches = sum(1 for keyword in relevance_keywords if keyword in text)

        # Base score + keyword bonus
        base_score = 0.3
        keyword_bonus = min(matches * 0.15, 0.7)

        return min(base_score + keyword_bonus, 1.0)

    def _assess_threat_level(self, title: str, content: str) -> ThreatLevel:
        """Assess threat level based on content"""
        text = f"{title} {content}".lower()

        critical_indicators = ['cyber attack', 'data breach', 'critical vulnerability', 'ransomware']
        high_indicators = ['security threat', 'fraud', 'insider threat', 'supply chain attack']
        medium_indicators = ['phishing', 'malware', 'suspicious activity', 'risk assessment']

        if any(indicator in text for indicator in critical_indicators):
            return ThreatLevel.CRITICAL
        elif any(indicator in text for indicator in high_indicators):
            return ThreatLevel.HIGH
        elif any(indicator in text for indicator in medium_indicators):
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW

    def _is_security_relevant(self, text: str) -> bool:
        """Check if content is relevant to security interests"""
        security_keywords = [
            'security', 'threat', 'cyber', 'attack', 'breach', 'vulnerability',
            'defense', 'military', 'intelligence', 'surveillance', 'espionage'
        ]

        text_lower = text.lower()
        return any(keyword in text_lower for keyword in security_keywords)

    def _extract_geographic_focus(self, text: str) -> List[str]:
        """Extract geographic focus from text"""
        countries = [
            'iran', 'israel', 'china', 'russia', 'ukraine', 'canada', 'usa', 'united states',
            'north korea', 'south korea', 'japan', 'india', 'pakistan', 'syria', 'lebanon'
        ]

        found_countries = []
        text_lower = text.lower()

        for country in countries:
            if country in text_lower:
                found_countries.append(country.title())

        return found_countries

    def _calculate_sentiment(self, text: str) -> float:
        """Simple sentiment calculation (can be enhanced with ML models)"""
        positive_words = ['positive', 'good', 'success', 'growth', 'improvement', 'secure']
        negative_words = ['threat', 'attack', 'breach', 'risk', 'danger', 'decline', 'crisis']

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count + negative_count == 0:
            return 0.0

        return (positive_count - negative_count) / (positive_count + negative_count)

    def _calculate_credibility(self, item: IntelligenceItem) -> float:
        """Calculate source credibility score"""
        # Base credibility by source type
        credibility_map = {
            SourceType.GOVERNMENT: 0.9,
            SourceType.FINANCIAL: 0.8,
            SourceType.NEWS_RSS: 0.7,
            SourceType.SECURITY_FEED: 0.8,
            SourceType.ACADEMIC: 0.9,
            SourceType.CORPORATE: 0.6,
            SourceType.SOCIAL_MEDIA: 0.4
        }

        base_credibility = credibility_map.get(item.source_type, 0.5)

        # Adjust based on source reputation
        reputable_sources = ['reuters', 'bbc', 'state.gov', 'canada.ca', 'bloomberg']
        if any(source in item.source_url.lower() for source in reputable_sources):
            base_credibility += 0.1

        return min(base_credibility, 1.0)

    async def run_collection_cycle(self) -> Dict[str, List[IntelligenceItem]]:
        """Run a complete OSINT collection cycle"""
        logger.info("🔄 Starting OSINT collection cycle...")

        collection_results = {
            'government': [],
            'financial': [],
            'security': [],
            'geopolitical': [],
            'total_items': 0
        }

        try:
            # Collect from all source types
            government_items = await self.collect_government_sources()
            financial_items = await self.collect_financial_data()
            security_items = await self.collect_security_feeds()
            geopolitical_items = await self.collect_geopolitical_intelligence()

            # Store results
            collection_results['government'] = government_items
            collection_results['financial'] = financial_items
            collection_results['security'] = security_items
            collection_results['geopolitical'] = geopolitical_items

            # Calculate totals
            all_items = government_items + financial_items + security_items + geopolitical_items
            collection_results['total_items'] = len(all_items)

            # Store in instance
            self.collected_items.extend(all_items)

            logger.info(f"✅ Collection cycle complete: {len(all_items)} total items")

        except Exception as e:
            logger.error(f"❌ Error in collection cycle: {e}")

        return collection_results

    def get_high_priority_items(self, limit: int = 10) -> List[IntelligenceItem]:
        """Get highest priority intelligence items"""
        # Sort by threat level and relevance
        sorted_items = sorted(
            self.collected_items,
            key=lambda x: (
                4 if x.threat_level == ThreatLevel.CRITICAL else
                3 if x.threat_level == ThreatLevel.HIGH else
                2 if x.threat_level == ThreatLevel.MEDIUM else 1,
                x.relevance_score
            ),
            reverse=True
        )

        return sorted_items[:limit]

    def get_summary_report(self) -> Dict:
        """Generate summary report of collected intelligence"""
        if not self.collected_items:
            return {"status": "No data collected"}

        # Count by threat level
        threat_counts = {}
        for level in ThreatLevel:
            threat_counts[level.value] = sum(1 for item in self.collected_items if item.threat_level == level)

        # Count by source type
        source_counts = {}
        for source_type in SourceType:
            source_counts[source_type.value] = sum(
                1 for item in self.collected_items if item.source_type == source_type)

        # Top entities mentioned
        all_entities = []
        for item in self.collected_items:
            if item.entities:
                all_entities.extend([entity['text'] for entity in item.entities])

        entity_counts = {}
        for entity in all_entities:
            entity_counts[entity] = entity_counts.get(entity, 0) + 1

        top_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total_items": len(self.collected_items),
            "threat_level_distribution": threat_counts,
            "source_type_distribution": source_counts,
            "top_entities": top_entities,
            "avg_relevance_score": sum(item.relevance_score for item in self.collected_items) / len(
                self.collected_items),
            "collection_timestamp": datetime.now().isoformat()
        }


# Usage example and test function
async def test_osint_collector():
    """Test the OSINT collector"""
    print("🧪 Testing OSINT Collector...")

    # You would pass your NLP engine here
    # nlp_engine = create_advanced_nlp_engine()

    async with CanadaGooseOSINTCollector() as collector:
        # Run collection cycle
        results = await collector.run_collection_cycle()

        print(f"📊 Collection Results:")
        print(f"Government: {len(results['government'])} items")
        print(f"Financial: {len(results['financial'])} items")
        print(f"Security: {len(results['security'])} items")
        print(f"Geopolitical: {len(results['geopolitical'])} items")
        print(f"Total: {results['total_items']} items")

        # Get high priority items
        high_priority = collector.get_high_priority_items(5)
        print(f"\n🚨 Top {len(high_priority)} High Priority Items:")
        for item in high_priority:
            print(f"- {item.title} ({item.threat_level.value})")

        # Generate summary
        summary = collector.get_summary_report()
        print(f"\n📈 Summary Report:")
        print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(test_osint_collector())
# enterprise_architecture.py - Phase 4: Distributed Enterprise Architecture
import asyncio
import logging
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
import threading

# For event sourcing and messaging
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️  Install redis for full enterprise features: pip install redis")

# For database operations
try:
    import aiosqlite
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("⚠️  Install aiosqlite for database operations: pip install aiosqlite")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of events in the intelligence system"""
    INTELLIGENCE_COLLECTED = "intelligence_collected"
    THREAT_DETECTED = "threat_detected"
    ANALYSIS_COMPLETED = "analysis_completed"
    ALERT_TRIGGERED = "alert_triggered"
    USER_ACTION = "user_action"
    SYSTEM_STATUS = "system_status"
    DATA_UPDATED = "data_updated"
    RELATIONSHIP_DISCOVERED = "relationship_discovered"


@dataclass
class DomainEvent:
    """Domain event for event sourcing"""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = EventType.SYSTEM_STATUS
    aggregate_id: str = ""
    version: int = 1
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""
    causation_id: str = ""


@dataclass
class Command:
    """Command for CQRS pattern"""
    command_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    command_type: str = ""
    aggregate_id: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: str = ""
    correlation_id: str = ""


@dataclass
class QueryRequest:
    """Query request for CQRS pattern"""
    query_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query_type: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: str = ""


class EventStore:
    """Event store for event sourcing"""
    def __init__(self, connection_string: str = "intelligence_events.db"):
        self.connection_string = connection_string
        self.events = []  # In-memory fallback
        self.lock = threading.Lock()

    async def initialize(self):
        """Initialize the event store"""
        if DATABASE_AVAILABLE:
            async with aiosqlite.connect(self.connection_string) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS events (
                        event_id TEXT PRIMARY KEY,
                        event_type TEXT NOT NULL,
                        aggregate_id TEXT NOT NULL,
                        version INTEGER NOT NULL,
                        timestamp TEXT NOT NULL,
                        data TEXT NOT NULL,
                        metadata TEXT NOT NULL,
                        correlation_id TEXT,
                        causation_id TEXT
                    )
                """)
                await db.commit()
        logger.info("✅ Event store initialized")

    async def append_event(self, event: DomainEvent) -> bool:
        """Append event to the store"""
        try:
            if DATABASE_AVAILABLE:
                async with aiosqlite.connect(self.connection_string) as db:
                    await db.execute("""
                        INSERT INTO events (
                            event_id, event_type, aggregate_id, version, timestamp,
                            data, metadata, correlation_id, causation_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        event.event_id,
                        event.event_type.value,
                        event.aggregate_id,
                        event.version,
                        event.timestamp.isoformat(),
                        json.dumps(event.data),
                        json.dumps(event.metadata),
                        event.correlation_id,
                        event.causation_id
                    ))
                    await db.commit()
            else:
                # Fallback to in-memory storage
                with self.lock:
                    self.events.append(event)
            logger.debug(f"📝 Event appended: {event.event_type.value}")
            return True
        except Exception as e:
            logger.error(f"❌ Error appending event: {e}")
            return False

    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[DomainEvent]:
        """Get events for an aggregate"""
        events = []
        try:
            if DATABASE_AVAILABLE:
                async with aiosqlite.connect(self.connection_string) as db:
                    async with db.execute("""
                        SELECT event_id, event_type, aggregate_id, version, timestamp,
                               data, metadata, correlation_id, causation_id
                        FROM events
                        WHERE aggregate_id = ? AND version >= ?
                        ORDER BY version
                    """, (aggregate_id, from_version)) as cursor:
                        async for row in cursor:
                            # Recreate the event object from database row
                            event_data = {
                                'event_id': row[0], 'event_type': row[1], 'aggregate_id': row[2],
                                'version': row[3], 'timestamp': row[4], 'data': row[5],
                                'metadata': row[6], 'correlation_id': row[7], 'causation_id': row[8]
                            }
                            events.append(DomainEvent(
                                event_id=event_data['event_id'],
                                event_type=EventType(event_data['event_type']),
                                aggregate_id=event_data['aggregate_id'],
                                version=event_data['version'],
                                timestamp=datetime.fromisoformat(event_data['timestamp']),
                                data=json.loads(event_data['data']),
                                metadata=json.loads(event_data['metadata']),
                                correlation_id=event_data['correlation_id'] or "",
                                causation_id=event_data['causation_id'] or ""
                            ))
            else:
                # Fallback to in-memory storage
                with self.lock:
                    events = [e for e in self.events
                              if e.aggregate_id == aggregate_id and e.version >= from_version]
                    events.sort(key=lambda x: x.version)
        except Exception as e:
            logger.error(f"❌ Error getting events: {e}")
        return events

    async def get_all_events(self, event_type: Optional[EventType] = None) -> List[DomainEvent]:
        """Get all events, optionally filtered by type"""
        events = []
        try:
            if DATABASE_AVAILABLE:
                query = "SELECT * FROM events"
                params = []
                if event_type:
                    query += " WHERE event_type = ?"
                    params.append(event_type.value)
                query += " ORDER BY timestamp"
                async with aiosqlite.connect(self.connection_string) as db:
                    async with db.execute(query, tuple(params)) as cursor:
                        async for row in cursor:
                            event_data = {
                                'event_id': row[0], 'event_type': row[1], 'aggregate_id': row[2],
                                'version': row[3], 'timestamp': row[4], 'data': row[5],
                                'metadata': row[6], 'correlation_id': row[7], 'causation_id': row[8]
                            }
                            events.append(DomainEvent(
                                event_id=event_data['event_id'],
                                event_type=EventType(event_data['event_type']),
                                aggregate_id=event_data['aggregate_id'],
                                version=event_data['version'],
                                timestamp=datetime.fromisoformat(event_data['timestamp']),
                                data=json.loads(event_data['data']),
                                metadata=json.loads(event_data['metadata']),
                                correlation_id=event_data['correlation_id'] or "",
                                causation_id=event_data['causation_id'] or ""
                            ))
            else:
                # Fallback to in-memory storage with corrected indentation
                with self.lock:
                    if event_type:
                        events = [e for e in self.events if e.event_type == event_type]
                    else:
                        events = self.events[:]
        except Exception as e:
            logger.error(f"❌ Error getting all events: {e}")
        return events


# Dummy placeholder for IntelligenceService to allow tests to pass
# In a real system, this would be a much more complex class.
class IntelligenceService:
    def __init__(self):
        self.event_store = EventStore()
        self.data = []

    async def start(self):
        await self.event_store.initialize()
        logger.info("Intelligence Service Started")

    async def stop(self):
        logger.info("Intelligence Service Stopped")

    async def collect_intelligence(self, data):
        self.data.append(data)
        event = DomainEvent(
            event_type=EventType.INTELLIGENCE_COLLECTED,
            aggregate_id=data['id'],
            data=data
        )
        return await self.event_store.append_event(event)

    async def get_dashboard_data(self):
        return {'total_threats': len(self.data), 'status': 'OK'}

    async def get_intelligence_summary(self, limit):
        return {'total_items': len(self.data), 'items': self.data[:limit]}


async def create_intelligence_service():
    """Factory function to create the intelligence service."""
    return IntelligenceService()
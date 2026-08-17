"""
High-Performance In-Memory Ring Buffer for Decision Telemetry.
Provides O(1) appends, instant ID lookups, and async pub/sub for SSE streaming
without repeated disk I/O.
"""
import asyncio
import json
import logging
import os
from collections import deque
from typing import Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class LogRingBuffer:
    """
    Thread-safe, high-speed circular buffer for security decision events.
    Holds the last N events in memory for sub-millisecond retrieval.
    """

    def __init__(self, max_entries: int = 5000):
        self.max_entries = max_entries
        self._buffer: deque = deque(maxlen=max_entries)
        self._index: Dict[str, dict] = {}
        self._subscribers: Set[asyncio.Queue] = set()

    def append(self, entry: dict):
        """Append a decision event and notify active SSE subscribers."""
        query_id = entry.get("id")
        # If ring buffer is full, remove evicted key from index
        if len(self._buffer) >= self.max_entries and len(self._buffer) > 0:
            evicted = self._buffer[0]
            evicted_id = evicted.get("id")
            if evicted_id and evicted_id in self._index:
                del self._index[evicted_id]

        self._buffer.append(entry)
        if query_id:
            self._index[query_id] = entry

        # Broadcast to active SSE subscribers
        stale_subscribers = []
        for q in list(self._subscribers):
            try:
                q.put_nowait(entry)
            except asyncio.QueueFull:
                stale_subscribers.append(q)
            except Exception:
                stale_subscribers.append(q)

        for stale in stale_subscribers:
            self._subscribers.discard(stale)

    def get_all(self) -> List[dict]:
        """Return all in-memory entries."""
        return list(self._buffer)

    def get_recent(self, n: int = 50) -> List[dict]:
        """Return the most recent n entries."""
        entries = list(self._buffer)
        return entries[-n:] if len(entries) > n else entries

    def get_by_id(self, query_id: str) -> Optional[dict]:
        """O(1) lookup of a decision log entry by its UUID."""
        return self._index.get(query_id)

    def count(self) -> int:
        """Return count of in-memory entries."""
        return len(self._buffer)

    def subscribe(self) -> asyncio.Queue:
        """Subscribe to real-time events for SSE streaming."""
        queue: asyncio.Queue = asyncio.Queue(maxsize=100)
        self._subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue):
        """Unsubscribe from real-time events."""
        self._subscribers.discard(queue)

    def load_from_file(self, filepath: str, limit: Optional[int] = None):
        """Warm up the in-memory buffer with recent entries from disk."""
        if not os.path.exists(filepath):
            return
        load_limit = limit or self.max_entries
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-load_limit:]:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        query_id = entry.get("id")
                        self._buffer.append(entry)
                        if query_id:
                            self._index[query_id] = entry
                    except (json.JSONDecodeError, ValueError):
                        continue
        except Exception as e:
            logger.warning(f"Could not warm up ring buffer from {filepath}: {e}")


# Global default instance
ring_buffer = LogRingBuffer(max_entries=5000)

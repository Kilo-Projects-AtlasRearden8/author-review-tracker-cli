from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return uuid.uuid4().hex


@dataclass
class Reader:
    id: str
    name: str
    email: str = ""
    genre: str = ""
    added_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Reader":
        return cls(**{k: data.get(k) for k in ("id", "name", "email", "genre", "added_at")})


@dataclass
class ReviewRequest:
    id: str
    reader_id: str
    book_title: str
    status: str = "pending"  # pending, mailed, received, declined
    format: str = "ebook"
    requested_at: str = field(default_factory=_now_iso)
    sent_at: Optional[str] = None
    received_at: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewRequest":
        return cls(**{k: data.get(k) for k in (
            "id", "reader_id", "book_title", "status", "format",
            "requested_at", "sent_at", "received_at",
        )})


@dataclass
class FollowUp:
    id: str
    request_id: str
    date: str
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "FollowUp":
        return cls(**{k: data.get(k) for k in ("id", "request_id", "date", "note")})

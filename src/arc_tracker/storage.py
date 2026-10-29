from __future__ import annotations

import json
import os
from typing import List, Optional

from .models import Reader, ReviewRequest, FollowUp, new_id


class Store:
    """Local JSON storage for readers, review requests, and follow-ups."""

    def __init__(self, path: str):
        self.path = path
        self.data: dict = {"readers": [], "requests": [], "followups": []}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                loaded = json.load(fh)
        except (json.JSONDecodeError, OSError):
            return
        if not isinstance(loaded, dict):
            return
        self.data = loaded
        for key in ("readers", "requests", "followups"):
            if not isinstance(self.data.get(key), list):
                self.data[key] = []

    def save(self) -> None:
        directory = os.path.dirname(os.path.abspath(self.path))
        os.makedirs(directory, exist_ok=True)
        tmp_path = self.path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as fh:
            json.dump(self.data, fh, indent=2)
        os.replace(tmp_path, self.path)

    # --- readers ---

    def add_reader(self, name: str, email: str = "", genre: str = "") -> Reader:
        reader = Reader(id=new_id(), name=name, email=email, genre=genre)
        self.data["readers"].append(reader.to_dict())
        self.save()
        return reader

    def list_readers(self) -> List[Reader]:
        return [Reader.from_dict(d) for d in self.data["readers"]]

    def get_reader(self, reader_id: str) -> Optional[Reader]:
        for d in self.data["readers"]:
            if d.get("id") == reader_id:
                return Reader.from_dict(d)
        return None

    # --- review requests ---

    def add_request(self, reader_id: str, book_title: str, fmt: str = "ebook") -> ReviewRequest:
        request = ReviewRequest(id=new_id(), reader_id=reader_id,
                                book_title=book_title, format=fmt)
        self.data["requests"].append(request.to_dict())
        self.save()
        return request

    def list_requests(self) -> List[ReviewRequest]:
        return [ReviewRequest.from_dict(d) for d in self.data["requests"]]

    def get_request(self, request_id: str) -> Optional[ReviewRequest]:
        for d in self.data["requests"]:
            if d.get("id") == request_id:
                return ReviewRequest.from_dict(d)
        return None

    def update_request(self, request: ReviewRequest) -> None:
        for i, d in enumerate(self.data["requests"]):
            if d.get("id") == request.id:
                self.data["requests"][i] = request.to_dict()
                self.save()
                return

    # --- follow-ups ---

    def add_followup(self, request_id: str, date: str, note: str = "") -> FollowUp:
        followup = FollowUp(id=new_id(), request_id=request_id, date=date, note=note)
        self.data["followups"].append(followup.to_dict())
        self.save()
        return followup

    def list_followups(self) -> List[FollowUp]:
        return [FollowUp.from_dict(d) for d in self.data["followups"]]

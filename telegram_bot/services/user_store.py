"""Foydalanuvchi ma'lumotlari xotirada saqlanadi (session store)."""

from typing import Dict, Optional

# { user_id: { "lang": "uz", "pending_photo": bytes | None } }
_store: Dict[int, dict] = {}

DEFAULT_LANG = "uz"


def get_lang(user_id: int) -> str:
    return _store.get(user_id, {}).get("lang", DEFAULT_LANG)


def set_lang(user_id: int, lang: str) -> None:
    if user_id not in _store:
        _store[user_id] = {}
    _store[user_id]["lang"] = lang


def set_pending_photo(user_id: int, photo_bytes: bytes) -> None:
    if user_id not in _store:
        _store[user_id] = {}
    _store[user_id]["pending_photo"] = photo_bytes


def get_pending_photo(user_id: int) -> Optional[bytes]:
    return _store.get(user_id, {}).get("pending_photo")


def clear_pending_photo(user_id: int) -> None:
    if user_id in _store:
        _store[user_id].pop("pending_photo", None)

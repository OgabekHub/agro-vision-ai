"""Natijani Telegram xabari formatida chiqarish."""

from i18n.messages import get_msg


def format_plant_result(data: dict, lang: str) -> str:
    """O'simlik natijasini formatlangan Markdown xabar sifatida qaytaradi."""
    regions = ", ".join(data.get("suitable_regions", []))
    confidence = round(data.get("confidence", 0) * 100, 1)

    return get_msg(
        lang, "plant_result",
        plant_name=data.get("plant_name", "—"),
        scientific_name=data.get("scientific_name", "—"),
        family=data.get("family", "—"),
        confidence=confidence,
        description=data.get("description", "—"),
        growing_season=data.get("growing_season", "—"),
        water_needs=data.get("water_needs", "—"),
        regions=f"📍 {regions}" if regions else "—",
    )


def format_disease_result(data: dict, lang: str) -> str:
    """Kasallik natijasini formatlangan Markdown xabar sifatida qaytaradi."""
    severity_raw = data.get("severity", "low")
    severity_labels = get_msg(lang, "severity")
    severity = severity_labels.get(severity_raw, severity_raw) if isinstance(severity_labels, dict) else severity_raw

    confidence = round(data.get("confidence", 0) * 100, 1)

    causes = _format_list(data.get("causes", []))
    treatments = _format_list(data.get("treatments", []))
    prevention = _format_list(data.get("prevention_tips", []))

    return get_msg(
        lang, "disease_result",
        disease_name=data.get("disease_name", "—"),
        plant_affected=data.get("plant_affected", "—"),
        severity=severity,
        confidence=confidence,
        description=data.get("description", "—"),
        causes=causes,
        treatments=treatments,
        prevention=prevention,
    )


def _format_list(items: list, bullet: str = "•") -> str:
    """Ro'yxatni Telegram formatida chiqaradi."""
    if not items:
        return "—"
    return "\n".join(f"{bullet} {item}" for item in items)

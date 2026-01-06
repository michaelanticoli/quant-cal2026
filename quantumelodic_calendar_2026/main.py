#!/usr/bin/env python3
"""Quantumelodic Calendar 2026 generator."""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Sequence

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
# Update these filenames if your CSV exports use different names.
EVENTS_CSV = DATA_DIR / "astrological_events_2026.csv"
VOIDS_CSV = DATA_DIR / "moon_voids_2026.csv"
ICS_PATH = OUTPUT_DIR / "Quantumelodic_2026_Calendar.ics"
SUMMARY_PATH = OUTPUT_DIR / "Calendar_Summary.txt"

DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%b %d, %Y",
    "%B %d, %Y",
)

TIME_FORMATS = (
    "%H:%M",
    "%I:%M %p",
    "%H%M",
    "%I %p",
)

DEFAULT_EVENT_DURATION = timedelta(hours=1)
DEFAULT_VOID_DURATION = timedelta(hours=2)
RNG = random.Random(2026)

EMOJI_PALETTE = ["✨", "🎵", "🌙", "💫", "🔭", "🪐", "🌌", "🎻"]
TONALITIES = [
    "in a lydian shimmer",
    "through a dorian bloom",
    "with velvet polyrhythms",
    "against a glass-harp drone",
    "inside a pulse of auroral bass",
]
IMAGERY = [
    "stardust lattices",
    "moonlit observatories",
    "choirs of nebulae",
    "tidal resonators",
    "quantum gardens",
]
REFLECTIONS = [
    "What melody is waiting beneath today's decision?",
    "Where can you leave more room for wonder?",
    "Which harmony needs your patience right now?",
    "How can you soften the dissonance you feel?",
    "What would it take to trust this tempo?",
]
MOVEMENTS = [
    "Bloom slowly, note by note.",
    "Let intuition improvise the bridge.",
    "Lean into the fermata and listen.",
    "Sync your breath with lunar swing.",
    "Hold the chord until gratitude appears.",
]


@dataclass
class CalendarMoment:
    """Single calendar block ready for export."""

    title: str
    start: datetime
    end: datetime
    description: str
    category: str
    position: str = ""


def main() -> None:
    """Entry point for the generator."""

    OUTPUT_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

    if not EVENTS_CSV.exists():
        raise FileNotFoundError(
            "Events CSV missing. Add data/astrological_events_2026.csv before running."
        )

    moments = build_schedule()
    if not moments:
        raise RuntimeError("No events were generated. Please confirm your CSV contents.")

    write_ics(moments)
    write_summary(moments)

    print("🎉 Quantumelodic Calendar 2026 generated!")
    print(f"   • ICS file: {ICS_PATH}")
    print(f"   • Summary: {SUMMARY_PATH}")


def build_schedule() -> List[CalendarMoment]:
    """Collect celestial events and moon voids into a single sorted list."""

    events = [
        row_to_moment(row, category="Celestial Event", duration=DEFAULT_EVENT_DURATION)
        for row in read_csv(EVENTS_CSV)
    ]

    voids: List[CalendarMoment] = []
    if VOIDS_CSV.exists():
        voids = [
            row_to_moment(
                row,
                category="Moon Void",
                duration=DEFAULT_VOID_DURATION,
                title_field="Event Description",
            )
            for row in read_csv(VOIDS_CSV)
        ]

    combined = [m for m in events + voids if m]
    combined.sort(key=lambda moment: moment.start)
    return combined


def read_csv(path: Path) -> List[dict]:
    """Load a CSV file into dictionaries, skipping blank lines."""

    rows: List[dict] = []
    if not path.exists():
        return rows

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if not row:
                continue
            if all(not (value or "").strip() for value in row.values()):
                continue
            rows.append({key.strip(): (value or "").strip() for key, value in row.items()})
    return rows


def row_to_moment(
    row: dict,
    *,
    category: str,
    duration: timedelta,
    title_field: str = "Event",
) -> CalendarMoment:
    """Convert a CSV row into a CalendarMoment."""

    position = row.get("Position", "").strip()
    title_stub = row.get(title_field, "").strip()
    timestamp = parse_timestamp(row.get("Date", ""), row.get("Time", ""))

    title = format_title(title_stub, position, category)
    description = build_description(title_stub or title, category)

    return CalendarMoment(
        title=title,
        start=timestamp,
        end=timestamp + duration,
        description=description,
        category=category,
        position=position,
    )


def parse_timestamp(date_value: str, time_value: str) -> datetime:
    """Parse flexible date/time strings."""

    date_clean = (date_value or "").strip()
    if not date_clean:
        raise ValueError("Each row must include a Date value.")

    for fmt in DATE_FORMATS:
        try:
            date_part = datetime.strptime(date_clean, fmt).date()
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Unsupported date format: {date_value!r}")

    time_clean = (time_value or "").strip()
    if not time_clean:
        time_clean = "00:00"

    for fmt in TIME_FORMATS:
        try:
            time_part = datetime.strptime(time_clean, fmt).time()
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Unsupported time format: {time_value!r}")

    return datetime.combine(date_part, time_part)


def format_title(title_stub: str, position: str, category: str) -> str:
    """Compose a display title that balances poetry and clarity."""

    emoji = RNG.choice(EMOJI_PALETTE)
    if title_stub and position:
        return f"{emoji} {position}: {title_stub}"
    if title_stub:
        return f"{emoji} {title_stub}"
    if position:
        return f"{emoji} {category} — {position}"
    return f"{emoji} {category}"


def build_description(title_stub: str, category: str) -> str:
    """Generate a lyrical narrative and reflection prompt."""

    text_title = title_stub or category
    tonal = RNG.choice(TONALITIES)
    vista = RNG.choice(IMAGERY)
    reflection = RNG.choice(REFLECTIONS)
    movement = RNG.choice(MOVEMENTS)
    emoji = RNG.choice(EMOJI_PALETTE)

    narrative = (
        f"{text_title} {tonal}, surrounded by {vista}. "
        f"{movement}"
    )
    prompt = f"Reflection: {reflection}"
    return f"{emoji} {narrative}\n{prompt}"


def write_ics(moments: Sequence[CalendarMoment]) -> None:
    """Emit an ICS file that calendar apps can import."""

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Quantumelodic//Calendar 2026//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Quantumelodic Calendar 2026",
        "X-WR-TIMEZONE:UTC",
    ]

    for index, moment in enumerate(moments, start=1):
        lines.extend(serialize_event(moment, index))

    lines.append("END:VCALENDAR")
    ICS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def serialize_event(moment: CalendarMoment, index: int) -> List[str]:
    """Convert a CalendarMoment into ICS VEVENT lines."""

    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    start = moment.start.strftime("%Y%m%dT%H%M%SZ")
    end = moment.end.strftime("%Y%m%dT%H%M%SZ")
    uid = f"{moment.start:%Y%m%dT%H%M%S}-{index}@quantumelodic"

    description = sanitize_text(moment.description)
    summary = sanitize_text(moment.title)
    category = sanitize_text(moment.category)

    return [
        "BEGIN:VEVENT",
        f"DTSTAMP:{stamp}",
        f"UID:{uid}",
        f"SUMMARY:{summary}",
        f"DTSTART:{start}",
        f"DTEND:{end}",
        f"CATEGORIES:{category}",
        f"DESCRIPTION:{description}",
        "END:VEVENT",
    ]


def sanitize_text(value: str) -> str:
    """Escape characters that could break ICS parsing."""

    escaped = value.replace("\\", "\\\\").replace("\n", "\\n")
    escaped = escaped.replace(",", r"\,").replace(";", r"\;")
    return escaped


def write_summary(moments: Sequence[CalendarMoment]) -> None:
    """Create a plain-text report describing the calendar."""

    total_events = sum(1 for moment in moments if moment.category == "Celestial Event")
    total_voids = sum(1 for moment in moments if moment.category == "Moon Void")
    first = moments[0]
    last = moments[-1]

    lines = [
        "QUANTUMELODIC CALENDAR 2026",
        "=" * 33,
        f"Events: {total_events}",
        f"Moon Voids: {total_voids}",
        "",
        f"First Entry:  {first.title} on {first.start:%B %d, %Y %H:%M}",
        f"Last Entry:   {last.title} on {last.start:%B %d, %Y %H:%M}",
        "",
        "Tempo Markers:",
    ]

    sample = list(moments[:5])
    for moment in sample:
        lines.append(f" - {moment.title} | {moment.start:%b %d %H:%M}")

    lines.append("")
    lines.append("Reflection Prompts:")
    for prompt in random.sample(REFLECTIONS, k=min(3, len(REFLECTIONS))):
        lines.append(f" - {prompt}")

    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

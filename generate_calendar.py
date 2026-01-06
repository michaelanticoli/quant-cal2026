#!/usr/bin/env python3
"""
Astroquantum Calendar 2026 Generator

A lightweight generator that transforms astrological event and Moon void CSV data
into a polished, import-ready 2026 calendar. It enriches each entry with poetic,
music-infused narratives and cosmic imagery, then exports a professional ICS file
compatible with all major calendar apps.
"""

import csv
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from pathlib import Path
import sys


# Poetic narratives for each event type
NARRATIVES = {
    'new_year': '🌟 As the cosmic wheel turns, we enter a year of quantum possibilities. The universe whispers: "Begin anew, dream boldly, become infinite."',
    'new_moon': '🌑 In darkness, seeds are planted. The New Moon invites you to set intentions, whisper wishes to the void, and trust in invisible growth. Like a silent symphony waiting for its first note.',
    'full_moon': '🌕 The Moon reaches her crescendo, illuminating hidden truths and awakening dormant dreams. A luminous beacon in the night, she sings: "Release, reflect, and radiate your light."',
    'spring_equinox': '🌸 Balance arrives as day equals night. Nature awakens from winter\'s slumber with a symphony of rebirth. The cosmic pendulum finds equilibrium.',
    'summer_solstice': '☀️ The Sun reaches its zenith, flooding the world with maximum light. Celebrate vitality, joy, and the golden symphony of endless daylight.',
    'autumn_equinox': '🍂 Once more, balance is achieved. As darkness grows, we harvest wisdom from the year\'s journey. The cosmic scales tip toward introspection.',
    'winter_solstice': '❄️ In the longest night, hope is reborn. The Sun returns, promising light after darkness. Ancient stones mark this eternal dance of celestial resurrection.',
    'moon_void': '🌫️ The Moon drifts between signs, creating a liminal space. A cosmic pause for reflection, not action. Let your soul float in this ethereal intermission.',
}

# Sign-specific cosmic imagery and music metaphors
SIGN_IMAGERY = {
    'aries': '♈ The Ram charges forward with fierce confidence, igniting the cosmos with pioneering fire. A brass fanfare announces new beginnings.',
    'taurus': '♉ The Bull grounds us in earthly pleasures, sensual beauty, and unwavering stability. A cello\'s deep resonance echoes through verdant fields.',
    'gemini': '♊ The Twins dance in duality, weaving stories with quicksilver words and curious minds. Flutes twitter in playful conversation.',
    'cancer': '♋ The Crab carries home in its shell, nurturing emotions like tides responding to lunar pull. A gentle harp strums with maternal tenderness.',
    'leo': '♌ The Lion roars with creative majesty, radiating warmth and theatrical brilliance. Orchestral strings swell with regal drama.',
    'virgo': '♍ The Maiden tends the harvest with precise devotion, finding sacred patterns in earthly details. A harpsichord articulates crystalline perfection.',
    'libra': '♎ The Scales seek harmony through beauty, justice, and elegant partnership. A string quartet balances in refined equilibrium.',
    'scorpio': '♏ The Scorpion plunges into transformative depths, embracing shadows to find hidden power. A haunting oboe calls from mysterious waters.',
    'sagittarius': '♐ The Archer aims arrows toward distant horizons, seeking truth through adventurous philosophy. Trumpets herald expansive journeys.',
    'capricorn': '♑ The Goat climbs mountainous ambitions with patient mastery and timeless wisdom. Timpani mark steady, purposeful ascent.',
    'aquarius': '♒ The Water Bearer pours innovative visions into collective consciousness, revolutionizing the future. Synthesizers hum with electric possibility.',
    'pisces': '♓ The Fishes swim in oceanic oneness, dissolving boundaries through compassion and mystical dreams. A wordless choir echoes cosmic unity.',
}

# Moon names and their poetic descriptions
MOON_NAMES = {
    'Wolf Moon': '🐺 January\'s Wolf Moon howls with primal wisdom, breaking winter\'s silence.',
    'Snow Moon': '❄️ February\'s Snow Moon blankets the world in crystalline contemplation.',
    'Worm Moon': '🌱 March\'s Worm Moon signals spring\'s return as earth awakens.',
    'Pink Moon': '🌸 April\'s Pink Moon blooms with wild phlox and renewed vitality.',
    'Flower Moon': '🌺 May\'s Flower Moon bursts forth in botanical abundance.',
    'Strawberry Moon': '🍓 June\'s Strawberry Moon sweetens the longest days.',
    'Buck Moon': '🦌 July\'s Buck Moon grows new antlers under summer\'s peak.',
    'Sturgeon Moon': '🐟 August\'s Sturgeon Moon swims deep with ancestral plenty.',
    'Corn Moon': '🌽 September\'s Corn Moon harvests golden abundance.',
    'Hunter\'s Moon': '🏹 October\'s Hunter\'s Moon tracks preparations for winter.',
    'Beaver Moon': '🦫 November\'s Beaver Moon builds shelter before the freeze.',
    'Cold Moon': '🌨️ December\'s Cold Moon illuminates the longest nights.',
}


def parse_date_time(date_str, time_str):
    """Parse date and time strings into a datetime object."""
    dt_str = f"{date_str} {time_str}"
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")


def get_moon_description(description):
    """Extract and enhance moon descriptions with poetic names."""
    for moon_name, moon_desc in MOON_NAMES.items():
        if moon_name in description:
            return f"{moon_desc}\n{description}"
    return description


def create_event_description(event_type, sign, base_description):
    """Create enriched description with narratives and cosmic imagery."""
    parts = []
    
    # Add base description
    parts.append(base_description)
    parts.append("")
    
    # Add narrative
    if event_type in NARRATIVES:
        parts.append(NARRATIVES[event_type])
        parts.append("")
    
    # Add sign imagery
    if sign and sign.lower() in SIGN_IMAGERY:
        parts.append(SIGN_IMAGERY[sign.lower()])
        parts.append("")
    
    # Add cosmic signature
    parts.append("✨ Part of your Astroquantum Calendar 2026 - where cosmos meets consciousness.")
    
    return "\n".join(parts)


def create_void_moon_description(sign, void_start, void_end):
    """Create description for Moon void periods."""
    duration = void_end - void_start
    hours = duration.total_seconds() / 3600
    
    parts = []
    parts.append(f"Moon void of course in {sign.title()}")
    parts.append("")
    parts.append(f"Duration: {hours:.1f} hours")
    parts.append("")
    parts.append(NARRATIVES['moon_void'])
    parts.append("")
    
    if sign.lower() in SIGN_IMAGERY:
        parts.append(f"Transitioning from: {SIGN_IMAGERY[sign.lower()]}")
        parts.append("")
    
    parts.append("⏸️ A cosmic intermission - pause, reflect, but avoid major decisions or new beginnings during this liminal space.")
    parts.append("")
    parts.append("✨ Part of your Astroquantum Calendar 2026 - where cosmos meets consciousness.")
    
    return "\n".join(parts)


def load_astrological_events(csv_file):
    """Load astrological events from CSV file."""
    events = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            events.append({
                'datetime': parse_date_time(row['date'], row['time']),
                'event_type': row['event_type'],
                'sign': row['sign'],
                'description': row['description']
            })
    return events


def load_moon_void_events(csv_file):
    """Load Moon void of course periods from CSV file."""
    events = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            void_start = parse_date_time(row['date'], row['void_start'])
            void_end = parse_date_time(row['date'], row['void_end'])
            events.append({
                'void_start': void_start,
                'void_end': void_end,
                'sign': row['moon_sign']
            })
    return events


def create_calendar():
    """Create the main calendar object."""
    cal = Calendar()
    cal.add('prodid', '-//Astroquantum Calendar 2026//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'Astroquantum 2026')
    cal.add('x-wr-caldesc', 'A cosmic journey through 2026 with astrological events, moon phases, and celestial wisdom')
    cal.add('x-wr-timezone', 'UTC')
    
    return cal


def add_event_to_calendar(cal, event_data, is_void_moon=False):
    """Add an event to the calendar."""
    event = Event()
    
    if is_void_moon:
        # Moon void event
        event.add('summary', f'🌫️ Moon Void in {event_data["sign"].title()}')
        event.add('dtstart', event_data['void_start'])
        event.add('dtend', event_data['void_end'])
        event.add('description', create_void_moon_description(
            event_data['sign'],
            event_data['void_start'],
            event_data['void_end']
        ))
        event.add('categories', ['Astrology', 'Moon Void', 'Liminal Space'])
    else:
        # Regular astrological event
        summary = event_data['description']
        
        # Add emoji based on event type
        if 'moon' in event_data['event_type']:
            if 'new' in event_data['event_type']:
                summary = f"🌑 {summary}"
            elif 'full' in event_data['event_type']:
                summary = f"🌕 {summary}"
        elif 'equinox' in event_data['event_type']:
            if 'spring' in event_data['event_type']:
                summary = f"🌸 {summary}"
            else:
                summary = f"🍂 {summary}"
        elif 'solstice' in event_data['event_type']:
            if 'summer' in event_data['event_type']:
                summary = f"☀️ {summary}"
            else:
                summary = f"❄️ {summary}"
        elif event_data['event_type'] == 'new_year':
            summary = f"🌟 {summary}"
        
        event.add('summary', summary)
        event.add('dtstart', event_data['datetime'])
        event.add('dtend', event_data['datetime'] + timedelta(hours=1))
        
        # Get enhanced description
        enhanced_desc = get_moon_description(event_data['description'])
        event.add('description', create_event_description(
            event_data['event_type'],
            event_data['sign'],
            enhanced_desc
        ))
        
        # Add categories
        categories = ['Astrology', event_data['event_type'].replace('_', ' ').title()]
        if event_data['sign']:
            categories.append(event_data['sign'].title())
        event.add('categories', categories)
    
    # Add common properties
    event.add('dtstamp', datetime.now())
    event.add('uid', f"{event_data.get('datetime', event_data.get('void_start'))}-astroquantum@calendar.com")
    event.add('status', 'CONFIRMED')
    event.add('transp', 'TRANSPARENT')
    
    cal.add_component(event)


def generate_calendar(astro_csv='astrological_events.csv', void_csv='moon_void.csv', output_file='astroquantum_2026.ics'):
    """Generate the complete ICS calendar file."""
    print("🌟 Astroquantum Calendar 2026 Generator")
    print("=" * 50)
    
    # Create calendar
    cal = create_calendar()
    
    # Load and add astrological events
    print(f"\n📚 Loading astrological events from {astro_csv}...")
    astro_events = load_astrological_events(astro_csv)
    print(f"   Found {len(astro_events)} astrological events")
    
    for event_data in astro_events:
        add_event_to_calendar(cal, event_data)
    
    # Load and add moon void events
    print(f"\n🌙 Loading Moon void periods from {void_csv}...")
    void_events = load_moon_void_events(void_csv)
    print(f"   Found {len(void_events)} Moon void periods")
    
    for void_data in void_events:
        add_event_to_calendar(cal, void_data, is_void_moon=True)
    
    # Write to file
    print(f"\n💫 Generating ICS file: {output_file}...")
    with open(output_file, 'wb') as f:
        f.write(cal.to_ical())
    
    print(f"\n✨ Success! Your cosmic calendar is ready!")
    print(f"   Total events: {len(astro_events) + len(void_events)}")
    print(f"   Output file: {output_file}")
    print(f"\n📱 Import this file into:")
    print(f"   • Apple Calendar (macOS/iOS)")
    print(f"   • Google Calendar")
    print(f"   • Microsoft Outlook")
    print(f"   • Any calendar app supporting ICS format")
    print(f"\n🌌 May your year be filled with cosmic wisdom and celestial wonder!")


if __name__ == "__main__":
    # Use command-line arguments if provided
    astro_csv = sys.argv[1] if len(sys.argv) > 1 else 'astrological_events.csv'
    void_csv = sys.argv[2] if len(sys.argv) > 2 else 'moon_void.csv'
    output_file = sys.argv[3] if len(sys.argv) > 3 else 'astroquantum_2026.ics'
    
    try:
        generate_calendar(astro_csv, void_csv, output_file)
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find input file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating calendar: {e}")
        sys.exit(1)

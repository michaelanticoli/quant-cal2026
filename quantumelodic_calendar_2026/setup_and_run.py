#!/usr/bin/env python3
"""Setup and run the Quantumelodic Calendar Generator"""

import os
import sys
from pathlib import Path

def setup_project():
    """Create necessary directories and check files"""
    
    # Create directories
    Path("data").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    
    print("🎵 QUANTUMELODIC CALENDAR 2026 SETUP")
    print("=" * 40)
    
    # Check for data files
    events_file = Path("data/astrological_events_2026.csv")
    voids_file = Path("data/moon_voids_2026.csv")
    
    if not events_file.exists():
        print("⚠️  Please add your events CSV to:")
        print(f"   {events_file}")
        print("\nYour file should have columns:")
        print("   Position, Date, Time, Event")
        return False
        
    print("✅ Found events file")
    
    if not voids_file.exists():
        print("📝 Moon voids file is optional")
    else:
        print("✅ Found moon voids file")
        
    return True

if __name__ == "__main__":
    if setup_project():
        print("\n🎼 Running calendar generator...")
        print("-" * 40)
        
        # Import and run main
        import main
        main.main()

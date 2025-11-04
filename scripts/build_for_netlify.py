"""
Build script for Netlify deployment
Generates the dashboard and prepares it for publishing

Author: Deepa Rao
"""

import os
import sys
import shutil
from pathlib import Path

# Add parent directory to path
script_dir = Path(__file__).parent.parent
sys.path.insert(0, str(script_dir))

def main():
    print("=" * 80)
    print("Building Sustainability Dashboard for Netlify")
    print("Author: Deepa Rao")
    print("=" * 80)
    print("")
    
    # Set environment
    os.environ['DATA_DIR'] = str(script_dir)
    
    # Ensure public directory exists
    public_dir = script_dir / 'public'
    public_dir.mkdir(exist_ok=True)
    print(f"✓ Created public directory: {public_dir}")
    
    # Run the enhanced agent to update database
    print("\n1. Running sustainability agent to fetch latest regulations...")
    try:
        import sustainability_agent_enhanced
        db_file = script_dir / "sustainability_updates_enhanced.db"
        dashboard_file = script_dir / "sustainability_dashboard_temp.html"
        sustainability_agent_enhanced.run_daily_task(str(db_file), str(dashboard_file))
        print("✓ Database updated")
    except Exception as e:
        print(f"⚠ Warning: Could not update database: {e}")
        print("  Continuing with existing data...")
    
    # Generate interactive dashboard
    print("\n2. Generating interactive dashboard...")
    try:
        import generate_interactive_dashboard
        db_path = script_dir / "sustainability_updates_enhanced.db"
        dashboard_path = script_dir / "public" / "index.html"
        generate_interactive_dashboard.generate_interactive_dashboard(
            str(db_path),
            str(dashboard_path)
        )
        print(f"✓ Dashboard generated: {dashboard_path}")
    except Exception as e:
        print(f"✗ Error generating dashboard: {e}")
        sys.exit(1)
    
    # Create a simple README in public folder
    readme_content = """# Sustainability Regulation Dashboard

**Prepared by:** Deepa Rao  
**Last Updated:** Auto-generated daily

## About

This dashboard tracks global sustainability regulations including:
- EU CSRD/ESRS
- IFRS S1/S2
- UK SRS
- Japan SSBJ
- India BRSR
- SBTi Standards

Visit [index.html](./index.html) to view the interactive dashboard.

---

*Automatically deployed via Netlify*
"""
    
    readme_path = public_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✓ Created README: {readme_path}")
    
    print("\n" + "=" * 80)
    print("Build Complete!")
    print("=" * 80)
    print(f"\nPublic directory ready at: {public_dir}")
    print("Files:")
    for file in public_dir.iterdir():
        size = file.stat().st_size / 1024
        print(f"  - {file.name} ({size:.1f} KB)")
    print("\nReady for Netlify deployment! 🚀")
    

if __name__ == "__main__":
    main()

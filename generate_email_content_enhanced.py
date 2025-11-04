"""
generate_email_content_enhanced.py
-----------------------------------

Generate professional email content with comprehensive regulation tracking metadata.

Author: Deepa Rao
"""

import os
import sqlite3
import sys
from datetime import datetime, UTC


def generate_professional_plain_text(conn: sqlite3.Connection) -> str:
    """Generate enhanced plain-text email with full metadata."""
    cur = conn.cursor()
    rows = cur.execute(
        """SELECT source, title, link, date, summary, first_published, last_updated,
           compliance_deadline, significant_changes, impact_level, affected_sectors, 
           jurisdiction FROM updates ORDER BY compliance_deadline, source, date DESC"""
    ).fetchall()
    
    lines = []
    lines.append("=" * 90)
    lines.append("SUSTAINABILITY REGULATORY UPDATES")
    lines.append("Prepared by: Deepa Rao | Sustainability Compliance Analyst")
    lines.append("=" * 90)
    lines.append(f"Generated: {datetime.now(UTC).strftime('%B %d, %Y at %H:%M UTC')}")
    lines.append(f"Total Regulations Tracked: {len(rows)}")
    lines.append("")
    
    # Statistics
    high_impact = len([r for r in rows if r[9] == "High"])
    medium_impact = len([r for r in rows if r[9] == "Medium"])
    low_impact = len([r for r in rows if r[9] == "Low"])
    
    lines.append("IMPACT SUMMARY")
    lines.append(f"  • High Impact: {high_impact} regulations")
    lines.append(f"  • Medium Impact: {medium_impact} regulations")
    lines.append(f"  • Low Impact: {low_impact} regulations")
    lines.append("")
    
    # Upcoming deadlines
    upcoming = [r for r in rows if r[7] and r[7] != "Voluntary commitment (5-24 month target-setting timeline)" and "2026" in r[7]]
    if upcoming:
        lines.append("⚠️  URGENT: UPCOMING COMPLIANCE DEADLINES")
        lines.append("-" * 90)
        for row in upcoming:
            lines.append(f"  📅 {row[7]} - {row[1]} ({row[11]})")
        lines.append("")
    
    current_source = None
    for row in rows:
        (source, title, link, date, summary, first_published, last_updated,
         compliance_deadline, significant_changes, impact_level, 
         affected_sectors, jurisdiction) = row
        
        if source != current_source:
            if current_source is not None:
                lines.append("")
            current_source = source
            lines.append("=" * 90)
            lines.append(f"SOURCE: {source} | JURISDICTION: {jurisdiction}")
            lines.append("=" * 90)
            lines.append("")
        
        lines.append(f"📋 {title}")
        lines.append(f"   Impact Level: {impact_level}")
        lines.append(f"   Link: {link}")
        lines.append("")
        
        lines.append("   KEY DATES:")
        lines.append(f"     • First Published: {first_published or date}")
        lines.append(f"     • Last Updated: {last_updated or date}")
        lines.append(f"     • Compliance Deadline: {compliance_deadline or 'To be announced'}")
        lines.append("")
        
        if affected_sectors:
            lines.append("   AFFECTED SECTORS:")
            sectors = [s.strip() for s in affected_sectors.split(',')]
            for sector in sectors:
                lines.append(f"     • {sector}")
            lines.append("")
        
        lines.append("   SUMMARY:")
        words = summary.split()
        line_buffer = "     "
        for word in words:
            if len(line_buffer) + len(word) + 1 > 88:
                lines.append(line_buffer)
                line_buffer = "     " + word
            else:
                line_buffer += (" " if line_buffer != "     " else "") + word
        if line_buffer.strip():
            lines.append(line_buffer)
        lines.append("")
        
        if significant_changes:
            lines.append("   📌 SIGNIFICANT CHANGES:")
            changes = [c.strip() for c in significant_changes.split(';')]
            for change in changes:
                if change:
                    lines.append(f"     • {change}")
            lines.append("")
        
        lines.append("-" * 90)
        lines.append("")
    
    lines.append("=" * 90)
    lines.append("END OF REPORT")
    lines.append("")
    lines.append("Prepared by: Deepa Rao")
    lines.append("Sustainability Compliance Analyst")
    lines.append("For inquiries or additional information, please contact the administrator.")
    lines.append("=" * 90)
    
    return "\n".join(lines)


def generate_professional_html(conn: sqlite3.Connection) -> str:
    """Generate professional HTML email with enhanced styling."""
    cur = conn.cursor()
    rows = cur.execute(
        """SELECT source, title, link, date, summary, first_published, last_updated,
           compliance_deadline, significant_changes, impact_level, affected_sectors, 
           jurisdiction FROM updates ORDER BY compliance_deadline, source, date DESC"""
    ).fetchall()
    
    high_impact = len([r for r in rows if r[9] == "High"])
    medium_impact = len([r for r in rows if r[9] == "Medium"])
    low_impact = len([r for r in rows if r[9] == "Low"])
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 800px;
    margin: 0 auto;
    padding: 0;
    background-color: #f5f5f5;
}}
.email-container {{
    background-color: #ffffff;
    margin: 20px auto;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}
.header {{
    background: linear-gradient(135deg, #2a5d84 0%, #1e4a6b 100%);
    color: white;
    padding: 40px 30px;
    text-align: center;
}}
.header h1 {{
    margin: 0 0 10px 0;
    font-size: 2rem;
    font-weight: 700;
}}
.header .subtitle {{
    opacity: 0.95;
    font-size: 1.1rem;
    margin-bottom: 15px;
}}
.header .author {{
    font-size: 0.95rem;
    opacity: 0.9;
    font-style: italic;
}}
.stats-banner {{
    display: flex;
    justify-content: space-around;
    padding: 25px;
    background: #f8f9fa;
    border-bottom: 3px solid #2a5d84;
}}
.stat-box {{
    text-align: center;
}}
.stat-number {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 5px;
}}
.stat-label {{
    font-size: 0.85rem;
    color: #666;
    text-transform: uppercase;
}}
.stat-high {{ color: #dc3545; }}
.stat-medium {{ color: #fd7e14; }}
.stat-low {{ color: #28a745; }}
.content {{
    padding: 30px;
}}
.urgent-section {{
    background: #fff5f5;
    border: 2px solid #dc3545;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 30px;
}}
.urgent-title {{
    color: #dc3545;
    font-weight: 700;
    font-size: 1.2rem;
    margin-bottom: 15px;
}}
.deadline-item {{
    padding: 10px 0;
    border-bottom: 1px solid #fdd;
}}
.deadline-item:last-child {{
    border-bottom: none;
}}
.source-section {{
    margin-bottom: 40px;
}}
.source-header {{
    background: #2a5d84;
    color: white;
    padding: 15px 20px;
    margin: 30px -30px 20px -30px;
    font-size: 1.3rem;
    font-weight: 600;
}}
.update-card {{
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 25px;
    margin-bottom: 20px;
}}
.update-title {{
    font-size: 1.2rem;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 15px;
}}
.badge-container {{
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
    flex-wrap: wrap;
}}
.badge {{
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}}
.badge-high {{ background: #ffe0e0; color: #dc3545; }}
.badge-medium {{ background: #fff3cd; color: #fd7e14; }}
.badge-low {{ background: #d4edda; color: #28a745; }}
.badge-jurisdiction {{ background: #e8f4f8; color: #2a5d84; }}
.metadata-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    background: #f8f9fa;
    padding: 15px;
    border-radius: 6px;
    margin: 15px 0;
    font-size: 0.9rem;
}}
.metadata-item {{
    display: flex;
    flex-direction: column;
}}
.metadata-label {{
    font-weight: 600;
    color: #666;
    font-size: 0.8rem;
    text-transform: uppercase;
    margin-bottom: 3px;
}}
.metadata-value {{
    color: #1a1a1a;
}}
.summary-box {{
    color: #444;
    line-height: 1.7;
    margin: 15px 0;
}}
.changes-box {{
    background: #fffbf0;
    border-left: 4px solid #fd7e14;
    padding: 15px;
    margin: 15px 0;
    border-radius: 4px;
}}
.changes-title {{
    font-weight: 600;
    color: #fd7e14;
    margin-bottom: 10px;
}}
.changes-list {{
    list-style: none;
    padding-left: 0;
}}
.changes-list li {{
    padding-left: 20px;
    position: relative;
    margin-bottom: 5px;
}}
.changes-list li:before {{
    content: "•";
    position: absolute;
    left: 0;
    color: #fd7e14;
    font-weight: bold;
}}
.sectors-box {{
    margin: 15px 0;
}}
.sectors-list {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}}
.sector-tag {{
    background: #e8f4f8;
    color: #2a5d84;
    padding: 5px 10px;
    border-radius: 16px;
    font-size: 0.85rem;
}}
.read-more-btn {{
    display: inline-block;
    margin-top: 15px;
    padding: 10px 20px;
    background: #2a5d84;
    color: white !important;
    text-decoration: none;
    border-radius: 6px;
    font-weight: 500;
}}
.footer {{
    background: #2a5d84;
    color: white;
    padding: 30px;
    text-align: center;
    margin-top: 40px;
}}
.footer-title {{
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 10px;
}}
.footer-author {{
    font-size: 1rem;
    margin-bottom: 15px;
}}
.footer-disclaimer {{
    font-size: 0.85rem;
    opacity: 0.9;
    line-height: 1.6;
}}
@media (max-width: 600px) {{
    .stats-banner {{ flex-direction: column; gap: 15px; }}
    .metadata-grid {{ grid-template-columns: 1fr; }}
    .source-header {{ margin-left: -20px; margin-right: -20px; }}
    .content {{ padding: 20px; }}
}}
</style>
</head>
<body>
<div class="email-container">
    <div class="header">
        <h1>🌍 Sustainability Regulatory Updates</h1>
        <div class="subtitle">Global ESG & Climate Disclosure Tracking</div>
        <div class="author">Prepared by: Deepa Rao, Sustainability Compliance Analyst</div>
    </div>
    
    <div class="stats-banner">
        <div class="stat-box">
            <div class="stat-number">{len(rows)}</div>
            <div class="stat-label">Total Updates</div>
        </div>
        <div class="stat-box">
            <div class="stat-number stat-high">{high_impact}</div>
            <div class="stat-label">High Impact</div>
        </div>
        <div class="stat-box">
            <div class="stat-number stat-medium">{medium_impact}</div>
            <div class="stat-label">Medium Impact</div>
        </div>
        <div class="stat-box">
            <div class="stat-number stat-low">{low_impact}</div>
            <div class="stat-label">Low Impact</div>
        </div>
    </div>
    
    <div class="content">
        <p style="color: #666; margin-bottom: 20px;">
            Generated on {datetime.now(UTC).strftime('%B %d, %Y at %H:%M UTC')}
        </p>
"""
    
    # Urgent deadlines section
    upcoming = [r for r in rows if r[7] and r[7] != "Voluntary commitment (5-24 month target-setting timeline)" and "2026" in r[7]]
    if upcoming:
        html += """
        <div class="urgent-section">
            <div class="urgent-title">⚠️ Urgent: Upcoming Compliance Deadlines</div>
"""
        for row in upcoming:
            html += f"""
            <div class="deadline-item">
                <strong>📅 {row[7]}</strong> - {row[1]} ({row[11]})
            </div>
"""
        html += """
        </div>
"""
    
    # Regulation updates
    current_source = None
    for row in rows:
        (source, title, link, date, summary, first_published, last_updated,
         compliance_deadline, significant_changes, impact_level, 
         affected_sectors, jurisdiction) = row
        
        if source != current_source:
            current_source = source
            html += f"""
        <div class="source-header">{source} - {jurisdiction}</div>
        <div class="source-section">
"""
        
        # Escape HTML
        safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe_summary = summary.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        impact_class = f"badge-{impact_level.lower()}"
        
        html += f"""
            <div class="update-card">
                <div class="update-title">{safe_title}</div>
                
                <div class="badge-container">
                    <span class="badge {impact_class}">{impact_level} Impact</span>
                    <span class="badge badge-jurisdiction">{jurisdiction}</span>
                </div>
                
                <div class="metadata-grid">
                    <div class="metadata-item">
                        <span class="metadata-label">First Published</span>
                        <span class="metadata-value">{first_published or date}</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">Last Updated</span>
                        <span class="metadata-value">{last_updated or date}</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">Compliance Deadline</span>
                        <span class="metadata-value">{compliance_deadline or 'To be announced'}</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">Impact Level</span>
                        <span class="metadata-value">{impact_level}</span>
                    </div>
                </div>
                
                <div class="summary-box">{safe_summary}</div>
"""
        
        if significant_changes:
            changes = [c.strip() for c in significant_changes.split(';')]
            html += """
                <div class="changes-box">
                    <div class="changes-title">📌 Significant Changes</div>
                    <ul class="changes-list">
"""
            for change in changes:
                if change:
                    safe_change = change.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    html += f"<li>{safe_change}</li>"
            html += """
                    </ul>
                </div>
"""
        
        if affected_sectors:
            sectors = [s.strip() for s in affected_sectors.split(',')]
            html += """
                <div class="sectors-box">
                    <div class="metadata-label">Affected Sectors</div>
                    <div class="sectors-list">
"""
            for sector in sectors:
                html += f'<span class="sector-tag">{sector}</span>'
            html += """
                    </div>
                </div>
"""
        
        html += f"""
                <a href="{link}" class="read-more-btn" target="_blank">Read Full Document →</a>
            </div>
"""
    
    html += """
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-title">Sustainability Regulation Tracker</div>
        <div class="footer-author">Prepared by: Deepa Rao | Sustainability Compliance Analyst</div>
        <div class="footer-disclaimer">
            This report tracks global sustainability regulations including EU CSRD/ESRS, 
            IFRS S1/S2, UK SRS, Japan SSBJ, India BRSR, and SBTi standards. 
            For questions, updates, or additional information, please contact the administrator.
        </div>
    </div>
</div>
</body>
</html>
"""
    
    return html


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "sustainability_updates_enhanced.db")
    
    if not os.path.exists(db_path):
        print(f"Error: Enhanced database not found at {db_path}")
        print("Run sustainability_agent_enhanced.py first to populate the database.")
        sys.exit(1)
    
    conn = sqlite3.connect(db_path)
    
    # Generate both formats
    plain_text = generate_professional_plain_text(conn)
    html = generate_professional_html(conn)
    
    # Save to files
    plain_path = os.path.join(script_dir, "email_content_enhanced_plain.txt")
    html_path = os.path.join(script_dir, "email_content_enhanced_html.html")
    
    with open(plain_path, "w", encoding="utf-8") as f:
        f.write(plain_text)
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✓ Enhanced plain text email saved to: {plain_path}")
    print(f"✓ Enhanced HTML email saved to: {html_path}")
    print("")
    print("=" * 90)
    print("PLAIN TEXT VERSION (Ready to copy):")
    print("=" * 90)
    print(plain_text[:2000])  # Show first 2000 chars
    print("\n... (see full content in file)")
    print("")
    print(f"For HTML version, open: {html_path}")
    
    conn.close()


if __name__ == "__main__":
    main()

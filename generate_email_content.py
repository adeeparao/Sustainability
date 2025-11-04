"""
Generate email-friendly formatted output from the sustainability database.
Produces both plain text and HTML email formats.
"""

import os
import sqlite3
import sys
from datetime import datetime, UTC


def generate_plain_text_email(conn: sqlite3.Connection) -> str:
    """Generate a clean plain-text email body."""
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT source, title, link, date, summary FROM updates ORDER BY source, date DESC"
    ).fetchall()
    
    lines = []
    lines.append("=" * 80)
    lines.append("SUSTAINABILITY REGULATORY UPDATES")
    lines.append("=" * 80)
    lines.append(f"Generated: {datetime.now(UTC).strftime('%B %d, %Y at %H:%M UTC')}")
    lines.append("")
    
    current_source = None
    for source, title, link, date, summary in rows:
        if source != current_source:
            if current_source is not None:
                lines.append("")
            current_source = source
            lines.append("-" * 80)
            lines.append(f"SOURCE: {source}")
            lines.append("-" * 80)
            lines.append("")
        
        lines.append(f"📋 {title}")
        lines.append(f"   Date: {date}")
        lines.append(f"   Link: {link}")
        lines.append("")
        # Wrap summary text
        words = summary.split()
        line_buffer = "   "
        for word in words:
            if len(line_buffer) + len(word) + 1 > 80:
                lines.append(line_buffer)
                line_buffer = "   " + word
            else:
                line_buffer += (" " if line_buffer != "   " else "") + word
        if line_buffer.strip():
            lines.append(line_buffer)
        lines.append("")
    
    lines.append("=" * 80)
    lines.append("End of Report")
    lines.append("=" * 80)
    
    return "\n".join(lines)


def generate_html_email(conn: sqlite3.Connection) -> str:
    """Generate a professional HTML email body."""
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT source, title, link, date, summary FROM updates ORDER BY source, date DESC"
    ).fetchall()
    
    lines = []
    lines.append("""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
}
.container {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
h1 {
    color: #2a5d84;
    border-bottom: 3px solid #2a5d84;
    padding-bottom: 10px;
    margin-top: 0;
}
h2 {
    color: #2a5d84;
    background-color: #e8f4f8;
    padding: 10px 15px;
    border-left: 4px solid #2a5d84;
    margin-top: 30px;
}
.update-item {
    margin: 20px 0;
    padding: 15px;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    background-color: #fafafa;
}
.update-title {
    font-size: 16px;
    font-weight: bold;
    color: #1a1a1a;
    margin-bottom: 8px;
}
.update-meta {
    font-size: 14px;
    color: #666;
    margin-bottom: 10px;
}
.update-summary {
    font-size: 14px;
    color: #444;
    line-height: 1.6;
}
.update-link {
    display: inline-block;
    margin-top: 10px;
    color: #2a5d84;
    text-decoration: none;
    font-weight: 500;
}
.update-link:hover {
    text-decoration: underline;
}
.footer {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #e0e0e0;
    font-size: 12px;
    color: #888;
    text-align: center;
}
</style>
</head>
<body>
<div class="container">
<h1>🌍 Sustainability Regulatory Updates</h1>
<p style="color: #666; font-size: 14px;">""")
    lines.append(f"Generated on {datetime.now(UTC).strftime('%B %d, %Y at %H:%M UTC')}")
    lines.append("</p>")
    
    current_source = None
    for source, title, link, date, summary in rows:
        if source != current_source:
            if current_source is not None:
                pass  # Just continue
            current_source = source
            lines.append(f"<h2>{source}</h2>")
        
        # Escape HTML special characters
        safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe_summary = summary.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        lines.append('<div class="update-item">')
        lines.append(f'<div class="update-title">{safe_title}</div>')
        lines.append(f'<div class="update-meta">📅 {date}</div>')
        lines.append(f'<div class="update-summary">{safe_summary}</div>')
        lines.append(f'<a href="{link}" class="update-link" target="_blank">Read More →</a>')
        lines.append('</div>')
    
    lines.append("""
<div class="footer">
<p>This is an automated digest from the Sustainability Agent.</p>
<p>For questions or to unsubscribe, please contact the sender.</p>
</div>
</div>
</body>
</html>""")
    
    return "\n".join(lines)


def main():
    # Find the database
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "sustainability_updates.db")
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        print("Run sustainability_agent.py first to populate the database.")
        sys.exit(1)
    
    conn = sqlite3.connect(db_path)
    
    # Generate both formats
    plain_text = generate_plain_text_email(conn)
    html = generate_html_email(conn)
    
    # Save to files
    plain_path = os.path.join(script_dir, "email_content_plain.txt")
    html_path = os.path.join(script_dir, "email_content_html.html")
    
    with open(plain_path, "w", encoding="utf-8") as f:
        f.write(plain_text)
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✓ Plain text email saved to: {plain_path}")
    print(f"✓ HTML email saved to: {html_path}")
    print("")
    print("=" * 80)
    print("PLAIN TEXT VERSION (copy this for plain email):")
    print("=" * 80)
    print(plain_text)
    print("")
    print(f"For HTML version, open: {html_path}")
    
    conn.close()


if __name__ == "__main__":
    main()

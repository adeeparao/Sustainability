"""
Generate Interactive Professional Dashboard
with clickable stat cards and compliance tracker

Author: Deepa Rao
"""

import sqlite3
import os
import sys
from datetime import datetime, UTC
import json


def generate_interactive_dashboard(db_path: str, html_path: str) -> None:
    """Generate interactive dashboard with clickable cards and compliance tracking."""
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        print("Run sustainability_agent_enhanced.py first.")
        sys.exit(1)
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    rows = cur.execute(
        """SELECT source, title, link, date, summary, first_published, last_updated,
           compliance_deadline, significant_changes, impact_level, affected_sectors, 
           jurisdiction FROM updates ORDER BY compliance_deadline, date DESC"""
    ).fetchall()
    
    # Calculate statistics
    total_updates = len(rows)
    high_impact = [r for r in rows if r[9] == "High"]
    medium_impact = [r for r in rows if r[9] == "Medium"]
    low_impact = [r for r in rows if r[9] == "Low"]
    
    # Count by source
    source_counts = {}
    for row in rows:
        source = row[0]
        source_counts[source] = source_counts.get(source, 0) + 1
    
    # Convert to JSON for JavaScript
    regulations_json = []
    for row in rows:
        regulations_json.append({
            "source": row[0],
            "title": row[1],
            "link": row[2],
            "date": row[3],
            "summary": row[4],
            "first_published": row[5] or row[3],
            "last_updated": row[6] or row[3],
            "compliance_deadline": row[7] or "To be announced",
            "significant_changes": row[8] or "",
            "impact_level": row[9],
            "affected_sectors": row[10] or "",
            "jurisdiction": row[11]
        })
    
    regulations_js = json.dumps(regulations_json, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sustainability Regulation Dashboard | Deepa Rao</title>
<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #1a1a1a;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}}

.container {{
    max-width: 1400px;
    margin: 0 auto;
    background: white;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    overflow: hidden;
}}

.header {{
    background: linear-gradient(135deg, #2a5d84 0%, #1e4a6b 100%);
    color: white;
    padding: 40px;
    text-align: center;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
    font-weight: 700;
}}

.header .subtitle {{
    font-size: 1.1rem;
    opacity: 0.9;
    margin-bottom: 20px;
}}

.header .meta {{
    font-size: 0.95rem;
    opacity: 0.85;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    flex-wrap: wrap;
}}

.meta-item {{
    display: flex;
    align-items: center;
    gap: 8px;
}}

.stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    padding: 40px;
    background: #f8f9fa;
}}

.stat-card {{
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
    transition: all 0.3s;
    cursor: pointer;
    position: relative;
}}

.stat-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}}

.stat-card:active {{
    transform: translateY(-2px);
}}

.stat-card::after {{
    content: "Click to view";
    position: absolute;
    bottom: 8px;
    right: 12px;
    font-size: 0.75rem;
    color: #999;
    opacity: 0;
    transition: opacity 0.2s;
}}

.stat-card:hover::after {{
    opacity: 1;
}}

.stat-number {{
    font-size: 2.5rem;
    font-weight: 700;
    color: #2a5d84;
    margin-bottom: 8px;
}}

.stat-label {{
    font-size: 0.95rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.impact-high .stat-number {{ color: #dc3545; }}
.impact-medium .stat-number {{ color: #fd7e14; }}
.impact-low .stat-number {{ color: #28a745; }}

.content {{
    padding: 40px;
}}

.section {{
    margin-bottom: 50px;
}}

.section-title {{
    font-size: 1.8rem;
    color: #2a5d84;
    margin-bottom: 25px;
    padding-bottom: 12px;
    border-bottom: 3px solid #2a5d84;
    display: flex;
    align-items: center;
    gap: 12px;
}}

/* Modal Styles */
.modal {{
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0,0,0,0.6);
    animation: fadeIn 0.3s;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

.modal-content {{
    background-color: #fefefe;
    margin: 3% auto;
    padding: 0;
    border-radius: 12px;
    width: 90%;
    max-width: 1000px;
    max-height: 85vh;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    animation: slideDown 0.3s;
}}

@keyframes slideDown {{
    from {{
        transform: translateY(-50px);
        opacity: 0;
    }}
    to {{
        transform: translateY(0);
        opacity: 1;
    }}
}}

.modal-header {{
    background: linear-gradient(135deg, #2a5d84 0%, #1e4a6b 100%);
    color: white;
    padding: 25px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.modal-title {{
    font-size: 1.8rem;
    font-weight: 600;
}}

.close {{
    color: white;
    font-size: 2rem;
    font-weight: 300;
    cursor: pointer;
    transition: transform 0.2s;
    line-height: 1;
}}

.close:hover {{
    transform: scale(1.2);
}}

.modal-body {{
    padding: 30px;
    max-height: calc(85vh - 100px);
    overflow-y: auto;
}}

.modal-summary {{
    background: #e8f4f8;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 25px;
    border-left: 4px solid #2a5d84;
}}

.modal-summary h3 {{
    color: #2a5d84;
    margin-bottom: 10px;
}}

.regulation-mini-card {{
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
    transition: all 0.2s;
}}

.regulation-mini-card:hover {{
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transform: translateX(4px);
}}

.regulation-mini-title {{
    font-size: 1.1rem;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 8px;
}}

.regulation-mini-meta {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 10px;
}}

.mini-badge {{
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
}}

.badge-high {{ background: #ffe0e0; color: #dc3545; }}
.badge-medium {{ background: #fff3cd; color: #fd7e14; }}
.badge-low {{ background: #d4edda; color: #28a745; }}
.badge-source {{ background: #e8f4f8; color: #2a5d84; }}

.regulation-mini-summary {{
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 10px;
    line-height: 1.5;
}}

.mini-link {{
    color: #2a5d84;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
}}

.mini-link:hover {{
    text-decoration: underline;
}}

/* Compliance Tracker Styles */
.compliance-tracker {{
    background: white;
    border: 2px solid #2a5d84;
    border-radius: 12px;
    padding: 30px;
    margin-bottom: 40px;
}}

.tracker-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    flex-wrap: wrap;
    gap: 15px;
}}

.tracker-title {{
    font-size: 1.6rem;
    color: #2a5d84;
    font-weight: 600;
}}

.tracker-controls {{
    display: flex;
    gap: 10px;
}}

.btn {{
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.9rem;
}}

.btn-primary {{
    background: #2a5d84;
    color: white;
}}

.btn-primary:hover {{
    background: #1e4a6b;
}}

.btn-secondary {{
    background: #6c757d;
    color: white;
}}

.btn-secondary:hover {{
    background: #5a6268;
}}

.compliance-grid {{
    display: grid;
    gap: 15px;
}}

.compliance-item {{
    background: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-left: 4px solid #6c757d;
    padding: 20px;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 40px 1fr auto;
    gap: 15px;
    align-items: start;
    transition: all 0.2s;
}}

.compliance-item.status-not-started {{
    border-left-color: #dc3545;
}}

.compliance-item.status-in-progress {{
    border-left-color: #fd7e14;
}}

.compliance-item.status-completed {{
    border-left-color: #28a745;
}}

.compliance-checkbox {{
    width: 24px;
    height: 24px;
    cursor: pointer;
    margin-top: 5px;
}}

.compliance-details {{
    flex: 1;
}}

.compliance-regulation {{
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 5px;
}}

.compliance-deadline {{
    font-size: 0.85rem;
    color: #dc3545;
    margin-bottom: 8px;
    font-weight: 500;
}}

.compliance-notes {{
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.9rem;
    margin-top: 8px;
    resize: vertical;
    min-height: 60px;
}}

.compliance-status {{
    display: flex;
    flex-direction: column;
    gap: 5px;
}}

.status-select {{
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.9rem;
    cursor: pointer;
}}

.team-input {{
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.9rem;
    width: 180px;
}}

.progress-summary {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    margin-bottom: 25px;
    padding: 20px;
    background: #e8f4f8;
    border-radius: 8px;
}}

.progress-stat {{
    text-align: center;
}}

.progress-number {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 5px;
}}

.progress-label {{
    font-size: 0.85rem;
    color: #666;
    text-transform: uppercase;
}}

.stat-not-started {{ color: #dc3545; }}
.stat-in-progress {{ color: #fd7e14; }}
.stat-completed {{ color: #28a745; }}

.compliance-calendar {{
    display: grid;
    gap: 15px;
}}

.deadline-card {{
    background: #fff;
    border: 2px solid #e0e0e0;
    border-left: 5px solid #2a5d84;
    padding: 20px;
    border-radius: 8px;
    transition: all 0.2s;
}}

.deadline-card:hover {{
    border-left-color: #667eea;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

.deadline-card.urgent {{
    border-left-color: #dc3545;
    background: #fff5f5;
}}

.deadline-date {{
    font-size: 1.1rem;
    font-weight: 600;
    color: #2a5d84;
    margin-bottom: 8px;
}}

.deadline-title {{
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 8px;
    color: #1a1a1a;
}}

.deadline-jurisdiction {{
    display: inline-block;
    padding: 4px 12px;
    background: #e8f4f8;
    border-radius: 20px;
    font-size: 0.85rem;
    color: #2a5d84;
    margin-bottom: 10px;
}}

.update-card {{
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 30px;
    margin-bottom: 25px;
    transition: all 0.2s;
}}

.update-card:hover {{
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    transform: translateX(4px);
}}

.update-header {{
    display: flex;
    justify-content: space-between;
    align-items: start;
    margin-bottom: 15px;
    flex-wrap: wrap;
    gap: 15px;
}}

.update-title {{
    font-size: 1.3rem;
    font-weight: 600;
    color: #1a1a1a;
    flex: 1;
    min-width: 250px;
}}

.update-badges {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}}

.badge {{
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    white-space: nowrap;
}}

.update-meta {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin: 20px 0;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    font-size: 0.9rem;
}}

.meta-row {{
    display: flex;
    flex-direction: column;
}}

.meta-label {{
    font-weight: 600;
    color: #666;
    font-size: 0.85rem;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.meta-value {{
    color: #1a1a1a;
}}

.update-summary {{
    color: #444;
    line-height: 1.7;
    margin: 15px 0;
}}

.update-changes {{
    background: #fffbf0;
    border-left: 4px solid #fd7e14;
    padding: 15px;
    margin: 15px 0;
    border-radius: 4px;
}}

.changes-title {{
    font-weight: 600;
    color: #fd7e14;
    margin-bottom: 8px;
    font-size: 0.95rem;
}}

.update-sectors {{
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
    padding: 5px 12px;
    border-radius: 16px;
    font-size: 0.85rem;
}}

.update-link {{
    display: inline-block;
    margin-top: 15px;
    padding: 10px 20px;
    background: #2a5d84;
    color: white;
    text-decoration: none;
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.2s;
}}

.update-link:hover {{
    background: #1e4a6b;
    transform: translateX(4px);
}}

.footer {{
    background: #2a5d84;
    color: white;
    padding: 30px;
    text-align: center;
}}

.footer-title {{
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 8px;
}}

.footer-subtitle {{
    opacity: 0.9;
    margin-bottom: 15px;
}}

.footer-meta {{
    opacity: 0.8;
    font-size: 0.9rem;
}}

@media (max-width: 768px) {{
    .header h1 {{ font-size: 1.8rem; }}
    .stats-grid {{ grid-template-columns: 1fr; padding: 20px; }}
    .content {{ padding: 20px; }}
    .update-header {{ flex-direction: column; }}
    .update-meta {{ grid-template-columns: 1fr; }}
    .compliance-item {{ grid-template-columns: 1fr; }}
    .tracker-header {{ flex-direction: column; align-items: start; }}
}}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🌍 Sustainability Regulation Dashboard</h1>
        <div class="subtitle">Interactive ESG & Climate Disclosure Tracking System</div>
        <div class="meta">
            <div class="meta-item">
                <span>📊</span>
                <span>Generated: {datetime.now(UTC).strftime('%B %d, %Y at %H:%M UTC')}</span>
            </div>
            <div class="meta-item">
                <span>👤</span>
                <span>Prepared by: <strong>Deepa Rao</strong></span>
            </div>
            <div class="meta-item">
                <span>📈</span>
                <span>{total_updates} Active Regulations</span>
            </div>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-card" onclick="showFilteredRegulations('all')">
            <div class="stat-number">{total_updates}</div>
            <div class="stat-label">Total Updates</div>
        </div>
        <div class="stat-card impact-high" onclick="showFilteredRegulations('high')">
            <div class="stat-number">{len(high_impact)}</div>
            <div class="stat-label">High Impact</div>
        </div>
        <div class="stat-card impact-medium" onclick="showFilteredRegulations('medium')">
            <div class="stat-number">{len(medium_impact)}</div>
            <div class="stat-label">Medium Impact</div>
        </div>
        <div class="stat-card impact-low" onclick="showFilteredRegulations('low')">
            <div class="stat-number">{len(low_impact)}</div>
            <div class="stat-label">Low Impact</div>
        </div>
"""
    
    # Add source breakdown cards
    for source, count in source_counts.items():
        html += f"""
        <div class="stat-card" onclick="showFilteredRegulations('source', '{source}')">
            <div class="stat-number">{count}</div>
            <div class="stat-label">{source}</div>
        </div>
"""
    
    html += """
    </div>

    <div class="content">
        <!-- Compliance Tracker Section -->
        <div class="section">
            <h2 class="section-title">✅ Compliance Tracker</h2>
            <div class="compliance-tracker">
                <div class="tracker-header">
                    <div class="tracker-title">Track Your Organization's Compliance</div>
                    <div class="tracker-controls">
                        <button class="btn btn-secondary" onclick="resetCompliance()">Reset All</button>
                        <button class="btn btn-primary" onclick="exportCompliance()">Export Report</button>
                    </div>
                </div>
                
                <div class="progress-summary" id="progressSummary">
                    <div class="progress-stat">
                        <div class="progress-number stat-not-started" id="countNotStarted">0</div>
                        <div class="progress-label">Not Started</div>
                    </div>
                    <div class="progress-stat">
                        <div class="progress-number stat-in-progress" id="countInProgress">0</div>
                        <div class="progress-label">In Progress</div>
                    </div>
                    <div class="progress-stat">
                        <div class="progress-number stat-completed" id="countCompleted">0</div>
                        <div class="progress-label">Completed</div>
                    </div>
                    <div class="progress-stat">
                        <div class="progress-number" id="countTotal" style="color: #2a5d84;">0</div>
                        <div class="progress-label">Total Items</div>
                    </div>
                </div>
                
                <div class="compliance-grid" id="complianceGrid">
                    <!-- Compliance items will be generated by JavaScript -->
                </div>
            </div>
        </div>
"""
    
    # Compliance calendar
    upcoming = [r for r in rows if r[7] and r[7] != "Voluntary commitment (5-24 month target-setting timeline)"]
    if upcoming:
        html += """
        <div class="section">
            <h2 class="section-title">📅 Compliance Calendar</h2>
            <div class="compliance-calendar">
"""
        for row in upcoming:
            deadline = row[7]
            title = row[1]
            jurisdiction = row[11]
            urgent_class = ""
            if deadline and "2026" in deadline:
                urgent_class = "urgent"
            
            html += f"""
                <div class="deadline-card {urgent_class}">
                    <div class="deadline-date">⏰ {deadline}</div>
                    <div class="deadline-title">{title}</div>
                    <span class="deadline-jurisdiction">{jurisdiction}</span>
                </div>
"""
        html += """
            </div>
        </div>
"""
    
    # All updates
    html += """
        <div class="section">
            <h2 class="section-title">📋 Detailed Regulation Updates</h2>
"""
    
    current_source = None
    for row in rows:
        (source, title, link, date, summary, first_published, last_updated,
         compliance_deadline, significant_changes, impact_level, 
         affected_sectors, jurisdiction) = row
        
        if source != current_source:
            current_source = source
            html += f"""
            <h3 style="color: #2a5d84; margin: 30px 0 20px 0; font-size: 1.5rem;">
                {source} - {jurisdiction}
            </h3>
"""
        
        # Escape HTML
        safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        safe_summary = summary.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe_changes = significant_changes.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") if significant_changes else ""
        
        impact_class = f"badge-{impact_level.lower()}"
        
        html += f"""
            <div class="update-card">
                <div class="update-header">
                    <div class="update-title">{safe_title}</div>
                    <div class="update-badges">
                        <span class="badge badge-source">{source}</span>
                        <span class="badge {impact_class}">{impact_level} Impact</span>
                    </div>
                </div>
                
                <div class="update-meta">
                    <div class="meta-row">
                        <span class="meta-label">First Published</span>
                        <span class="meta-value">{first_published or date}</span>
                    </div>
                    <div class="meta-row">
                        <span class="meta-label">Last Updated</span>
                        <span class="meta-value">{last_updated or date}</span>
                    </div>
                    <div class="meta-row">
                        <span class="meta-label">Compliance Deadline</span>
                        <span class="meta-value">{compliance_deadline or 'To be announced'}</span>
                    </div>
                    <div class="meta-row">
                        <span class="meta-label">Jurisdiction</span>
                        <span class="meta-value">{jurisdiction}</span>
                    </div>
                </div>
                
                <div class="update-summary">{safe_summary}</div>
"""
        
        if safe_changes:
            html += f"""
                <div class="update-changes">
                    <div class="changes-title">📌 Significant Changes</div>
                    <div>{safe_changes}</div>
                </div>
"""
        
        if affected_sectors:
            sectors = [s.strip() for s in affected_sectors.split(',')]
            html += """
                <div class="update-sectors">
                    <div class="meta-label">Affected Sectors</div>
                    <div class="sectors-list">
"""
            for sector in sectors:
                html += f'<span class="sector-tag">{sector}</span>'
            html += """
                    </div>
                </div>
"""
        
        html += f"""
                <a href="{link}" class="update-link" target="_blank">Read Full Document →</a>
            </div>
"""
    
    html += f"""
        </div>
    </div>

    <div class="footer">
        <div class="footer-title">Sustainability Regulation Tracker</div>
        <div class="footer-subtitle">Comprehensive ESG & Climate Disclosure Monitoring</div>
        <div class="footer-meta">
            <p>Prepared by: Deepa Rao | Sustainability Compliance Analyst</p>
            <p style="margin-top: 8px; opacity: 0.7;">
                This dashboard tracks global sustainability regulations including EU CSRD/ESRS, 
                IFRS S1/S2, UK SRS, Japan SSBJ, India BRSR, and SBTi standards.
            </p>
            <p style="margin-top: 12px; font-size: 0.85rem;">
                For questions or updates, please contact the administrator.
            </p>
        </div>
    </div>
</div>

<!-- Modal for filtered regulations -->
<div id="regulationModal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2 class="modal-title" id="modalTitle">Regulations</h2>
            <span class="close" onclick="closeModal()">&times;</span>
        </div>
        <div class="modal-body" id="modalBody">
            <!-- Content will be populated by JavaScript -->
        </div>
    </div>
</div>

<script>
// Store regulations data
const regulations = {regulations_js};

// Load compliance data from localStorage
function loadComplianceData() {{
    const saved = localStorage.getItem('complianceData');
    if (saved) {{
        return JSON.parse(saved);
    }}
    // Initialize with default data
    const defaultData = regulations.map((reg, idx) => ({{
        id: idx,
        regulation: reg.title,
        source: reg.source,
        deadline: reg.compliance_deadline,
        status: 'not-started',
        team: '',
        notes: ''
    }}));
    return defaultData;
}}

// Save compliance data to localStorage
function saveComplianceData(data) {{
    localStorage.setItem('complianceData', JSON.stringify(data));
    updateProgressSummary(data);
}}

// Initialize compliance tracker
function initComplianceTracker() {{
    const data = loadComplianceData();
    renderComplianceGrid(data);
    updateProgressSummary(data);
}}

// Render compliance grid
function renderComplianceGrid(data) {{
    const grid = document.getElementById('complianceGrid');
    grid.innerHTML = '';
    
    data.forEach((item, idx) => {{
        const div = document.createElement('div');
        div.className = `compliance-item status-${{item.status}}`;
        div.innerHTML = `
            <input type="checkbox" class="compliance-checkbox" 
                   ${{item.status === 'completed' ? 'checked' : ''}}
                   onchange="toggleComplete(${{idx}})">
            <div class="compliance-details">
                <div class="compliance-regulation">${{item.regulation}}</div>
                <div class="compliance-deadline">⏰ Deadline: ${{item.deadline}}</div>
                <textarea class="compliance-notes" 
                          placeholder="Add notes, action items, or progress updates..."
                          onchange="updateNotes(${{idx}}, this.value)">${{item.notes}}</textarea>
            </div>
            <div class="compliance-status">
                <select class="status-select" onchange="updateStatus(${{idx}}, this.value)">
                    <option value="not-started" ${{item.status === 'not-started' ? 'selected' : ''}}>Not Started</option>
                    <option value="in-progress" ${{item.status === 'in-progress' ? 'selected' : ''}}>In Progress</option>
                    <option value="completed" ${{item.status === 'completed' ? 'selected' : ''}}>Completed</option>
                </select>
                <input type="text" class="team-input" 
                       placeholder="Team/Owner"
                       value="${{item.team}}"
                       onchange="updateTeam(${{idx}}, this.value)">
            </div>
        `;
        grid.appendChild(div);
    }});
}}

// Update progress summary
function updateProgressSummary(data) {{
    const notStarted = data.filter(d => d.status === 'not-started').length;
    const inProgress = data.filter(d => d.status === 'in-progress').length;
    const completed = data.filter(d => d.status === 'completed').length;
    
    document.getElementById('countNotStarted').textContent = notStarted;
    document.getElementById('countInProgress').textContent = inProgress;
    document.getElementById('countCompleted').textContent = completed;
    document.getElementById('countTotal').textContent = data.length;
}}

// Toggle complete
function toggleComplete(idx) {{
    const data = loadComplianceData();
    data[idx].status = data[idx].status === 'completed' ? 'in-progress' : 'completed';
    saveComplianceData(data);
    renderComplianceGrid(data);
}}

// Update status
function updateStatus(idx, status) {{
    const data = loadComplianceData();
    data[idx].status = status;
    saveComplianceData(data);
    renderComplianceGrid(data);
}}

// Update team
function updateTeam(idx, team) {{
    const data = loadComplianceData();
    data[idx].team = team;
    saveComplianceData(data);
}}

// Update notes
function updateNotes(idx, notes) {{
    const data = loadComplianceData();
    data[idx].notes = notes;
    saveComplianceData(data);
}}

// Reset compliance
function resetCompliance() {{
    if (confirm('Are you sure you want to reset all compliance tracking data?')) {{
        localStorage.removeItem('complianceData');
        initComplianceTracker();
    }}
}}

// Export compliance report
function exportCompliance() {{
    const data = loadComplianceData();
    let report = 'Sustainability Compliance Report\\n';
    report += 'Prepared by: Deepa Rao\\n';
    report += `Generated: ${{new Date().toLocaleString()}}\\n\\n`;
    report += '='.repeat(80) + '\\n\\n';
    
    const notStarted = data.filter(d => d.status === 'not-started').length;
    const inProgress = data.filter(d => d.status === 'in-progress').length;
    const completed = data.filter(d => d.status === 'completed').length;
    
    report += `Summary:\\n`;
    report += `  Total Items: ${{data.length}}\\n`;
    report += `  Completed: ${{completed}}\\n`;
    report += `  In Progress: ${{inProgress}}\\n`;
    report += `  Not Started: ${{notStarted}}\\n\\n`;
    report += '='.repeat(80) + '\\n\\n';
    
    data.forEach(item => {{
        report += `Regulation: ${{item.regulation}}\\n`;
        report += `Source: ${{item.source}}\\n`;
        report += `Deadline: ${{item.deadline}}\\n`;
        report += `Status: ${{item.status.toUpperCase()}}\\n`;
        report += `Team/Owner: ${{item.team || 'Not assigned'}}\\n`;
        report += `Notes: ${{item.notes || 'No notes'}}\\n`;
        report += '-'.repeat(80) + '\\n\\n';
    }});
    
    const blob = new Blob([report], {{ type: 'text/plain' }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `compliance-report-${{new Date().toISOString().split('T')[0]}}.txt`;
    a.click();
}}

// Show filtered regulations
function showFilteredRegulations(filter, value) {{
    let filtered = [];
    let title = '';
    let summary = '';
    
    if (filter === 'all') {{
        filtered = regulations;
        title = 'All Regulations';
        summary = `Displaying all ${{regulations.length}} sustainability regulations tracked in the system.`;
    }} else if (filter === 'high' || filter === 'medium' || filter === 'low') {{
        filtered = regulations.filter(r => r.impact_level.toLowerCase() === filter);
        title = `${{filter.charAt(0).toUpperCase() + filter.slice(1)}} Impact Regulations`;
        const impactDesc = {{
            'high': 'These regulations have significant organizational impact requiring immediate attention, substantial resources, and comprehensive implementation strategies.',
            'medium': 'These regulations require moderate organizational changes with planned implementation over multiple phases.',
            'low': 'These regulations have minimal direct impact but should be monitored for future developments.'
        }};
        summary = `${{filtered.length}} regulation(s) classified as ${{filter}} impact. ${{impactDesc[filter]}}`;
    }} else if (filter === 'source') {{
        filtered = regulations.filter(r => r.source === value);
        title = `${{value}} Regulations`;
        summary = `${{filtered.length}} regulation(s) from ${{value}}. These represent the current requirements and standards issued by this regulatory body.`;
    }}
    
    displayModal(title, summary, filtered);
}}

// Display modal
function displayModal(title, summary, regulations) {{
    document.getElementById('modalTitle').textContent = title;
    
    let html = `<div class="modal-summary">
        <h3>Summary</h3>
        <p>${{summary}}</p>
    </div>`;
    
    regulations.forEach(reg => {{
        const impactClass = `badge-${{reg.impact_level.toLowerCase()}}`;
        html += `
            <div class="regulation-mini-card">
                <div class="regulation-mini-title">${{reg.title}}</div>
                <div class="regulation-mini-meta">
                    <span class="mini-badge badge-source">${{reg.source}}</span>
                    <span class="mini-badge ${{impactClass}}">${{reg.impact_level}} Impact</span>
                    <span class="mini-badge" style="background: #f0f0f0; color: #666;">${{reg.jurisdiction}}</span>
                </div>
                <div class="regulation-mini-summary">${{reg.summary.substring(0, 200)}}...</div>
                <div style="margin-top: 10px; font-size: 0.85rem; color: #666;">
                    <strong>Deadline:</strong> ${{reg.compliance_deadline}}
                </div>
                ${{reg.significant_changes ? `
                <div style="margin-top: 10px; padding: 10px; background: #fffbf0; border-radius: 4px; font-size: 0.85rem;">
                    <strong style="color: #fd7e14;">Key Changes:</strong> ${{reg.significant_changes}}
                </div>` : ''}}
                <a href="${{reg.link}}" class="mini-link" target="_blank">Read Full Document →</a>
            </div>
        `;
    }});
    
    document.getElementById('modalBody').innerHTML = html;
    document.getElementById('regulationModal').style.display = 'block';
}}

// Close modal
function closeModal() {{
    document.getElementById('regulationModal').style.display = 'none';
}}

// Close modal on outside click
window.onclick = function(event) {{
    const modal = document.getElementById('regulationModal');
    if (event.target === modal) {{
        closeModal();
    }}
}}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {{
    initComplianceTracker();
}});
</script>

</body>
</html>
"""
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✓ Interactive dashboard saved to {html_path}")
    print(f"  - Click any stat card to view filtered regulations")
    print(f"  - Use compliance tracker to monitor your organization's progress")
    print(f"  - All compliance data saved locally in your browser")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "sustainability_updates_enhanced.db")
    html_path = os.path.join(script_dir, "sustainability_dashboard_interactive.html")
    
    print("Generating Interactive Dashboard...")
    print("Author: Deepa Rao")
    print("")
    
    generate_interactive_dashboard(db_path, html_path)
    
    print("")
    print("✓ Complete! Open the interactive dashboard now.")
    print(f"  File: {html_path}")

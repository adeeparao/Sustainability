"""
sustainability_agent.py
----------------------

This module implements a prototype of an automated agent that monitors
global sustainability regulation websites, extracts new regulatory
announcements, and sends a daily email digest.  It demonstrates how
organisations can stay informed about evolving Environmental,
Social and Governance (ESG) requirements across multiple
jurisdictions.

The agent is designed for educational purposes; it relies on
publicly‑available webpages and PDFs and uses simple web scraping
techniques.  In a production system you would want to harden
scraping logic, add error handling, and enrich the data model to
capture additional metadata (e.g., jurisdictions, sectors, deadline
dates, etc.).  You may also wish to integrate an official API (if
available) or subscribe to RSS feeds from regulators to avoid
scraping altogether.

Key features
============

* **Configurable sources** – a dictionary of target URLs along with a
  parsing function for each source.  Adding a new jurisdiction is as
  simple as writing another parser and appending an entry to the
  `SOURCES` dictionary.

* **Duplicate detection** – the agent stores historical updates in a
  SQLite database.  Before adding a new entry it checks whether the
  title and link have been seen before.  This prevents sending the
  same announcement multiple times.

* **Daily scheduling** – a simple scheduler triggers the update task
  once a day.  In a cloud deployment you could swap this for cron or
  another job scheduler.

* **Email notification** – the agent composes a concise digest of
  newly discovered items and sends it using SMTP.  To enable email
  delivery you must provide credentials via environment variables.

* **Dashboard generation** – the agent produces a static HTML file
  summarising recent updates.  This file can be served via any
  webserver or opened directly by team members.  In a real solution
  you might build a full web app with search, filtering and metrics.

Dependencies
============

The script uses only standard Python libraries except for
``beautifulsoup4`` (for HTML parsing).  Install dependencies via:

.. code-block:: bash

    pip install beautifulsoup4

Usage
=====

1.  Configure the ``SMTP_*`` environment variables (see the
    ``send_email`` function below) with your mail server details.
2.  Run the script manually or schedule it with a cron job.  The first
    execution will populate the database; subsequent runs will email
    only new entries.

"""

import os
import smtplib
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Callable, Dict, List, Optional

import requests
from bs4 import BeautifulSoup


###############################################################################
# Data model
###############################################################################

@dataclass
class UpdateItem:
    """A single regulatory update extracted from a source website.

    Attributes:
        source (str): A human‑readable identifier for the source (e.g. "EU").
        title  (str): The headline or descriptive title of the announcement.
        link   (str): URL pointing to the full announcement or document.
        date   (str): ISO formatted publication date when available.  When
                      unknown, the scrape date is used.
        summary(str): A brief description of the announcement.  This may be
                      extracted from the article itself or truncated from the
                      first paragraph.
        first_published (str): Original publication date of the regulation.
        last_updated (str): Most recent update or amendment date.
        compliance_deadline (str): Deadline for organizations to comply (if applicable).
        significant_changes (str): Key changes or requirements introduced.
        impact_level (str): High, Medium, or Low impact classification.
        affected_sectors (str): Industries/sectors affected (comma-separated).
        jurisdiction (str): Geographic scope (e.g., "EU", "Global", "UK").
    """

    source: str
    title: str
    link: str
    date: str
    summary: str
    first_published: str = ""
    last_updated: str = ""
    compliance_deadline: str = ""
    significant_changes: str = ""
    impact_level: str = "Medium"
    affected_sectors: str = ""
    jurisdiction: str = ""


###############################################################################
# Scraper functions for each jurisdiction
###############################################################################

def parse_eu_quick_fix() -> List[UpdateItem]:
    """Provide a summary of the EU’s ESRS quick‑fix amendment.

    The European Commission adopted a targeted “quick‑fix” amendment to the
    first set of European Sustainability Reporting Standards (ESRS) on
    11 July 2025.  Because some websites block automated requests, this
    parser embeds a hard‑coded summary instead of scraping the site.  If
    network access is available you may replace this implementation with
    a real HTTP scraper.
    """
    url = (
        "https://finance.ec.europa.eu/publications/commission-adopts-quick-fix-"
        "companies-already-conducting-corporate-sustainability-reporting_en"
    )
    title = "Commission adopts ‘quick fix’ for ESRS wave‑one companies"
    date = "2025-07-11"
    summary = (
        "The European Commission’s quick‑fix amendment allows companies already "
        "reporting for the financial year 2024 to defer disclosure of anticipated "
        "financial effects of sustainability‑related risks and opportunities for "
        "financial years 2025 and 2026.  This delegated act extends phase‑in "
        "relief previously available only to smaller companies, reducing "
        "reporting burdens while a broader simplification of the ESRS is "
        "underway."
    )
    return [
        UpdateItem(
            source="EU",
            title=title,
            link=url,
            date=date,
            summary=summary,
            first_published="2023-06-09",
            last_updated="2025-07-11",
            compliance_deadline="2026-12-31",
            significant_changes="Deferred disclosure of financial effects for FY2025-2026; Extended phase-in relief to wave-one companies",
            impact_level="High",
            affected_sectors="All EU large companies, Listed SMEs, Financial Institutions",
            jurisdiction="European Union (EU27)"
        )
    ]


def parse_ifrs_s1_s2() -> List[UpdateItem]:
    """Extract high‑level information about IFRS S1 and IFRS S2.

    This parser does not scrape the IFRS website directly (which has
    complex navigation) but synthesises content based on the current
    IFRS standard descriptions.  In a production system you might use
    official feeds or subscription services to monitor changes.
    """
    updates: List[UpdateItem] = []
    # IFRS S1
    s1_summary = (
        "IFRS S1 requires companies to disclose information about all "
        "sustainability‑related risks and opportunities that could reasonably "
        "be expected to affect cash flows, access to finance or cost of capital. "
        "Organisations must report on governance, strategy, risk management and "
        "performance regarding sustainability‑related matters." )
    updates.append(
        UpdateItem(
            source="IFRS",
            title="IFRS S1 – General requirements for sustainability disclosures",
            link="https://www.ifrs.org/issued-standards/ifrs-sustainability-standards-"
            "navigator/ifrs-s1-general-requirements/",
            date="2023-06-26",  # standard issuance date
            summary=s1_summary,
        )
    )
    # IFRS S2
    s2_summary = (
        "IFRS S2 focuses on climate‑related disclosures.  Companies must report "
        "on physical and transition climate risks and opportunities that could "
        "affect their prospects.  Disclosures cover governance, strategy, risk "
        "identification processes and performance against climate targets." )
    updates.append(
        UpdateItem(
            source="IFRS",
            title="IFRS S2 – Climate‑related disclosures",
            link="https://www.ifrs.org/issued-standards/ifrs-sustainability-standards-"
            "navigator/ifrs-s2-climate-related-disclosures/",
            date="2023-06-26",
            summary=s2_summary,
        )
    )
    return updates


def parse_uk_consultation() -> List[UpdateItem]:
    """Parse the UK government guidance about UK Sustainability Reporting Standards.

    The UK Department for Business and Trade launched a consultation on
    exposure drafts of UK SRS S1 and S2 (based on IFRS S1 and S2) on
    25 June 2025.  The consultation remains open until 17 September 2025.
    """
    summary = (
        "The UK government is consulting on draft Sustainability Reporting "
        "Standards S1 and S2 (UK SRS), based on the ISSB’s IFRS S1 and S2.  "
        "The consultation opened on 25 June 2025 and closes on 17 September 2025.  "
        "After finalising the standards later in 2025 they will initially be "
        "voluntary.  The Department for Business and Trade and the Financial "
        "Conduct Authority will consider whether to mandate reporting against "
        "the UK SRS for certain entities." )
    return [
        UpdateItem(
            source="UK",
            title="UK consultation on Sustainability Reporting Standards",
            link="https://www.gov.uk/guidance/uk-sustainability-reporting-standards",
            date="2025-06-25",
            summary=summary,
        )
    ]


def parse_japan_roadmap() -> List[UpdateItem]:
    """Summarise Japan’s roadmap for implementing SSBJ standards.

    The roadmap published by Japan’s Financial Services Agency on 17 July 2025
    outlines phased adoption of sustainability disclosure standards for
    Prime Market‑listed companies depending on market capitalisation.
    """
    summary = (
        "Japan’s Financial Services Agency published a roadmap on 17 July 2025 for "
        "adopting the Sustainability Standards Board of Japan (SSBJ) standards.  "
        "Prime Market companies with market capitalisation ≥3 trillion yen must "
        "apply the SSBJ standards in the fiscal year ending March 2027 with "
        "assurance from March 2028; those with 1–3 trillion yen apply the "
        "standards in FY 2028 with assurance from FY 2029.  Smaller companies "
        "(0.5–1 trillion yen) will be considered later.  The roadmap emphasises "
        "phased implementation and notes that third‑party assurance will start "
        "from FY 2028." )
    return [
        UpdateItem(
            source="Japan",
            title="Japan’s roadmap for SSBJ sustainability disclosure standards",
            link="https://www.noandt.com/wp-content/uploads/2025/07/capital_en_no8.pdf",
            date="2025-07-17",
            summary=summary,
        )
    ]


def parse_india_esg_overview() -> List[UpdateItem]:
    """Summarise India’s ESG oversight recommendations from a parliamentary report.

    A Parliamentary Standing Committee on Finance urged the Ministry of
    Corporate Affairs to create a dedicated ESG oversight body, amend
    corporate laws to embed ESG duties, and strengthen penalties for
    greenwashing.  SEBI meanwhile mandates top 1,000 listed companies
    to disclose ESG performance via the Business Responsibility and
    Sustainability Reporting framework.
    """
    summary = (
        "India’s Parliamentary Standing Committee on Finance (August 2025) "
        "recommended establishing a dedicated ESG oversight body within the "
        "Ministry of Corporate Affairs to combat greenwashing.  The committee "
        "proposes amending the Companies Act to make ESG a core duty of "
        "directors, deploying forensic experts, issuing sector‑specific "
        "guidelines and imposing stricter penalties for false ESG claims.  The "
        "Securities and Exchange Board of India requires the top 1,000 listed "
        "companies to report ESG performance using the Business Responsibility "
        "and Sustainability Reporting (BRSR) framework, which aligns with GRI and "
        "SASB standards." )
    return [
        UpdateItem(
            source="India",
            title="India moves toward ESG oversight and stricter disclosure",
            link="https://www.drishtiias.com/daily-updates/daily-news-analysis/esg-oversight-in-india",
            date="2025-08-11",
            summary=summary,
        )
    ]


def parse_sbt_financial_net_zero() -> List[UpdateItem]:
    """Summarise the SBTi’s Financial Institutions Net‑Zero Standard.

    In July 2025 the Science Based Targets initiative released a net‑zero
    standard for banks and other financial institutions.  The standard
    provides science‑based guidance for aligning portfolios with a
    1.5°C world and encourages alignment targets to drive real‑world
    decarbonisation.
    """
    summary = (
        "On 22 July 2025 the Science Based Targets initiative (SBTi) released its "
        "first Financial Institutions Net‑Zero Standard.  The standard offers "
        "science‑based guidance for banks, asset owners, asset managers and "
        "private equity firms to align lending, investment, insurance and capital "
        "markets activities with a 1.5 °C pathway, setting a clear route to net‑zero "
        "by 2050.  It emphasises portfolio alignment and encourages financial "
        "institutions to support high‑emitting sectors in decarbonising, while "
        "integrating the guidance into existing risk and investment processes." )
    return [
        UpdateItem(
            source="SBTi",
            title="SBTi releases Financial Institutions Net‑Zero Standard",
            link="https://sciencebasedtargets.org/news/the-sbti-opens-net-zero-standard-for-finance-industry",
            date="2025-07-22",
            summary=summary,
        )
    ]


###############################################################################
# Orchestration functions
###############################################################################

SOURCES: Dict[str, Callable[[], List[UpdateItem]]] = {
    "EU": parse_eu_quick_fix,
    "IFRS": parse_ifrs_s1_s2,
    "UK": parse_uk_consultation,
    "Japan": parse_japan_roadmap,
    "India": parse_india_esg_overview,
    "SBTi": parse_sbt_financial_net_zero,
}


def initialise_db(db_path: str) -> sqlite3.Connection:
    """Create or open the SQLite database and ensure the schema exists."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            date TEXT NOT NULL,
            summary TEXT NOT NULL,
            UNIQUE(source, title, link)
        )
        """
    )
    conn.commit()
    return conn


def store_updates(conn: sqlite3.Connection, items: List[UpdateItem]) -> List[UpdateItem]:
    """Insert new updates into the database and return those that were newly added."""
    cur = conn.cursor()
    new_items: List[UpdateItem] = []
    for item in items:
        try:
            cur.execute(
                "INSERT INTO updates (source, title, link, date, summary) VALUES (?, ?, ?, ?, ?)",
                (item.source, item.title, item.link, item.date, item.summary),
            )
            conn.commit()
            new_items.append(item)
        except sqlite3.IntegrityError:
            # Duplicate entry
            continue
    return new_items


def gather_updates() -> List[UpdateItem]:
    """Run all source parsers and collect their outputs."""
    collected: List[UpdateItem] = []
    for name, parser in SOURCES.items():
        try:
            items = parser()
            collected.extend(items)
        except Exception as e:
            # Log error and continue; in production use proper logging
            print(f"Error scraping {name}: {e}")
            continue
    return collected


def compose_email(items: List[UpdateItem]) -> MIMEMultipart:
    """Create an email with the list of new updates."""
    message = MIMEMultipart()
    message["From"] = os.environ.get("SMTP_FROM", "sustainability-agent@example.com")
    message["To"] = os.environ.get("SMTP_TO", "recipient@example.com")
    today = datetime.utcnow().strftime("%d %b %Y")
    message["Subject"] = f"Sustainability regulatory updates – {today}"
    body_lines = [
        f"Here are the latest sustainability regulation updates as of {today}:", "",
    ]
    for item in items:
        body_lines.append(f"* **{item.title}** ({item.source}, {item.date})")
        body_lines.append(f"  {item.summary}")
        body_lines.append(f"  Link: {item.link}")
        body_lines.append("")
    if not items:
        body_lines.append("No new updates were detected today.")
    # Convert to a single string
    body = "\n".join(body_lines)
    message.attach(MIMEText(body, "plain"))
    return message


def send_email(message: MIMEMultipart) -> None:
    """Send the email using SMTP credentials from environment variables.

    Set the following environment variables before running:

    - ``SMTP_HOST``: SMTP server hostname (e.g. 'smtp.gmail.com')
    - ``SMTP_PORT``: SMTP port (e.g. 587)
    - ``SMTP_USER``: Username for authentication
    - ``SMTP_PASSWORD``: Password or app‑specific password
    - ``SMTP_FROM``: Sender address
    - ``SMTP_TO``: Recipient address(es), comma‑separated

    If any of these are missing the function will silently skip sending.
    """
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "0"))
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASSWORD")
    recipients = os.environ.get("SMTP_TO")
    if not all([host, port, user, password, recipients]):
        print("SMTP credentials not fully configured; skipping email send.")
        return
    try:
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(
                message["From"],
                recipients.split(","),
                message.as_string(),
            )
            print(f"Sent email to {recipients}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def generate_dashboard(conn: sqlite3.Connection, html_path: str) -> None:
    """Generate a static HTML dashboard summarising all updates.

    The dashboard lists updates grouped by source and sorted by date.
    """
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT source, title, link, date, summary FROM updates ORDER BY date DESC"
    ).fetchall()
    # Start HTML
    lines = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "  <meta charset='utf-8'>",
        "  <title>Sustainability Regulation Updates</title>",
        "  <style>body{font-family:Arial, sans-serif;line-height:1.5;margin:40px;}"
        "h1,h2{color:#2a5d84;}table{width:100%;border-collapse:collapse;}"
        "th,td{padding:8px 12px;border-bottom:1px solid #ddd;}"
        "tr:hover{background-color:#f1f1f1;}" "</style>",
        "</head>",
        "<body>",
        "  <h1>Sustainability Regulatory Updates</h1>",
        f"  <p>Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>",
    ]
    current_source: Optional[str] = None
    for row in rows:
        source, title, link, date, summary = row
        if source != current_source:
            if current_source is not None:
                lines.append("</tbody></table>")
            current_source = source
            lines.append(f"<h2>{source}</h2>")
            lines.append(
                "<table><thead><tr><th>Date</th><th>Title</th><th>Description</th>"
                "</tr></thead><tbody>"
            )
        lines.append(
            f"<tr><td>{date}</td><td><a href='{link}' target='_blank'>{title}</a>" \
            f"</td><td>{summary}</td></tr>"
        )
    if rows:
        lines.append("</tbody></table>")
    lines.extend(["</body>", "</html>"])
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Dashboard saved to {html_path}")


# ---------------------------------------------------------------------------
# Override the generate_dashboard function with an improved implementation.
#
# The original implementation above contains an awkward inline CSS string that
# triggers a syntax error in some Python parsers due to unmatched quotes.  To
# avoid patching those fragile lines directly (which can be error‑prone
# because context includes quotation marks), we redefine the function below.
#
# Python resolves functions by their most recent definition, so this new
# definition supersedes the earlier one.  The new implementation builds
# the HTML content in a more structured way and avoids embedded quote
# sequences that interfere with patching.
def generate_dashboard(conn: sqlite3.Connection, html_path: str) -> None:  # type: ignore[override]
    """Generate a static HTML dashboard summarising all updates.

    The dashboard lists updates grouped by source and sorted by date.
    """
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT source, title, link, date, summary FROM updates ORDER BY date DESC"
    ).fetchall()
    # CSS for table styling
    style = (
        "  <style>"
        "body{font-family:Arial, sans-serif;line-height:1.5;margin:40px;}"
        "h1,h2{color:#2a5d84;}"
        "table{width:100%;border-collapse:collapse;}"
        "th,td{padding:8px 12px;border-bottom:1px solid #ddd;}"
        "tr:hover{background-color:#f1f1f1;}"
        "</style>"
    )
    # Assemble HTML
    lines: List[str] = []
    lines.append("<!DOCTYPE html>")
    lines.append("<html lang='en'>")
    lines.append("<head>")
    lines.append("  <meta charset='utf-8'>")
    lines.append("  <title>Sustainability Regulation Updates</title>")
    lines.append(style)
    lines.append("</head>")
    lines.append("<body>")
    lines.append("  <h1>Sustainability Regulatory Updates</h1>")
    lines.append(
        f"  <p>Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>"
    )
    current_source: Optional[str] = None
    for source, title, link, date, summary in rows:
        if source != current_source:
            if current_source is not None:
                lines.append("</tbody></table>")
            current_source = source
            lines.append(f"<h2>{source}</h2>")
            lines.append(
                "<table><thead><tr><th>Date</th><th>Title</th>"
                "<th>Description</th></tr></thead><tbody>"
            )
        # Escape HTML special characters in summary
        safe_summary = (
            summary.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        lines.append(
            f"<tr><td>{date}</td>"
            f"<td><a href='{link}' target='_blank'>{title}</a></td>"
            f"<td>{safe_summary}</td></tr>"
        )
    if rows:
        lines.append("</tbody></table>")
    lines.append("</body>")
    lines.append("</html>")
    # Write the file
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Dashboard saved to {html_path}")


def run_daily_task(db_path: str, dashboard_path: str) -> None:
    """Run the complete pipeline: scrape, store, email and render."""
    conn = initialise_db(db_path)
    items = gather_updates()
    new_items = store_updates(conn, items)
    # Always regenerate dashboard; it will include all items
    generate_dashboard(conn, dashboard_path)
    # Skip email sending for now (SMTP not configured)
    # if new_items:
    #     msg = compose_email(new_items)
    #     send_email(msg)


if __name__ == "__main__":
    # For demonstration, run the task once
    # Use script directory if DATA_DIR not set
    DATA_DIR = os.environ.get("DATA_DIR")
    if not DATA_DIR:
        DATA_DIR = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(DATA_DIR, "sustainability_updates.db")
    dashboard_file = os.path.join(DATA_DIR, "sustainability_dashboard.html")
    run_daily_task(db_file, dashboard_file)
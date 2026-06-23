#!/usr/bin/env python3
"""
Ajoute une entrée au suivi des prompts de Thibaut Arnol.

Usage :
  ./add_thibaut_entry.py --content "Message de Thibaut..." --channel email
  ./add_thibaut_entry.py --content "Suggestion sur le style CSS" --channel discord --date "2026-06-23 14:30"

Options :
  --content   Texte du prompt (obligatoire)
  --channel   Canal : email, discord, openwebui (défaut: email)
  --date      Date/heure (défaut: maintenant)
  --data      Chemin du fichier JSON (défaut: ~/contact/thibaut_entries.json)
  --html      Chemin du fichier HTML (défaut: ~/contact/thibaut_activity.html)

Retourne 0 si succès, le nombre d'entrées en stdout.
"""

import json, os, sys, argparse
from datetime import datetime

HOME = os.path.expanduser("~")
DEFAULT_DATA = os.path.join(HOME, "news_letter", "contact", "thibaut_entries.json")
DEFAULT_HTML = os.path.join(HOME, "news_letter", "contact", "thibaut_activity.html")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Suivi des prompts — Thibaut Arnol</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #0f1319;
  color: #e2e8f0;
  line-height: 1.7;
}
.container { max-width: 860px; margin: 0 auto; padding: 24px 20px; }
header {
  background: linear-gradient(135deg, #4c1d95, #1e40af);
  color: white; padding: 28px 24px;
  border-radius: 14px; margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}
header h1 { font-size: 1.6em; margin-bottom: 6px; }
header p { opacity: 0.85; font-size: 0.93em; }
.header-meta { margin-top: 12px; display: flex; gap: 12px; flex-wrap: wrap; font-size: 0.82em; }
.header-meta span { background: rgba(255,255,255,0.12); padding: 4px 14px; border-radius: 20px; backdrop-filter: blur(4px); }
.stats-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
.stat-chip { background: #151b23; border: 1px solid #212936; padding: 8px 16px; border-radius: 10px; font-size: 0.88em; }
.stat-chip strong { color: #818cf8; }
.stat-chip .num { color: #60a5fa; font-weight: 700; }
.timeline { position: relative; padding-left: 28px; }
.timeline::before { content: ''; position: absolute; left: 8px; top: 0; bottom: 0; width: 2px; background: #212936; }
.entry {
  background: #151b23; border: 1px solid #212936; border-radius: 12px; padding: 18px;
  margin-bottom: 14px; position: relative; transition: border-color 0.2s;
}
.entry:hover { border-color: #818cf8; }
.entry::before {
  content: ''; position: absolute; left: -24px; top: 22px;
  width: 12px; height: 12px; border-radius: 50%;
  background: #818cf8; border: 2px solid #0f1319;
}
.entry-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 6px; }
.entry-date { font-size: 0.82em; color: #94a3b8; }
.entry-channel { font-size: 0.75em; padding: 2px 10px; border-radius: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.channel-email { background: #1e3a5f; color: #60a5fa; }
.channel-discord { background: #312e81; color: #818cf8; }
.channel-openwebui { background: #1a4731; color: #34d399; }
.entry-content { color: #cbd5e1; font-size: 0.93em; white-space: pre-wrap; word-wrap: break-word; }
.entry-empty {
  background: #151b23; border: 1px dashed #212936; border-radius: 12px;
  padding: 32px; text-align: center; color: #64748b; font-size: 0.95em;
}
.entry-empty p { margin-top: 6px; font-size: 0.85em; }
footer { margin-top: 28px; padding-top: 14px; border-top: 1px solid #212936; font-size: 0.78em; color: #475569; text-align: center; }
</style>
</head>
<body>
<div class="container">

<header>
  <h1>📋 Suivi des prompts — Thibaut Arnol</h1>
  <p>Historique des interactions et suggestions</p>
  <div class="header-meta">
    <span>🔄 Mis à jour : {last_update}</span>
    <span>📬 Contact : thibaut.arnol@outlook.fr</span>
  </div>
</header>

<div class="stats-bar">
  <div class="stat-chip">
    <span class="num">{count}</span> prompt(s) reçu(s)
  </div>
  <div class="stat-chip">
    Dernière activité : <strong>{last_activity}</strong>
  </div>
</div>

<div class="timeline">
{entries_html}
</div>

<footer>
  Généré automatiquement — Hermes Agent &middot; <a href="https://github.com/ChrisDelapierre/newsletter_medicale" style="color:#475569;">newsletter_medicale</a>
</footer>

</div>
</body>
</html>
"""

ENTRY_TEMPLATE = """  <div class="entry">
    <div class="entry-header">
      <span class="entry-date">{date}</span>
      <span class="entry-channel channel-{channel}">{channel_label}</span>
    </div>
    <div class="entry-content">{content_html}</div>
  </div>"""

EMPTY_HTML = """  <div class="entry-empty">
    🕊️ Aucun prompt reçu pour le moment
    <p>Les messages de Thibaut apparaîtront ici au fur et à mesure.</p>
  </div>"""

CHANNEL_LABELS = {
    "email": "Email",
    "discord": "Discord",
    "openwebui": "Open WebUI",
}

def escape_html(text):
    """Échappe les caractères HTML dangereux."""
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;"))

def load_entries(data_path):
    if os.path.exists(data_path):
        with open(data_path, "r") as f:
            return json.load(f)
    return []

def save_entries(data_path, entries):
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    with open(data_path, "w") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

def build_entries_html(entries):
    if not entries:
        return EMPTY_HTML
    parts = []
    for e in reversed(entries):  # plus récent en premier
        channel = e.get("channel", "email")
        label = CHANNEL_LABELS.get(channel, channel.capitalize())
        content = escape_html(e.get("content", ""))
        parts.append(ENTRY_TEMPLATE.format(
            date=e.get("date", "—"),
            channel=channel,
            channel_label=label,
            content_html=content,
        ))
    return "\n".join(parts)

def regenerate_html(data_path, html_path, entries):
    last_update = datetime.now().strftime("%d/%m/%Y à %H:%M")
    count = len(entries)
    last_activity = entries[-1]["date"] if entries else "—"
    entries_html = build_entries_html(entries)

    html = (HTML_TEMPLATE
        .replace("{last_update}", last_update)
        .replace("{count}", str(count))
        .replace("{last_activity}", last_activity)
        .replace("{entries_html}", entries_html))
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, "w") as f:
        f.write(html)

def main():
    parser = argparse.ArgumentParser(description="Ajoute une entrée au suivi Thibaut Arnol")
    parser.add_argument("--content", required=True, help="Contenu du prompt")
    parser.add_argument("--channel", default="email", choices=["email", "discord", "openwebui"],
                        help="Canal de réception")
    parser.add_argument("--date", help="Date/heure (format libre, défaut: maintenant)")
    parser.add_argument("--data", default=DEFAULT_DATA, help="Fichier JSON des entrées")
    parser.add_argument("--html", default=DEFAULT_HTML, help="Fichier HTML généré")
    args = parser.parse_args()

    date_str = args.date if args.date else datetime.now().strftime("%d/%m/%Y à %H:%M")

    entries = load_entries(args.data)
    entries.append({
        "date": date_str,
        "channel": args.channel,
        "content": args.content,
    })
    save_entries(args.data, entries)
    regenerate_html(args.data, args.html, entries)

    print(f"✅ Entrée ajoutée — {len(entries)} au total")
    return 0

if __name__ == "__main__":
    sys.exit(main())

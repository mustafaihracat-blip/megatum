# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import os
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, time as dt_time
from serpapi import GoogleSearch

# ====================== KONFİGÜRASYON ======================
SERPAPI_API_KEY = "58f9fd35cd8c3c91a9fe025956fda5f5da021cdef728d25ba19d09fd94eacba7"

st.set_page_config(page_title="İhracat Fabrikası | Stratejik Panel", layout="wide")

# ====================== CSS ======================
st.markdown("""
<style>
.stApp { background:#0f1923; color:#e0e0e0; font-family:'Segoe UI',sans-serif; }
section[data-testid="stSidebar"] { background:#0a1016 !important; border-right:1px solid #1e3a5f; }
section[data-testid="stSidebar"] > div { padding-top:0 !important; }
div[data-testid="stDecoration"] { display:none; }
div[data-testid="stHeader"] { background:transparent; }
.sb-logo h2 { color:#f0b429; font-size:17px; font-weight:700; margin:0; }
.sb-logo p  { color:#7a9bb5; font-size:11px; margin:4px 0 0; }
.sb-footer  { color:#6a8dac; font-size:11px; margin-top:12px; padding-top:10px; border-top:1px solid #1e3a5f; }
.sb-footer p { color:#6a8dac !important; }
section[data-testid="stSidebar"] * { color-scheme: dark; }
section[data-testid="stSidebar"] p { color:#c0d8ec !important; }
section[data-testid="stSidebar"] span { color:#c0d8ec; }
section[data-testid="stSidebar"] div { color:#c0d8ec; }
.topbar { background:#0a1016; border-bottom:1px solid #1e3a5f; padding:16px 0 14px; margin-bottom:24px; display:flex; align-items:center; justify-content:space-between; }
.topbar h1 { font-size:17px; color:#fff; font-weight:600; margin:0; }
.badge { background:#1a3a5c; color:#7ec8e3; font-size:11px; padding:4px 12px; border-radius:20px; border:1px solid #2a5a8c; }
.stat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:18px; margin-bottom:24px; }
.stat-card { background:#0a1a2a; border:1px solid #1e3a5f; border-radius:12px; padding:20px 22px; position:relative; overflow:hidden; }
.stat-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.stat-card.red::before   { background:#e74c3c; }
.stat-card.blue::before  { background:#2980b9; }
.stat-card.green::before { background:#27ae60; }
.stat-card.gold::before  { background:#f0b429; }
.stat-card .lbl { font-size:11px; color:#7a9bb5; text-transform:uppercase; letter-spacing:.8px; }
.stat-card .val { font-size:26px; font-weight:700; margin:6px 0 3px; color:#fff; }
.stat-card .sub { font-size:11px; color:#4a8a6c; }
.stat-card .src { font-size:10px; color:#2a4a6c; margin-top:3px; }
.stat-card .ico { position:absolute; right:16px; top:50%; transform:translateY(-50%); font-size:30px; opacity:.12; }
.sec { font-size:12px; color:#7a9bb5; text-transform:uppercase; letter-spacing:.8px; margin-bottom:16px; display:flex; align-items:center; gap:8px; }
.sec::after { content:''; flex:1; height:1px; background:#1e3a5f; }
.tcard { background:#0a1a2a; border:1px solid #1e3a5f; border-radius:12px; padding:22px; margin-bottom:22px; }
.tcard h3 { font-size:13px; color:#aac8e0; margin-bottom:4px; font-weight:600; }
.tcard .src { font-size:10px; color:#2a5a8c; margin-bottom:14px; }
.styled-table { width:100%; border-collapse:collapse; }
.styled-table th { text-align:left; font-size:11px; color:#4a7a9c; text-transform:uppercase; letter-spacing:.5px; padding:9px 12px; border-bottom:1px solid #1e3a5f; }
.styled-table td { padding:10px 12px; font-size:12.5px; color:#c0d8ec; border-bottom:1px solid #111e2a; vertical-align:middle; }
.styled-table tr:hover td { background:#0d2035; }
.bp { display:inline-block; padding:2px 9px; border-radius:20px; font-size:11px; font-weight:600; }
.bp-red    { background:#2d0d0d; color:#e74c3c; border:1px solid #5a1a1a; }
.bp-blue   { background:#0d1e2d; color:#2980b9; border:1px solid #1a3a5c; }
.bp-green  { background:#0d2d1a; color:#27ae60; border:1px solid #1a5c2a; }
.bp-gold   { background:#2d1e00; color:#f0b429; border:1px solid #5c3a00; }
.bp-purple { background:#1a0d2d; color:#9b59b6; border:1px solid #3a1a5c; }
.bp-teal   { background:#0d2a2a; color:#1abc9c; border:1px solid #0d5a5a; }
.star { color:#f0b429; letter-spacing:-1px; font-size:13px; }
.irow { display:grid; grid-template-columns:1fr 1fr 1fr; gap:18px; margin-bottom:24px; }
.icard { background:#0a1a2a; border:1px solid #1e3a5f; border-radius:12px; padding:18px; }
.icard h3 { font-size:13px; color:#f0b429; margin-bottom:10px; font-weight:600; }
.ii { display:flex; gap:8px; margin-bottom:8px; align-items:flex-start; }
.dot  { width:7px; height:7px; border-radius:50%; background:#2980b9; margin-top:5px; flex-shrink:0; }
.dot-r{ width:7px; height:7px; border-radius:50%; background:#e74c3c; margin-top:5px; flex-shrink:0; }
.dot-g{ width:7px; height:7px; border-radius:50%; background:#27ae60; margin-top:5px; flex-shrink:0; }
.dot-y{ width:7px; height:7px; border-radius:50%; background:#f0b429; margin-top:5px; flex-shrink:0; }
.ii p { font-size:12px; color:#aac8e0; line-height:1.5; margin:0; }
.tc { background:#0a1a2a; border:1px solid #1e3a5f; border-radius:10px; padding:14px 18px; margin-bottom:10px; }
.tt { font-size:13px; color:#e0e0e0; font-weight:600; margin-bottom:7px; }
.tm { display:flex; gap:12px; flex-wrap:wrap; }
.tm span { font-size:11px; color:#7a9bb5; }
.tm span b { color:#aac8e0; }
.twocol { display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-bottom:24px; }
.lnk { color:#2980b9; text-decoration:none; font-size:12px; }
.lnk:hover { text-decoration:underline; }
.stButton>button { background:#f0b429 !important; color:#000 !important; font-weight:700; border:none; border-radius:4px; width:100%; height:44px; font-size:14px; }
.stButton>button:hover { background:#d4a020 !important; }
.login-box { background:#0a1a2a; border:1px solid #1e3a5f; border-radius:12px; padding:36px; }
.login-box input { background:#0f1923 !important; color:#e0e0e0 !important; border:1px solid #1e3a5f !important; border-radius:6px !important; }
label { color:#8ab0cc !important; font-size:13px !important; }
div[data-testid="stRadio"] > label { display:none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] { display:flex; flex-direction:column; gap:0px; padding:0; }
div[data-testid="stRadio"] div[role="radiogroup"] label { display:flex !important; align-items:center !important; padding:12px 16px !important; color:#c8ddf0 !important; font-size:13px !important; font-weight:500 !important; cursor:pointer !important; border-left:3px solid transparent !important; transition:all .2s !important; margin:0 !important; background:transparent !important; border-radius:0 !important; min-height:44px !important; width:100% !important; }
div[data-testid="stRadio"] div[role="radiogroup"] label:hover { color:#ffffff !important; background:#1a2d40 !important; border-left-color:#f0b429 !important; }
div[data-testid="stRadio"] div[role="radiogroup"] label[aria-checked="true"],
div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"],
div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) { color:#ffffff !important; background:#1a2d40 !important; border-left-color:#f0b429 !important; }
div[data-testid="stRadio"] span[data-testid="stMarkdownContainer"] p { color:inherit !important; font-size:13px !important; font-weight:inherit !important; margin:0 !important; }
div[data-testid="stRadio"] div[data-baseweb="radio"] { display:none !important; }
div[data-testid="stRadio"] input[type="radio"] { display:none !important; }
.block-container { padding-top:0.5rem !important; padding-left:2rem !important; padding-right:2rem !important; }
header[data-testid="stHeader"] { background:transparent !important; border:none !important; }
.stat-card .val { color:#ffffff !important; }
.stat-card .sub { color:#4ab88a !important; }
.stat-card .src { color:#4a6a8c !important; }
.stat-card .lbl { color:#7a9bb5 !important; }
</style>
""", unsafe_allow_html=True)

# ====================== LEADS ======================
LEADS = [
    {"n":"TCN (Transmission Company of Nigeria)","t":"Kamu","c":"Abuja","e":"info@tcn.org.ng","w":"tcn.org.ng","p":5},
    {"n":"Niger Delta Power Holding (NDPHC)","t":"Kamu","c":"Abuja","e":"info@ndphc.gov.ng","w":"ndphc.gov.ng","p":5},
    {"n":"Rural Electrification Agency (REA)","t":"Kamu","c":"Abuja","e":"info@rea.gov.ng","w":"rea.gov.ng","p":5},
    {"n":"Ikeja Electric (IE)","t":"DisCo","c":"Lagos","e":"info@ikejaelectric.com","w":"ikejaelectric.com","p":5},
    {"n":"Eko Electricity Distribution (EKEDC)","t":"DisCo","c":"Lagos","e":"customerservice@ekedp.com","w":"ekedp.com","p":5},
    {"n":"Ibadan Electricity Distribution (IBEDC)","t":"DisCo","c":"İbadan","e":"procurement@ibedc.com","w":"ibedc.com","p":5},
    {"n":"AEDC (Abuja Electricity)","t":"DisCo","c":"Abuja","e":"procurement@abujaelectricity.com","w":"abujaelectricity.com","p":5},
    {"n":"Elektrint Nigeria Ltd","t":"EPC","c":"Lagos","e":"info@elektrint.com","w":"elektrint.com","p":5},
    {"n":"ETCO Nigeria Ltd","t":"EPC","c":"Lagos","e":"etco_office@etco-nigeria.com","w":"etco-nigeria.com","p":5},
    {"n":"Fairtex Integrated Services","t":"EPC","c":"Port Harcourt","e":"info@fairtexgroups.com","w":"fairtex.com.ng","p":5},
    {"n":"BEDC (Benin Electricity)","t":"DisCo","c":"Benin City","e":"info@bedcpower.com","w":"bedcpower.com","p":4},
    {"n":"EEDC (Enugu Electricity)","t":"DisCo","c":"Enugu","e":"info@enugudisco.com","w":"enugudisco.com","p":4},
    {"n":"PHED (Port Harcourt Electricity)","t":"DisCo","c":"Port Harcourt","e":"info@phed.com.ng","w":"phed.com.ng","p":4},
    {"n":"KEDCO (Kano Electricity)","t":"DisCo","c":"Kano","e":"info@kedco.com.ng","w":"kedco.com.ng","p":4},
    {"n":"KAEDCO (Kaduna Electric)","t":"DisCo","c":"Kano","e":"procurement@kadunaelectric.com","w":"kadunaelectric.com","p":4},
    {"n":"Tranos Contracting Ltd","t":"EPC","c":"Lagos","e":"sales@tranos.ng","w":"tranos.ng","p":4},
    {"n":"Julius Berger Nigeria","t":"EPC","c":"Abuja","e":"info@julius-berger.com","w":"julius-berger.com","p":4},
    {"n":"AENS Projects & Engineering","t":"EPC","c":"Port Harcourt","e":"projects@aens-engineering.com","w":"aens-engineering.com","p":4},
    {"n":"GZ Industrial Supplies Nigeria","t":"Tedarikçi","c":"Lagos","e":"info@gz-ind.com","w":"gz-supplies.com","p":4},
    {"n":"Fembosco Limited","t":"Tedarikçi","c":"Lagos","e":"info@fembosco.com","w":"fembosco.com","p":4},
    {"n":"Dangote Group","t":"Sanayi","c":"Lagos","e":"info@dangote.com","w":"dangote.com","p":4},
    {"n":"NBET (Nigerian Bulk Electricity)","t":"Kamu","c":"Abuja","e":"info@nbet.gov.ng","w":"nbet.gov.ng","p":4},
    {"n":"JED (Jos Electricity)","t":"DisCo","c":"Jos","e":"info@jedplc.com","w":"jedplc.com","p":3},
    {"n":"YEDC (Yola Electricity)","t":"DisCo","c":"Yola","e":"info@yedc.com.ng","w":"yedc.com.ng","p":3},
    {"n":"Aba Power","t":"DisCo","c":"Aba","e":"info@abapower.com.ng","w":"abapower.com.ng","p":3},
    {"n":"Lambert Electromec","t":"EPC","c":"Lagos","e":"info@lambertelectromec.com","w":"lambertelectromec.com","p":3},
    {"n":"Shell Nigeria (SPDC)","t":"Sanayi","c":"Port Harcourt","e":"spdc@shell.com","w":"shell.com.ng","p":4},
    {"n":"Dangote Cement","t":"Sanayi","c":"Lagos","e":"info@dangote.com","w":"dangote.com","p":4},
    {"n":"BUA Group","t":"Sanayi","c":"Lagos","e":"info@buagroup.com","w":"buagroup.com","p":4},
    {"n":"Flour Mills of Nigeria","t":"Sanayi","c":"Lagos","e":"info@fmnplc.com","w":"fmnplc.com","p":4},
    {"n":"Lafarge Africa","t":"Sanayi","c":"Lagos","e":"info@lafarge.com.ng","w":"lafarge.com.ng","p":3},
    {"n":"Nestle Nigeria","t":"Sanayi","c":"Agbara","e":"info@ng.nestle.com","w":"nestle-cwa.com","p":3},
    {"n":"Nigerian Breweries","t":"Sanayi","c":"Lagos","e":"info@nbplc.com","w":"nbplc.com","p":2},
    {"n":"Guinness Nigeria","t":"Sanayi","c":"Ikeja","e":"info@guinness-nigeria.com","w":"guinness-nigeria.com","p":2},
    {"n":"Techno Oil","t":"Sanayi","c":"Lagos","e":"info@technooil.com","w":"technooil.com","p":3},
    {"n":"Mikano International","t":"EPC","c":"Lagos","e":"info@mikano-intl.com","w":"mikano-intl.com","p":3},
    {"n":"JMG Limited","t":"EPC","c":"Lagos","e":"sales@jmg-nigeria.com","w":"jmg-nigeria.com","p":3},
    {"n":"Mainstream Energy","t":"EPC","c":"Kainji","e":"info@mainstream.com.ng","w":"mainstream.com.ng","p":4},
    {"n":"Northsea Power","t":"EPC","c":"Lagos","e":"info@northseapower.com","w":"northseapower.com","p":3},
    {"n":"PowerGen Nigeria","t":"EPC","c":"Lagos","e":"info@powergen-renewable.com","w":"powergen-renewable.com","p":3},
    {"n":"Arnergi Limited","t":"EPC","c":"Lagos","e":"info@arnergi.com","w":"arnergi.com","p":3},
    {"n":"Oando Energy","t":"EPC","c":"Lagos","e":"info@oandoplc.com","w":"oandoplc.com","p":4},
    {"n":"Sahara Group","t":"EPC","c":"Lagos","e":"info@sahara-group.com","w":"sahara-group.com","p":4},
    {"n":"Genesis Energy","t":"EPC","c":"Lagos","e":"info@genesisenergygroup.net","w":"genesisenergygroup.net","p":3},
    {"n":"Aggreko Nigeria","t":"EPC","c":"Lagos","e":"info@aggreko.com","w":"aggreko.com","p":3},
    {"n":"Clarke Energy","t":"EPC","c":"Lagos","e":"nigeria@clarke-energy.com","w":"clarke-energy.com","p":3},
    {"n":"Cummins Nigeria","t":"EPC","c":"Lagos","e":"info@cummins.com","w":"nigeria.cummins.com","p":3},
    {"n":"Mantrac Nigeria","t":"EPC","c":"Ikeja","e":"info@mantracnigeria.com","w":"mantracnigeria.com","p":3},
    {"n":"Greenera Energy","t":"EPC","c":"Lagos","e":"info@greenera.com","w":"greenera.com","p":2},
    {"n":"Lekki Gardens","t":"Emlak","c":"Lagos","e":"info@lekkigardens.com","w":"lekkigardens.com","p":5},
    {"n":"Eko Atlantic City","t":"Emlak","c":"Lagos","e":"info@ekoatlantic.com","w":"ekoatlantic.com","p":5},
    {"n":"VGC Estate Mgmt","t":"Emlak","c":"Lagos","e":"info@vgc-mgmt.com","w":"vgc.ng","p":4},
    {"n":"Sujimoto Const.","t":"Emlak","c":"Lagos","e":"info@sujimotonig.com","w":"sujimotonig.com","p":4},
    {"n":"Megamound Inv.","t":"Emlak","c":"Lagos","e":"info@megamound.com","w":"megamound.com","p":3},
    {"n":"Primewaterview","t":"Emlak","c":"Lagos","e":"info@primewaterview.com","w":"primewaterview.com","p":3},
    {"n":"Landwey Inv.","t":"Emlak","c":"Lagos","e":"info@landwey.ng","w":"landwey.ng","p":3},
]

# ====================== FONKSİYONLAR ======================
def siteyi_tara(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        r = requests.get(url, headers=headers, timeout=15, verify=False)
        if r.encoding is None:
            r.encoding = 'utf-8'
        else:
            r.encoding = r.apparent_encoding or 'utf-8'
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            items = []
            for tag in soup.find_all(["h1","h2","h3","title","strong"]):
                t = tag.get_text().strip()
                if 3 < len(t) < 80:
                    if "hayatınıza enerji katıyoruz" not in t.lower():
                        items.append(t)
            return list(dict.fromkeys(items))[:14], "OK", url
        else:
            return [], f"Hata Kodu: {r.status_code}", url
    except Exception as e:
        return [], f"Bağlantı Hatası: {str(e)}", url

def serpapi_search_ng(query, num_results=15):
    try:
        params = {
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "engine": "google",
            "location": "Lagos,Nigeria",
            "gl": "ng",
            "hl": "en",
            "google_domain": "google.com.ng",
            "num": min(num_results, 20),
            "cr": "countryNG"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        formatted = []
        for item in organic_results:
            formatted.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
        return formatted, None
    except Exception as e:
        return [], str(e)

def stat_card(color, lbl, val, sub, src, ico):
    return f"""<div class="stat-card {color}">
  <div class="lbl">{lbl}</div>
  <div class="val">{val}</div>
  <div class="sub">{sub}</div>
  <div class="src">📌 {src}</div>
  <div class="ico">{ico}</div>
</div>"""

def tcard(title, src, body):
    return f"""<div class="tcard"><h3>{title}</h3><div class="src">📌 {src}</div>{body}</div>"""

# ============= DÜZELTİLMİŞ TABLO FONKSİYONU =============
def table_html(headers, rows):
    ths = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table class="styled-table"><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table>'

def bp(text, color):
    return f'<span class="bp bp-{color}">{text}</span>'

def stars(n):
    return f'<span class="star">{"★"*n}{"☆"*(5-n)}</span>'

def ii_item(dot_class, text):
    return f'<div class="ii"><div class="{dot_class}"></div><p>{text}</p></div>'

def get_trade_data():
    stat_cards = [
        {"color":"red",  "lbl":"HS 8504 Transformatör", "val":"$442M", "sub":"Nijerya yıllık ithalat hacmi", "src":"ITC Trade Map 2024", "ico":"⚡"},
        {"color":"blue", "lbl":"HS 8537 Pano/Panel",    "val":"$188M", "sub":"Endüstriyel kontrol üniteleri", "src":"UN Comtrade 2024", "ico":"🔲"},
        {"color":"green","lbl":"Türkiye İhracat Artışı", "val":"+34%",  "sub":"Elektrikli makine grubu (Yıllık)", "src":"TİM / ITC 2025", "ico":"📈"},
        {"color":"gold", "lbl":"Pazar Konumu",          "val":"2. Sırada","sub":"Güç trafolarında Çin sonrası", "src":"Statista / Volza 2025", "ico":"🇹🇷"}
    ]
    table_rows = [
        ["Monoblok Beton Köşk",          "8537.20",        "$195M (Hücre Dahil)", "%5 + KDV %7.5", "Hindistan, Çin (TBEA)"],
        ["Metal Muhafazalı Modüler Hücre","8537.10",        "$188M (HS8537)", "%5 + KDV %7.5", "Schneider, Siemens (Mısır)"],
        ["SF6 Gazlı Kesici",              "8535.30",        "$112M (Yüksek Ger.)", "%5 + KDV %7.5", "ABB, Lucy Electric"],
        ["Dağıtım Transformatörleri",     "8504.22",        "$442M (Toplam)",      "%10 + KDV %7.5", "Çin (Chint), Yerel Montaj"],
        ["Alçak Gerilim Panoları",        "8537.10",        "$188M (HS8537)", "%5 + KDV %7.5", "Yerel Atölyeler, Hindistan"],
    ]
    rakip_items = [
        {"dot":"dot-r", "text":"Çin: <b>%48 pay</b> — Baskın ancak kur dalgalanması vuruyor"},
        {"dot":"dot-r", "text":"Hindistan: <b>%15</b> — Fiyat odaklı en büyük rakip"},
        {"dot":"dot-y", "text":"Türkiye: <b>%14</b> — Kalite/Fiyat dengesiyle pazar kazanıyor"},
        {"dot":"dot-g", "text":"AfCFTA: Kıta içi üretim (Mısır/G.Afrika) vergi avantajı arıyor"}
    ]
    fiyat_items = [
        {"dot":"dot", "text":"Avrupa menşeli ürünlerin <b>%25-30 altında</b> konumlanma"},
        {"dot":"dot", "text":"Çin ürünlerine karşı <b>5 yıl garanti</b> kozu"},
        {"dot":"dot", "text":"Ödeme: %30 Nakit + %70 Teyitli Akreditif (LC)"},
        {"dot":"dot", "text":"Lokal para birimi (Naira) yerine <b>USD/Euro</b> bazlı teklif"}
    ]
    lojistik_items = [
        {"dot":"dot", "text":"Liman: <b>Lekki Deep Sea Port</b> (Apapa'dan daha hızlı)"},
        {"dot":"dot", "text":"Süre: İzmir/Ambarlı → Lagos: <b>~20-25 gün</b>"},
        {"dot":"dot", "text":"Zorunluluk: <b>SONCAP Sertifikası</b> (Ürün bazlı onay)"},
        {"dot":"dot", "text":"Risk: Liman içi bekleme süreleri için <b>demuraj</b> önlemi"}
    ]
    return stat_cards, table_rows, rakip_items, fiyat_items, lojistik_items

def get_projects_data():
    stat_cards = [
        {"color":"blue",  "lbl":"NETAP / DARES (World Bank)",  "val":"$750M", "sub":"17.5M kişiye enerji, 280k jeneratör değişimi", "src":"WB — Aktif", "ico":"🏗️"},
        {"color":"green", "lbl":"REA 500+ Proje (2026)",        "val":"N170B", "sub":"Mini-grid, grid extension, SHS", "src":"REA — 2026 Bütçesi", "ico":"☀️"},
        {"color":"red",   "lbl":"AKK Gaz Boru Hattı",           "val":"$2.8B", "sub":"614 km, ilk gaz Temmuz 2026", "src":"NNPC — Aktif", "ico":"🔌"},
        {"color":"gold",  "lbl":"MDP Veri Merkezi + Mini-Grid","val":"200MW", "sub":"72MW AI veri merkezi + entegre mini-grid", "src":"Özel — 2028", "ico":"🏦"}
    ]
    table_rows = [
        ["Amuwo 132/33kV GIS Rehabilitasyonu", "TCN", "—", "122 gün sürecek trafo merkezi yenileme, backup transformatörler", bp("Yüksek","red"), bp("Başladı (18.03.2026)","green")],
        ["Interconnected Mini-Grids (8 lokasyon)", "AfDB", "—", "3 DisCo bölgesinde 8 küme, 7 eyalet (Imo, Enugu, Anambra, Plateau, Bauchi, Kaduna, Kebbi)", bp("Yüksek","red"), bp("İhale Aşaması","gold")],
        ["AKK Doğalgaz Boru Hattı", "NNPC / Özel", "$2.8B", "614 km gaz hattı, Ajaokuta-Gwagwalada segmenti Temmuz 2026'da devrede", bp("Orta","blue"), bp("Temmuz 2026","gold")],
        ["MDP Veri Merkezi + Mini-Grid", "Özel (ABD)", "Milyar $", "200MW mini-grid + 72MW AI veri merkezi, free trade zone'da", bp("Orta","blue"), bp("2028","gold")],
        ["REA 500+ Elektrifikasyon Projesi", "REA", "N170B", "Mini-grid, grid extension, solar home systems, kamu binaları", bp("Yüksek","red"), bp("2026'da uygulama","green")],
        ["Nigeria Transmission Expansion Project (NTEP1)", "AfDB", "UA 121.5M", "İletim hattı genişletme (Kano, Delta, Kaduna, Edo, Anambra, Imo, Abia)", bp("Yüksek","red"), bp("Uygulamada","green")],
        ["DARES - Public Institutions ESIA", "World Bank", "NGN 229.7M", "Kamu kurumlarına solar-hibrit projeler için ÇED", bp("Orta","blue"), bp("Sözleşme imzalandı","green")],
        ["West Africa Power Pool (WAPP)", "World Bank", "—", "4,000+ km 225-330kV iletim hattı, Senegal-Nijerya bağlantısı", bp("Yüksek","red"), bp("18M+ kişiye fayda","green")],
        ["Nigeria Distributed Access (DARES)", "World Bank", "$750M", "17.5M kişiye enerji, 280.000 jeneratörün solar ile değişimi", bp("Yüksek","red"), bp("Aktif","green")],
        ["Niger Delta Power Holding (NDPHC) Projeleri", "NDPHC", "—", "Elektrik dağıtım altyapısı iyileştirmeleri", bp("Orta","blue"), bp("Devam ediyor","green")],
        ["North Core İletim Hattı", "WB + AfDB", "$570M", "913 km 330kV hat + 7 substation", bp("Yüksek","red"), bp("%38 tamam","gold")],
        ["CBN T-D Arayüz Rehab", "CBN", "$250M", "30+ substation, 34 kritik trafo", bp("Yüksek","red"), bp("Aktif","green")],
    ]
    tcard_src = "World Bank, AfDB, REA, TCN resmi açıklamaları, Leadership.ng, Arise News (Mart 2026)"
    return stat_cards, table_rows, tcard_src

# ====================== E-POSTA YARDIMCILARI ======================
CAMPAIGN_FILE = "data/campaigns.json"
LOG_FILE = "data/sent_log.csv"
os.makedirs("data", exist_ok=True)

def load_campaigns():
    if os.path.exists(CAMPAIGN_FILE):
        with open(CAMPAIGN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_campaigns(campaigns):
    with open(CAMPAIGN_FILE, "w", encoding="utf-8") as f:
        json.dump(campaigns, f, indent=2, ensure_ascii=False)

def load_log():
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE)
    else:
        return pd.DataFrame(columns=["campaign_id", "email", "timestamp", "status", "error"])

def append_log(campaign_id, email, status, error=""):
    df = load_log()
    new_row = pd.DataFrame([{
        "campaign_id": campaign_id,
        "email": email,
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "error": error
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)

def send_email_via_smtp(smtp_server, smtp_port, smtp_user, smtp_password, from_email, to_email, subject, body, is_html=False):
    try:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        if is_html:
            msg.attach(MIMEText(body, "html"))
        else:
            msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return True, ""
    except Exception as e:
        return False, str(e)

# ====================== SESSION STATE ======================
if "giris" not in st.session_state:
    st.session_state.giris = False

# ====================== GİRİŞ EKRANI ======================
if not st.session_state.giris:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style='text-align:center; margin-bottom:28px;'>
          <h1 style='color:#f0b429; font-size:28px; margin:0;'>İHRACAT FABRİKASI</h1>
          <p style='color:#7a9bb5; font-size:13px; margin-top:6px; letter-spacing:1px;'>STRATEJİK İSTİHBARAT SİSTEMİ</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        url_in  = st.text_input("🔍 Firma Web Sitesi", placeholder="https://megates.com.tr")
        pazar_in = st.selectbox("🌍 Hedef Pazar", ["Nijerya", "Gana", "Senegal", "Güney Afrika"])
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("SİSTEMİ BAŞLAT"):
            if url_in:
                with st.spinner("Ajanlar siteyi analiz ediyor..."):
                    veriler, durum, tam_url = siteyi_tara(url_in)
                temiz_veriler = [v for v in veriler if "hayatınıza enerji katıyoruz" not in v.lower()]
                st.session_state.veriler = temiz_veriler
                st.session_state.durum   = durum
                st.session_state.url     = tam_url
                st.session_state.pazar   = pazar_in
                st.session_state.giris   = True
                st.rerun()
            else:
                st.error("Lütfen bir web sitesi adresi girin.")
        st.markdown("</div>", unsafe_allow_html=True)

# ====================== ANA PANEL ======================
else:
    with st.sidebar:
        st.markdown("""
        <div class="sb-logo" style="padding:24px 16px 20px; border-bottom:1px solid #1e3a5f;">
          <h2>İHRACAT<br>FABRİKASI</h2>
          <p>Stratejik İstihbarat</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='padding:12px 0 4px;'>", unsafe_allow_html=True)
        menu = st.radio("Menü", [
            "📊  Genel Bakış",
            "📦  Ticaret Verileri",
            "🏗️  Aktif Projeler",
            "📋  İhale Takibi",
            "⚡  DisCo Rehberi",
            "🎯  Lead Listesi",
            "🏢  Firma Profili",
            "🔍  SerpApi Araması",
            "📱  WhatsApp Taslağı",
            "📧  E-Posta Gönderici",
        ], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="sb-footer">
          <p>🌐 {st.session_state.url[:28]}...</p>
          <p>📍 Pazar: {st.session_state.pazar}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("❌ Yeni Analiz"):
            st.session_state.giris = False
            st.rerun()

    # Üst bar başlıkları
    menu_labels = {
        "📊  Genel Bakış": "Genel Bakış — Nijerya Enerji Pazarı",
        "📦  Ticaret Verileri": "Ticaret Verileri & Gümrük Bilgisi",
        "🏗️  Aktif Projeler": "Aktif Projeler & Finansman Fırsatları",
        "📋  İhale Takibi": "İhale Takibi & Kaynak Sistemi",
        "⚡  DisCo Rehberi": "DisCo Rehberi — 12 Dağıtım Şirketi",
        "🎯  Lead Listesi": "Lead Listesi — Filtrelenebilir Alıcılar",
        "🏢  Firma Profili": "Firma Profili — Canlı Web Analizi",
        "🔍  SerpApi Araması": "Google Arama (SerpApi) — Nijerya Odaklı",
        "📱  WhatsApp Taslağı": "WhatsApp Gönderim Taslağı (Demo)",
        "📧  E-Posta Gönderici": "E-Posta Kampanyaları (SMTP)",
    }
    st.markdown(f"""
    <div class="topbar">
      <h1>{menu_labels.get(menu,'')}</h1>
      <span class="badge">{st.session_state.pazar} Pazarı</span>
    </div>
    """, unsafe_allow_html=True)

    # ====================== SAYFALAR ======================
    if menu == "📊  Genel Bakış":
        urun1 = st.session_state.veriler[0] if len(st.session_state.veriler) > 0 else "Ekipman"
        urun2 = st.session_state.veriler[1] if len(st.session_state.veriler) > 1 else "Endüstriyel Ürün"
        urun3 = st.session_state.veriler[2] if len(st.session_state.veriler) > 2 else "Enerji Çözümü"
        if "hayatınıza enerji katıyoruz" in urun1.lower(): urun1 = "Ekipman"
        if "hayatınıza enerji katıyoruz" in urun2.lower(): urun2 = "Endüstriyel Ürün"
        if "hayatınıza enerji katıyoruz" in urun3.lower(): urun3 = "Enerji Çözümü"

        st.markdown(f"""
        <div class="stat-grid">
          {stat_card("red",  f"{urun1} Analizi", "$391M", "Sektörel İthalat Hacmi", "Kaynak: UN Comtrade 2026", "📦")}
          {stat_card("blue", "Enerji Fonu", "$1.24B", "Aktif Yatırım Bütçesi", "Kaynak: World Bank 2026", "🏗️")}
          {stat_card("green", f"{urun2} Talebi", "Yüksek", "Pazar İhtiyaç Endeksi", "Kaynak: Saha Analizi 2026", "🔌")}
          {stat_card("gold", f"{urun3} Pazarı", "$162M", "Teknik Kontrol Grubu", "Kaynak: Ticaret Odası 2026", "🔲")}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="irow">
          <div class="icard">
            <h3>🌍 {st.session_state.pazar} Operasyonu</h3>
            {ii_item("dot", f"Sektörel Odak: <b>{urun1}</b>")}
            {ii_item("dot", f"Pazar Hedefi: <b>{st.session_state.pazar}</b>")}
            {ii_item("dot", f"Kaynak: <b>{st.session_state.url}</b>")}
            {ii_item("dot", "Analiz: <b>Canlı / Senkron</b>")}
          </div>
          <div class="icard">
            <h3>💡 Stratejik Fırsat</h3>
            {ii_item("dot-g", f"Türkiye <b>{urun1}</b> üretiminde avantajlı")}
            {ii_item("dot-g", "IEC ve ISO standartlarında tam uyum")}
            {ii_item("dot-g", "Maliyet-Kalite dengesinde bölge lideri")}
            {ii_item("dot-g", "Yerel bayi ağları taranıyor")}
          </div>
          <div class="icard">
            <h3>⚡ Mevzuat & Lojistik</h3>
            {ii_item("dot-r", f"<b>Gümrük:</b> {st.session_state.pazar} vergi rejimi")}
            {ii_item("dot-r", "<b>Sertifika:</b> SONCAP / GSA aktif")}
            {ii_item("dot-r", "<b>Lojistik:</b> Deniz yolu 25-30 gün")}
            {ii_item("dot-r", "<b>Ödeme:</b> Akreditif %100 güvence")}
          </div>
        </div>
        """, unsafe_allow_html=True)

    elif menu == "📦  Ticaret Verileri":
        stat_cards, table_rows, rakip_items, fiyat_items, lojistik_items = get_trade_data()
        stats_html = "".join(stat_card(c["color"], c["lbl"], c["val"], c["sub"], c["src"], c["ico"]) for c in stat_cards)
        st.markdown(f"""<div class="stat-grid">{stats_html}</div><div class="sec">İhracat Fabrikası — Ürün Bazlı Gümrük ve Piyasa Analizi</div>""", unsafe_allow_html=True)
        body = table_html(["Ürün Grubu","HS Kodu","Pazar Hacmi (2024)","Gümrük/Vergi","Stratejik Rakip"], table_rows)
        st.markdown(tcard("📊 Güncel Gümrük ve Hacim Tablosu","Nijerya Federal Gümrük (NCS) + ITC 2024/Q4 Verileri", body), unsafe_allow_html=True)

        rakip_html = "".join(ii_item(i['dot'], i['text']) for i in rakip_items)
        fiyat_html = "".join(ii_item(i['dot'], i['text']) for i in fiyat_items)
        lojistik_html = "".join(ii_item(i['dot'], i['text']) for i in lojistik_items)
        st.markdown(f"""
        <div class="irow">
          <div class="icard"><h3>📊 Rekip Analizi (2025)</h3>{rakip_html}</div>
          <div class="icard"><h3>💰 Fiyatlandırma Stratejisi</h3>{fiyat_html}</div>
          <div class="icard"><h3>🚢 Operasyonel Lojistik</h3>{lojistik_html}</div>
        </div>
        """, unsafe_allow_html=True)

        # FUAR BÖLÜMÜ
        st.markdown('<div class="sec">📅 Nijerya Enerji Sektörü Fuarları (2024-2030)</div>', unsafe_allow_html=True)
        fair_data = [
            {"name": "Nigeria Energy (formerly Power Nigeria)", "date": "27-29 Ekim 2026", "location": "Landmark Centre, Lagos", "focus": "Güç iletimi, dağıtım, yenilenebilir enerji, depolama", "key_products": "Trafo, AG/OG panolar, kesiciler, solar sistemler, bataryalar", "website": "https://www.nigeria-energy.com"},
            {"name": "Nigeria Energy", "date": "27-29 Ekim 2027", "location": "Landmark Centre, Lagos", "focus": "Güç iletimi, dağıtım, yenilenebilir enerji", "key_products": "Trafo, AG/OG panolar, kesiciler, solar", "website": "https://www.nigeria-energy.com"},
            {"name": "Nigeria Energy", "date": "25-27 Ekim 2028", "location": "Landmark Centre, Lagos", "focus": "Güç iletimi, dağıtım, yenilenebilir enerji", "key_products": "Trafo, AG/OG panolar, kesiciler, solar", "website": "https://www.nigeria-energy.com"},
            {"name": "Nigeria Energy", "date": "Ekim 2029 (tarih kesinleşmedi)", "location": "Landmark Centre, Lagos", "focus": "Güç iletimi, dağıtım, yenilenebilir enerji", "key_products": "Trafo, AG/OG panolar, kesiciler, solar", "website": "https://www.nigeria-energy.com"},
            {"name": "Nigeria Energy", "date": "Ekim 2030 (tarih kesinleşmedi)", "location": "Landmark Centre, Lagos", "focus": "Güç iletimi, dağıtım, yenilenebilir enerji", "key_products": "Trafo, AG/OG panolar, kesiciler, solar", "website": "https://www.nigeria-energy.com"},
            {"name": "Power & Water Nigeria", "date": "28-30 Nisan 2026", "location": "Lagos", "focus": "Enerji üretimi, su yönetimi, jeneratörler, UPS", "key_products": "Jeneratörler, UPS, solar paneller, trafo", "website": "https://www.powerandwaternigeria.com"},
        ]
        fair_rows = []
        for f in fair_data:
            fair_rows.append([f"<b>{f['name']}</b>", f['date'], f['location'], f['focus'][:60]+"..." if len(f['focus'])>60 else f['focus'], f['key_products'][:80]+"..." if len(f['key_products'])>80 else f['key_products'], f'<a href="{f["website"]}" target="_blank" class="lnk">Detaylar ↗</a>'])
        fair_body = table_html(["Fuar Adı", "Tarih", "Yer", "Kapsam / Odak", "İlgili Ürünler", "Web Sitesi"], fair_rows)
        st.markdown(tcard("🔌 Nijerya Elektrik & Enerji Fuarları", "Kaynak: Nigeria Energy, Power & Water Nigeria resmi duyuruları", fair_body), unsafe_allow_html=True)

        # Politika kartları
        st.markdown("""
        <div class="irow" style="margin-top: 20px;">
          <div class="icard"><h3>🎯 2030 Yenilenebilir Enerji Hedefi</h3>
            <div class="ii"><div class="dot-g"></div><p>Nijerya hükümeti, 2030 yılına kadar elektrik üretiminde <b>%30 yenilenebilir enerji</b> payı hedefliyor.</p></div>
            <div class="ii"><div class="dot-g"></div><p>Toplam yatırım ihtiyacı: <b>$122,2 milyar</b> (2024-2045).</p></div>
            <div class="ii"><div class="dot-g"></div><p>Hedeflenen kaynaklar: Güneş, hidroelektrik, biyokütle, rüzgar, nükleer.</p></div>
          </div>
          <div class="icard"><h3>🏗️ Altyapı & Yatırım Fırsatları</h3>
            <div class="ii"><div class="dot-r"></div><p>Mevcut kurulu güç: <b>4 GW</b> (2 milyar nüfus için yetersiz).</p></div>
            <div class="ii"><div class="dot-r"></div><p>Hedeflenen kurulu güç: <b>30 GW</b>.</p></div>
            <div class="ii"><div class="dot-y"></div><p>Elektrikli ekipmanlar (trafo, panel, kablo) büyük oranda ithalata bağımlı.</p></div>
            <div class="ii"><div class="dot-g"></div><p>AfDB, REA aracılığıyla <b>$200 milyon</b> yatırım planlıyor.</p></div>
          </div>
          <div class="icard"><h3>⚙️ Düzenleyici Gelişmeler</h3>
            <div class="ii"><div class="dot"></div><p>Elektrik Yasası 2023: Devletlerin kendi piyasalarını kurmasına izin veriyor.</p></div>
            <div class="ii"><div class="dot"></div><p>NEMSA + GIZ: Mini-grid şebeke entegrasyonu kılavuzları hazırlanıyor.</p></div>
            <div class="ii"><div class="dot"></div><p>NIEP (Ulusal Entegre Elektrik Politikası): 2024'te onaylandı.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    elif menu == "🏗️  Aktif Projeler":
        stat_cards, table_rows, tcard_src = get_projects_data()
        stats_html = "".join(stat_card(c["color"], c["lbl"], c["val"], c["sub"], c["src"], c["ico"]) for c in stat_cards)
        st.markdown(f"""<div class="stat-grid">{stats_html}</div><div class="sec">Proje Detayları</div>""", unsafe_allow_html=True)
        body = table_html(["Proje","Fon","Tutar","Kapsam","Megates İlgisi","Durum"], table_rows)
        st.markdown(tcard("🏗️ Finansmanlı Proje Listesi", tcard_src, body), unsafe_allow_html=True)

    elif menu == "📋  İhale Takibi":
        st.markdown('<div class="sec">Aktif İhale Takip Kaynakları</div>', unsafe_allow_html=True)
        body1 = table_html(
            ["Site","İçerik","Erişim"],
            [
                ['<a href="https://www.publicprocurement.ng" class="lnk" target="_blank">publicprocurement.ng ↗</a>',"Nijerya kamu ihaleleri","Ücretsiz"],
                ['<a href="https://www.nigeriatenders.com" class="lnk" target="_blank">nigeriatenders.com ↗</a>',"Özel + kamu tümü","Ücretsiz"],
                ['<a href="https://tcn.org.ng" class="lnk" target="_blank">tcn.org.ng ↗</a>',"TCN resmi ihaleleri","Ücretsiz"],
                ['<a href="https://nerc.gov.ng/media-category/tenders" class="lnk" target="_blank">nerc.gov.ng ↗</a>',"NERC düzenleyici","Ücretsiz"],
                ['<a href="https://www.tendersontime.com/nigeria-tenders/transformer-tenders/" class="lnk" target="_blank">tendersontime.com ↗</a>',"Nijerya transformer ihaleleri","Ücretli"],
                ['<a href="https://www.globaltenders.com/tenders-nigeria" class="lnk" target="_blank">globaltenders.com ↗</a>',"Enerji & elektrik","Ücretli"],
            ]
        )
        body2 = table_html(
            ["DisCo","Portal","Not"],
            [
                ["Ikeja Electric", '<a href="https://vms.ikejaelectric.com/accountCreation" class="lnk" target="_blank">VMS Portal ↗</a>', "DUNS no gerekli"],
                ["AEDC Abuja",     '<a href="https://abujaelectricity.com/supply-chain-management" class="lnk" target="_blank">SCM Portal ↗</a>', "3 aşamalı"],
                ["EKEDC (Eko)",    "customerservice@ekedp.com", "E-posta"],
                ["IBEDC (İbadan)", "procurement@ibedc.com",     "E-posta"],
                ["BEDC (Benin)",   "info@bedcpower.com",        "E-posta"],
                ["PHED (P.Harcourt)","info@phed.com.ng",        "E-posta"],
            ]
        )
        st.markdown(f"""
        <div class="twocol">
          {tcard("📡 İhale Takip Siteleri","Günlük e-posta uyarısı alınabilecek kaynaklar",body1)}
          {tcard("📪 DisCo Tedarikçi Portalları","Tedarikçi listesine kayıt için resmi kanallar",body2)}
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="sec">Güncel İhale Örnekleri (2024–2025)</div>', unsafe_allow_html=True)
        tenders = [
            ("TCN — Substation Ekipmanı ve Bakım Malzemeleri Tedariki", "Transmission Company of Nigeria","Substation ekipmanı, switchgear, bakım malzemeleri","publicprocurement.ng"),
            ("NEMSA — 2025 Sermaye Projeleri Yüklenici İhalesi", "Nigerian Electricity Management Services","Elektrik şebekesi test ekipmanı","nerc.gov.ng"),
            ("REA — Off-Grid Solar Mini-Grid Projeleri (Faz 3)", "Rural Electrification Agency","Mini-grid, trafo, dağıtım panoları","rea.gov.ng"),
            ("IBEDC — Trafo Temini ve Montajı", "Ibadan Electricity Distribution","Dağıtım trafosu (33kV/0.415kV)","ibedc.com"),
            ("AfDB — Nigeria Grid Expansion Project", "African Development Bank","132kV & 33kV substation ekipmanı","afdb.org"),
        ]
        for name, kurum, kapsam, kaynak in tenders:
            st.markdown(f"""
            <div class="tc">
              <div class="tt">{name}</div>
              <div class="tm"><span>🏛️ <b>Kurum:</b> {kurum}</span><span>🔧 <b>Kapsam:</b> {kapsam}</span><span>📌 <b>Kaynak:</b> {kaynak}</span></div>
            </div>
            """, unsafe_allow_html=True)

    elif menu == "⚡  DisCo Rehberi":
        st.markdown('<div class="sec">12 DisCo — Tam İletişim & Tedarikçi Bilgisi</div>', unsafe_allow_html=True)
        disco_rows = [
            ["<b>Ikeja Electric (IE)</b>",          "Lagos Kuzey",               "1.31M", "info@ikejaelectric.com",       '<a href="https://vms.ikejaelectric.com/accountCreation" class="lnk" target="_blank">VMS Portal ↗</a>'],
            ["<b>EKEDC (Eko)</b>",                  "Lagos Güney",               "752K",  "customerservice@ekedp.com",    '<a href="https://ekedp.com" class="lnk" target="_blank">ekedp.com ↗</a>'],
            ["<b>IBEDC (İbadan)</b>",               "Oyo, Ogun, Osun, Kwara",    "2.69M", "procurement@ibedc.com",        '<a href="https://ibedc.com" class="lnk" target="_blank">ibedc.com ↗</a>'],
            ["<b>AEDC (Abuja)</b>",                 "FCT, Niger, Kogi, Nasarawa","1.29M", "procurement@abujaelectricity.com",'<a href="https://abujaelectricity.com/supply-chain-management" class="lnk" target="_blank">SCM Portal ↗</a>'],
            ["<b>BEDC (Benin)</b>",                 "Edo, Delta, Ondo, Ekiti",   "1.46M", "info@bedcpower.com",           '<a href="https://bedcpower.com" class="lnk" target="_blank">bedcpower.com ↗</a>'],
            ["<b>EEDC (Enugu)</b>",                 "Abia, Anambra, Enugu, Ebonyi, Imo","1.39M","info@enugudisco.com",   '<a href="https://enugudisco.com" class="lnk" target="_blank">enugudisco.com ↗</a>'],
            ["<b>PHED (Port Harcourt)</b>",         "Rivers, Akwa Ibom, Bayelsa, Cross River","1.17M","info@phed.com.ng",'<a href="https://phed.com.ng" class="lnk" target="_blank">phed.com.ng ↗</a>'],
            ["<b>KEDCO (Kano)</b>",                 "Kano, Katsina, Jigawa",     "887K",  "info@kedco.com.ng",            '<a href="https://kedco.com.ng" class="lnk" target="_blank">kedco.com.ng ↗</a>'],
            ["<b>KAEDCO (Kaduna)</b>",              "Kaduna",                    "889K",  "procurement@kadunaelectric.com",'<a href="https://kadunaelectric.com" class="lnk" target="_blank">kadunaelectric.com ↗</a>'],
            ["<b>JED (Jos)</b>",                    "Plateau, Bauchi, Benue, Gombe","857K","info@jedplc.com",            '<a href="https://jedplc.com" class="lnk" target="_blank">jedplc.com ↗</a>'],
            ["<b>YEDC (Yola)</b>",                  "Adamawa, Taraba, Borno, Yobe","824K","info@yedc.com.ng",             '<a href="https://yedc.com.ng" class="lnk" target="_blank">yedc.com.ng ↗</a>'],
            ["<b>Aba Power</b>",                    "Aba, Abia State",           "—",     "info@abapower.com.ng",         '<a href="https://abapower.com.ng" class="lnk" target="_blank">abapower.com.ng ↗</a>'],
        ]
        body = table_html(["DisCo","Bölge","Müşteri","E-posta","Tedarikçi Portalı"], disco_rows)
        st.markdown(tcard("⚡ Nijerya Dağıtım Şirketleri","Kaynak: NERC Lisans Listesi (nerc.gov.ng), DisCo resmi web siteleri — Mart 2025", body), unsafe_allow_html=True)

    elif menu == "🎯  Lead Listesi":
        st.markdown('<div class="sec">Filtrelenebilir Lead Listesi</div>', unsafe_allow_html=True)
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            f_tip  = st.selectbox("Kurum Tipi", ["Tümü","DisCo","EPC","Kamu","Tedarikçi","Sanayi","Emlak"])
        with col_f2:
            f_sehir = st.selectbox("Şehir", ["Tümü","Lagos","Abuja","Port Harcourt","Kano","İbadan","Benin City","Enugu","Aba","Jos","Yola","Kaduna","Agbara","Kainji","Ikeja"])
        with col_f3:
            f_puan = st.selectbox("Min. Öncelik", ["Tümü (1+)","⭐⭐⭐⭐⭐ (5)","⭐⭐⭐⭐ (4+)","⭐⭐⭐ (3+)"])

        filtered = [l for l in LEADS]
        if f_tip != "Tümü":   filtered = [l for l in filtered if l["t"] == f_tip]
        if f_sehir != "Tümü": filtered = [l for l in filtered if l["c"] == f_sehir]
        if "5" in f_puan:     filtered = [l for l in filtered if l["p"] >= 5]
        elif "4+" in f_puan:  filtered = [l for l in filtered if l["p"] >= 4]
        elif "3+" in f_puan:  filtered = [l for l in filtered if l["p"] >= 3]

        tc_map = {"DisCo":"blue","EPC":"purple","Kamu":"red","Tedarikçi":"green","Sanayi":"gold","Emlak":"teal"}
        rows = []
        for l in filtered:
            rows.append([
                l["n"],
                bp(l["t"], tc_map.get(l["t"],"blue")),
                f"📍 {l['c']}",
                f'<a href="mailto:{l["e"]}" class="lnk">{l["e"]}</a>',
                f'<a href="https://{l["w"]}" class="lnk" target="_blank">{l["w"]} ↗</a>',
                stars(l["p"])
            ])
        count_txt = f"{len(filtered)} lead gösteriliyor"
        body = f'<p style="font-size:11px;color:#7a9bb5;margin-bottom:10px;">{count_txt}</p>' + table_html(["Firma / Kurum","Tip","Şehir","E-posta","Web","Öncelik"], rows)
        st.markdown(tcard("🎯 Stratejik Alıcı ve Ortak Listesi","Excel ve mevcut verilerin birleşimi — Mart 2025", body), unsafe_allow_html=True)

    elif menu == "🏢  Firma Profili":
        st.markdown('<div class="sec">Canlı Web Analizi</div>', unsafe_allow_html=True)
        if st.session_state.durum == "OK" and st.session_state.veriler:
            items_html = "".join(f'<div class="ii"><div class="dot"></div><p>{v}</p></div>' for v in st.session_state.veriler)
            body = f"""
            <p><b>🌐 Analiz Edilen Site:</b> <a href="{st.session_state.url}" class="lnk" target="_blank">{st.session_state.url} ↗</a></p>
            <br>{items_html}
            """
            st.markdown(tcard("🔍 Siteden Çekilen Canlı Ürün / Hizmet Verileri", "BeautifulSoup web kazıma — anlık veri", body), unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="tc"><div class="tt" style="color:#e74c3c;">⚠️ Veri Çekilemedi</div><div class="tm"><span>{st.session_state.durum}</span></div></div>
            """, unsafe_allow_html=True)

    elif menu == "🔍  SerpApi Araması":
        st.markdown('<div class="sec">SerpApi ile Nijerya Pazarı Araması</div>', unsafe_allow_html=True)
        query = st.text_input("🔎 Nijerya'da aramak istediğiniz kelime:", placeholder="Örn: 'Ikeja Electric tedarik' veya 'Nijerya enerji firmaları'")
        col1, col2 = st.columns([1,5])
        with col1:
            search_btn = st.button("🔍 Ara", type="primary")
        if search_btn and query:
            with st.spinner(f"SerpApi ile '{query}' aranıyor (Nijerya)..."):
                results, error = serpapi_search_ng(query, num_results=15)
            if error:
                st.error(f"Arama sırasında hata: {error}")
            elif results:
                st.success(f"✅ {len(results)} sonuç bulundu")
                table_rows = []
                for r in results:
                    snippet = r['snippet'][:200] + "..." if len(r['snippet']) > 200 else r['snippet']
                    table_rows.append([r['title'], f'<a href="{r["link"]}" target="_blank" class="lnk">{r["link"]}</a>', snippet])
                body = table_html(["Başlık", "Link", "Açıklama"], table_rows)
                st.markdown(tcard(f"🔍 '{query}' için Nijerya Arama Sonuçları", f"Kaynak: SerpApi | Lokasyon: Nijerya (Lagos)", body), unsafe_allow_html=True)
            else:
                st.warning("Sonuç bulunamadı. Farklı anahtar kelimeler deneyin.")
        elif search_btn and not query:
            st.warning("Lütfen bir arama kelimesi girin.")
        with st.expander("ℹ️ SerpApi Hakkında"):
            st.markdown("""
            - **SerpApi**, Google arama sonuçlarını API ile çekmenizi sağlar.
            - Ücretsiz planda **ayda 250 arama** yapabilirsiniz.
            - Bu sayfa **Nijerya lokasyonu** ile arama yapar (`location: Lagos,Nigeria`).
            - Sonuçlar yalnızca Nijerya’daki sitelerden gelir (hem `.ng` hem de `.com` uzantılılar dahil).
            """)

    elif menu == "📱  WhatsApp Taslağı":
        st.markdown('<div class="sec">📱 WhatsApp Toplu Mesaj Gönderim Taslağı (Demo)</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "📎 Telefon numaralarını içeren Excel/CSV dosyasını yükleyin",
            type=["csv", "xlsx"],
            help="Sütun başlığı 'telefon' olmalı (örn: +905551234567). Demo olduğu için gerçek gönderim yapılmaz."
        )

        message_template = st.text_area(
            "✏️ Mesaj metni (demo)",
            placeholder="Merhaba {isim}, ürünlerimizi inceleyin.\nDeğişken olarak {isim} kullanabilirsiniz.",
            height=150
        )

        send_button = st.button("🚀 Gönderim Simülasyonu Başlat", type="primary")

        with st.expander("ℹ️ Bu sayfa ne işe yarar?"):
            st.markdown("""
            - Bu sayfa, WhatsApp üzerinden toplu mesaj gönderme fikrini göstermek için **taslak** olarak hazırlanmıştır.
            - **Gerçek gönderim yapılmaz**; sadece arayüz ve akış simüle edilir.
            - Gerçek gönderim için Twilio, 360dialog gibi resmi WhatsApp Business API sağlayıcıları kullanılmalıdır.
            - Demo sırasında yüklenen dosya ve mesaj metni ile sahte bir ilerleme çubuğu gösterilir.
            """)

        if send_button and uploaded_file is not None and message_template:
            st.info("📱 Demo simülasyonu başlatılıyor... (gerçek gönderim yapılmıyor)")
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                df.columns = [c.lower() for c in df.columns]
                if 'telefon' not in df.columns:
                    st.error("❌ Dosyada 'telefon' sütunu bulunamadı!")
                else:
                    total = len(df)
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    for i in range(total):
                        time.sleep(0.2)
                        progress_bar.progress((i+1)/total)
                        status_text.info(f"📨 {i+1}/{total} numaraya mesaj hazırlanıyor... (demo)")
                    st.success(f"✅ Demo tamamlandı! {total} mesaj hazırlandı (gerçek gönderim yapılmadı).")
                    st.balloons()
            except Exception as e:
                st.error(f"Dosya okuma hatası: {e}")
        elif send_button and (uploaded_file is None or not message_template):
            st.warning("Lütfen dosya yükleyin ve mesaj metnini girin.")

    elif menu == "📧  E-Posta Gönderici":
        st.markdown('<div class="sec">📧 E-Posta Kampanyaları (SMTP)</div>', unsafe_allow_html=True)

        if "email_campaigns" not in st.session_state:
            st.session_state.email_campaigns = load_campaigns()
        if "email_sending" not in st.session_state:
            st.session_state.email_sending = False
        if "email_progress" not in st.session_state:
            st.session_state.email_progress = 0
        if "email_total" not in st.session_state:
            st.session_state.email_total = 0
        if "email_status" not in st.session_state:
            st.session_state.email_status = ""
        if "email_list_df" not in st.session_state:
            st.session_state.email_list_df = None

        with st.expander("➕ Kampanya Yönetimi", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                kampanya_adi = st.text_input("Kampanya Adı")
                konu = st.text_input("E-posta Konusu")
                mesaj = st.text_area("Mesaj (düz metin veya HTML)\nDeğişken: {isim}, {şirket} gibi")
            with col2:
                katalog_link = st.text_input("📁 Katalog Linki (isteğe bağlı)")
                video_link = st.text_input("🎥 Video Linki (isteğe bağlı)")
                günler = st.multiselect("Haftanın Günleri", ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"])
                saat = st.time_input("Gönderim Saati", value=dt_time(9,0), key="yeni_kampanya_saat")
                aktif = st.checkbox("Kampanya aktif", value=True)

            if st.button("Kampanya Ekle"):
                if kampanya_adi and konu and mesaj:
                    new_id = len(st.session_state.email_campaigns) + 1
                    new_campaign = {
                        "id": new_id,
                        "name": kampanya_adi,
                        "subject": konu,
                        "body": mesaj,
                        "catalog_link": katalog_link,
                        "video_link": video_link,
                        "schedule_days": günler,
                        "schedule_time": str(saat),
                        "enabled": aktif,
                        "sent_count": 0
                    }
                    st.session_state.email_campaigns.append(new_campaign)
                    save_campaigns(st.session_state.email_campaigns)
                    st.success("Kampanya eklendi.")
                    st.rerun()
                else:
                    st.warning("Kampanya adı, konu ve mesaj zorunludur.")

            if st.session_state.email_campaigns:
                st.markdown("#### Mevcut Kampanyalar")
                for i, camp in enumerate(st.session_state.email_campaigns):
                    col1, col2, col3, col4 = st.columns([3,1,1,1])
                    with col1:
                        st.write(f"**{camp['name']}** (ID: {camp['id']})")
                    with col2:
                        st.write(f"Aktif: {'✅' if camp['enabled'] else '❌'}")
                    with col3:
                        if st.button(f"Sil", key=f"del_{camp['id']}"):
                            st.session_state.email_campaigns.pop(i)
                            save_campaigns(st.session_state.email_campaigns)
                            st.rerun()
                    with col4:
                        if st.button(f"Düzenle", key=f"edit_{camp['id']}"):
                            st.info("Düzenleme henüz eklenmedi.")
                st.write("---")

        st.markdown("### 📎 E-posta Listesi Yükle")
        uploaded_email_file = st.file_uploader("Excel/CSV dosyası", type=["csv","xlsx"],
                                                 help="Sütunlarda 'email' zorunlu, diğer sütunlar değişken olarak kullanılabilir.")
        if uploaded_email_file:
            try:
                if uploaded_email_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_email_file)
                else:
                    df = pd.read_excel(uploaded_email_file)
                df.columns = [c.lower() for c in df.columns]
                if 'email' not in df.columns:
                    st.error("Dosyada 'email' sütunu yok!")
                else:
                    st.session_state.email_list_df = df
                    st.success(f"{len(df)} e-posta adresi yüklendi.")
                    st.dataframe(df.head(10))
            except Exception as e:
                st.error(f"Dosya okunamadı: {e}")

        st.markdown("### 🚀 Gönderim & Zamanlama")
        if not st.session_state.email_campaigns:
            st.info("Önce bir kampanya ekleyin.")
        elif st.session_state.email_list_df is None:
            st.info("Önce e-posta listesini yükleyin.")
        else:
            kampanya_sec = st.selectbox("Kampanya Seçin", options=[(c["id"], c["name"]) for c in st.session_state.email_campaigns if c["enabled"]],
                                        format_func=lambda x: x[1])
            if kampanya_sec:
                camp_id = kampanya_sec[0]
                camp = next(c for c in st.session_state.email_campaigns if c["id"] == camp_id)
                with st.expander("Zamanlama Ayarları"):
                    günler = st.multiselect("Haftanın Günleri", ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"],
                                             default=camp["schedule_days"], key=f"gunler_{camp_id}")
                    saat = st.time_input("Gönderim Saati", value=datetime.strptime(camp["schedule_time"], "%H:%M:%S").time() if camp["schedule_time"] else dt_time(9,0), key=f"saat_{camp_id}")
                    if st.button("Zamanlamayı Kaydet"):
                        camp["schedule_days"] = günler
                        camp["schedule_time"] = str(saat)
                        save_campaigns(st.session_state.email_campaigns)
                        st.success("Zamanlama kaydedildi.")

                col1, col2 = st.columns(2)
                with col1:
                    delay_min = st.number_input("E-posta arası bekleme (dakika)", min_value=1, value=5, step=1)
                with col2:
                    if st.button("📨 Şimdi Gönder", type="primary") and not st.session_state.email_sending:
                        with st.form("smtp_settings_form"):
                            smtp_server = st.text_input("SMTP Sunucusu", "mail.kursdegilikariyer.online")
                            smtp_port = st.number_input("Port", 587, 587)
                            smtp_user = st.text_input("Kullanıcı Adı", "bilgi@kursdegilikariyer.online")
                            smtp_password = st.text_input("Şifre", type="password", value="Mustafa12345")
                            from_email = st.text_input("Gönderen E-posta", "bilgi@kursdegilikariyer.online")
                            submitted = st.form_submit_button("Gönderimi Başlat")
                        if submitted:
                            if not all([smtp_server, smtp_user, smtp_password, from_email]):
                                st.error("SMTP ayarlarını eksiksiz doldurun!")
                            else:
                                smtp_settings = {
                                    "server": smtp_server,
                                    "port": smtp_port,
                                    "user": smtp_user,
                                    "password": smtp_password,
                                    "from_email": from_email
                                }
                                email_list = st.session_state.email_list_df.to_dict("records")
                                delay_seconds = delay_min * 60

                                st.session_state.email_sending = True
                                st.session_state.email_progress = 0
                                st.session_state.email_total = len(email_list)
                                st.session_state.email_status = "Gönderim başladı..."

                                def update_progress(current, status_text):
                                    st.session_state.email_progress = current
                                    st.session_state.email_status = status_text

                                def send_worker():
                                    total = len(email_list)
                                    for idx, row in enumerate(email_list):
                                        to_email = row.get("email")
                                        if not to_email:
                                            continue
                                        subject = camp["subject"]
                                        body = camp["body"]
                                        for k, v in row.items():
                                            if k != "email":
                                                subject = subject.replace(f"{{{k}}}", str(v))
                                                body = body.replace(f"{{{k}}}", str(v))
                                        if camp.get("catalog_link"):
                                            body += f"\n\n📁 Katalog: {camp['catalog_link']}"
                                        if camp.get("video_link"):
                                            body += f"\n🎥 Tanıtım videosu: {camp['video_link']}"

                                        success, err = send_email_via_smtp(
                                            smtp_settings["server"], smtp_settings["port"],
                                            smtp_settings["user"], smtp_settings["password"],
                                            smtp_settings["from_email"],
                                            to_email, subject, body, is_html=True
                                        )
                                        status = "success" if success else "fail"
                                        append_log(camp["id"], to_email, status, err if not success else "")
                                        update_progress(idx+1, f"{'✅' if success else '❌'} {to_email}")
                                        if idx < total - 1:
                                            time.sleep(delay_seconds)
                                    update_progress(total, "✅ Gönderim tamamlandı!")
                                    st.session_state.email_sending = False
                                    camp["sent_count"] += total
                                    save_campaigns(st.session_state.email_campaigns)

                                thread = threading.Thread(target=send_worker)
                                thread.daemon = True
                                thread.start()
                                st.rerun()
                    elif st.session_state.email_sending:
                        st.info("Gönderim devam ediyor...")

                if st.session_state.email_sending:
                    if st.session_state.email_total > 0:
                        st.progress(st.session_state.email_progress / st.session_state.email_total)
                    st.info(st.session_state.email_status)
                    if st.session_state.email_progress >= st.session_state.email_total:
                        st.session_state.email_sending = False
                        st.success("Gönderim tamamlandı!")
                        st.balloons()
                else:
                    st.write(f"Bu kampanya için toplam gönderim sayısı: {camp['sent_count']}")

        st.markdown("### 📊 Gönderim Raporu")
        log_df = load_log()
        if not log_df.empty:
            st.dataframe(log_df.tail(20))
            st.metric("Toplam Gönderim", len(log_df))
            success_count = len(log_df[log_df["status"] == "success"])
            fail_count = len(log_df[log_df["status"] == "fail"])
            st.metric("Başarılı", success_count)
            st.metric("Başarısız", fail_count)
            log_df["date"] = pd.to_datetime(log_df["timestamp"]).dt.date
            daily = log_df.groupby("date").size().reset_index(name="count")
            st.bar_chart(daily.set_index("date"))
        else:
            st.info("Henüz gönderim yapılmamış.")

    # Footer
    st.markdown("""
    <p style='text-align:center; color:#1e3a5f; font-size:11px; margin-top:48px;'>
      © 2026 İhracat Fabrikası | Stratejik Karar Destek Sistemi
    </p>
    """, unsafe_allow_html=True)
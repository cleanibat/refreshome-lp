#!/usr/bin/env python3
"""Capture une fois pour toutes le site WordPress d'origine (HTML brut, CSS, polices, images) dans source/.
Usage : python3 tools/scrape.py   (relançable : les fichiers déjà téléchargés sont gardés)"""
import os, re, json, hashlib, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'source')
BASE = 'https://refreshome.fr'
PAGES = ['/', '/confirmation/', '/mentions-legales/', '/politique-de-confidentialite/']
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'}
manifest = {}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r: return r.read()

def local_name(url):
    u = urllib.parse.urlparse(url)
    path = u.path
    if 'fonts.gstatic.com' in u.netloc: return 'fonts/' + os.path.basename(path)
    name = path.lstrip('/').replace('wp-content/', '').replace('wp-includes/', 'inc/')
    return name

def fetch(url):
    url = urllib.parse.urljoin(BASE + '/', url.replace('http://refreshome.fr', BASE)).split('#')[0]
    clean = url.split('?')[0] if 'fonts.googleapis' not in url else url
    if clean in manifest: return manifest[clean]
    if 'fonts.googleapis' in url:
        name = 'css/gfonts-' + hashlib.md5(url.encode()).hexdigest()[:8] + '.css'
    else:
        name = local_name(clean)
    dest = os.path.join(SRC, 'assets', name)
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try: data = get(url)
        except Exception as e: print('ERREUR', url, e); return None
        open(dest, 'wb').write(data)
    manifest[clean] = name
    if name.endswith('.css'):  # ressources référencées par le CSS
        css = open(dest, encoding='utf-8', errors='ignore').read()
        for m in set(re.findall(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', css)):
            if m.startswith('data:'): continue
            fetch(urllib.parse.urljoin(url, m))
    return name

os.makedirs(SRC, exist_ok=True)
for p in PAGES:
    html = get(BASE + p).decode('utf-8')
    slug = p.strip('/') or 'index'
    open(os.path.join(SRC, slug + '.html'), 'w').write(html)
    for m in re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*>', html):
        href = re.search(r'href=["\']([^"\']+)', m).group(1)
        fetch(href.replace('&#038;', '&').replace('&amp;', '&'))
    for m in set(re.findall(r'(https?://refreshome\.fr/wp-content/uploads/[^"\'\s,)]+?\.(?:jpg|jpeg|png|svg|webp|gif))', html)):
        fetch(m)
    for m in set(re.findall(r'url\(\s*["\']?(https?://refreshome\.fr/[^"\')]+)', html)):
        fetch(m)
    print(p, 'ok')
# CSS des avis Trustindex (chargé par leur script)
fetch(BASE + '/wp-content/uploads/trustindex-google-widget.css')
fetch('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&display=swap')
json.dump(manifest, open(os.path.join(SRC, 'manifest.json'), 'w'), indent=1)
print(len(manifest), 'ressources')

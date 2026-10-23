#!/usr/bin/env python3
"""Site statique refreshome.fr, reproduction à l'identique du WordPress/Elementor d'origine (capturé dans source/ par tools/scrape.py).

- HTML : balisage Elementor/Blocksy d'origine, nettoyé (plus de jQuery, WordPress, plugins, Tally).
- CSS : toutes les feuilles d'origine dans leur ordre, purgées (PurgeCSS) et minifiées en un seul fichier.
- JS : assets/site.js remplace les scripts d'origine (en-tête collant Blocksy, menu mobile, carrousels Swiper,
  animation slideInUp, accordéon FAQ, fonds différés Elementor, widget d'avis Trustindex chargé au défilement).
- Pages services ajoutées : services.py (mêmes blocs que l'accueil).
Usage : python3 build.py"""
import os, re, json, shutil, subprocess, urllib.parse, datetime, copy
from bs4 import BeautifulSoup, Comment
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'source')
A_SRC = os.path.join(SRC, 'assets')
OUT = ROOT
A_OUT = os.path.join(OUT, 'assets')
MANIFEST = json.load(open(os.path.join(SRC, 'manifest.json')))
DOMAIN = 'https://refreshome.fr'
GTM_ID = ''  # GTM-XXXXXXX : vide = snippet commenté
TODAY = datetime.date.today().isoformat()

used_assets = set()   # chemins relatifs à assets/ à copier/convertir


# ------------------------------------------------------------------ ressources
def asset_for(url):
    """URL d'origine -> chemin local relatif à assets/ (images converties en WebP)."""
    url = url.replace('&#038;', '&').replace('&amp;', '&').replace('http://refreshome.fr', DOMAIN)
    if url.startswith('/') and not url.startswith('//'): url = DOMAIN + url
    clean = url.split('?')[0].split('#')[0]
    name = MANIFEST.get(clean)
    if not name: return None
    used_assets.add(name)
    if re.search(r'\.(jpe?g|png)$', name, re.I) and 'favicon' not in name:
        return re.sub(r'\.(jpe?g|png)$', '.webp', name, flags=re.I)
    return name

BG_IMAGES = ('Hero-photo', 'Hero-background', 'Hero-bottom', 'Lights-blue')

def convert_assets():
    for name in sorted(used_assets):
        src = os.path.join(A_SRC, name)
        if not os.path.exists(src): continue
        if re.search(r'\.(jpe?g|png)$', name, re.I) and 'favicon' not in name:
            dst = os.path.join(A_OUT, re.sub(r'\.(jpe?g|png)$', '.webp', name, flags=re.I))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            im = Image.open(src)
            if im.mode in ('P', 'LA', 'RGBA') or 'transparency' in im.info:
                im = im.convert('RGBA'); im.save(dst, 'WEBP', quality=72 if im.width > 600 else 88, method=6, alpha_quality=60 if im.width > 600 else 90)
            else:
                im = im.convert('RGB')
                cap = 1920 if any(k in name for k in BG_IMAGES) else 960
                if im.width > cap: im = im.resize((cap, round(im.height * cap / im.width)), Image.LANCZOS)
                im.save(dst, 'WEBP', quality=74, method=6)
        else:
            dst = os.path.join(A_OUT, name)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)


# ------------------------------------------------------------------ CSS
def css_files_in_order(pages_html):
    """Feuilles de style + <style> du <head>, dans l'ordre d'apparition (accueil d'abord)."""
    seen, parts = set(), []
    for html in pages_html:
        head = html.split('</head>')[0]
        for m in re.finditer(r'<link[^>]+rel=["\']stylesheet["\'][^>]*>|<style[^>]*>.*?</style>', head, re.S):
            tag = m.group(0)
            if tag.startswith('<link'):
                href = re.search(r'href=["\']([^"\']+)', tag).group(1).replace('&#038;', '&')
                if 'Roboto' in href: continue          # police chargée mais jamais utilisée
                key = href.split('?')[0] if 'googleapis' not in href else href
                if key in seen: continue
                seen.add(key)
                parts.append(('file', href))
            else:
                body = re.sub(r'^<style[^>]*>|</style>$', '', tag, flags=re.S)
                if 'e-lazyloaded' in body and ('inline', body) in parts: continue
                if body.strip() and ('inline', body) not in parts: parts.append(('inline', body))
    return parts

def rewrite_css_urls(css, css_url):
    def rep(m):
        u = m.group(1).strip('\'"')
        if u.startswith('data:') or u.startswith('#'): return m.group(0)
        full = urllib.parse.urljoin(css_url, u)
        loc = asset_for(full)
        return f'url({loc})' if loc else m.group(0)
    return re.sub(r'url\(\s*([^)]+?)\s*\)', rep, css)

SKIP_CSS = ('no-scripts.min.css', 'fluent-forms', 'fontawesome')

def mingcute_subset():
    """Police d'icônes MingCute (435 Ko) réduite aux icônes réellement utilisées dans les pages générées."""
    from fontTools import subset
    src_css = open(os.path.join(A_SRC, 'uploads/elementor/custom-icons/mingcute/css/mingcute.css')).read()
    used = set()
    for root, _, files in os.walk(OUT):
        if '/source' in root or '/assets' in root or '/.git' in root or '/tools' in root: continue
        for f in files:
            if f == 'index.html': used |= set(re.findall(r'icon-mingcute[A-Za-z0-9_-]+', open(os.path.join(root, f)).read()))
    rules, cps = [], []
    for cls in sorted(used):
        m = re.search(r'\.' + re.escape(cls) + r':before\s*\{\s*content:\s*\'\\([0-9a-f]+)\';', src_css)
        if m: rules.append(f".{cls}:before{{content:'\\{m.group(1)}'}}"); cps.append(int(m.group(1), 16))
    os.makedirs(os.path.join(A_OUT, 'fonts'), exist_ok=True)
    opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = []
    font = subset.load_font(os.path.join(A_SRC, 'uploads/elementor/custom-icons/mingcute/font/mingcute.ttf'), opts)
    s = subset.Subsetter(opts); s.populate(unicodes=cps); s.subset(font)
    subset.save_font(font, os.path.join(A_OUT, 'fonts/mingcute-subset.woff2'), opts)
    base = re.search(r'\[class\^="icon-mingcute"\]:before.*?\}', src_css, re.S).group(0)
    return ("@font-face{font-family:'mingcute';src:url(fonts/mingcute-subset.woff2) format('woff2');font-weight:normal;font-style:normal;font-display:block}\n"
            + base + '\n' + '\n'.join(rules))

def build_css(pages_html, extra_css):
    out = []
    for kind, val in css_files_in_order(pages_html):
        if kind == 'file':
            url = val.replace('http://refreshome.fr', DOMAIN)
            if url.startswith('/'): url = DOMAIN + url
            name = MANIFEST.get(url if 'googleapis' in url else url.split('?')[0])
            if not name: print('CSS manquant', url); continue
            if any(x in name for x in SKIP_CSS): continue
            if 'mingcute.css' in name:
                out.append(mingcute_subset()); continue
            css = open(os.path.join(A_SRC, name), encoding='utf-8', errors='ignore').read()
            out.append(f'/* {name} */\n' + rewrite_css_urls(css, url))
        else:
            out.append(rewrite_css_urls(val, DOMAIN + '/'))
    out.append(extra_css)
    css = '\n'.join(out)
    css = css.replace('background-color: transparent; /\n', 'background-color: transparent;\n')
    css = css.replace('font-display:block', 'font-display:swap').replace('font-display: block', 'font-display: swap')
    open(os.path.join(ROOT, 'tools', 'full.css'), 'w').write(css)
    open(os.path.join(A_OUT, 'site.css'), 'w').write(css)
    return css

def purge_css():
    t = os.path.join(ROOT, 'tools')
    r = subprocess.run('mkdir -p tools/purged && npx -y purgecss@6 --config tools/purgecss.config.cjs --output tools/purged/', shell=True, cwd=ROOT, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit('purgecss a échoué')
    r = subprocess.run('npx -y lightningcss-cli@1 --minify tools/purged/site.css -o assets/site.css', shell=True, cwd=ROOT, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit('lightningcss a échoué')
    print('CSS', os.path.getsize(os.path.join(A_OUT, 'site.css')) // 1024, 'Ko')


# ------------------------------------------------------------------ HTML
SAFE_SCRIPT_TYPES = ('application/ld+json',)

def rel(path_from, target):
    """Lien relatif depuis une page (ex. 'nettoyage-toiture/') vers un chemin du site ('', 'confirmation/', 'assets/x')."""
    return '../' * path_from.count('/') + target

def fix_url(u, path):
    if not u: return u
    if u.startswith(('mailto:', 'tel:', 'javascript:', 'data:')): return u
    if u.startswith('#'): return u
    m = re.match(r'^(?:https?://refreshome\.fr)?(/[^#?]*)?(\?[^#]*)?(#.*)?$', u)
    if not m or (u.startswith('http') and 'refreshome.fr' not in u): return u
    p, q, h = m.group(1) or '/', m.group(2) or '', m.group(3) or ''
    if p.startswith('/wp-content/'):
        loc = asset_for(DOMAIN + p)
        return rel(path, 'assets/' + loc) if loc else u
    target = p.lstrip('/')
    if target and not target.endswith('/') and '.' not in target.split('/')[-1]: target += '/'
    r = rel(path, target) or './'
    if r == './' and h and path == '': return h   # ancre sur la page courante
    return r + q + h

def clean_page(html, path, form_html, title=None, desc=None, robots='index, follow'):
    soup = BeautifulSoup(html, 'lxml')
    # --- scripts / commentaires / liens inutiles
    for s in soup.find_all('script'):
        if s.get('type') not in SAFE_SCRIPT_TYPES: s.decompose()
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)): c.extract()
    for l in soup.body.find_all('link'): l.decompose()
    for st in soup.head.find_all(['style', 'link', 'meta', 'noscript', 'script']): st.decompose()
    for n in soup.body.find_all('noscript'): n.decompose()
    # --- formulaire Tally -> formulaire HTML
    tally = soup.select_one('#contact .elementor-widget-container')
    if tally:
        tally.clear(); tally.append(BeautifulSoup(form_html.replace('ROOT/', rel(path, '')), 'lxml').body.contents[0])
    # --- avis Trustindex : CSS locale
    for d in soup.select('[data-css-url]'):
        d['data-css-url'] = rel(path, 'assets/trustindex-google-widget.css')
    # --- icônes Font Awesome de l'accordéon -> SVG (Font Awesome n'est plus chargé)
    PLUS = '<svg viewBox="0 0 448 512" aria-hidden="true"><path fill="currentColor" d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"/></svg>'
    MINUS = '<svg viewBox="0 0 448 512" aria-hidden="true"><path fill="currentColor" d="M432 256c0 17.7-14.3 32-32 32L48 288c-17.7 0-32-14.3-32-32s14.3-32 32-32l352 0c17.7 0 32 14.3 32 32z"/></svg>'
    for i in soup.select('i.fa-plus'): i.replace_with(BeautifulSoup(PLUS, 'html.parser'))
    for i in soup.select('i.fa-minus'): i.replace_with(BeautifulSoup(MINUS, 'html.parser'))
    for a in soup.select('a.uc_trigger[href^="javascript"]'): a['href'] = '#'
    # --- états posés par le JS Blocksy/Elementor au chargement
    CUR = {'current-menu-item', 'current_page_item', 'current-menu-ancestor', 'current-menu-parent'}
    for li in soup.select('li.menu-item'):
        li['class'] = [c for c in li['class'] if c not in CUR]
    for a in soup.select('a[aria-current]'): del a['aria-current']
    for n in soup.select('nav[data-responsive]'): n['data-responsive'] = 'yes'
    # --- URLs
    for tag in soup.find_all(True):
        if tag.name == 'img' and tag.has_attr('srcset') and 'wp-content/uploads' in tag.get('src', ''):
            src0 = tag['src']
            if re.search(r'-\d+x\d+\.(jpe?g|png)$', src0):  # vignette WordPress -> image d'origine
                src0 = re.sub(r'-\d+x\d+(\.(jpe?g|png))$', r'\1', src0)
            tag['src'] = fix_url(src0, path); del tag['srcset']; tag.attrs.pop('sizes', None)
        for attr in ('href', 'src', 'data-src', 'poster'):
            if tag.has_attr(attr) and isinstance(tag[attr], str):
                if attr == 'data-src' and 'trustindex' in tag[attr]: continue
                tag[attr] = fix_url(tag[attr], path)
        if tag.has_attr('srcset'):
            parts = []
            for p in tag['srcset'].split(','):
                p = p.strip().split()
                if not p: continue
                parts.append(' '.join([fix_url(p[0], path)] + p[1:]))
            tag['srcset'] = ', '.join(parts)
        if tag.has_attr('style') and 'url(' in tag['style']:
            tag['style'] = re.sub(r'url\(([^)]+)\)', lambda m: f"url({fix_url(m.group(1).strip(chr(39)+chr(34)), path)})", tag['style'])
        if tag.name == 'img' and tag.get('src', '').endswith('.webp'):
            # dimensions explicites pour éviter les décalages
            pass
    # --- <head> neuf
    head = soup.head
    t = soup.title.string if soup.title else 'Refreshome'
    head.clear()
    canon = DOMAIN + '/' + path
    root = rel(path, '')
    gtm = (f"<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>"
           if GTM_ID else '<!-- GTM : renseigner GTM_ID dans build.py -->')
    hero_pre = ''
    if path == '' or path in SERVICE_PATHS:
        hero_pre = f'<link rel="preload" as="image" href="{root}assets/uploads/2025/05/Hero-photo-min.webp" fetchpriority="high">'
    head_html = f'''<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title or t}</title>
<meta name="description" content="{desc or ''}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="Refreshome">
<meta property="og:title" content="{title or t}"><meta property="og:description" content="{desc or ''}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMAIN}/assets/uploads/2025/05/Hero-photo-min.webp">
<link rel="icon" href="{root}assets/uploads/2025/06/favicon-refreshome-150x150.png" sizes="32x32"><link rel="apple-touch-icon" href="{root}assets/uploads/2025/06/favicon-refreshome.png">
<link rel="preload" href="{root}assets/fonts/iJWKBXyIfDnIV7nBrXyw023e.woff2" as="font" type="font/woff2" crossorigin>
{hero_pre}
<link rel="stylesheet" href="{root}assets/site.css?v={VERSION}">
{gtm}'''
    head.append(BeautifulSoup(head_html, 'html.parser'))
    if GTM_ID:
        soup.body.insert(0, BeautifulSoup(f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>', 'html.parser'))
    soup.body.append(BeautifulSoup(f'<script>{INLINE_JS}</script><script src="{root}assets/site.js?v={VERSION}" defer></script><script src="{root}assets/swiper.min.js" defer></script>', 'html.parser'))
    if soup.html.has_attr('class'): del soup.html['class']
    soup.html['lang'] = 'fr-FR'
    return soup

SERVICE_PATHS = set()
# Animations d'entrée Elementor : lancées dès que le HTML est lu, comme le faisait Elementor (sans attendre les autres scripts)
INLINE_JS = ("!function(){var a=document.querySelectorAll('.elementor-invisible[data-settings]');if(!a.length)return;"
  "var go=function(e){var s={};try{s=JSON.parse(e.getAttribute('data-settings'))}catch(x){}var n=s._animation||s.animation;"
  "if(!n){e.classList.remove('elementor-invisible');return}setTimeout(function(){e.classList.remove('elementor-invisible');e.classList.add('animated',n)},parseInt(s._animation_delay||s.animation_delay||0,10))};"
  "if(!('IntersectionObserver'in window)){a.forEach(go);return}var o=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){o.unobserve(x.target);go(x.target)}})});"
  "a.forEach(function(e){e.setAttribute('data-anim','1');o.observe(e)})}();")
VERSION = datetime.datetime.now().strftime('%Y%m%d%H%M')

def write(soup, path):
    out = os.path.join(OUT, path, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    html = '<!DOCTYPE html>\n' + str(soup)
    html = re.sub(r'\n\s*\n+', '\n', html)
    open(out, 'w').write(html)


# ------------------------------------------------------------------ main
if __name__ == '__main__':
    from services import build_services, nav_patch, FORM_HTML, FORM_CSS, PAGE_META
    pages = {'': 'index', 'confirmation/': 'confirmation', 'mentions-legales/': 'mentions-legales',
             'politique-de-confidentialite/': 'politique-de-confidentialite'}
    for d in ('uploads', 'themes', 'plugins', 'assets'):
        shutil.rmtree(os.path.join(A_OUT, d), ignore_errors=True)
    raw = {p: open(os.path.join(SRC, f + '.html')).read() for p, f in pages.items()}
    SERVICE_PATHS.update(build_services.paths())
    soups = {}
    for p, html in raw.items():
        meta = PAGE_META.get(p, {})
        soups[p] = clean_page(html, p, FORM_HTML, **meta)
    # pages services : dérivées de l'accueil
    for p, soup in build_services(raw[''], clean_page, FORM_HTML).items():
        soups[p] = soup
    for p, soup in soups.items():
        nav_patch(soup, p, rel)
        write(soup, p)
    # assets
    css = build_css(list(raw.values()), FORM_CSS)
    purge_css()
    convert_assets()
    shutil.copy2(os.path.join(A_SRC, 'uploads/trustindex-google-widget.css'), os.path.join(A_OUT, 'trustindex-google-widget.css'))
    urls = [DOMAIN + '/'] + [DOMAIN + '/' + p for p in sorted(SERVICE_PATHS)]
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + ''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls) + '</urlset>\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
    print(len(soups), 'pages')

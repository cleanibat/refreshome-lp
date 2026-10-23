# -*- coding: utf-8 -*-
"""Formulaire (remplace Tally, même rendu), métadonnées SEO, pages services ajoutées (mêmes blocs que l'accueil)."""

# Ordre des choix = ordre du formulaire Tally d'origine, puis prestations ajoutées
CHOICES = ['Toiture', 'Façade', 'Terrasse', 'Panneau solaire', 'Gouttières', 'Traitement de charpente',
           'Faîtière', 'Cache-moineaux', 'Peinture de façade', 'Peinture isolante', 'Nettoyage professionnel']
DELAIS = ['Dès que possible', '1 à 2 mois', '2 à 6 mois', '+ 6 mois']

def form_html(checked=()):
    keys = 'ABCDEFGHIJKLMNOP'
    opts = ''.join(
        f'<label class="rh-opt"><input type="checkbox" name="Besoin[]" value="{c}"{" checked" if c in checked else ""}>'
        f'<span class="rh-key">{keys[i]}</span><span>{c}</span></label>' for i, c in enumerate(CHOICES))
    delais = ''.join(f'<option>{d}</option>' for d in DELAIS)
    return f'''<form id="devisForm" class="rh-form" method="POST" action="ROOT/contact.php" enctype="multipart/form-data">
<input type="hidden" name="Source" value="SOURCE">
<div class="rh-hp" aria-hidden="true"><label>Ne pas remplir<input name="_honey" tabindex="-1" autocomplete="off"></label></div>
<fieldset class="rh-field"><legend class="rh-label">Quelles prestations souhaitez-vous ?<span class="rh-req" aria-hidden="true">*</span></legend><div class="rh-opts">{opts}</div></fieldset>
<div class="rh-field"><label class="rh-label" for="rh-nom">Nom complet<span class="rh-req" aria-hidden="true">*</span></label><input class="rh-input" id="rh-nom" name="Nom" required autocomplete="name"></div>
<div class="rh-field"><label class="rh-label" for="rh-email">E-mail<span class="rh-req" aria-hidden="true">*</span></label><input class="rh-input" id="rh-email" name="Email" type="email" required autocomplete="email"></div>
<div class="rh-row">
<div class="rh-field"><label class="rh-label" for="rh-tel">Numéro de téléphone<span class="rh-req" aria-hidden="true">*</span></label><input class="rh-input" id="rh-tel" name="Téléphone" type="tel" required autocomplete="tel"></div>
<div class="rh-field rh-cp"><label class="rh-label" for="rh-cp">Code postal<span class="rh-req" aria-hidden="true">*</span></label><input class="rh-input" id="rh-cp" name="Code postal" required inputmode="numeric" autocomplete="postal-code"></div>
</div>
<div class="rh-field"><label class="rh-label" for="rh-delai">Délai souhaité<span class="rh-req" aria-hidden="true">*</span></label><select class="rh-input rh-select" id="rh-delai" name="Délai" required><option value="" disabled selected hidden></option>{delais}</select></div>
<div class="rh-field"><label class="rh-file" for="rh-photos">Ajouter des photos : bâtiment - moyen d'accès (non obligatoire)</label><input class="rh-input rh-fileinput" id="rh-photos" type="file" name="photos[]" accept="image/*" multiple></div>
<div class="rh-submit"><button type="submit" class="rh-btn">Envoyer<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button></div>
</form>'''

FORM_HTML = form_html()

FORM_CSS = '''
@font-face{font-family:Inter;src:url(fonts/inter-latin.woff2) format("woff2");font-weight:400 700;font-display:swap}
.rh-form{font-family:Inter,"Inter Fallback",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#37352f;font-size:16px;line-height:1.15;text-align:left;padding:0 2px 2px}
.rh-form *{box-sizing:border-box}
.rh-field{margin:0 0 28px;border:0;padding:0;min-width:0}
.rh-label{display:flex;align-items:center;font-size:18px;font-weight:600;line-height:22.5px;color:#37352f;margin:0 0 12px;padding:0}
.rh-req{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;margin-left:6px;border-radius:50%;background:rgba(55,53,47,.09);font-size:12px;font-weight:700;line-height:1;padding-top:4px}
.rh-input{display:block;width:100%;height:36px;padding:0 10px;font:inherit;font-size:16px;color:#37352f;background:rgba(255,255,255,.5);border:0;border-radius:8px;box-shadow:rgba(0,0,0,.12) 0 1px 1px 0,rgba(61,59,53,.16) 0 0 0 1px,rgba(61,59,53,.08) 0 2px 5px 0;outline:none;-webkit-appearance:none;appearance:none}
.rh-input:focus{box-shadow:rgba(0,0,0,.12) 0 1px 1px 0,rgba(35,131,226,.57) 0 0 0 1px,rgba(35,131,226,.35) 0 0 0 2px,rgba(61,59,53,.08) 0 2px 5px 0}
.rh-select{padding-right:40px;background:rgba(255,255,255,.5) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%2337352f' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E") no-repeat right 12px center}
.rh-opts{display:grid;grid-template-columns:1fr 1fr;gap:12px 10px}
.rh-opt{position:relative;display:flex;align-items:center;gap:10px;min-height:36px;padding:8px 10px;border-radius:8px;cursor:pointer;background:rgba(255,255,255,.5);box-shadow:rgba(0,0,0,.12) 0 1px 1px 0,rgba(61,59,53,.16) 0 0 0 1px,rgba(61,59,53,.08) 0 2px 5px 0;font-size:16px;line-height:18.4px;transition:box-shadow .15s,background .15s}
.rh-opt input{position:absolute;opacity:0;pointer-events:none}
.rh-key{display:inline-flex;align-items:center;justify-content:center;flex:none;width:18px;height:18px;border-radius:3px;background:#605e5a;color:#fff;font-size:12px;font-weight:900;line-height:12px}
.rh-opt:has(input:checked){background:rgba(0,0,0,.04);box-shadow:rgba(0,0,0,.12) 0 1px 1px 0,#000 0 0 0 2px,rgba(61,59,53,.08) 0 2px 5px 0}
.rh-opt:has(input:checked) .rh-key{background:#000}
.rh-opt:has(input:focus-visible){outline:2px solid rgba(35,131,226,.57);outline-offset:2px}
.rh-row{display:grid;grid-template-columns:1.6fr 1fr;gap:10px}
.rh-file{display:block;font-size:16px;line-height:1.4;color:#37352f;margin:0 0 10px}
.rh-fileinput{height:auto;padding:8px 10px;font-size:14px}
.rh-submit{margin-top:40px}
.rh-btn{display:inline-flex;align-items:center;gap:8px;height:36px;padding:0 13.5px;border:0;border-radius:8px;background:#000;color:#fff;font:inherit;font-size:15px;font-weight:600;cursor:pointer;transition:opacity .15s}
.rh-btn:hover{opacity:.85}
.rh-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
@media (max-width:600px){.rh-opts{grid-template-columns:1fr}.rh-row{grid-template-columns:1fr}}
'''

PAGE_META = {
    '': dict(title='Refreshome – Nettoyage toiture, terrasse, façade et panneaux solaires à Rouen',
             desc='Nettoyage de toiture, terrasse, façade et panneaux solaires, gouttières, faîtières, charpente et peinture à Rouen et dans toute la Normandie. Devis gratuit.'),
    'confirmation/': dict(title='Confirmation – Refreshome', desc='Votre demande de devis a bien été reçue.', robots='noindex, follow'),
    'mentions-legales/': dict(title='Mentions légales – Refreshome', desc='Mentions légales du site refreshome.fr.', robots='noindex, follow'),
    'politique-de-confidentialite/': dict(title='Politique de confidentialité – Refreshome', desc='Politique de confidentialité du site refreshome.fr.', robots='noindex, follow'),
}

# ------------------------------------------------------------------ pages services ajoutées
import copy, re
from bs4 import BeautifulSoup

U = 'https://refreshome.fr/wp-content/uploads/2025/05/'
P = {  # photos réelles de l'ancien site (à remplacer par des photos de chantier dédiées quand le client les fournit)
    'toit': U + 'Nettoyage-de-toit-Refreshome-min.jpg', 'pro': U + 'Nettoyage-de-toiture-professionnel-Refreshome-min.jpg',
    'bp': U + 'Nettoyage-de-toiture-avec-machine-basse-pression-Refreshome-min.jpg', 'toiture': U + 'Nettoyage-toiture-Refreshome-min.jpg',
    'facade': U + 'Nettoyage-facade-Refreshome-min.jpg', 'pignon': 'https://refreshome.fr/wp-content/uploads/2025/07/Copie-de-Beige-White-Minimalist-Beauty-Skincare-Before-After-Collage-Instagram-Post.png',
    'dalle': U + 'Nettoyage-de-terrasse-Refreshome-min.jpg', 'jet': U + 'Nettoyage-de-terrasse-avec-jet-deau-Refreshome-min.jpg',
    'equipe': U + 'Qui-sommes-nous-Refreshome-min.jpg', 'pv': U + 'Panneaux-solaires-propres-Refreshome.jpg',
}
ICON = {'toit': U + 'Nettoyage-de-Toiture.svg', 'facade': U + 'Nettoyage-de-Facade.svg', 'parking': U + 'Nettoyage-de-Parkings.svg'}

SERVICES = {
 'traitement-charpente': dict(
    menu='Traitement de charpente', choice='Traitement de charpente', icon='toit', photos=['pro', 'toit', 'toiture', 'bp'],
    title='Traitement de charpente à Rouen – Refreshome', desc='Traitement préventif et curatif de charpente contre capricornes, vrillettes et champignons à Rouen et en Normandie. Diagnostic et devis gratuits.',
    badge=('Traitement de charpente à ', 'Rouen'), h1=('Protégez votre charpente ', 'durablement'),
    lead='Inspection de la charpente, puis traitement préventif ou curatif contre les capricornes, vrillettes et champignons du bois. À Rouen et partout en Normandie.',
    h2=('Notre ', 'traitement de charpente', ' ?'),
    cards=[('Traitement de Charpente', ['Solidité', 'Prévention', 'Valeur'], ['Traitement préventif ou curatif selon l’état des bois', 'Insectes xylophages : capricornes, vrillettes', 'Champignons et moisissures du bois'], 'Une charpente traitée, c’est une maison qui tient debout.'),
           ('Notre méthode', ['Inspection', 'Bûchage', 'Injection'], ['Inspection et sondage des bois', 'Bûchage des parties dégradées', 'Injection au cœur des bois porteurs puis pulvérisation'], 'Toutes les faces accessibles sont traitées.'),
           ('Les signes à surveiller', ['Trous', 'Sciure', 'Humidité'], ['Petits trous ronds dans les bois', 'Sciure (vermoulure) sous les poutres', 'Bois friable, taches d’humidité, filaments blancs'], 'En cas de doute, nous venons inspecter.'),
           ('Souvent associé', ['Toiture', 'Faîtage', 'Avant-toit'], ['Rénovation de faîtière en cas d’infiltration', 'Réparation de cache-moineaux', 'Nettoyage et traitement de toiture'], 'Un seul interlocuteur du toit à la charpente.')],
    faq=[('Comment savoir si ma charpente est attaquée ?', 'Trous ronds, sciure, bois friable : en cas de doute, nous venons l’inspecter.'),
         ('Préventif ou curatif ?', 'Le préventif protège un bois sain, le curatif traite une attaque en cours. Nous vous indiquons lequel il faut après inspection.'),
         ('Faut-il vider les combles ?', 'Il faut un accès dégagé aux bois. Nous vous précisons quoi déplacer avant l’intervention.'),
         ('Peut-on rester dans la maison ?', 'Oui. Nous vous indiquons le délai avant de réoccuper les combles selon le produit utilisé.'),
         ('Combien coûte un traitement de charpente ?', 'Le prix dépend de la surface et du type de traitement. Le devis est gratuit et sans engagement.')]),
 'gouttieres': dict(
    menu='Réparation et pose de gouttières', choice='Gouttières', icon='toit', photos=['toit', 'toiture', 'pro', 'bp'],
    title='Réparation et pose de gouttières à Rouen – Refreshome', desc='Réparation de fuites, remplacement et pose de gouttières zinc, PVC ou alu, nettoyage et débouchage à Rouen et en Normandie. Devis gratuit.',
    badge=('Gouttières à ', 'Rouen'), h1=('Des gouttières ', 'qui font leur travail'),
    lead='Fuite, joint, gouttière qui déborde ou se décroche : nous nettoyons, réparons ou remplaçons vos gouttières et descentes d’eau.',
    h2=('Réparation et pose ', 'de gouttières', ' ?'),
    cards=[('Réparation de Gouttières', ['Étanchéité', 'Protection', 'Durabilité'], ['Fuites et joints repris', 'Crochets et pente remis en état', 'Descentes d’eau pluviale débouchées'], 'Une gouttière qui fuit, c’est une façade qui s’abîme.'),
           ('Pose de Gouttières', ['Zinc', 'PVC', 'Aluminium'], ['Remplacement complet ou partiel', 'Zinc, PVC ou aluminium selon la maison', 'Grilles anti-feuilles en option'], 'Nous vous conseillons le bon matériau.'),
           ('Nettoyage de Gouttières', ['Débouchage', 'Entretien', 'Prévention'], ['Feuilles et mousses retirées', 'Gouttières et descentes rincées', 'Contrôle de l’écoulement'], 'Une à deux fois par an, surtout à l’automne.'),
           ('Les signes à surveiller', ['Débordement', 'Coulures', 'Affaissement'], ['L’eau passe par-dessus à chaque averse', 'Coulures sur la façade', 'Gouttière qui s’affaisse ou se décroche'], 'Mieux vaut réparer avant les dégâts.')],
    faq=[('Faut-il réparer ou remplacer ?', 'Une fuite ou un crochet se réparent ; une gouttière percée ou déformée se remplace. Nous vous le disons après diagnostic.'),
         ('Quel matériau choisir ?', 'Zinc, PVC ou aluminium : nous vous conseillons selon la maison et votre budget.'),
         ('À quelle fréquence nettoyer ses gouttières ?', 'Une à deux fois par an, surtout après la chute des feuilles.'),
         ('Intervenez-vous en hauteur ?', 'Oui, avec l’équipement adapté à la hauteur et à l’accès.'),
         ('Combien coûte une intervention ?', 'Le prix dépend de la longueur, du matériau et de l’accès. Le devis est gratuit.')]),
 'renovation-faitiere': dict(
    menu='Rénovation de faîtière', choice='Faîtière', icon='toit', photos=['pro', 'toiture', 'bp', 'toit'],
    title='Rénovation de faîtière à Rouen – Refreshome', desc='Rénovation de faîtières et de faîtage : mortier fissuré, faîtières cassées, infiltrations. Scellement ou faîtage à sec ventilé à Rouen et en Normandie.',
    badge=('Rénovation de faîtière à ', 'Rouen'), h1=('Un faîtage refait, ', 'un toit hors d’eau'),
    lead='Mortier fissuré, faîtières qui bougent ou infiltrations au sommet du toit : nous reprenons le faîtage pour remettre votre toiture hors d’eau.',
    h2=('Rénovation ', 'de faîtière', ' ?'),
    cards=[('Rénovation de Faîtière', ['Étanchéité', 'Solidité', 'Esthétique'], ['Dépose des faîtières et purge de l’ancien mortier', 'Scellement au mortier ou faîtage à sec ventilé', 'Remplacement des faîtières cassées'], 'Le faîtage est le point le plus exposé du toit.'),
           ('Faîtage à sec ventilé', ['Ventilation', 'Durabilité', 'Sans fissure'], ['Closoir souple sous les faîtières', 'Fixation mécanique, sans mortier qui fissure', 'La toiture respire'], 'Nous vous conseillons selon votre toiture.'),
           ('Les signes à surveiller', ['Fissures', 'Infiltrations', 'Mousse'], ['Mortier fissuré qui tombe dans la gouttière', 'Faîtières déplacées ou cassées', 'Traces d’eau dans les combles'], 'Réparer tôt évite d’abîmer la charpente.'),
           ('Souvent associé', ['Toiture', 'Charpente', 'Gouttières'], ['Nettoyage et hydrofuge de toiture', 'Traitement de charpente si l’eau a touché les bois', 'Nettoyage des gouttières'], 'Un toit complet en un seul passage.')],
    faq=[('Mortier ou faîtage à sec ?', 'Le faîtage à sec ventilé évite les fissures du mortier ; nous vous conseillons selon votre toiture.'),
         ('Combien de temps dure le chantier ?', 'En général une à deux journées pour une maison, selon la longueur du faîtage.'),
         ('Faut-il un échafaudage ?', 'Cela dépend de la hauteur et de l’accès. Nous vous le précisons dans le devis.'),
         ('Peut-on combiner avec un nettoyage ?', 'Oui, c’est le bon moment : toiture propre et faîtage refait en un seul passage.'),
         ('Combien coûte une rénovation de faîtière ?', 'Le prix dépend de la longueur et de la méthode. Le devis est gratuit.')]),
 'cache-moineaux': dict(
    menu='Réparation de cache-moineaux', choice='Cache-moineaux', icon='toit', photos=['toit', 'facade', 'toiture', 'pro'],
    title='Réparation de cache-moineaux à Rouen – Refreshome', desc='Réparation et remplacement de cache-moineaux en bois, peinture, habillage PVC et grilles anti-oiseaux à Rouen et en Normandie. Devis gratuit.',
    badge=('Cache-moineaux à ', 'Rouen'), h1=('Des avant-toits ', 'comme neufs'),
    lead='Planches pourries, peinture écaillée ou oiseaux qui nichent sous le toit : nous réparons, remplaçons ou habillons vos cache-moineaux.',
    h2=('Réparation de ', 'cache-moineaux', ' ?'),
    cards=[('Réparation de Cache-moineaux', ['Finitions', 'Protection', 'Esthétique'], ['Remplacement des planches abîmées', 'Peinture ou lasure du bois', 'Habillage PVC sans entretien'], 'Un détail qui change toute la façade.'),
           ('Anti-oiseaux', ['Ventilation', 'Propreté', 'Tranquillité'], ['Grilles qui bloquent oiseaux et frelons', 'La ventilation de la toiture est conservée', 'Nids retirés avant la pose'], 'Plus de nids sous le toit.'),
           ('Les signes à surveiller', ['Bois', 'Peinture', 'Nids'], ['Bois noirci ou pourri', 'Peinture écaillée, trous, planches manquantes', 'Oiseaux ou frelons entre les chevrons'], 'Le cache-moineau ferme l’espace entre le mur et le toit.'),
           ('Souvent associé', ['Gouttières', 'Façade', 'Charpente'], ['Réparation et pose de gouttières', 'Peinture de façade', 'Traitement des bois de charpente'], 'Un seul passage pour tout l’avant-toit.')],
    faq=[('Qu’est-ce qu’un cache-moineau ?', 'La planche qui ferme l’espace entre le haut du mur et la toiture, entre les chevrons.'),
         ('Réparer ou remplacer ?', 'Une planche saine se repeint ; une planche pourrie se remplace. Nous vous le disons après diagnostic.'),
         ('Bois ou PVC ?', 'Le bois garde le cachet d’origine ; le PVC ne demande plus d’entretien.'),
         ('Et la ventilation de la toiture ?', 'Nous posons des grilles qui bloquent les oiseaux tout en laissant l’air circuler.'),
         ('Combien coûte la réparation ?', 'Le prix dépend de la longueur et du matériau. Le devis est gratuit.')]),
 'peinture-facade': dict(
    menu='Peinture de façade', choice='Peinture de façade', icon='facade', photos=['facade', 'pignon', 'equipe', 'toiture'],
    title='Peinture de façade à Rouen – Refreshome', desc='Nettoyage, rebouchage des fissures et mise en peinture de façades, pignons et murs à Rouen et en Normandie. Devis gratuit.',
    badge=('Peinture de façade à ', 'Rouen'), h1=('Une façade repeinte, ', 'une maison valorisée'),
    lead='Nettoyage, réparation des fissures et mise en peinture de vos façades, pignons, murs et soubassements.',
    h2=('Notre service de ', 'peinture de façade', ' ?'),
    cards=[('Peinture de Façade', ['Esthétique', 'Protection', 'Valorisation'], ['Nettoyage de la façade sans pression', 'Rebouchage des fissures, fixateur ou sous-couche', 'Deux couches de peinture façade'], 'Une façade repeinte, c’est une maison qui prend de la valeur.'),
           ('Préparation du support', ['Nettoyage', 'Fissures', 'Fixateur'], ['Dépôts verts, noirs et rouges éliminés', 'Fissures ouvertes et rebouchées', 'Support sain avant peinture'], 'La tenue de la peinture se joue à la préparation.'),
           ('Les signes à surveiller', ['Écaillage', 'Fissures', 'Humidité'], ['Peinture qui farine ou s’écaille', 'Fissures qui laissent entrer l’eau', 'Couleur terne même après nettoyage'], 'Si la peinture est saine, un nettoyage suffit.'),
           ('Souvent associé', ['Isolante', 'Avant-toit', 'Nettoyage'], ['Peinture isolante pour plus de confort l’été', 'Réparation de cache-moineaux', 'Nettoyage de façade seul'], 'Nous vous conseillons la solution adaptée.')],
    faq=[('Faut-il une autorisation de la mairie ?', 'Un changement de couleur ou d’aspect peut nécessiter une déclaration préalable : nous vous indiquons la démarche.'),
         ('Quelle est la meilleure période ?', 'Du printemps au début de l’automne, par temps sec et doux.'),
         ('Le nettoyage ne suffit-il pas ?', 'Si la peinture est saine, un nettoyage suffit. Si elle s’écaille ou se fissure, il faut repeindre.'),
         ('Combien de temps dure le chantier ?', 'Quelques jours pour une maison, selon la surface et la préparation.'),
         ('Combien coûte une peinture de façade ?', 'Le prix dépend de la surface, du support et de la préparation. Le devis est gratuit.')]),
 'peinture-isolante': dict(
    menu='Peinture isolante', choice='Peinture isolante', icon='facade', photos=['bp', 'pro', 'facade', 'toit'],
    title='Peinture isolante toiture et façade à Rouen – Refreshome', desc='Peinture isolante thermo-réfléchissante pour toiture et façade, appliquée après nettoyage à Rouen et en Normandie. Devis gratuit.',
    badge=('Peinture isolante à ', 'Rouen'), h1=('Plus de fraîcheur l’été, ', 'un toit protégé'),
    lead='Une peinture thermo-réfléchissante appliquée sur votre toiture ou votre façade, après nettoyage et préparation du support.',
    h2=('Notre service de ', 'peinture isolante', ' ?'),
    cards=[('Peinture Isolante', ['Confort', 'Protection', 'Esthétique'], ['Réfléchit une partie du rayonnement solaire', 'Imperméabilise le support', 'Redonne une teinte uniforme'], 'Elle complète l’isolation, sans la remplacer.'),
           ('Notre méthode', ['Nettoyage', 'Préparation', 'Application'], ['Démoussage ou nettoyage du support', 'Traitement fongicide, fixateur, reprise des fissures', 'Deux couches de peinture isolante'], 'La peinture n’accroche que sur un support propre.'),
           ('Supports traités', ['Tuiles', 'Fibrociment', 'Façades'], ['Tuiles et fibrociment', 'Bac acier', 'Façades enduites'], 'Nous vérifions la compatibilité avant le devis.'),
           ('Souvent associé', ['Toiture', 'Façade', 'Faîtage'], ['Nettoyage de toiture', 'Peinture de façade', 'Rénovation de faîtière'], 'Un toit propre, protégé et plus frais.')],
    faq=[('La peinture isolante remplace-t-elle une isolation ?', 'Non. Elle complète l’isolation en limitant l’absorption de chaleur ; elle ne remplace pas un isolant.'),
         ('Sur quels supports ?', 'Tuiles, fibrociment, bac acier et façades enduites, après préparation.'),
         ('Faut-il nettoyer avant ?', 'Oui, toujours : la peinture n’accroche que sur un support propre et sain.'),
         ('Quelle est la meilleure période ?', 'Par temps sec et doux, du printemps au début de l’automne.'),
         ('Combien coûte une peinture isolante ?', 'Le prix dépend de la surface et du support. Le devis est gratuit.')]),
 'nettoyage-professionnel': dict(
    menu='Nettoyage pour professionnels', choice='Nettoyage professionnel', icon='parking', photos=['dalle', 'equipe', 'jet', 'facade'], b2b=True,
    title='Nettoyage extérieur pour professionnels à Rouen – Refreshome', desc='Nettoyage de parkings, espaces de collectivités, résidences de bailleurs sociaux et devantures de commerce à Rouen et en Normandie. Contrats d’entretien.',
    badge=('Nettoyage professionnel à ', 'Rouen'), h1=('Des extérieurs impeccables ', 'pour votre activité'),
    lead='Parkings, collectivités, bailleurs sociaux et devantures de commerce : interventions ponctuelles ou contrats d’entretien, planifiées selon votre activité.',
    h2=('Nos services de ', 'nettoyage pour les professionnels', ' ?'),
    cards=[('Nettoyage de Parkings', ['Image', 'Sécurité', 'Propreté'], ['Parkings d’entreprise, de magasins et de résidences', 'Traces d’huile, gommes, mousses, chewing-gums', 'Intervention planifiée selon vos horaires'], 'Un parking propre, c’est la première impression.'),
           ('Collectivités', ['Espaces publics', 'Bâtiments', 'Mobilier'], ['Parvis, places et trottoirs', 'Façades de bâtiments publics', 'Mobilier urbain'], 'Nous répondons à vos demandes de devis.'),
           ('Bailleurs sociaux', ['Résidences', 'Façades', 'Abords'], ['Abords de résidences et halls extérieurs', 'Façades et toitures', 'Locaux poubelles'], 'Un seul prestataire pour tout votre parc.'),
           ('Devantures de commerce', ['Vitrine', 'Enseigne', 'Terrasse'], ['Façades et vitrines', 'Enseignes', 'Terrasses de cafés et restaurants'], 'Entretenir = valoriser + faire des économies.')],
    faq=[('Intervenez-vous en dehors des heures d’ouverture ?', 'Nous planifions l’intervention avec vous pour gêner le moins possible votre activité.'),
         ('Proposez-vous des contrats d’entretien ?', 'Oui : formules sur-mesure avec interventions planifiées et devis personnalisé.'),
         ('Travaillez-vous avec les collectivités et bailleurs ?', 'Oui, envoyez-nous votre cahier des charges ou votre demande de devis.'),
         ('Que faites-vous des eaux de lavage ?', 'Nous adaptons la méthode au site et à son réseau d’évacuation ; nous en parlons lors de la visite.'),
         ('Quelle zone couvrez-vous ?', 'Rouen, sa métropole et toute la Normandie.')]),
}

CARD_IDS = ['c5365dd', '54f226c', '529c28c', 'b079cec']

def _set_html(el, html):
    el.clear(); el.append(BeautifulSoup(html, 'html.parser'))

def build_services(home_html, clean_page, form):
    out = {}
    for slug, s in SERVICES.items():
        soup = BeautifulSoup(home_html, 'lxml')
        q = lambda i: soup.select_one(f'[data-id="{i}"]')
        # --- hero
        _set_html(q('72416d0').select_one('.elementor-icon-list-text'), f'{s["badge"][0]}<b>{s["badge"][1]}</b>')
        _set_html(q('cb7d21d').select_one('h1'), f'{s["h1"][0]}<b>{s["h1"][1]}</b>')
        _set_html(q('780c72a').select_one('.elementor-widget-container'), f'<p>{s["lead"]}</p>')
        # --- section services : 4 cartes au gabarit d'origine
        h = s['h2']; _set_html(q('9a1ef3a').select_one('h2'), f'{h[0]}<b>{h[1]}</b>{h[2]}')
        for cid, card, ph in zip(CARD_IDS, s['cards'], s['photos']):
            c = q(cid); title, tags, bullets, tip = card
            c['id'] = 'service-' + slug if cid == CARD_IDS[0] else c.get('id')
            img = c.select('img')[0]
            img['src'] = P[ph]; img['alt'] = f'{title} – Refreshome'
            for a in ('srcset', 'sizes', 'width', 'height', 'fetchpriority'): img.attrs.pop(a, None)
            img['loading'] = 'lazy'
            icon = c.select('img')[1]; icon['src'] = ICON[s['icon']]
            c.select_one('h3').string = title
            ptags = [p for p in c.select('[data-widget_type="heading.default"] p')]
            for p, t in zip(ptags[:3], tags): p.string = t
            ptags[-1].string = '💡 ' + tip
            ul = c.select_one('[data-widget_type="icon-list.default"] ul')
            lis = ul.select("li"); tpl = copy.copy(lis[0])
            for li in lis: li.decompose()
            for b in bullets:
                li = copy.copy(tpl); li.select_one('.elementor-icon-list-text').string = b; ul.append(li)
        # --- sections retirées sur les pages services (offres et bonus gardés pour les pros)
        if not s.get('b2b'):
            for i in ('8e1dacf', '15cd9e7'): q(i).decompose()
        # --- FAQ
        acc = soup.select_one('[id^="uc_content_accordion"] .uc_container') or soup.select_one('.uc_ac_box').parent
        boxes = acc.select(':scope > .uc_ac_box'); tpl = boxes[0]
        for b in boxes: b.extract()
        for n, (qq, aa) in enumerate(s['faq']):
            b = copy.copy(tpl)
            b['class'] = [c for c in b['class'] if c != 'uc-item-active'] + (['uc-item-active'] if n == 0 else [])
            b['id'] = f'#ue-tab{n + 1}'
            b.select_one('.ue_heading_title').string = qq
            _set_html(b.select_one('.ue-item-text'), f'<p>{aa}</p>')
            cont = b.select_one('.uc_content')
            if n == 0: cont['style'] = 'display:block'
            else: cont.attrs.pop('style', None)
            acc.append(b)
        cleaned = clean_page(str(soup), slug + '/', form.replace('value="' + s['choice'] + '"', 'value="' + s['choice'] + '" checked'),
                             title=s['title'], desc=s['desc'])
        out[slug + '/'] = cleaned
    return out
build_services.paths = lambda: [k + '/' for k in SERVICES]

def nav_patch(soup, path, rel):
    """Ajoute les nouvelles pages au sous-menu « Services » (desktop + mobile) et à « Nos services » du pied de page."""
    for f in soup.select('#devisForm input[name=Source]'):
        f['value'] = {'': 'Accueil'}.get(path, path.strip('/'))
    for sub in soup.select('#header-menu-1 .sub-menu, .mobile-menu .sub-menu'):
        tpl = sub.select('li')[-1]
        for slug, s in SERVICES.items():
            li = copy.copy(tpl); a = li.select_one('a')
            a['href'] = rel(path, slug + '/'); a.string = s['menu']; a.attrs.pop('aria-current', None)
            li['class'] = [c for c in li.get('class', []) if not c.startswith('menu-item-') or c in ('menu-item-type-custom', 'menu-item-object-custom')]
            li.attrs.pop('id', None)
            sub.append(li)
    for ul in soup.select('[data-id="4972f5a"] ul.elementor-nav-menu'):
        lis = ul.select(':scope > li'); last = lis[-1]; tpl = lis[0]
        for slug, s in SERVICES.items():
            li = copy.copy(tpl); a = li.select_one('a')
            a['href'] = rel(path, slug + '/'); a.string = s['menu']; a.attrs.pop('aria-current', None)
            a['class'] = [c for c in a.get('class', []) if c != 'elementor-item-anchor']
            last.insert_before(li)

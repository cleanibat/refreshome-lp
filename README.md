# Refreshome – site refreshome.fr (statique, identique à l'original)

Reproduction à l'identique du site WordPress/Elementor/Blocksy de Refreshome (visuel et animations), sans WordPress ni plugins, plus 7 pages services.
Aperçu : https://cleanibat.github.io/refreshome-lp/ (le formulaire n'envoie rien sur l'aperçu, c'est normal).

## Fonctionnement
- `tools/scrape.py` : capture une fois l'original (HTML, CSS, polices, images) dans `source/`. À relancer seulement si le site d'origine change.
- `build.py` : nettoie le balisage d'origine, regroupe et purge le CSS (`assets/site.css`), convertit les images en WebP (plafonnées à la taille d'affichage), génère les pages.
- `services.py` : formulaire (même rendu que l'ancien Tally), titres/descriptions SEO, contenu des 7 pages services (mêmes blocs que l'accueil).
- `assets/site.js` : remplace jQuery + Blocksy + Elementor (en-tête collant « shrink », menu mobile, sous-menu, carrousels Swiper aux réglages d'origine, animation slideInUp, accordéon FAQ, fonds différés, avis Trustindex chargés au défilement).

```
python3 build.py
```
Nécessite : Python 3 + `pip3 install beautifulsoup4 lxml pillow fonttools brotli`, Node (npx purgecss, lightningcss).

## Pages
- Reprises à l'identique : `/`, `/confirmation/` (Calendly), `/mentions-legales/`, `/politique-de-confidentialite/`
- Ajoutées : `/traitement-charpente/`, `/gouttieres/`, `/renovation-faitiere/`, `/cache-moineaux/`, `/peinture-facade/`, `/peinture-isolante/`, `/nettoyage-professionnel/`
- Les nouvelles pages sont dans le sous-menu « Services » (desktop et mobile) et dans « Nos services » du pied de page.

## Formulaire
`contact.php` (aucun service tiers) : CSV + photos hors docroot, e-mail au client avec photos jointes, Aymeric en Cci, redirection vers `/confirmation/`. Test : `contact.php?test=1`.

## Écarts volontaires avec l'original
- Formulaire Tally → formulaire HTML au même rendu (choix A/B/C…, champs, bouton noir « Envoyer »), avec les nouvelles prestations.
- Menu mobile : l'original ne s'affichait pas correctement (panneau transparent par-dessus la page) ; ici il s'ouvre normalement, même style.
- Icônes : Font Awesome (FAQ) remplacé par les mêmes icônes en SVG ; police d'icônes MingCute réduite aux 9 icônes utilisées.

## Bascule refreshome.fr (Hostinger)
1. Sauvegarde complète du WordPress (fichiers + base) depuis hPanel.
2. SPF sur refreshome.fr : `v=spf1 include:_spf.google.com include:_spf.mail.hostinger.com ~all`.
3. Accès SSH Hostinger → secrets du dépôt (workflow `deploy-ssh.yml`, en déclenchement manuel tant que WordPress n'est pas sauvegardé), puis réactiver `push`.
4. GTM : `GTM_ID` dans `build.py`, importer le conteneur (conversion Ads existante `AW-17623850704 / ohQNCNuR7v8cENC92tNB`, pixel Meta `952469813385770`).
5. Test du formulaire, `check_site.sh https://refreshome.fr/`, sitemap dans Search Console.

## À valider par le client
- Textes des 7 nouvelles pages ; photos : ce sont celles de l'ancien site (toitures, façades), à remplacer par des photos de chantier de chaque service.
- Téléphone (37 dans les mentions, 38 dans la politique de confidentialité) et forme juridique (auto-entreprise / SASU).

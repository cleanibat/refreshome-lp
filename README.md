# Refreshome – site refreshome.fr (statique)

Refonte du site WordPress/Elementor de Refreshome (nettoyage extérieur, Rouen) en site statique HTML/CSS sans framework.
Aperçu : https://cleanibat.github.io/refreshome-lp/ (le formulaire n'envoie rien sur l'aperçu, c'est normal).

## Générer
```
python3 build.py
```
Textes dans `content.py`, gabarits et CSS dans `build.py`. Photos sources dans `src_img/` (non déployées), versions web WebP dans `img/`.

## Pages
- `/` accueil (mêmes sections que l'ancien site : services, réalisations, qui sommes-nous, offres & packs, bonus, avis, FAQ, devis)
- Nettoyage : `/nettoyage-toiture/`, `/nettoyage-terrasse/`, `/nettoyage-facade/`, `/nettoyage-panneaux-solaires/`, `/nettoyage-professionnel/` (B2B)
- Toiture & charpente : `/traitement-charpente/`, `/gouttieres/`, `/renovation-faitiere/`, `/cache-moineaux/`
- Peinture : `/peinture-facade/`, `/peinture-isolante/`
- `/confirmation/` (page merci + Calendly), `/mentions-legales/`, `/politique-de-confidentialite/`, `/404/`

Les URL de l'ancien site (`/confirmation/`, `/mentions-legales/`, `/politique-de-confidentialite/`) sont conservées.

## Formulaire
`contact.php` (HTML classique, aucun service tiers) : CSV `leads_refreshome.csv` + photos hors docroot, e-mail au client avec photos jointes, Aymeric en Cci, redirection 303 vers `/confirmation/`. Test : `contact.php?test=1`.
Le formulaire Tally de l'ancien site est remplacé.

## Bascule refreshome.fr (Hostinger)
1. Sauvegarde complète du WordPress (fichiers + base) depuis hPanel.
2. SPF sur refreshome.fr (DNS Hostinger) : `v=spf1 include:_spf.google.com include:_spf.mail.hostinger.com ~all` (le domaine n'a aucun SPF aujourd'hui ; Google Workspace gère les MX).
3. Accès SSH Hostinger → secrets du dépôt (voir workflow `deploy-ssh.yml`, aujourd'hui en déclenchement manuel), puis réactiver `push`.
4. GTM : renseigner `SITE['gtm']` dans `content.py`, régénérer, importer le conteneur (Conversion Ads existante `AW-17623850704 / ohQNCNuR7v8cENC92tNB`, pixel Meta `952469813385770`).
5. Test de bout en bout du formulaire, `check_site.sh https://refreshome.fr/`, soumettre `sitemap.xml` dans Search Console.

## À valider par le client
- Pages nouvelles (charpente, gouttières, faîtière, cache-moineaux, peintures, B2B) : méthodes et vocabulaire.
- Téléphone (06 99 04 62 37 dans les mentions, 06 99 04 62 38 dans l'ancienne politique de confidentialité) et forme juridique (auto-entreprise ou SASU).
- Nom du 4e pack (« Pack Image Pro », l'ancien site affichait deux fois « Pack Énergie Maximale »).
- « Hydrofuge coloré garanti 10 ans » et « jusqu'à +30 % de performance » repris de l'ancien site.

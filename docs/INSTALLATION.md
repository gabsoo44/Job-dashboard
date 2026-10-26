# Installation et fonctionnement

Dashboard de suivi de candidatures qui se met à jour **chaque nuit tout seul**, même PC éteint :

1. Une GitHub Action lit le libellé Gmail **« Candidatures »** (lecture seule).
2. Claude Code (modèle Haiku, via ton abonnement Claude) classe chaque mail : accusé de réception, CV consulté, entretien, refus, etc.
3. Les candidatures et leur statut sont mis à jour dans un fichier **chiffré** (AES-256-GCM).
4. Le site est redéployé sur GitHub Pages ; il demande ton mot de passe et déchiffre les données **dans ton navigateur**.

Coût : 0 € en plus de ton abonnement Claude (Pro ou Max) — pas de clé API. La synchro consomme un peu de ton quota ; si le quota est épuisé une nuit, elle rattrape la nuit suivante.

> **Pourquoi le repo est public** : GitHub Pages gratuit exige un repo public. Ce n'est pas un problème : le code est public, mais les données ne sont jamais en clair dans le repo (seulement `web/data/store.enc.json`, illisible sans ton mot de passe). **Choisis un mot de passe long** (une phrase de 4-5 mots) : c'est lui qui protège tes données.

## Mise en place (une seule fois)

### 1. Repo GitHub public
```bash
git init && git add . && git commit -m "init"
gh repo create job-dashboard --public --source=. --push
```

### 2. Accès Gmail en lecture seule
1. [Google Cloud Console](https://console.cloud.google.com) → nouveau projet → *APIs & Services* → activer **Gmail API**.
2. *OAuth consent screen* : type **External**, ajoute ton adresse en utilisateur test, puis **Publish app** (« In production »).
   ⚠️ En mode « Testing », le token expire après 7 jours. En production (non vérifié, usage perso), il n'expire pas.
3. *Credentials* → Create → **OAuth client ID** → *Desktop app* → télécharge `client_secret.json`.
4. En local (connecte-toi avec la boîte qui contient le libellé « Candidatures », écran « non vérifiée » → Avancé → continuer) :
   ```bash
   py -m pip install -r requirements.txt
   py scripts/gmail_auth.py client_secret.json
   ```
   Le script affiche 3 valeurs.

### 3. Secrets GitHub
Repo → *Settings → Secrets and variables → Actions* :
`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`, `DASHBOARD_PASSWORD` (ton mot de passe du dashboard) et `CLAUDE_CODE_OAUTH_TOKEN` :
```bash
npm install -g @anthropic-ai/claude-code
claude setup-token
```
Connecte-toi avec ton compte Claude ; la commande affiche un jeton longue durée (`sk-ant-oat…`) à coller dans le secret.

### 4. GitHub Pages
Repo → *Settings → Pages → Source : **GitHub Actions***.

### 5. Premier lancement
*Actions → Sync et déploiement → Run workflow* avec **backfill** coché : reconstruit toute la liste depuis tout le libellé. Le lien du site apparaît dans le job *deploy*. Ensuite, tout tourne seul vers 3h du matin (heure de Paris).

## Ajouter ou modifier une candidature depuis le site
1. GitHub → avatar → *Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token*.
   Repository access : **Only select repositories → Job-dashboard**. Permissions : **Contents → Read and write**. Expiration au choix.
2. Sur le dashboard : **Connexion GitHub** → colle le jeton (il reste dans ce navigateur uniquement).
3. **+ Ajouter** ou **Modifier** sur une ligne. Les changements sont chiffrés avec ton mot de passe dans
   `web/data/manual.enc.json`, que la synchro de nuit ne touche jamais. Un nouveau mail (refus, entretien…)
   plus récent que ta modification reprend la main sur le statut.

Autre option sans jeton : *Actions → Run workflow* → `set_id`, `set_status`, `set_note`.

## Recalculer sans relire Gmail
Les classifications de Claude sont stockées (chiffrées). Après une amélioration des règles : *Run workflow* avec **rebuild** coché (quelques secondes, sans Gmail ni Claude).

## Tester en local
```bash
set DASHBOARD_PASSWORD=...           # + les 4 autres variables
py scripts/sync.py --backfill --dry-run
cd web && py -m http.server 8765
```

## Confidentialité
Les mails du libellé sont envoyés à l'API Anthropic (2 500 caractères max par mail) pour classification. Gmail n'est accédé qu'en lecture seule. Voir `CLAUDE.md` pour le contexte technique.

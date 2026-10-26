# Job Dashboard

Un tableau de bord personnel pour suivre mes candidatures d'emploi.

## Pourquoi ce projet

En recherche d'emploi, on postule vite à des dizaines (voire des centaines) d'offres, sur plusieurs plateformes : LinkedIn, HelloWork, Indeed, sites d'entreprises… Les réponses arrivent ensuite au compte-gouttes dans la boîte mail, mélangées au reste. Très vite, on ne sait plus où on a postulé, qui a répondu et quelles candidatures sont encore en attente.

Ce dashboard règle ça : il **regroupe toutes mes candidatures au même endroit** et les **classe automatiquement selon leur état**, pour voir en un coup d'œil où j'en suis dans ma recherche.

## Ce que fait le dashboard

- **Se met à jour tout seul** chaque jour à partir de mes e-mails de candidature (confirmations, refus, entretiens…).
- **Classe chaque candidature** dans un conteneur :
  - **Envoyée** : postulée il y a moins de 3 jours
  - **En cours** : en attente de réponse, depuis moins de 2 mois
  - **Sans réponse** : aucune nouvelle depuis plus de 2 mois
  - **Refus** : réponse négative reçue
- **Met en avant** les réponses positives et les candidatures à finaliser.
- **Filtre par année** et permet de rechercher une entreprise ou un poste.
- **Permet d'ajouter ou de corriger** une candidature à la main.
- **Reste privé** : les données sont chiffrées et le site est protégé par un mot de passe.

## Technologies

Python · GitHub Actions · Gmail API · Claude (classification des e-mails) · HTML/JavaScript · GitHub Pages

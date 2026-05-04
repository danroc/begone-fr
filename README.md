# Begone: Liste de Blocage :fr:

Ce repo contient des listes de blocage de numéros indésirables pour la France, à
utiliser avec l'application [Begone][begone-app] sur iOS.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé l'application [Begone][begone-app] sur
votre iPhone. Une fois l'application installée, lancez-la et suivez les instructions
pour l'activer en tant qu'application de blocage d'appels sur iOS.

## Installation

Ouvrez [cette page](#installation) sur votre iPhone et suivez les instructions
ci-dessous :

1. Appuyez longuement sur le lien de la liste souhaitée ci-dessous et sélectionnez
   **Télécharger le fichier lié**.

   - [Numéros de démarchage][list-spam] (recommandée)
   - [Numéros VOIP][list-voip]
     - [Numéros OnOff][list-onoff]
     - [Numéros Ubicentrex][list-ubicentrex]
   - [Liste complète][list-all]

2. Ouvrez l'application Begone et sélectionnez **Importer de nouveaux numéros**.

3. Sélectionnez **Fichiers**.

4. Importez le fichier que vous venez de télécharger.

## Contribution

### Configurer l'environnement de développement

1. Créez un nouvel environnement virtuel Python et installez les dépendances
   nécessaires.

   ```bash
   uv venv
   uv sync
   # ou exécutez 'make init'
   ```

2. Activez l'environnement virtuel.

   ```bash
   source .venv/bin/activate
   ```

### Ajouter de nouveaux numéros à la liste de blocage

1. Mettez à jour le fichier `data/numbers.yaml` avec les nouveaux numéros que vous
   souhaitez bloquer.

2. Exécutez `make` pour générer les nouvelles listes dans le dossier `dist`.

[begone-app]: https://apps.apple.com/fr/app/id1596818195
[list-all]: https://raw.githubusercontent.com/danroc/begone-fr-list/refs/heads/main/dist/begone-fr-tout.xml
[list-spam]: https://raw.githubusercontent.com/danroc/begone-fr-list/refs/heads/main/dist/begone-fr-demarchage.xml
[list-voip]: https://raw.githubusercontent.com/danroc/begone-fr-list/refs/heads/main/dist/begone-fr-voip.xml
[list-onoff]: https://raw.githubusercontent.com/danroc/begone-fr-list/refs/heads/main/dist/begone-fr-onoff.xml
[list-ubicentrex]: https://raw.githubusercontent.com/danroc/begone-fr-list/refs/heads/main/dist/begone-fr-ubicentrex.xml

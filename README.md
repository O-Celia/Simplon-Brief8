---
page_type: sample
languages:
  - python
products:
  - azure
  - azure-redis-cache
description: "This sample creates a multi-container application in an Azure Kubernetes Service (AKS) cluster."
---

# Automatisation de la mise à jour d’une application sur Docker avec une pipeline Jenkins

Ce projet consiste à automatiser le déploiement, la mise à jour et la gestion d'une application conteneurisée sur un cluster Kubernetes (AKS) à l'aide d'une pipeline Jenkins. Voici un aperçu des étapes clés pour configurer et exécuter ce workflow.

## Table des Matières

1. Description du Projet
2. Technologies Utilisées
3. Étapes Principales
4. Structure du Projet
5. Notes Importantes

### 1. Description du Projet

L’objectif principal est de mettre en place une infrastructure scalable et automatisée pour gérer une application web construite avec Flask. Ce projet inclut :

- Le déploiement d’un cluster Kubernetes (AKS).
- L’installation et la configuration d’un serveur Jenkins pour orchestrer les pipelines.
- La création d'une pipeline CI/CD pour construire, publier, et déployer une application Docker.
- L'intégration d’un DNS personnalisé pour chaque environnement (qal, prod).
- Des tests de charge pour valider les performances.

### 2. Technologies Utilisées

*Cloud* : Microsoft Azure (AKS, Azure CLI) <br/>
*Orchestrateur* : Kubernetes <br/>
*CI/CD* : Jenkins <br/>
*Conteneurs* : Docker <br/>
*Langages* : Python (Flask), Bash<br/>
*Outils complémentaires* :
- kubectl pour interagir avec Kubernetes.
- git pour la gestion du code source.
- jq et parallel pour des manipulations avancées de données et exécutions simultanées.
- pip et requests-toolbelt pour les dépendances Python.

### 3. Étapes Principales

1. Déploiement du Cluster AKS

Un cluster Kubernetes avec un nœud est créé sur Azure. Les namespaces nécessaires aux environnements qal et prod sont configurés.

**Pour plus d’informations : Consultez la procédure dans les fichiers.**

2. Installation et Configuration de Jenkins

Une machine virtuelle (VM) est configurée pour accueillir Jenkins. Cette étape inclut :

- L’installation des dépendances (Java, Jenkins, Azure CLI, Docker, etc.).
- L’ajout des clés nécessaires pour les accès.
- La configuration de Jenkins pour interagir avec le cluster AKS et Docker Hub.

3. Création de DNS pour les Environnements

Un enregistrement DNS est créé sur Gandi pour pointer vers l’IP publique de l’application. Cela permet d’accéder facilement aux environnements via des URL personnalisées.

4. Pipeline Jenkins

La pipeline CI/CD comporte plusieurs étapes automatisées :

- Clonage du Dépôt Git : Récupération du code source de l’application.
- Construction de l’Image Docker : Création d'une image Docker de l’application.
- Publication de l’Image sur Docker Hub : Poussée de l’image avec un tag correspondant à la version.
- Déploiement sur Kubernetes : Mise à jour des manifests YAML et application des changements sur le cluster.
- Test de Charge : Validation des performances de l’application via des requêtes simultanées.

5. Script de Mise à Jour Automatique

Le script auto-maj.sh permet d’incrémenter automatiquement la version de l’application et de pousser les modifications dans le dépôt Git.

### 4. Structure du Projet

- azure-vote/ : Contient le code de l’application Flask.
- Dockerfile : Fichier pour construire l’image Docker.
- auto-maj.sh : Script Bash pour automatiser la mise à jour des versions.
- vote.yaml : Manifest YAML pour le déploiement Kubernetes.
- Jenkinsfile : Pipeline Jenkins définissant les étapes CI/CD.

### 5. Notes Importantes

- Configurations spécifiques : Des ajustements comme l’augmentation des ressources de la VM Jenkins (2vCPU minimum) sont nécessaires pour un fonctionnement optimal.
- Environnements : Les namespaces qal et prod permettent de séparer les déploiements selon l’environnement de développement.
- Sécurité : L'ajout des credentials pour Docker Hub et le cluster Kubernetes est essentiel pour la pipeline.

<br/> Pour plus de détails sur chaque étape ou commande, référez-vous aux fichiers inclus dans le projet.

# Fork : Azure Voting App

This sample creates a multi-container application in an Azure Kubernetes Service (AKS) cluster. The application interface has been built using Python / Flask. The data component is using Redis.

To walk through a quick deployment of this application, see the AKS [quick start](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough?WT.mc_id=none-github-nepeters).

To walk through a complete experience where this code is packaged into container images, uploaded to Azure Container Registry, and then run in and AKS cluster, see the [AKS tutorials](https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-app?WT.mc_id=none-github-nepeters).

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

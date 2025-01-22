# Audit du projet de création d'une plateforme Big Data

## Sources de données

**API:**
- **OpenWeatherMap** : 60 requêtes par minute, 1 000 000 requêtes par mois.
- **AQICN** : extraction de tous les champs pour obtenir des données brutes.

**Problèmes:**
- Aucun problème d'accès aux données ou de limitations de requêtes n'a été rencontré.

## Modélisation des données

**Modèle de données:**
- Utilisation de tables dimensionnelles.

**Problèmes:**
- Aucun problème de modélisation des données n'a été rencontré.
- Aucun problème de performance de la base de données n'a été rencontré.

## Traitement et ETL

**Problèmes:**
- Des difficultés ont été rencontrées lors de l'extraction, la transformation et le chargement des données en raison du format nested JSON.
- Ces problèmes ont été résolus en utilisant **Kafka** et **Spark** pour convertir les données en format tabulaire.

**Optimisation:**
- L'utilisation de Kafka et Spark a permis de traiter et de transformer les données efficacement.

## Architecture et technologies

**Technologies:**
- Les technologies utilisées (**Kafka** et **Spark**) ont été efficaces et n'ont posé aucun problème.

**Problèmes:**
- Aucun problème lors de la mise en œuvre de l'architecture du système.

**Utilisation de AWS:**
- Déploiement de **Kafka** et **Spark** sur **AWS EC2** pour un traitement en ligne.
- Stockage des données dans **Amazon S3**.
- Utilisation de **AWS Glue** pour la catalogisation des données.
- Chargement des données dans **Amazon Redshift** pour l'analyse.

## Sécurité des données

**Problèmes:**
- Aucun problème de sécurité des données n'a été rencontré.
- Aucun problème de conformité avec le RGPD n'a été rencontré.

**Évaluation des risques et mesures de contrôle (RGPD):**
- **Accès illégitime aux données:**
  - **Impacts:** Fuite de données personnelles, utilisation frauduleuse des données, perte de confiance des utilisateurs, pertes financières et de réputation.
  - **Menaces:** Attaques de hackers externes, menaces internes des employés, vulnérabilités des logiciels, phishing et ingénierie sociale.
  - **Sources:** Mesures de protection d'accès insuffisantes, absence de chiffrement des données, protection réseau insuffisante, erreurs des employés.
  - **Mesures:** Chiffrement (TLS/SSL, AES-256), contrôle d'accès (IAM dans AWS, authentification à deux facteurs), journalisation (AWS CloudTrail, Amazon CloudWatch).

- **Modification indésirable des données:**
  - **Impacts:** Altération de l'intégrité des données, prise de décisions erronées, perte de confiance des utilisateurs.
  - **Menaces:** Erreurs internes des employés, attaques externes, vulnérabilités des logiciels.
  - **Sources:** Contrôle d'accès insuffisant, protection réseau insuffisante, facteur humain.
  - **Mesures:** Contrôle d'accès (IAM dans AWS, authentification à deux facteurs), journalisation (AWS CloudTrail, Amazon CloudWatch), chiffrement des données.

- **Disparition des données:**
  - **Impacts:** Fuite de données personnelles, perte de confiance des utilisateurs.
  - **Menaces:** Attaques de hackers externes, vulnérabilités des logiciels.
  - **Sources:** Protection réseau insuffisante, absence de chiffrement des données.
  - **Mesures:** Chiffrement, contrôle d'accès, anonymisation.

## Qualité des données

**Problèmes:**
- À Lyon, il manquait des données AQI. Ce problème a été résolu en utilisant des données historiques et des valeurs médianes.
- Le principal problème était la présence de valeurs nulles dans certaines données.

## Gestion du projet

**Problèmes:**
- Aucun problème de gestion de projet n'a été rencontré.

**Méthodologies:**
- Vous avez utilisé la **méthodologie Agile** pour gérer ce projet. Cette approche vous a permis d'être flexibles et réactifs face aux changements et aux défis rencontrés. Les itérations régulières et les réunions de rétrospective ont facilité une communication ouverte et une amélioration continue du processus.

## Problèmes clés et défis

**Problèmes clés:**
- Le principal problème était la présence de valeurs nulles dans certaines données.

**Points positifs:**
- Après avoir étudié et compris les données, le travail s'est déroulé sans encombre.

## Recommandations pour l'avenir

**Améliorations:**
- Déployer **Kafka** et **Spark** sur **AWS EC2** pour assurer un fonctionnement en ligne et envoyer automatiquement les données vers **S3**.
- Continuer d'utiliser **AWS Glue** pour la catalogisation des données et **Amazon Redshift** pour l'analyse approfondie des données.

## Contexte

GoodAir a besoin de récupérer et stocker un certain nombre d’informations afin de les mettre à disposition de ses chercheurs. Ces données doivent pouvoir être accessibles sur un outil de data visualisation mais aussi exportables pour des études plus avancées. Le laboratoire GoodAir fait appel à vous pour auditer le projet.

Ce laboratoire a pour objectif de suivre la qualité de l’air et de l’eau afin de proposer des recommandations à la population, d’étudier les conséquences du changement climatique, et de déterminer des seuils d’alerte. Il pourra mener des recherches scientifiques sur le sujet tout en développant des plateformes de sensibilisation pour le grand public.

Le laboratoire est composé d’une dizaine de chercheurs et d’analystes dans le domaine du climat, de la biologie, et de la météorologie. Comme pour toute recherche, l’équipe du laboratoire a besoin de se reposer sur des données. Celles-ci doivent être fiables, disponibles, et pertinentes. Dans une problématique de limitation des coûts et du temps de collecte, le directeur du laboratoire souhaite se baser sur des sources de données déjà existantes.

TotalGreen est une société française travaillant dans le secteur des énergies renouvelables. Afin de développer son pôle de R&D, TotalGreen développe GoodAir : un laboratoire de recherche pour étudier la qualité de l’air et la qualité de l’eau en France.

## Spécifications du besoin

1. **Accès aux données:**
   - L’API OpenWeatherMap propose une formule gratuite dont le nombre d’appels quotidien est limité. GoodAir souhaite se limiter à cette formule. Le livrable proposé doit donc s’assurer de ne pas dépasser les quotas imposés par l’API.

2. **Modélisation:**
   - Les données de ces deux sources doivent être modélisées dans une base de données normalisée. Puisqu’elle sera connectée à un outil de data visualisation, la modélisation doit permettre de requêter des volumes de données conséquentes en un laps de temps minimal.

3. **Historisation:**
   - Les deux sources de données sont disponibles à travers des API qui renvoient les informations en temps réel. GoodAir aurait besoin que le livrable soit capable de récupérer ces données chaque heure, en faire une capture et la stocker. Les données ainsi récupérées pourront être directement ajoutées à la base de données.

4. **Sécurité:**
   - Dans une problématique de conformité avec le RGPD, l’ensemble des traitements et des entrepôts de données doivent être localisés en France ou dans l’Union Européenne. De plus l’accès aux données doit se faire de façon sécurisée (système d’authentification).

5. **Qualité et fiabilité:**
   - Une surveillance de la qualité des données doit pouvoir être mise en place au cours de la chaîne de traitement. Si cela s’avère pertinent, un processus de nettoyage sera mis en place. Le livrable doit aussi être capable d’alerter les équipes en cas de problème sur le pipeline ou la disponibilité des données.

6. **Gestion de projet:**
   - GoodAir souhaite suivre de près l’évolution du projet pour y apporter des précisions ou modifications si nécessaire. Le laboratoire souhaite donc que vous travailliez sur le projet de façon itérative, en proposant un **MVP (Minimum Viable Product)** qui sera amélioré à chaque itération.
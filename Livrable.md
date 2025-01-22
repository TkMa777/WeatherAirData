# Audit du projet de création d'une plateforme Big Data pour le laboratoire GoodAir

## 1. Introduction
**Objet:**

Réaliser une analyse de l'architecture actuelle de la plateforme Big Data utilisée par le laboratoire GoodAir pour évaluer son efficacité, sa sécurité et sa conformité aux exigences du projet.
            
**Brève description du projet :**

Le Laboratoire GoodAir surveille la qualité de l'air pour conseiller le public, étudier les impacts du changement climatique et déterminer des seuils d'alerte. La plateforme Big Data est utilisée pour collecter, traiter, stocker et analyser les données nécessaires à la recherche.
## 2. Présentation du système et de l'architecture

**Composants utilisés:**

- Apache Kafka: Utilisé pour collecter des données toutes les 20 secondes.
- Apache Spark: Traite les données provenant de Kafka et les envoie à AWS.
- AWS S3: Sert Data Lake pour stocker des données brutes.
- AWS Glue: Effectue les processus ETL, l'assurance qualité, le nettoyage et la transformation des données.
- AWS Athena: Utilisé pour analyser les données stockées dans S3 ou à partir du stockage Glue.
- Amazon Redshift: Base de données. stocke des données structurées pour un accès et une analyse rapides.
- ML 
- Tableau: Visualise les données pour fournir des rapports aux chercheurs.

**Schéma d'architecture:**

![Image caption](/images/Archi.png)


## 3. Collecte de données

**Processus de collecte de données:**

Les données sont collectées à l'aide d'Apache Kafka toutes les 20 secondes. Cela garantit la réception en temps opportun des données pour un traitement et une analyse ultérieurs.
**Les sources de données:**

- API openweathermap.org
- API aqicn.org

## 4. Stockage de données

**Data Lake S3, Base de données Redshift :**

Toutes les données brutes sont stockées dans AWS S3, permettant un stockage de données évolutif et une conservation à long terme.

Une fois traitées et nettoyées, les données sont chargées dans Amazon Redshift, où elles sont normalisées et optimisées pour un accès et une analyse rapides.

## 5. Traitement de la tranformation



**Usage Apache Spark:**

Apache Spark traite de grandes quantités de données provenant de Kafka et effectue les tâches de calcul nécessaires à la transformation et à l'analyse des données.

**Processus ETL avec AWS Glue:**

AWS Glue gère les processus ETL, y compris les contrôles de qualité des données et le nettoyage des données, afin de garantir des données de haute qualité pour une analyse plus approfondie.
## 6. Sécurité des données

**Mesures de sécurité:**

- AWS IAM: gère l'accès aux ressources AWS en fournissant l'authentification et l'autorisation des utilisateurs.
- Conformité au RGPD: toutes les données sont stockées et traitées conformément aux exigences du RGPD pour protéger les informations personnelles.

## 7. Qualité et fiabilité des données

**Vérification et nettoyage des données:**

La qualité des données est vérifiée et garantie à l'aide d'AWS Glue et d'Amazon Redshift. Les processus de nettoyage et de validation des données sont inclus dans les processus ETL pour maintenir une qualité élevée des données.
## 8. Historicisation des données



**Stockage des données historiques:**

Les données historiques sont stockées dans Redshift et peuvent être facilement restaurées si nécessaire, offrant un stockage de données à long terme et la possibilité d'analyser les données historiques.

Nous utilisons une **schéma étoilée dimensionnelle** pour organiser et structurer ces données, ce qui permet une analyse efficace et une gestion simplifiée.
![Image caption](/images/model.png)



## 9. Performances et évolutivité



**Évolutivité avec Apache Spark:**

Apache Spark fait face efficacement à l'augmentation du volume de données grâce à la possibilité d'évoluer en ajoutant de nouveaux Workers.
**Plans d'amélioration des performances:**


Le plan est d'utiliser AWS EC2 pour améliorer les performances et l'intégration d'Apache Kafka et Spark.

## 10. ML


![Image caption](/images/Archi.png)


# WeatherAirData

## Introduction

WeatherAirData est une application qui collecte des données météorologiques et de qualité de l'air à partir de différentes sources en temps réel, les traite à l'aide d'Apache Spark et les envoie à Kafka pour une gestion et une analyse ultérieures. L'application est conçue pour permettre une intégration fluide avec AWS S3 pour le stockage des données traitées.

Cette application est idéale pour les projets nécessitant :
- Le traitement de grandes quantités de données en streaming.
- L'intégration avec des systèmes distribués comme Kafka et Spark.
- L'analyse en temps réel des conditions météorologiques et de la qualité de l'air.

---

## Configuration

Le fichier `jobs/config.py` est ignoré dans le dépôt Git pour protéger les informations sensibles comme les clés AWS.

Avant de démarrer le projet, créez le fichier `config.py` en copiant `jobs/config_template.py` et en ajoutant vos propres clés et paramètres :
```bash
cp jobs/config_template.py jobs/config.py
```

Pour exécuter ce projet, assurez-vous que Docker et Docker Compose sont installés sur votre machine. Si vous utilisez AWS S3 pour stocker des données, configurez vos clés AWS avant de démarrer.

Pour démarrer tous les services nécessaires, exécutez la commande suivante dans le répertoire racine du projet :


```bash
docker-compose up -d
```

Une fois les services démarrés, vérifiez que tous les conteneurs fonctionnent en exécutant :

```bash
docker ps
```

Les conteneurs suivants devraient être visibles et actifs : zookeeper, broker, spark-master, spark-worker-1, spark-worker-2 et kafdrop.

Assurez-vous que le fichier spark-city.py est disponible dans le répertoire /opt/bitnami/spark/jobs à l’intérieur du conteneur Spark Master. Pour vérifier cela, exécutez la commande suivante :

```bash
docker exec -it weatherairdata-spark-master-1 ls /opt/bitnami/spark/jobs
```

Si le fichier est présent, vous pouvez exécuter votre application Spark en utilisant la commande suivante :
```bash
docker exec -it weatherairdata-spark-master-1 spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk:1.11.469 \
  /opt/bitnami/spark/jobs/spark-city.py
```

Après avoir exécuté cette commande, les données seront envoyées aux topics Kafka. Pour vérifier les données dans Kafka, connectez-vous au conteneur broker avec la commande suivante :

```bash
docker exec -it broker bash
```

Puis, vérifiez les messages dans les topics weather_data et quality_data :

```bash
kafka-console-consumer --bootstrap-server localhost:9092 --topic weather_data --from-beginning
kafka-console-consumer --bootstrap-server localhost:9092 --topic quality_data --from-beginning
```



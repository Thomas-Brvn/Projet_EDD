# Utiliser l'image officielle d'Airflow comme base
FROM apache/airflow:2.10.2

# Copier le fichier requirements.txt dans l'image
COPY requirements.txt /opt/airflow/requirements.txt

# Installer les dépendances supplémentaires
RUN if [ -e "/opt/airflow/requirements.txt" ]; then \
      python -m pip install --upgrade pip; \
      pip install -r /opt/airflow/requirements.txt; \
    fi

# Définir le répertoire de travail
WORKDIR /opt/airflow

# Exposer le port par défaut d'Airflow
EXPOSE 8080

# Définir la commande par défaut pour démarrer Airflow
CMD ["airflow", "webserver"]

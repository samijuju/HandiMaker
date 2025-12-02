# Utilisation d'une image Python légère
FROM python:3.12-slim-bookworm

# Variables d'environnement pour Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Installation de uv dans le conteneur
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Définir le dossier de travail
WORKDIR /app

# Copier les fichiers de définition de projet uv
COPY pyproject.toml .

# Installer les dépendances système (si besoin de compiler, sinon optionnel pour pure python)
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Installer les dépendances Python via uv dans l'environnement système du conteneur
# IMPORTANT : Comme uv sync --frozen va échouer si on a supprimé le lock
# On change temporairement pour régénérer le lock dans le build (solution de réparation)
# Une fois stable, on remettras --frozen
RUN uv sync --no-install-project

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

# Création des dossiers pour éviter les erreurs de permissions
RUN mkdir -p /app/staticfiles /app/media

# Collecter les fichiers statiques (CSS/JS) pour WhiteNoise
RUN python manage.py collectstatic --noinput

# Exposer le port interne
EXPOSE 8000

# Commande de démarrage avec Gunicorn (Serveur de production)
CMD ["gunicorn", "Handi.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
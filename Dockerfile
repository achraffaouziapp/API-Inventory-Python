# =========================
# Stage 1 : builder
# =========================
FROM python:3.11-slim AS builder

WORKDIR /app

# Copier uniquement les requirements pour profiter du cache Docker
COPY requirements.txt .

# Installer les dépendances dans un dossier isolé
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
       --target /install


# =========================
# Stage 2 : runtime
# =========================
FROM python:3.11-alpine AS runtime

WORKDIR /app

# Créer un utilisateur non-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copier les libs Python installées depuis le builder
COPY --from=builder /install /usr/local/lib/python3.11/site-packages

# Copier uniquement le code nécessaire
COPY app ./app

# Exposer le port de l’API
EXPOSE 5000

# Changer d’utilisateur
USER appuser

# Commande de lancement de l’API Flask
CMD ["python", "-m", "app.main"]

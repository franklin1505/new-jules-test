# API d'Authentification Personnalisée

## Description Courte
Cette API fournit un système d'authentification utilisateur personnalisé avec des fonctionnalités d'enregistrement, de connexion et de déconnexion. Les noms d'utilisateur et les mots de passe sont générés automatiquement lors de l'enregistrement.

## Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

## Installation Locale

1.  **Cloner le dépôt**:
    ```bash
    git clone <url-du-repo>
    cd <nom-du-repertoire-clone>
    ```
    (Remplacez `<url-du-repo>` et `<nom-du-repertoire-clone>` par les valeurs appropriées)

2.  **Créer un environnement virtuel**:
    ```bash
    python -m venv venv
    ```

3.  **Activer l'environnement virtuel**:
    -   Sur Windows:
        ```bash
        venv\Scripts\activate
        ```
    -   Sur macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Installer les dépendances**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration de la Base de Données

1.  **Appliquer les migrations**:
    Assurez-vous que votre base de données est configurée dans `settings.py` (par défaut, Django utilise SQLite, ce qui ne nécessite pas de configuration supplémentaire pour un démarrage rapide).
    ```bash
    python manage.py migrate
    ```

## Lancer le Serveur de Développement

1.  **Exécuter la commande**:
    ```bash
    python manage.py runserver
    ```
2.  **Accéder à l'API**:
    Par défaut, le serveur sera accessible à l'adresse `http://127.0.0.1:8000/`.

## Fonctionnalités d'Authentification

### Création de Compte (Register)
-   **Endpoint**: `POST /api/users/register/`
-   **Corps de la requête** (JSON):
    ```json
    {
        "email": "votre_email@example.com",
        "user_type": "client"
    }
    ```
    (Le champ `user_type` est optionnel et sa valeur par défaut est 'client'. Les options sont 'client' ou 'administrator'.)
-   **Réponse Succès** (JSON):
    ```json
    {
        "id": 1,
        "email": "votre_email@example.com",
        "user_type": "client",
        "username": "votre_e_x7g2", // Nom d'utilisateur généré
        "generated_password": "UnMotDePasseFort!" // Mot de passe généré
    }
    ```
    **Note importante**: Conservez précieusement le `generated_password` et le `username` retournés. Le mot de passe ne sera plus accessible après cette étape.

### Connexion (Login)
-   **Endpoint**: `POST /api/users/login/`
-   **Corps de la requête** (JSON):
    ```json
    {
        "username": "nom_utilisateur_genere",
        "password": "mot_de_passe_genere"
    }
    ```
-   **Réponse Succès** (JSON):
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
    Ces tokens (`access` et `refresh`) devront être utilisés pour les requêtes authentifiées.

### Déconnexion (Logout)
-   **Endpoint**: `POST /api/users/logout/`
-   **Authentification Requise**: Oui. Le token d'accès doit être fourni dans l'en-tête `Authorization`.
    ```
    Authorization: Bearer <votre_token_d_acces>
    ```
-   **Action**: Enregistre l'heure de déconnexion de l'utilisateur (`last_logout_time`).
-   **Réponse Succès** (JSON):
    ```json
    {
        "detail": "Successfully logged out."
    }
    ```

## Points d'API Principaux (Module Utilisateurs)

-   `POST /api/users/register/`: Création d'un nouvel utilisateur.
-   `POST /api/users/login/`: Connexion d'un utilisateur et obtention des tokens JWT.
-   `POST /api/users/login/refresh/`: Rafraîchissement du token d'accès JWT.
-   `POST /api/users/logout/`: Déconnexion d'un utilisateur.

(Note: Si un module `products` existe et est pertinent, ses points d'API pourraient être listés ici également.)

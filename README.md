# FitConnect Analytics Platform

Couche analytics construite autour de **FitConnect Hub** — une PWA fitness mobile-first avec coach IA que je développe en parallèle.

FitConnect Hub n'est pas encore en production, donc les données ici sont synthétiques. Mais le pipeline, lui, est réel : génération d'événements, modélisation Snowflake, calcul de KPIs, insights IA, et une API FastAPI par-dessus.

---

## Contexte

FitConnect Hub est une PWA fitness avec coach IA, suivi nutrition et sport, photos de progression, génération de trajets de marche et notifications intelligentes.

Ce projet c'est la partie data engineering autour de ce produit. L'idée : simuler la stack analytics qu'un vrai SaaS utiliserait pour comprendre si ses utilisateurs s'engagent, convertissent, ou churnent — et pourquoi.

---

## Ce qu'il y a dans ce repo

- Génération de données synthétiques (utilisateurs, événements, abonnements)
- Ingestion dans Snowflake et design du schéma (RAW → ANALYTICS)
- Modèles SQL écrits en style dbt
- Calcul de KPIs SaaS (DAU/WAU/MAU, MRR, ARR, churn, conversion premium)
- Insights hebdomadaires générés par IA via Snowflake Cortex + Claude Sonnet
- API FastAPI qui expose les KPIs et insights depuis les exports de démo
- Setup Docker
- Cahier des charges dashboard Power BI

---

## Architecture

```text
Génération de données (Python + Faker)
        │
        ▼
Exports CSV (data/raw/)
        │
        ▼
Snowflake — schéma RAW
        │
        ▼
Modèles SQL (dbt-style)
        │
        ▼
Snowflake — schéma ANALYTICS
        ├── Marts KPI
        ├── Marts Engagement
        ├── Marts Revenue
        ├── Insights IA (Snowflake Cortex)
        └── API FastAPI → Dashboard Power BI
```

---

## Données générées

Trois tables brutes principales :

| Table | Contenu |
|---|---|
| `RAW_USERS` | Profils utilisateurs |
| `RAW_EVENTS` | Événements produit |
| `RAW_SUBSCRIPTIONS` | Abonnements et churn |

Les événements simulés couvrent les vraies fonctionnalités de FitConnect Hub : inscription, onboarding, messages coach IA, repas enregistrés, estimation macros, entraînements, poids/eau/sommeil/humeur, photos de progression, trajets de marche, notifications, abonnements premium.

---

## Modèle analytics

STG_USERS / STG_EVENTS / STG_SUBSCRIPTIONS
│
▼
DIM_USERS / FACT_EVENTS / FACT_APP_SESSIONS
│
▼
MART_KPI_OVERVIEW / MART_ENGAGEMENT / MART_REVENUE
│
▼
AI_WEEKLY_INSIGHTS
---

## KPIs suivis

**Utilisateurs & Engagement**
- Utilisateurs totaux / premium
- Taux de conversion premium
- DAU / WAU / MAU
- Sessions, durée moyenne, événements par session
- Engagement coach IA, repas, entraînements, trajets, marches

**Revenus**
- Abonnements actifs / annulés
- MRR / ARR / Churn

---

## Insights IA avec Snowflake Cortex

Les insights sont générés directement dans Snowflake via Snowflake Cortex et Claude Sonnet, et stockés en JSON dans la table `AI_WEEKLY_INSIGHTS`.

```json
{
  "summary": "...",
  "anomalies": [],
  "recommendations": [],
  "next_actions": []
}
```

L'idée : montrer qu'une plateforme data peut produire non seulement des chiffres, mais aussi une lecture business directement exploitable.

---

## API FastAPI

```bash
# Lancer en local
python3 -m uvicorn api.main:app --reload

# Docs interactives
http://127.0.0.1:8000/docs
```

Endpoints disponibles :

GET /                   → statut
GET /health             → health check
GET /kpis/overview      → KPIs globaux
GET /kpis/engagement    → métriques engagement
GET /kpis/revenue       → métriques revenus
GET /insights/weekly    → insights IA de la semaine
---

## Lancer le projet

```bash
# Installer les dépendances
python3 -m pip install -r requirements.txt

# Générer les données synthétiques
python3 pipelines/generate_synthetic_data.py

# Lancer l'API
python3 -m uvicorn api.main:app --reload

# Ou via Docker
docker compose up --build

# Lancer les tests
python3 -m pytest
```

---

## Structure du projet

fitconnect-analytics-platform/
├── api/                    # API FastAPI
├── data/
│   ├── raw/                # CSV générés localement
│   ├── processed/
│   └── sample_exports/     # Exports utilisés pour la démo
├── dbt/                    # Modèles analytics versionnés
├── docs/                   # Documentation du modèle de données
├── pipelines/              # Génération et chargement des données
├── powerbi/                # Plan du dashboard Power BI
├── sql/                    # Scripts Snowflake et Cortex AI
├── tests/                  # Tests API
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
---

## Stack

`Python` `pandas` `Faker` `Snowflake` `SQL` `dbt-style` `Snowflake Cortex` `Claude Sonnet` `FastAPI` `Docker` `Power BI`

---

## État du projet

**Fait ✓**
- Génération de données synthétiques
- Tables RAW dans Snowflake
- Modélisation analytics SQL/dbt-style
- Marts KPI, engagement et revenus
- Insights IA avec Snowflake Cortex
- Exports de démonstration
- API FastAPI
- Configuration Docker
- Tests API
- Cahier des charges Power BI

**En cours**
- Finalisation du dashboard Power BI
- Captures d'écran
- Documentation finale avec visuels
- Amélioration de l'auth Snowflake pour automatiser entièrement dbt/loader

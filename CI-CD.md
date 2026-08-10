CI/CD & Deployment
===================

This document describes a simple CI/CD setup for this repo that builds, tests, and deploys the app as a container.
It includes GitHub Actions workflows for:

- CI: run tests and push a container image to GitHub Container Registry (GHCR)
- Deploy to Cloud Run: build container and deploy to Google Cloud Run
- Deploy to GKE: build container, push to GCR, and update a GKE deployment

Files added by automation
-------------------------
- Dockerfile — multi-stage build (build client, install Python deps, run uvicorn)
- .dockerignore
- docker-compose.dev.yml — local dev compose with backend and frontend dev server
- .github/workflows/ci.yml — CI (tests + build & push to GHCR)
- .github/workflows/cloud-run-deploy.yml — build & deploy to Cloud Run
- .github/workflows/gke-deploy.yml — build & deploy to GKE
- k8s/deployment.yaml — Kubernetes Deployment manifest (placeholder image)
- k8s/service.yaml — Kubernetes Service (LoadBalancer)

Cloud Run (recommended)
-----------------------
Why Cloud Run:
- Serverless: minimal infra to manage
- Integrates well with Cloud Build & Container Registry
- Good free tier for small projects; fast way to learn DevOps practices

Required repository secrets (GitHub):
- GCP_PROJECT — Google Cloud project ID
- GCP_SA_KEY — JSON service account key (Base64 or raw JSON). Must have permissions: Cloud Run Admin, Cloud Build Editor, Service Account User
- CLOUD_RUN_SERVICE — desired Cloud Run service name
- CLOUD_RUN_REGION — e.g. us-central1

Usage notes:
- The Cloud Run GitHub Action uses gcloud to build with Cloud Build and deploy the image.
- To create a service account key:
  1. In Google Cloud Console, create a service account.
  2. Grant roles: Cloud Run Admin, Cloud Build Editor, Service Account User.
  3. Create key (JSON) and add it to GitHub repo secrets as GCP_SA_KEY.

GKE
---
Why GKE:
- Great for learning Kubernetes and common production patterns
- Requires more setup: VPC, private clusters, node pools, ingress, LB, certs

Required repository secrets (GitHub):
- GCP_PROJECT
- GCP_SA_KEY
- GKE_CLUSTER — cluster name
- GKE_ZONE — cluster zone (or REGION)

Notes:
- The provided k8s manifests are a starting point. Replace gcr.io/PROJECT_ID/... with your project image paths or let the workflow build the image and update the deployment image via kubectl set image.

Local dev
---------
- docker-compose.dev.yml starts backend (uvicorn --reload) and client dev server (Vite).
- Use the included Dockerfile to build production images locally for testing:
  docker build -t personal-assistant-agent:local .
  docker run -p 8080:8080 --env PORT=8080 personal-assistant-agent:local

Security & secrets
------------------
- Never commit credentials.json, token.json, or .env to the repo.
- Add token.json, credentials.json, .env, venv/ to .gitignore (already present).
- Rotate keys if they are exposed and follow least privilege for service accounts.

Next steps & learning path
-------------------------
1. Create a GCP project and enable Cloud Run, Cloud Build, and GKE APIs.
2. Create a service account and add required roles; store its JSON key in GitHub secrets.
3. Push to main to trigger the Cloud Run workflow (or run workflow manually).
4. For GKE, create a cluster and set GKE_CLUSTER/GKE_ZONE secrets, then push to main to trigger deployment.

If you'd like, I can:
- Create a small Terraform template to provision the Cloud Run service & IAM (recommended for reproducible infra).
- Add health endpoints to the FastAPI app (/health) to support Kubernetes probes (I can add the endpoint and tests).
- Configure GitHub Actions to build to Artifact Registry instead of GCR (preferred in some organizations).


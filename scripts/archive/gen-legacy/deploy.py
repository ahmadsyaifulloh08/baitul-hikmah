#!/usr/bin/env python3
"""Deploy Baitul Hikmah to Cloudflare Pages via Wrangler.

Usage:
    python3 deploy.py          # Deploy production (main → baitul-hikmah.id)

Requires: wrangler installed
Env: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID
"""
import os, sys, subprocess

PROJECT = "baitul-hikmah"
OUT_DIR = os.path.join(os.path.dirname(__file__), "out")
ACCOUNT_ID = "e4cd70f84267e96fcb4391058053b995"


def deploy():
    if not os.path.exists(OUT_DIR):
        print(f"❌ {OUT_DIR} not found. Run 'npm run build' first.")
        sys.exit(1)

    print(f"🚀 Deploying production → baitul-hikmah.id")

    cmd = [
        "npx", "wrangler", "pages", "deploy", OUT_DIR,
        f"--project-name={PROJECT}",
        "--branch=main",
        "--commit-dirty=true",
    ]

    env = os.environ.copy()
    env.setdefault("CLOUDFLARE_ACCOUNT_ID", ACCOUNT_ID)

    if not env.get("CLOUDFLARE_API_TOKEN"):
        print("❌ CLOUDFLARE_API_TOKEN not set")
        sys.exit(1)

    result = subprocess.run(cmd, env=env, capture_output=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    deploy()

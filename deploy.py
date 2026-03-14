#!/usr/bin/env python3
"""Deploy Baitul Hikmah to Cloudflare Pages via Wrangler.

Usage:
    python3 deploy.py dev      # Deploy branch=develop → develop.baitul-hikmah.pages.dev
    python3 deploy.py prod     # Deploy branch=main → baitul-hikmah.id
    python3 deploy.py          # Default: dev

Requires: wrangler installed (node /tmp/wrangler-install/node_modules/wrangler/bin/wrangler.js)
Env: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID
"""
import os, sys, subprocess

WRANGLER = "/tmp/wrangler-install/node_modules/wrangler/bin/wrangler.js"
PROJECT = "baitul-hikmah"
OUT_DIR = os.path.join(os.path.dirname(__file__), "out")

ENVS = {
    "dev":  {"branch": "develop", "domain": "develop.baitul-hikmah.pages.dev"},
    "prod": {"branch": "main",    "domain": "baitul-hikmah.id"},
}


def deploy(env_name="dev"):
    if env_name not in ENVS:
        print(f"❌ Unknown env '{env_name}'. Use: dev | prod")
        sys.exit(1)

    cfg = ENVS[env_name]
    branch = cfg["branch"]

    if not os.path.exists(OUT_DIR):
        print(f"❌ {OUT_DIR} not found. Run 'npm run build' first.")
        sys.exit(1)

    if not os.path.exists(WRANGLER):
        print(f"❌ Wrangler not found at {WRANGLER}")
        print("   Install: cd /tmp && mkdir wrangler-install && cd wrangler-install && yarn add wrangler")
        sys.exit(1)

    print(f"🚀 Deploying [{env_name}] branch={branch} → {cfg['domain']}")

    cmd = [
        "node", WRANGLER, "pages", "deploy", OUT_DIR,
        f"--project-name={PROJECT}",
        f"--branch={branch}",
        "--commit-dirty=true",
    ]

    env = os.environ.copy()
    env.setdefault("CLOUDFLARE_API_TOKEN", "")
    env.setdefault("CLOUDFLARE_ACCOUNT_ID", "e4cd70f84267e96fcb4391058053b995")

    if not env["CLOUDFLARE_API_TOKEN"]:
        print("❌ CLOUDFLARE_API_TOKEN not set")
        sys.exit(1)

    result = subprocess.run(cmd, env=env, capture_output=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else "dev"
    deploy(env)

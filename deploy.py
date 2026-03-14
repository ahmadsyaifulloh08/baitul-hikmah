#!/usr/bin/env python3
"""Deploy to CF Pages using direct upload API."""
import os, sys, json, hashlib, uuid
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

API_TOKEN = os.environ.get("CF_API_TOKEN", "l-OSpBgNKqpeRoiE0VwDVqPDCDGnVJkqW6HiXc_p")
ACCOUNT_ID = "e4cd70f84267e96fcb4391058053b995"
PROJECT_NAME = "baitul-hikmah"
OUT_DIR = Path(__file__).parent / "out"

def deploy(branch="main"):
    # Collect files
    file_entries = {}
    for p in sorted(OUT_DIR.rglob("*")):
        if p.is_file():
            content = p.read_bytes()
            h = hashlib.sha256(content).hexdigest()
            rel = "/" + str(p.relative_to(OUT_DIR))
            file_entries[rel] = {"hash": h, "content": content}
    
    print(f"Found {len(file_entries)} files")
    
    # Build manifest
    manifest = {rel: info["hash"] for rel, info in file_entries.items()}
    
    # Step 1: Create deployment
    boundary = uuid.uuid4().hex
    manifest_json = json.dumps(manifest)
    
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="manifest"\r\n\r\n{manifest_json}\r\n'
        f'--{boundary}\r\nContent-Disposition: form-data; name="branch"\r\n\r\n{branch}\r\n'
        f'--{boundary}--\r\n'
    ).encode()
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments"
    req = Request(url, data=body, headers={
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }, method="POST")
    
    try:
        resp = urlopen(req, timeout=120)
        result = json.loads(resp.read())
    except HTTPError as e:
        print(f"❌ Create deployment: {e.code} {e.read().decode()[:500]}")
        sys.exit(1)
    
    print(f"Full response keys: {list(result.get('result', {}).keys())}")
    print(f"Has missing_hashes: {'missing_hashes' in result.get('result', {})}")
    deployment = result["result"]
    deploy_id = deployment["id"]
    jwt = deployment.get("jwt", "")
    missing = deployment.get("missing_hashes", [])
    
    print(f"✅ Deployment {deploy_id}")
    print(f"   Missing: {len(missing)} / {len(file_entries)}")
    print(f"   JWT present: {bool(jwt)}")
    print(f"   Keys: {list(deployment.keys())}")
    
    # Step 2: Upload ALL files (even if not "missing") to ensure they're there
    if jwt:
        upload_url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments/{deploy_id}/files"
        
        # Collect all unique hashes
        all_hashes = {}
        for rel, info in file_entries.items():
            all_hashes[info["hash"]] = info["content"]
        
        hashes_to_upload = missing if missing else list(all_hashes.keys())
        
        # Upload in batches
        batch_size = 50
        total = len(hashes_to_upload)
        for i in range(0, total, batch_size):
            batch = hashes_to_upload[i:i+batch_size]
            boundary2 = uuid.uuid4().hex
            parts = []
            
            for h in batch:
                if h in all_hashes:
                    parts.append(f'--{boundary2}\r\nContent-Disposition: form-data; name="{h}"; filename="{h}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode())
                    parts.append(all_hashes[h])
                    parts.append(b'\r\n')
            
            parts.append(f'--{boundary2}--\r\n'.encode())
            body2 = b''.join(parts)
            
            req2 = Request(upload_url, data=body2, headers={
                "Authorization": f"Bearer {jwt}",
                "Content-Type": f"multipart/form-data; boundary={boundary2}",
            }, method="POST")
            
            try:
                urlopen(req2, timeout=300)
                print(f"   Batch {i//batch_size + 1}/{(total+batch_size-1)//batch_size} ✓")
            except HTTPError as e:
                err = e.read().decode()[:300]
                if "duplicate" in err.lower() or "already" in err.lower():
                    print(f"   Batch {i//batch_size + 1}: already uploaded, skipping")
                else:
                    print(f"❌ Upload: {e.code} {err}")
                    sys.exit(1)
    
    # Step 3: Complete (always, even if no uploads needed)
    if jwt:
        complete_url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments/{deploy_id}/complete"
        req3 = Request(complete_url, data=b'', headers={
            "Authorization": f"Bearer {jwt}",
        }, method="PATCH")
        try:
            resp3 = urlopen(req3, timeout=60)
            print("✅ Deployment finalized!")
        except HTTPError as e:
            print(f"⚠️ Complete: {e.code} {e.read().decode()[:200]}")
    
    print(f"\n🌐 https://{deploy_id}.{PROJECT_NAME}.pages.dev")
    print(f"🌐 https://{PROJECT_NAME}.pages.dev")

if __name__ == "__main__":
    branch = sys.argv[1] if len(sys.argv) > 1 else "main"
    deploy(branch)

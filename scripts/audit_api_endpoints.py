import httpx
import time

client = httpx.Client(base_url="http://127.0.0.1:8000")

print("=" * 80)
print("COMPREHENSIVE BACKEND API AUDIT")
print("=" * 80)

endpoints = [
    # 1. Health
    ("GET", "/api/v1/health", None, None, 200),
    # 2. Branches
    ("GET", "/api/v1/branches", None, None, 200),
    # 3. Subjects
    ("GET", "/api/v1/subjects", None, None, 200),
    ("GET", "/api/v1/subjects?branch_id=1", None, None, 200),
    # 4. Vocabulary
    ("GET", "/api/v1/vocabulary", None, None, 200),
    ("GET", "/api/v1/vocabulary?search=circuit", None, None, 200),
    ("GET", "/api/v1/vocabulary?validation_status=verified", None, None, 200),
    ("GET", "/api/v1/vocabulary/1", None, None, 200),
    ("GET", "/api/v1/vocabulary/9999", None, None, 404), # non-existent ID
    # 5. Signs
    ("GET", "/api/v1/signs/1", None, None, 200),
    ("GET", "/api/v1/signs/9999", None, None, 404),
    # 6. History
    ("GET", "/api/v1/history?limit=10", None, None, 200),
    # 7. Translation
    ("POST", "/api/v1/translate", {"text": "What is a database?"}, None, 200),
    ("POST", "/api/v1/translate", {"text": ""}, None, 422), # empty validation error
    ("POST", "/api/v1/translate", {}, None, 422), # missing text
    # 8. Document upload validation
    ("POST", "/api/v1/documents/upload", None, {"file": ("malicious.sh", b"rm -rf /", "text/x-sh")}, 400),
]

for method, path, json_body, files, expected_status in endpoints:
    t0 = time.perf_counter()
    if method == "GET":
        resp = client.get(path)
    elif method == "POST":
        if files:
            resp = client.post(path, files=files)
        else:
            resp = client.post(path, json=json_body)
    duration_ms = (time.perf_counter() - t0) * 1000.0

    passed = (resp.status_code == expected_status)
    mark = "PASS" if passed else "FAIL"

    print(f"[{mark}] {method:4} {path:35} -> Status: {resp.status_code} (Expected: {expected_status}) | {duration_ms:.2f}ms")
    if not passed:
        print(f"       Response: {resp.text[:200]}")

# 9. Test CORS headers
cors_resp = client.options(
    "/api/v1/translate",
    headers={
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type"
    }
)
print(f"\nCORS Preflight Test: Status={cors_resp.status_code}")
print(f"  Access-Control-Allow-Origin: {cors_resp.headers.get('access-control-allow-origin')}")
print(f"  Access-Control-Allow-Methods: {cors_resp.headers.get('access-control-allow-methods')}")

client.close()


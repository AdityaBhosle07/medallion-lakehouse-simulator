import requests

BASE_URL = "http://127.0.0.1:8000"
ENDPOINTS = ["/api/profitability", "/api/utilization", "/api/benchmarking"]

def test_endpoints():
    for ep in ENDPOINTS:
        resp = requests.get(BASE_URL + ep)
        assert resp.status_code == 200, f"{ep} failed with {resp.status_code}: {resp.text}"
        data = resp.json()
        assert isinstance(data, list), f"{ep} did not return a list"
        assert len(data) > 0, f"{ep} returned empty list"
        print(f"PASS: {ep} returned {len(data)} records")

if __name__ == "__main__":
    test_endpoints()
import json
from pathlib import Path
from urllib.request import Request, urlopen

BASE_URL = "http://127.0.0.1:8000/chat"
CASES = Path(__file__).with_name("day3_conversations.jsonl")


def run():
    results = []
    for line in CASES.read_text(encoding="utf-8").splitlines():
        case = json.loads(line)
        payload = json.dumps({"session_id": case["session_id"], "message": case["message"]}).encode()
        req = Request(BASE_URL, data=payload, headers={"Content-Type": "application/json", "Accept": "application/json"}, method="POST")
        with urlopen(req, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
        results.append({
            "id": case["id"],
            "category": case["category"],
            "status": "ok",
            "analysis": body["analysis"],
            "response": body["response"],
            "retrieved_count": len(body.get("retrieved", [])),
        })
    out = Path(__file__).with_name("day3_runtime_results.json")
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Completed {len(results)} Day-3 conversations. Results: {out}")


if __name__ == "__main__":
    run()

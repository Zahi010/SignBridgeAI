import httpx
import json

client = httpx.Client(base_url="http://127.0.0.1:8000")

test_sentences = [
    "What is a database?",
    "Explain how an operating system works with memory.",
    "What is a deadlock in operating systems?",
    "Explain the difference between voltage and current.",
    "What is the function of a processor?",
    "How does a transformer work?",
    "Explain the concept of an algorithm.",
    "The database stores information.",
    "What is the relationship between memory and a processor?",
    "Explain deadlock prevention in operating systems."
]

print("=" * 80)
print("AUDITING TEXT-TO-ISL TRANSLATION PIPELINE (10 TEST CASES)")
print("=" * 80)

results = []

for idx, sentence in enumerate(test_sentences, 1):
    resp = client.post("/api/v1/translate", json={"text": sentence})
    if resp.status_code == 200:
        data = resp.json()
        extracted = [c["term"] for c in data["extracted_concepts"]]
        gloss = " ".join(data["isl_gloss_sequence"])
        status = data["status"]
        vid_avail = data["video_output"]["available"]
        vid_url = data["video_output"]["video_url"]
        avatar_avail = data["avatar_output"]["available"]
        latency = data.get("total_pipeline_duration_ms", 0.0)
        rules = [g["rule_type"] for g in data["grammar_notes"]]
        
        result_item = {
            "index": idx,
            "input": sentence,
            "status": status,
            "extracted_concepts": extracted,
            "gloss": gloss,
            "grammar_rules": rules,
            "video_available": vid_avail,
            "video_url": vid_url,
            "avatar_available": avatar_avail,
            "latency_ms": latency,
            "reason": data["status_reason"]
        }
        results.append(result_item)

        print(f"\n[Test {idx}] \"{sentence}\"")
        print(f"  Status:             {status.upper()}")
        print(f"  Extracted Concepts: {', '.join(extracted) if extracted else 'NONE'}")
        print(f"  ISL Gloss:          {gloss if gloss else 'NONE'}")
        print(f"  Grammar Rules:      {', '.join(rules) if rules else 'None'}")
        print(f"  Video Available:    {vid_avail} ({vid_url})")
        print(f"  Avatar Available:   {avatar_avail}")
        print(f"  Backend Latency:    {latency} ms")
        print(f"  Assessment:         {data['status_reason'][:120]}...")
    else:
        print(f"\n[Test {idx}] \"{sentence}\" FAILED with HTTP {resp.status_code}: {resp.text}")

client.close()


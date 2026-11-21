import httpx

client = httpx.Client(base_url="http://127.0.0.1:8000")

print("=" * 60)
print("TESTING DOCUMENT UPLOADS")
print("=" * 60)

# 1. Test DOCX Upload
with open("data/sample_lecture.docx", "rb") as f:
    r_docx = client.post(
        "/api/v1/documents/upload",
        files={"file": ("sample_lecture.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    )
print(f"1. DOCX Upload: Status = {r_docx.status_code}")
if r_docx.status_code == 200:
    d = r_docx.json()
    print(f"   - File Type: {d['file_type']}")
    print(f"   - Total Words: {d['total_words']}")
    print(f"   - Approx Pages: {d['page_or_slide_count']}")
    print(f"   - Detected Concepts Count: {d['detected_concepts_count']}")
    concepts = [c["term"] for c in d["translation_summary"]["extracted_concepts"]]
    print(f"   - Concepts: {concepts}")
else:
    print(f"   - Error: {r_docx.text}")

# 2. Test PPTX Upload
with open("data/sample_lecture.pptx", "rb") as f:
    r_pptx = client.post(
        "/api/v1/documents/upload",
        files={"file": ("sample_lecture.pptx", f, "application/vnd.openxmlformats-officedocument.presentationml.presentation")}
    )
print(f"\n2. PPTX Upload: Status = {r_pptx.status_code}")
if r_pptx.status_code == 200:
    d = r_pptx.json()
    print(f"   - File Type: {d['file_type']}")
    print(f"   - Total Slides: {d['page_or_slide_count']}")
    print(f"   - Total Words: {d['total_words']}")
    print(f"   - Detected Concepts Count: {d['detected_concepts_count']}")
    concepts = [c["term"] for c in d["translation_summary"]["extracted_concepts"]]
    print(f"   - Concepts: {concepts}")
else:
    print(f"   - Error: {r_pptx.text}")

# 3. Test Invalid Extension (.txt)
r_invalid = client.post(
    "/api/v1/documents/upload",
    files={"file": ("bad_file.txt", b"some plain text", "text/plain")}
)
print(f"\n3. Invalid Ext (.txt): Status = {r_invalid.status_code}")
print(f"   - Detail: {r_invalid.json().get('detail')}")

# 4. Test Empty File
r_empty = client.post(
    "/api/v1/documents/upload",
    files={"file": ("empty.pdf", b"", "application/pdf")}
)
print(f"\n4. Empty File: Status = {r_empty.status_code}")
print(f"   - Detail: {r_empty.json().get('detail')}")

client.close()


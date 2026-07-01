import os
import json
import anthropic
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

def extract_text_from_pdf(pdf_path):
    if PyPDF2 is None:
        return ""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text[:8000]

def extract_contract_dates(pdf_path, vendor_name=""):
    text = extract_text_from_pdf(pdf_path)
    if not text:
        return {"error": "Could not extract text from PDF"}

    prompt = (
        "Extract key dates from this vendor contract. Return JSON only, no other text.\n\n"
        "Contract text:\n" + text + "\n\n"
        "Return this exact JSON structure:\n"
        '{"vendor_name": "string", "contract_end_date": "YYYY-MM-DD or null", '
        '"auto_renewal_date": "YYYY-MM-DD or null", "notice_deadline": "YYYY-MM-DD or null", '
        '"contract_value": "string or null", "key_terms": "one sentence summary"}'
    )

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = msg.content[0].text.strip()
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = extract_contract_dates(sys.argv[1])
        print(json.dumps(result, indent=2))

"""Independent public GET checks; never sends repository data to a supplier."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
LANE = OUT.parents[2] / "luna47e"
matrix = json.loads((LANE / "artifacts/luna47e/primitive-matrix.json").read_bytes())
sources = {a+":"+s["id"]: s
           for a, p in matrix["source_catalogs"].items()
           for s in json.loads((LANE / p).read_bytes())["sources"]}


class LinkedData(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside = False
        self.scripts = []
        self.current = ""

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self.inside = True
            self.current = ""

    def handle_data(self, data):
        if self.inside:
            self.current += data

    def handle_endtag(self, tag):
        if tag == "script" and self.inside:
            self.scripts.append(self.current)
            self.inside = False


def fetch(component):
    candidates = [sources[s] for s in component["source_refs"]
                  if sources[s]["kind"] == "distributor"]
    source = candidates[0]
    url = source["url"]
    result = subprocess.run(
        ["curl.exe", "--silent", "--show-error", "--location", "--max-time", "60",
         "--write-out", "\n%{http_code}", url], capture_output=True, check=False)
    data, _, status = result.stdout.rpartition(b"\n")
    record = dict(part=component["part_number"], url=url,
                  retrieved_at_utc=datetime.now(timezone.utc).isoformat(),
                  curl_exit=result.returncode, http_status=status.decode(errors="replace"),
                  raw_sha256=hashlib.sha256(data).hexdigest(), raw_bytes=len(data),
                  raw_not_retained=True, shipping_owner_access="BLOCKED")
    parser = LinkedData()
    parser.feed(data.decode("utf-8", errors="replace"))
    products = []
    for script in parser.scripts:
        try:
            parsed = json.loads(script)
        except ValueError:
            continue
        values = parsed if isinstance(parsed, list) else parsed.get("@graph", [parsed])
        products.extend(v for v in values if v.get("@type") == "Product")
    matches = [p for p in products if p.get("mpn") == component["part_number"]]
    record["exact_product_matches"] = len(matches)
    record["selected_public_offer"] = [
        {k: p.get(k) for k in ("mpn", "offers")} for p in matches]
    record["result"] = ("independent exact-part public offer observed"
                        if status == b"200" and matches else
                        "BLOCKED: no independently parsed exact-part offer")
    return record


with ThreadPoolExecutor(max_workers=8) as pool:
    records = list(pool.map(fetch, matrix["components"]))
(OUT / "independent-public-offers.json").write_text(
    json.dumps(dict(records=records,
                    scope="Public offers, not supplier authenticity, delivery, owner access or circuit validation"),
               indent=2)+"\n", encoding="utf-8")
for r in records:
    print(r["part"], r["http_status"], r["exact_product_matches"], r["result"])

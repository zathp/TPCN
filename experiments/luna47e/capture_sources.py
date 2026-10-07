"""Public documentary evidence capture only; no circuit or TPCN execution.

Run from the lane root. Requires pypdf for PDF metadata/excerpts. Uses curl
without credentials/cookies, does not submit forms or circumvent access blocks.
Raw content is hashed in memory, not redistributed. Excerpts are limited.
The destination must not exist, so retained observations cannot be overwritten.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = [
    ("fpaa_store", "manufacturer_store", "https://okikadevices.com/products.json?limit=50"),
    ("fpaa_chip", "manufacturer", "https://okikadevices.com/products/an231e04-dynamically-reconfigurable-fpaa-chip-with-4-cabs"),
    ("fpaa_shield", "manufacturer", "https://okikadevices.com/products/flexanalog%E2%84%A2-arduino-shield"),
    ("fpaa_ds", "manufacturer_pdf", "https://okikadevices.com/cdn/shop/files/Okika_AN231E04DSv2.2.pdf?v=12643572874655327773"),
    ("fpaa_um", "manufacturer_pdf", "https://okikadevices.com/cdn/shop/files/FlexAnalog_AN231E04UM_User_Manual.pdf?v=9738655095111332330"),
    ("fpaa_boxcar", "manufacturer", "https://okikadevices.com/pages/boxcar-integration-an-example-using-an231e04-fpaa-in-a-pulse-induction-metal-detector"),
    ("fpaa_distributor", "distributor", "https://www.digikey.com/en/products/detail/okika-devices/AN231E04-QFNSP/28167850"),
    ("fpaa_board_distributor", "distributor", "https://www.digikey.com/en/products/detail/okika-devices/AN231K04-DUAL2/28167223"),
    ("legacy_anadigm", "manufacturer_legacy", "https://www.anadigm.com/an231e04.asp"),
    ("opamp_ds", "manufacturer_pdf", "https://www.ti.com/lit/ds/symlink/tlv9062.pdf"),
    ("comparator_ds", "manufacturer_pdf", "https://www.ti.com/lit/ds/symlink/tlv3201.pdf"),
    ("timer_ds", "manufacturer_pdf", "https://www.ti.com/lit/ds/symlink/lmc555.pdf"),
    ("pot_ds", "manufacturer_pdf", "https://ww1.microchip.com/downloads/en/DeviceDoc/11195c.pdf"),
    ("dac_ds", "manufacturer_pdf", "https://ww1.microchip.com/downloads/en/DeviceDoc/22248a.pdf"),
    ("cap_ds", "manufacturer_pdf", "https://www.tdk-electronics.tdk.com/inf/20/20/db/fc_2009/MKT_B32520_529.pdf"),
    ("cap_ds_mirror", "manufacturer_pdf_distributor_mirror", "https://datasheet.lcsc.com/datasheet/pdf/58115b0c2f21f05a3509bc03212563f4.pdf?productCode=C15523"),
    ("opamp_stock", "distributor", "https://www.lcsc.com/product-detail/C398355.html"),
    ("comparator_stock", "distributor", "https://www.lcsc.com/product-detail/C105188.html"),
    ("timer_stock", "distributor", "https://www.lcsc.com/product-detail/C90760.html"),
    ("pot_stock", "distributor", "https://www.lcsc.com/product-detail/C1539831.html"),
    ("dac_stock", "distributor", "https://www.lcsc.com/product-detail/C640392.html"),
    ("cap_stock", "distributor", "https://www.lcsc.com/product-detail/C15523.html"),
    ("diode_stock", "distributor", "https://www.lcsc.com/product-detail/C917479.html"),
    ("diode_ds", "manufacturer_pdf", "https://www.vishay.com/docs/81857/1n4148.pdf"),
    ("resistor_stock", "distributor", "https://www.lcsc.com/product-detail/C1364475.html"),
    ("resistor_ds_mirror", "manufacturer_pdf_distributor_mirror", "https://datasheet.lcsc.com/datasheet/pdf/78d4ba5bf7705bcd93e9318716385ddc.pdf?productCode=C1364475"),
    ("pot_page_block", "manufacturer", "https://www.microchip.com/en-us/product/MCP41010"),
    ("dac_page_block", "manufacturer", "https://www.microchip.com/en-us/product/MCP4921"),
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def capture(identity: str, kind: str, url: str, inspect_pdf: bool) -> dict:
    result = subprocess.run(
        ["curl.exe", "-L", "-sS", "--max-time", "60", "--max-filesize", "12000000",
         "-w", "\nLUNA47E_HTTP:%{http_code}:%{url_effective}", url],
        capture_output=True, timeout=75, check=False,
    )
    data, _, trailer = result.stdout.rpartition(b"\nLUNA47E_HTTP:")
    status, _, effective = trailer.decode("utf-8", errors="replace").partition(":")
    record = {
        "id": identity, "kind": kind, "url": url, "effective_url": effective,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": "curl.exe unauthenticated HTTPS GET, redirects followed",
        "http_status": status, "curl_exit": result.returncode,
        "raw_bytes": len(data), "raw_sha256": digest(data),
        "error": result.stderr.decode("utf-8", errors="replace").strip() or None,
        "state": "retrieved" if status == "200" and result.returncode == 0 else "unavailable",
    }
    if record["state"] != "retrieved":
        return record
    try:
        if data.startswith(b"%PDF"):
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            texts = [p.extract_text() or "" for p in reader.pages]
            record["pdf_pages"] = len(texts)
            record["pdf_metadata"] = {str(k): str(v) for k, v in (reader.metadata or {}).items()}
            words = ["integrator", "capacitor", "supply voltage", "operating conditions",
                     "quiescent", "current", "resolution", "tolerance", "hysteresis",
                     "absolute", "rectif", "oscillator", "clock"]
            excerpts = []
            for word in words:
                for page, text in enumerate(texts, 1):
                    match = re.search(re.escape(word), text, re.IGNORECASE)
                    if match:
                        excerpts.append({"page": page, "keyword": word,
                                         "text": text[max(0, match.start()-35):match.start()+110]})
                        break
            record["brief_excerpts"] = excerpts[:8]
            if inspect_pdf:
                print(f"\nPDF {identity}: {len(texts)} pages")
                for page, text in enumerate(texts, 1):
                    if page == 1 or re.search(
                        "recommended operating|electrical characteristics|switched capacitor|"
                        "Integrator|SumFilter|Rectifier|Capacitor Bank", text, re.I
                    ):
                        print(f"--- page {page} ---\n{text[:9500]}")
            return record
        text = data.decode("utf-8", errors="replace")
        if identity == "legacy_anadigm" and "/lander" in text:
            record["state"] = "unavailable"
            record["error"] = "Legacy endpoint returns JavaScript /lander redirect, not product evidence."
        elif identity == "fpaa_store":
            products = json.loads(text)["products"]
            record["offers"] = [
                {"title": p["title"], "handle": p["handle"],
                 "variants": [{k: v.get(k) for k in ("sku", "price", "available", "inventory_quantity")}
                              for v in p["variants"]]}
                for p in products if any(
                    v.get("sku") in ("AN231E04-QFNSP", "OTC2312", "AN231K04-DUAL2", "OTC9300L")
                    for v in p["variants"])
            ]
            record["price_currency"] = "Store price strings; USD not assumed without page currency evidence."
        elif "lcsc.com/product-detail" in url:
            scripts = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
                                 text, re.S)
            product = next((json.loads(s) for s in scripts if '"@type":"Product"' in s), None)
            if product:
                record["product"] = {k: product.get(k) for k in
                                     ("name", "sku", "mpn", "brand", "offers", "subjectOf")}
            prices = re.search(r'"productPriceList":(\[.*?\])', text, re.S)
            record["price_tiers"] = json.loads(prices.group(1)) if prices else None
            shipping = re.search(r'"overseasStockVO":(\{.*?\})', text, re.S)
            record["shipping_stock"] = json.loads(shipping.group(1)) if shipping else None
            if not product:
                record["state"] = "unavailable"
                record["error"] = "No identifiable product offer in response; do not infer stock."
        else:
            record["structured_price_currencies"] = sorted(set(
                re.findall(r'"priceCurrency"\s*:\s*"([A-Z]{3})"', text)
            ))
            clean = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.S)
            clean = re.sub(r"<[^>]+>", " ", clean)
            clean = re.sub(r"\s+", " ", clean)
            excerpts = []
            for word in ("integrat", "CAMs", "comparator", "oscillator", "capacitor", "SPI",
                         "supply", "rectif", "priceCurrency", "3.3"):
                m = re.search(word, clean, re.I)
                if m:
                    excerpts.append({"keyword": word, "text": clean[max(0,m.start()-35):m.start()+110]})
            record["brief_excerpts"] = excerpts[:8]
    except Exception as exc:
        record["processing_error"] = str(exc)
    return record


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--inspect-pdf", action="store_true")
    parser.add_argument("--only", help="Comma-separated source IDs; omitted captures all.")
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    allowed = (ROOT / "artifacts/luna47e").resolve()
    if not output.is_relative_to(allowed) or output.exists():
        raise SystemExit("Output must be a new file under artifacts/luna47e.")
    records = []
    selected = set(args.only.split(",")) if args.only else {s[0] for s in SOURCES}
    if not selected <= {s[0] for s in SOURCES}:
        raise SystemExit("Unknown source ID")
    for identity, kind, url in SOURCES:
        if identity not in selected:
            continue
        try:
            record = capture(identity, kind, url, args.inspect_pdf)
        except Exception as exc:
            record = {"id": identity, "kind": kind, "url": url, "state": "unavailable",
                      "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                      "error": str(exc)}
        records.append(record)
        print(identity, record["state"], record.get("http_status"), record.get("raw_sha256"))
    catalog = {"schema": "LUNA47E-SOURCES-1", "capture_revision": 1,
               "source_baseline": "2cef8ea4b37a4ae586e3f383511cba63c9268ddc",
               "authorization_revision": "789dda5988daf72f375d9713bd76a6da2b9e8b34",
               "capture_script_sha256": digest(Path(__file__).read_bytes()),
               "raw_policy": "Hashed in memory; only limited extracts and selected structured offers retained.",
               "sources": records}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
    print("Retained", output, digest(output.read_bytes()))


if __name__ == "__main__":
    main()

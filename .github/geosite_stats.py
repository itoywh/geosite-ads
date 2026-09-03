#!/usr/bin/env python3
"""Generate release-body ads stats from a built geosite.dat.

Usage: geosite_stats.py <geosite.dat> [<geosite.dat> ...]

Parses each v2ray geosite.dat (protobuf wire format, stdlib only) and prints a
markdown table of every CATEGORY-ADS-* category plus the aggregate
category-ads-all row. Meant to be embedded into GitHub Release notes by CI.
"""
import sys
from collections import Counter
from datetime import datetime, timezone


def read_varint(data, i):
    val, shift = 0, 0
    while True:
        b = data[i]; i += 1
        val |= (b & 0x7F) << shift
        shift += 7
        if not (b & 0x80):
            return val, i
        if shift > 70:
            raise ValueError("varint too long")


def parse_geosite(data):
    """Return {category: [(value, type), ...]}. Pure protobuf wire parsing."""
    result = {}
    i, n = 0, len(data)
    while i < n:
        if data[i] != 0x0A:
            break
        outer_len, j = read_varint(data, i + 1)
        record_end = j + outer_len
        if record_end > n:
            break
        if j >= record_end or data[j] != 0x0A:
            i = record_end
            continue
        code_len, k = read_varint(data, j + 1)
        code = data[k:k + code_len].decode("utf-8", "replace")
        k += code_len
        domains = []
        while k < record_end:
            if data[k] != 0x12:
                break
            dl, m = read_varint(data, k + 1)
            msg_end = m + dl
            dtype, value = None, None
            p = m
            while p < msg_end:
                t = data[p]
                if t == 0x08:
                    dtype, v = read_varint(data, p + 1)
                    p = v
                elif t == 0x12:
                    vl, v = read_varint(data, p + 1)
                    value = data[v:v + vl].decode("utf-8", "replace")
                    p = v + vl
                else:
                    p = msg_end
            domains.append((value, dtype))
            k = msg_end
        result[code] = domains
        i = record_end
    return result


def category_stats(domains):
    cnt = Counter(t for _, t in domains)
    plain = len({v for v, t in domains if t in (0, 2) and v})
    return len(domains), plain, cnt.get(3, 0)


def fmt_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    # Sources maintained by this fork (2026-09-02 decision: official + AW only).
    # Categories present upstream but NOT maintained here (e.g. category-ads-ir)
    # are intentionally not listed.
    SOURCES = (
        ("CATEGORY-ADS-OFFICIAL", "official"),
        ("CATEGORY-ADS-AWAVENUEADSRULE", "aw"),
    )
    for path in sys.argv[1:]:
        try:
            data = open(path, "rb").read()
        except OSError as e:
            print(f"{path}: {e}", file=sys.stderr)
            continue
        g = parse_geosite(data)
        rows = []
        for code, short in SOURCES:
            doms = g.get(code)
            if doms is None:
                rows.append((short, "MISSING", "-", "-"))
                continue
            total, plain, full = category_stats(doms)
            rows.append((short, total, plain, full))
        all_doms = g.get("CATEGORY-ADS-ALL")
        all_row = None
        if all_doms is not None:
            all_row = ("all (union)",) + category_stats(all_doms)
        print(f"## Ads rules in geosite.dat ({fmt_time()})")
        print()
        print("| source | total | domain/suffix | full: |")
        print("|---|---|---|---|")
        for short, total, plain, full in rows:
            print(f"| category-ads-{short} | {total} | {plain} | {full} |")
        if all_row:
            print(f"| {all_row[0]} | {all_row[1]} | {all_row[2]} | {all_row[3]} |")
        print()
        print("Notes:")
        print("- `category-ads-official`: upstream v2fly `category-ads-all` subset (raw include index, expanded at build time).")
        print("- `category-ads-aw`: AWAvenueAdsRule subset (advertising + privacy scope).")
        print("- `category-ads-all` = union of official + aw; count is not the sum of the two above because overlapping domains are absorbed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

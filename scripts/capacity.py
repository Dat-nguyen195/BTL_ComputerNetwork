#!/usr/bin/env python3
"""Reproduce Step 3 from CSV. Results are known-load estimates, not measurements."""
import argparse
import csv
import io
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITES = ("Main", "DBP", "BHTQ")


def inputs(path):
    with Path(path).open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    data = {}
    for row in rows:
        key = row["parameter"], row["site"]
        if key in data:
            raise ValueError(f"Duplicate input: {key}")
        data[key] = None if not row["value"] else float(row["value"])
    return data


def calculate(data, server_scope="per-device", guests=(0, 0, 0),
              guest_scope="per-device", overhead=0.0,
              down_share=1.0, up_share=1.0, guest_upload=None):
    def get(name, site="all"):
        value = data[name, site]
        if value is None or not math.isfinite(value) or value < 0:
            raise ValueError(f"Missing/negative input: {name}/{site}")
        return value

    if server_scope not in ("per-device", "per-site", "global"):
        raise ValueError("Invalid server scope")
    if guest_scope not in ("per-device", "global"):
        raise ValueError("Invalid guest scope")
    if len(guests) != 3 or any(n < 0 or int(n) != n for n in guests):
        raise ValueError("Three nonnegative integer guest counts required")
    if not all(math.isfinite(v) for v in (overhead, down_share, up_share)) or overhead < 0 or not 0 <= down_share <= 1 or not 0 <= up_share <= 1:
        raise ValueError("Overhead >= 0; Internet shares must be in [0, 1]")
    if guest_upload is not None and (not math.isfinite(guest_upload) or guest_upload < 0):
        raise ValueError("Guest upload must be nonnegative")
    if not 0 < get("target_utilization") <= 1 or not 0 < get("peak_fraction") <= 1:
        raise ValueError("Utilization and peak fraction must be in (0, 1]")
    if get("peak_window") == 0:
        raise ValueError("Peak window must be positive")
    peak_factor = 8 * get("peak_fraction") / (get("peak_window") * 3600)
    design_factor = (1 + get("growth_5years")) * (1 + overhead) / get("target_utilization")
    totals = [0.0, 0.0]
    result = []

    def metrics(site, down, up):
        peak_down, peak_up = down * peak_factor, up * peak_factor
        design_down, design_up = peak_down * design_factor, peak_up * design_factor
        return dict(site=site, down_mb_day=down, up_mb_day=up,
                    peak_down_mbps=peak_down, peak_up_mbps=peak_up,
                    design_down_mbps=design_down, design_up_mbps=design_up,
                    internet_down_mbps=design_down * down_share,
                    internet_up_mbps=design_up * up_share,
                    guest_upload="UNKNOWN" if guest_upload is None else "specified",
                    scope="KNOWN LOAD ONLY; camera/PACS/backup extras unquantified")

    for site, count in zip(SITES, guests):
        server_count = get("servers", site) if server_scope == "per-device" else int(server_scope == "per-site")
        down = get("workstations", site) * get("workstation_download") + server_count * get("server_download")
        up = get("workstations", site) * get("workstation_upload") + server_count * get("server_upload")
        if guest_scope == "per-device":
            down += count * get("guest_download")
        up += count * (guest_upload or 0)
        totals[0] += down
        totals[1] += up
        # Global totals cannot be assigned to a site without an extra assumption.
        if server_scope != "global" and guest_scope != "global":
            result.append(metrics(site, down, up))
    if server_scope == "global":
        totals[0] += get("server_download")
        totals[1] += get("server_upload")
    if guest_scope == "global":
        totals[0] += get("guest_download")
    result.append(metrics("TOTAL", *totals))
    return result


def as_csv(rows):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: f"{v:.6f}" if isinstance(v, float) else v for k, v in row.items()})
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=ROOT / "docs/03-capacity/capacity-inputs.csv")
    parser.add_argument("--server-scope", choices=("per-device", "per-site", "global"), default="per-device")
    parser.add_argument("--guest-scope", choices=("per-device", "global"), default="per-device")
    parser.add_argument("--guests", type=int, nargs=3, default=(0, 0, 0), metavar=("MAIN", "DBP", "BHTQ"))
    parser.add_argument("--overhead", type=float, default=0, help="extra traffic ratio; e.g. 0.10, not a measured fact")
    parser.add_argument("--internet-down-share", type=float, default=1)
    parser.add_argument("--internet-up-share", type=float, default=1)
    parser.add_argument("--guest-upload-mb", type=float, default=None, help="MB/day/guest; omitted means unknown")
    args = parser.parse_args()
    try:
        rows = calculate(inputs(args.inputs), args.server_scope, args.guests,
                         args.guest_scope, args.overhead, args.internet_down_share,
                         args.internet_up_share, args.guest_upload_mb)
    except (ValueError, KeyError) as exc:
        parser.error(str(exc))
    print(as_csv(rows), end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env bash
set -euo pipefail
cd '/media/nguyen-dat/New Volume/HK1_261/ComputerNetwork/BTL/BTL_2'
python3 scripts/collect_packet_tracer.py --input test_results/packet-tracer/verification-guided-20261111-224618/lab.pkt --output test_results/packet-tracer/verification-guided-20261111-224618/evidence
python3 scripts/check_packet_runtime.py --run test_results/packet-tracer/verification-guided-20261111-224618/evidence --project test_results/packet-tracer/verification-guided-20261111-224618/lab.pkt > test_results/packet-tracer/verification-guided-20261111-224618/checker.txt 2>&1
cat test_results/packet-tracer/verification-guided-20261111-224618/checker.txt

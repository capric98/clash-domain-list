#!/usr/bin/env python3
# coding=utf-8
from email import policy
import os

source_dir = "data"
output_dir = "output"

jobs = {
    "cn": {
        "data": ["cn"],
        "policy": "DIRECT"
    },
    "netflix": {
        "data": ["netflix"],
        "policy": "${POLICY}"
    },
    "ADs": {
        "data": ["category-ads"],
        "policy": "${POLICY}"
    },
    "scholar": {
        "data": ["category-scholar-cn", "category-scholar-!cn"],
        "policy": "${POLICY}"
    }
}

def parse_file(file: str, policy: str) -> list[str]:
    rules = []

    file = os.path.join(source_dir, file)
    if not os.path.exists(file): return rules
    print("Parsing: "+file)

    with open(file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # print(" ", line)
            if not line: continue
            elif line.startswith("#"): continue
            elif line.startswith("regexp:"): continue
            elif line.startswith("include:"):
                tmp_rules = parse_file(line[8:], policy)
                if tmp_rules: rules += tmp_rules
            else:
                rule = parse_line(line, policy)
                if rule: rules.append(rule)

    return rules

def parse_line(line: str, policy: str) -> str:
    domain = ""

    if line.find("#")!=-1: line = line[:line.find("#")]
    if line.find("@")!=-1: line = line[:line.find("@")]

    line = line.strip()
    if not line: return domain # empty line

    if line.startswith("full:"):
        domain = "  - {}, {}, {}".format("DOMAIN", line[5:], policy)
    elif line.startswith("domain:"):
        domain = "  - {}, {}, {}".format("DOMAIN-SUFFIX", line[7:], policy)
    elif line.startswith("keyword:"):
        domain = "  - {}, {}, {}".format("DOMAIN-KEYWORD", line[8:], policy)
    else:
        domain = "  - {}, {}, {}".format("DOMAIN-SUFFIX", line, policy)

    return domain

if __name__=="__main__":
    for k in jobs:
        job = jobs[k]
        if "policy" not in job: job["policy"] = "${POLICY}"

        if isinstance(job["data"], list):
            rules = []
            for f in job["data"]:
                rules += parse_file(f, job["policy"])
        elif isinstance(job["data"], str):
            rules = parse_file(job["data"], job["policy"])
        else: rules = None

        if rules:
            with open(os.path.join(output_dir, k+".yaml"), mode="w", encoding="utf-8") as f:
                for rule in rules:
                    print(rule, file=f)

                print("", file=f)
                print("  # - MATCH, DIRECT", file=f)
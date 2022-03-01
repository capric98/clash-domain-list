#!/usr/bin/env python3
# coding=utf-8
import os

source_dir = "data"
output_dir = "output"

jobs = [
    "netflix",
    "geolocation-cn",
    "category-ads",
    "category-scholar-cn",
    "category-scholar-!cn",
]

def parse_file(file: str) -> list[str]:
    file = os.path.join(source_dir, file)
    if not os.path.exists(file): return None
    print("Parsing: "+file)

    rules = []
    with open(file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # print(" ", line)
            if not line: continue
            elif line.startswith("#"): continue
            elif line.startswith("regex:"): continue
            elif line.startswith("include:"):
                tmp_rules = parse_file(line[8:])
                if tmp_rules: rules = rules + tmp_rules
            else:
                rule = parse_line(line)
                if rule: rules.append(rule)

    return rules

def parse_line(line: str) -> str:
    domain = ""

    if line.find("#")!=-1: line = line[:line.find("#")]
    if line.find("@")!=-1: line = line[:line.find("@")]

    line = line.strip()
    if not line: return domain # empty line

    if line.startswith("full:"):
        domain = "  - {}, {}, {}".format("DOMAIN", line[5:], "${POLICY}")
    elif line.startswith("domain:"):
        domain = "  - {}, {}, {}".format("DOMAIN-SUFFIX", line[7:], "${POLICY}")
    elif line.startswith("keyword:"):
        domain = "  - {}, {}, {}".format("DOMAIN-KEYWORD", line[8:], "${POLICY}")
    else:
        domain = "  - {}, {}, {}".format("DOMAIN-SUFFIX", line, "${POLICY}")

    return domain

if __name__=="__main__":
    for job in jobs:
        rules = parse_file(job)
        if rules:
            with open(os.path.join(output_dir, job+".yaml"), mode="w", encoding="utf-8") as f:
                for rule in rules:
                    print(rule, file=f)

                print("", file=f)
                print("  # - MATCH, DIRECT", file=f)
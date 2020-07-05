#!/usr/bin/env python3
import os
import parse

if __name__=="__main__":
    os.chdir("data")

    print("  # CN sites -> DIRECT")
    print("  - DOMAIN-SUFFIX,cn,DIRECT")
    cns = parse.parse_file("geolocation-cn")
    for d in cns:
        print("  - ", d.type, ",", d.domain, ",", "DIRECT", sep="")

    print("")
    print("  # Ads -> REJECT")
    ads = parse.parse_file("category-ads-all")
    for d in ads:
        print("  - ", d.type, ",", d.domain, ",", "REJECT", sep="")
from typing import List

class Domain:
    def __init__(self, domain):
        self.domain = domain
        self.type = ""

def parse_file(file: str) -> List[Domain]:
    domain_list = []
    with open(file, encoding="UTF-8") as f:
        for line in f:
            if line[-1]=="\n":
                line = line[:-1]
            if len(line)==0:
                continue
            if line[0]=="#":
                continue
            if line.find("regex:")!=-1:
                continue
            if line.find("include:")!=-1:
                domain_list = domain_list + parse_file(line[line.find("include:")+8:])
                continue

            domain_list.append(parse_line(line))

    return domain_list

def parse_line(line: str) -> Domain:
    domain = Domain("")
    domain.type = "DOMAIN-SUFFIX"

    if line.find("#")!=-1:
        line = line[:line.find("#")]
    if line.find("@")!=-1:
        line = line[:line.find("@")]
    while line[-1]==" ":
        line = line[:-1]

    if line.find("full:")!=-1 and line[:5]=="full:":
        line = line[5:]
        domain.type = "DOMAIN"
    if line.find("domain:")!=-1 and line[:7]=="domain:":
        line = line[7:]
        domain.type = "DOMAIN-SUFFIX"
    if line.find("keyword:")!=-1 and line[:8]=="keyword:":
        line = line[8:]
        domain.type = "DOMAIN-KEYWORD"

    domain.domain = line

    return domain
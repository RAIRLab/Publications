
import json 
import urllib.request
import xml.etree.ElementTree as ET

DBLP_PID_ENTRYPOINT = "https://dblp.dagstuhl.de/pid/"

class Publication:
    def __init__(self, obj, bibstr):
        self.title = obj.find(".//title").text #Title acts as ID
        self.bibstr = bibstr
        
        try:
            self.authorPIDs = [o.attrib["name"] for o in obj.find(".//author")]
        except Exception:
            try: #If author is not present, fallback to editors
                self.authorPIDs = [o.attrib["name"] for o in obj.find(".//editor")]
            except Exception:
                self.authorPIDs = []
        
        try:
            self.year = int(obj.find(".//year").text)
        except Exception:
            self.year = 0
        
    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)

class Member:
    def __init__(self, obj) -> None:
        print(f"Fetching {obj['name']}'s publications from DBLP...")
        self.name = obj["name"]
        self.pid = obj["id"]
        self.perm = obj["perm"]
        url = DBLP_PID_ENTRYPOINT + self.pid
        rawXML = urllib.request.urlopen(url + ".xml").read().decode("utf-8")
        rawBib = urllib.request.urlopen(url + ".bib").read().decode("utf-8")
        bibs = rawBib.split("\n\n")[:-1] # split bib file by entry 
        xmlTree = ET.fromstring(rawXML)
        xmlPubs = xmlTree.findall(".//r") #This has to work since being in DBLP means having at least one publication
        assert len(xmlPubs) == len(bibs), "Number of publications in XML and BIB file do not match"
        self.pubs = [Publication(x, b) for x, b in zip(xmlPubs, bibs)]

    def pubsByYear(self):
        """Returns a list of publications, partially sorted by year."""
        return sorted(self.pubs, key=lambda x: x.year)
    
    def __eq__(self, other):
        return self.pid == other.pid

    def __hash__(self):
        return hash(self.pid)

if __name__ == '__main__':
    with open('members.json', 'r') as f:
        members = json.load(f)
    members = [Member(obj) for obj in members] 
    memberPIDmap = {m.pid: m for m in members}

    #DBLP gives us a list of publications for each member. 
    #We want to use this data to create a list of publications with their authors instead.

    pubAuthors = {} #Maps a publication title to its RAIR affiliated authors
    for m in members:
        for p in m.pubs:
            if p.title in pubAuthors:
                pubAuthors[p.title][1].append(m)
            else:
                pubAuthors[p.title] = [p, [m]]

    #Prunes members from a papers author list if they are not a "current member". 
    #Being a current member at time of publication is defined as 8 years away from a member's first publication
    #coauthored with Selmer Bringsjord, or being marked as a permanent member.
    for m in members:
        if m.perm:
            continue
        firstSelmerPub = None
        for p in m.pubsByYear():
            if "99/3934" in p.authorPIDs: #Selmer Bringsjord's PID
                firstSelmerPub = p
                break
        if firstSelmerPub is None:
            continue
        for p in m.pubs:
            if p.year - firstSelmerPub.year > 8:
                break
            if p.title in pubAuthors:
                pubAuthors[p.title][1].remove(m) 

    #Prunes publications with less than 2 current members as authors
    pubAuthors2 = {k: v for k, v in pubAuthors.items() if len(v[1]) > 1}

    #group publications by year
    pubsByYear = {}
    for _, v in pubAuthors2.items():
        p = v[0]
        if p.year in pubsByYear:
            pubsByYear[p.year].append(p)
        else:
            pubsByYear[p.year] = [p]

    #Iterate over the years in reverse order and generate an inline tex bibtex string for each year
    texBibFileStr = ""

    for year in sorted(pubsByYear.keys(), reverse=True):
        bibStr = "\n\n".join([p.bibstr for p in pubsByYear[year]])
        texBibFileStr += f"""
\\begin{{filecontents}}{{{year}.bib}}
    {bibStr}
\\end{{filecontents}}
\\begin{{refsection}}[{year}.bib]
    \\nocite{{*}}
    \\printbibliography[title={year}, heading=bibliography]
\\end{{refsection}}
"""
    texBibFile = texBibFileStr.encode("ascii", "backslashreplace")
    #write the tex file
    with open("publications.tex", "wb") as f:
        f.write(texBibFile)

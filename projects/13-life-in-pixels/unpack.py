import re
import sys

GUN = (
    "24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$"
    "2o8bo3bob2o4bobo$10bo5bo7bo$11bo3bo$12b2o!"
)
pattern = sys.argv[1] if len(sys.argv) > 1 else GUN

unpacked = re.sub(r"(\d+)(.)", lambda found: found[2] * int(found[1]), pattern)
for row in unpacked.rstrip("!").split("$"):
    print(row.replace("b", "  ").replace("o", "██"))

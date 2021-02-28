import blueprint
import fluids
import json


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def station_name(entities):
    return "[virtual-signal=ltn-cleanup-station] " + ' '.join(["[fluid=" + f + "]" for f in entities])


def process(base, entities):
    entities = entities + ["water"] * (12 - len(entities))
    return base.replace('"type": "virtual", "name": "signal-0"', '"type": "fluid", "name": "' + entities[0] + '"')\
        .replace('"type": "virtual", "name": "signal-1"', '"type": "fluid", "name": "' + entities[1] + '"')\
        .replace('"type": "virtual", "name": "signal-2"', '"type": "fluid", "name": "' + entities[2] + '"')\
        .replace('"type": "virtual", "name": "signal-3"', '"type": "fluid", "name": "' + entities[3] + '"')\
        .replace('"type": "virtual", "name": "signal-4"', '"type": "fluid", "name": "' + entities[4] + '"')\
        .replace('"type": "virtual", "name": "signal-5"', '"type": "fluid", "name": "' + entities[5] + '"')\
        .replace('"type": "virtual", "name": "signal-6"', '"type": "fluid", "name": "' + entities[6] + '"')\
        .replace('"type": "virtual", "name": "signal-7"', '"type": "fluid", "name": "' + entities[7] + '"')\
        .replace('"type": "virtual", "name": "signal-8"', '"type": "fluid", "name": "' + entities[8] + '"')\
        .replace('"type": "virtual", "name": "signal-9"', '"type": "fluid", "name": "' + entities[9] + '"')\
        .replace('"type": "virtual", "name": "signal-A"', '"type": "fluid", "name": "' + entities[10] + '"')\
        .replace('"type": "virtual", "name": "signal-B"', '"type": "fluid", "name": "' + entities[11] + '"')\
        .replace("[station-name]", station_name(entities))


if __name__ == "__main__":
    gas_base = json.dumps(blueprint.from_file("./gas_stop.json"))
    liquid_base = json.dumps(blueprint.from_file("./liquid_stop.json"))

    sheets = []
    i = 1
    for chunk in chunks(fluids.gasses, 12):
        sheets.append(blueprint.sheet(json.loads(process(gas_base, chunk)), f"Gas venting #{i}"))
        i += 1

    i = 1
    for chunk in chunks(fluids.liquids, 12):
        sheets.append(blueprint.sheet(json.loads(process(liquid_base, chunk)), f"Liquid sinking #{i}"))
        i += 1

    print(blueprint.encode(blueprint.book(sheets)))

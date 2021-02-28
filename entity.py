from enum import Enum


def py_gas_vent(id, pos):
    return {
        "entity_number": id,
        "name": "py-gas-vent",
        "position": {
            "x": pos["x"],
            "y": pos["y"]
        },
        "direction": pos["dir"].value
    }


def train_stop(id, pos, connections, name):
    return {
        "entity_number": id,
        "name": "train-stop",
        "position": {
                "x": pos["x"],
                "y": pos["y"]
        },
        "direction": pos["dir"].value,
        "control_behavior": {
            "train_stopped_signal": {
                "type": "virtual",
                "name": "signal-T"
            }
        },
        "connections": {
            "1": {
                "green": [{"entity_id": e} for e in connections]
            }
        },
        "station": name
    }


def power_pole(id, pos, connections):
    return {
        "entity_number": id,
        "name": "medium-electric-pole",
        "position": {
            "x": pos["x"],
            "y": pos["y"]
        },
        "neighbours": connections
    }


def pump(id, pos, allow, connections):
    return {
        "entity_number": id,
        "name": "pump",
        "position": {
                "x": pos["x"],
                "y": pos["y"]
        },
        "direction": pos["dir"].value,
        "control_behavior": {
            "circuit_condition": {
                "first_signal": {
                    "type": "fluid",
                    "name": allow
                },
                "second_signal": {
                    "type": "virtual",
                    "name": "signal-T"
                },
                "comparator": ">"
            }
        },
        "connections": {
            "1": {
                "green": [{"entity_id": e} for e in connections]
            }
        }
    }


def straight_rail(id, pos):
    return {
        "entity_number": id,
        "name": "straight-rail",
        "position": {
                "x": pos["x"],
                "y": pos["y"]
        },
        "direction": pos["dir"].value
    }


def rail_signal(id, pos):
    return {
        "entity_number": id,
        "name": "rail-signal",
        "position": {
                "x": pos["x"],
                "y": pos["y"]
        },
        "direction": pos["dir"].value
    }


class Direction(Enum):
    north = 0
    northeast = 1
    east = 2
    southeast = 3
    south = 4
    southwest = 5
    west = 6
    northwest = 7

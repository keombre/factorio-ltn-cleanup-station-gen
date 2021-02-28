import entity
import blueprint
import fluids
from entity import Direction


def generate_pump_row(prev_id, pos, fluids, conn_first=None, conn_last=None):
    ret = []
    i = 0
    for fluid in fluids:
        con = []
        if conn_first and i == 0:
            con.append(conn_first)
        else:
            con.append(prev_id + i)
        if conn_last and i == len(fluids) - 1:
            con.append(conn_last)
        else:
            con.append(prev_id + i + 2)
        ret.append(entity.pump(
            prev_id + i + 1, {"x": pos["x"] + i, "y": pos["y"], "dir": pos["dir"]}, fluid, con))
        i += 1
    return ret


def generate_gas_vent_row(prev_id, pos):
    return [entity.py_gas_vent(prev_id + i + 1, {"x": pos["x"] + i, "y": pos["y"], "dir": pos["dir"]}) for i in range(6)]


def generate_bottom_void_row(prev_id, pos, fluids, conn_first=None, conn_last=None):
    return generate_pump_row(prev_id, {"x": pos["x"] + 1, "y": pos["y"] + 0, "dir": Direction.south}, fluids, conn_first, prev_id + 6) + \
        generate_gas_vent_row(prev_id + 24, {"x": pos["x"] + 1, "y": pos["y"] + 1, "dir": Direction.west}) + \
        generate_pump_row(prev_id + 6, {"x": pos["x"] + 8, "y": pos["y"] + 0, "dir": Direction.south}, fluids, prev_id + 6, prev_id + 12) + \
        generate_gas_vent_row(prev_id + 30, {"x": pos["x"] + 8, "y": pos["y"] + 1, "dir": Direction.west}) + \
        generate_pump_row(prev_id + 12, {"x": pos["x"] + 15, "y": pos["y"] + 0, "dir": Direction.south}, fluids, prev_id + 12, prev_id + 18) + \
        generate_gas_vent_row(prev_id + 36, {"x": pos["x"] + 15, "y": pos["y"] + 1, "dir": Direction.west}) + \
        generate_pump_row(prev_id + 18, {"x": pos["x"] + 22, "y": pos["y"] + 0, "dir": Direction.south}, fluids, prev_id + 18, conn_last) + \
        generate_gas_vent_row(
            prev_id + 42, {"x": pos["x"] + 22, "y": pos["y"] + 1, "dir": Direction.west})


def generate_top_void_row(prev_id, pos, fluids, conn_first=None, conn_last=None):
    return generate_pump_row(prev_id, {"x": pos["x"] + 1, "y": pos["y"] + 0, "dir": Direction.north}, fluids, conn_first, prev_id + 6) + \
        generate_gas_vent_row(prev_id + 24, {"x": pos["x"] + 1, "y": pos["y"] - 2, "dir": Direction.east}) + \
        generate_pump_row(prev_id + 6, {"x": pos["x"] + 8, "y": pos["y"] + 0, "dir": Direction.north}, fluids, prev_id + 6, prev_id + 12) + \
        generate_gas_vent_row(prev_id + 30, {"x": pos["x"] + 8, "y": pos["y"] - 2, "dir": Direction.east}) + \
        generate_pump_row(prev_id + 12, {"x": pos["x"] + 15, "y": pos["y"] + 0, "dir": Direction.north}, fluids, prev_id + 12, prev_id + 18) + \
        generate_gas_vent_row(prev_id + 36, {"x": pos["x"] + 15, "y": pos["y"] - 2, "dir": Direction.east}) + \
        generate_pump_row(prev_id + 18, {"x": pos["x"] + 22, "y": pos["y"] + 0, "dir": Direction.north}, fluids, prev_id + 18, conn_last) + \
        generate_gas_vent_row(
            prev_id + 42, {"x": pos["x"] + 22, "y": pos["y"] - 2, "dir": Direction.east})


def generate_power_poles(prev_id, pos):
    return [
        entity.power_pole(prev_id, {"x": pos["x"], "y": pos["y"]}, [
                          prev_id + 1, prev_id + 5]),
        entity.power_pole(
            prev_id + 1, {"x": pos["x"] + 7, "y": pos["y"]}, [prev_id, prev_id + 2, prev_id + 6]),
        entity.power_pole(
            prev_id + 2, {"x": pos["x"] + 14, "y": pos["y"]}, [prev_id + 1, prev_id + 3, prev_id + 7]),
        entity.power_pole(
            prev_id + 3, {"x": pos["x"] + 21, "y": pos["y"]}, [prev_id + 2, prev_id + 4, prev_id + 8]),
        entity.power_pole(
            prev_id + 4, {"x": pos["x"] + 28, "y": pos["y"]}, [prev_id + 3, prev_id + 9]),

        entity.power_pole(
            prev_id + 5, {"x": pos["x"], "y": pos["y"] + 4}, [prev_id + 6, prev_id]),
        entity.power_pole(prev_id + 6, {"x": pos["x"] + 7, "y": pos["y"] + 4}, [
                          prev_id + 5, prev_id + 7, prev_id + 1]),
        entity.power_pole(prev_id + 7, {"x": pos["x"] + 14, "y": pos["y"] + 4}, [
                          prev_id + 6, prev_id + 8, prev_id + 2]),
        entity.power_pole(prev_id + 8, {"x": pos["x"] + 21, "y": pos["y"] + 4}, [
                          prev_id + 7, prev_id + 9, prev_id + 3]),
        entity.power_pole(
            prev_id + 9, {"x": pos["x"] + 28, "y": pos["y"] + 4}, [prev_id + 8, prev_id + 4])
    ]


def generate_tracks(prev_id, pos):
    return [entity.straight_rail(prev_id + i + 1, {"x": pos["x"] + i * 2, "y": pos["y"], "dir": Direction.east}) for i in range(22)]


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def generate_stop_name(fluids):
    return "[virtual-signal=ltn-cleanup-station] " + ' '.join(["[fluid=" + f + "]" for f in fluids])

if __name__ == "__main__":
    for chunk in chunks(fluids.gasses, 12):
        text = blueprint.encode(blueprint.sheet(
            generate_top_void_row(0, {"x": 1, "y": -1}, chunk[:6], 133) +
            generate_bottom_void_row(48, {"x": 1, "y": 3}, chunk[6:], 133) +
            generate_power_poles(96, {"x": 1, "y": -1}) +
            generate_tracks(105, {"x": -5, "y": 1}) +
            [
                entity.rail_signal(132, {"x": 36, "y": -1, "dir": Direction.east}),
                entity.train_stop(
                    133, {"x": -5, "y": -1, "dir": Direction.west}, [1, 49], generate_stop_name(chunk))
            ]
        ))

        print(text)
        print()
        print()

from typing import Tuple
import json
from datetime import time
from typing import List, Tuple


def add_train(pk: int, human_id: str, in_warehouse: bool, last_station_pk: int):
    t = {
        "model": "choochoo_app.Train",
        "pk": pk,
        "fields": {
            "is_in_warehouse": in_warehouse,
            "human_id": human_id,
            "last_station": last_station_pk,
        },
    }
    return t


def add_material(material_id: str, human_name: str = None):
    # m = Material(material_id=material_id, human_name=human_name)
    # m.save()
    ...


def add_station(pk: int, is_warehouse: bool):
    s = {
        "model": "choochoo_app.Station",
        "pk": pk,
        "fields": {"is_warehouse": is_warehouse},
    }
    return s


def add_path_segment(pk: int, route_fk: int, src_fk: int, dst_fk: int, time: int):
    p = {
        "model": "choochoo_app.PathSegment",
        "pk": pk,
        "fields": {"route": route_fk, "src": src_fk, "dst": dst_fk, "travel_time": time},
    }
    return p


def add_path(start: int, route: int, path: List[str]):
    out = []
    for i in range(start, start + len(path) - 1):
        src = path[i - start][0]
        dst = path[i + 1 - start][0]
        time = path[i - start][1]
        out.append(add_path_segment(i, route, src, dst, time))

    out.append(
        add_path_segment(len(path) - 1, route, path[-1][0], path[0][0], path[-1][1])
    )
    return out


def add_route(pk: int, train_fk: int, time: str):
    route = {
        "model": "choochoo_app.Route",
        "pk": pk,
        "fields": {"time": time, "train": train_fk},
    }

    return route


def add_order(time, quantity, material, station, user):
    # o = Order(time=time, quantity=quantity, material=material, station=station, user=user)
    # o.save()
    # return o
    ...


def make_example_network():
    out = []
    out.append(add_station(0, True))
    for i in range(1, 11):
        out.append(add_station(i, False))

    out.append(add_train(0, "Train1", True, 0))
    out.append(add_route(0, 0, "10:00:00"))

    out += add_path(
        0,
        0,
        [
            (0, 4),
            (1, 2),
            (2, 2),
            (3, 5),
            (4, 2),
            (5, 2),
            (6, 4),
        ],
    )

    out.append(add_train(1, "Train2", True, 0))
    out.append(add_route(1, 1, "11:00:00"))
    out += add_path(
        6,
        1,
        [
            (0, 4),
            (7, 1),
            (8, 1),
            (9, 1),
            (10, 4),
        ],
    )

    out.append(add_train(2, "Train3", True, 0))
    out.append(add_route(2, 2, "12:00:00"))
    out += add_path(
        11,
        2,
        [
            (0, 4),
            (1, 2),
            (2, 1),
            (8, 1),
            (9, 1),
            (5, 2),
            (6, 4),
        ],
    )

    with open("data.json", "w", encoding="utf-8") as fp:
        json.dump(out, fp)


make_example_network()

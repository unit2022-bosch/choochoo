from random import randint
from typing import Tuple
import json
from datetime import datetime, time, timedelta
from typing import List, Tuple
import pandas as pd
import pytz


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


def add_material(pk: int, material_id: str, human_name: str = None):
    m = {
        "model": "choochoo_app.Material",
        "pk": pk,
        "fields": {"material_id": material_id, "human_name": human_name},
    }
    return m


def add_routeID(id: int):
    return {"model": "choochoo_app.RouteID", "pk": id, "fields": {}}


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
        "fields": {
            "route_id": route_fk,
            "src": src_fk,
            "dst": dst_fk,
            "travel_time": time,
        },
    }
    return p


def add_path(start: int, route_id: int, path: List[str]):
    out = []
    for i in range(start, start + len(path) - 1):
        src = path[i - start][0]
        dst = path[i + 1 - start][0]
        time = path[i - start][1]
        out.append(add_path_segment(i, route_id, src, dst, time))

    out.append(
        add_path_segment(len(path) - 1, route_id, path[-1][0], path[0][0], path[-1][1])
    )
    return out


def add_route(pk: int, route_id: int, train_fk: int, time: datetime):
    route = {
        "model": "choochoo_app.Route",
        "pk": pk,
        "fields": {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "train": train_fk,
            "route_id": route_id,
        },
    }

    return route


def add_order(
    pk: int,
    time_added: datetime,
    time_departure: datetime,
    quantity: int,
    material: int,
    station: int,
    user: int,
):
    o = {
        "model": "choochoo_app.Order",
        "pk": pk,
        "fields": {
            "time_added": time_added.strftime("%Y-%m-%d %H:%M:%S"),
            "time_of_departure": time_departure.strftime("%Y-%m-%d %H:%M:%S"),
            "quantity": quantity,
            "material": material,
            "station": station,
            "user": user,
            "is_complete": False,
        },
    }
    return o


def make_example_network():
    out = []
    df = pd.read_csv("materials.csv", names=["name"])
    for i, mat in enumerate(df["name"].to_list()):
        out.append(add_material(i, mat, mat + " Human"))

    out.append(add_station(0, True))
    for i in range(1, 11):
        out.append(add_station(i, False))

    out.append(add_routeID(0))
    out.append(add_train(0, "Train1", True, 0))
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

    out.append(add_routeID(1))
    out.append(add_train(1, "Train2", True, 0))
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

    out.append(add_routeID(2))
    out.append(add_train(2, "Train3", True, 0))
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

    for i in range(100):
        out.append(
            add_route(
                i,
                0,
                0,
                datetime(2021, 4, 13, 17, 0, 0) + timedelta(minutes=15),
            )
        )
    for i in range(100):
        out.append(
            add_route(
                100 + i,
                1,
                1,
                datetime(2021, 4, 13, 17, 15, 0) + timedelta(minutes=15),
            )
        )
    for i in range(100):
        out.append(
            add_route(
                200 + i,
                2,
                2,
                datetime(2021, 4, 13, 17, 30, 0) + timedelta(minutes=15),
            )
        )

    for i in range(100):
        rand_time = datetime.now()
        rand_secs = randint(0, 5000)
        rand_time += timedelta(seconds=rand_secs)
        rand_station = randint(1, 10)
        rand_quant = randint(1, 1000)
        rand_material = randint(0, df.shape[0] - 1)
        o = add_order(
            i, rand_time, rand_time, rand_quant, rand_material, rand_station, None
        )
        out.append(o)

    with open("data.json", "w", encoding="utf-8") as fp:
        json.dump(out, fp)


if __name__ == "__main__":
    make_example_network()

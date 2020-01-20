# -*- coding: utf-8 -*-
from influx_db import Influxdb_Prototype


class InstanceDB(Influxdb_Prototype):
    def __init__(self):
        super(InstanceDB, self).__init__('instance')


class InstanceRIDB(Influxdb_Prototype):
    def __init__(self):
        super(InstanceRIDB, self).__init__('instance_ri')


if __name__ == '__main__':
    import traceback

    try:
        db = InstanceDB()

        print("\n========== List ==========")
        print(db.list(condition="pda_server = 'WIN-6I9H2SO6EFG'",
                      sort=[("time", "DESC")], limit=10, offset=0))

    except Exception:
        traceback.print_exc()
        formatted_lines = traceback.format_exc().splitlines()
        print(formatted_lines[-1])


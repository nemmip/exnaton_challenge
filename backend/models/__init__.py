from backend.models.measurement import Measurement, Tags


def table_obj(name: str):
    table_dict = {
      'measurement': Measurement,
      'tags': Tags
    }
    return table_dict[name]
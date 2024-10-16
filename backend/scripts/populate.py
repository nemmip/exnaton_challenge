import requests
from backend.models import measurement


def get_data_set(muid: str) -> list:
    req = requests.get(
        f"https://exnaton-public-s3-bucket20230329123331528000000001.s3.eu-central-1.amazonaws.com/challenge/{muid}.json")
    data = req.json()['data']
    return data


def populate_data(session, data, value_str):
    tags_row = None
    for record in data:
        if tags_row is None:
            tags_row = measurement.Tags(muid=record['tags']['muid'], quality=record['tags']['quality'])
            session.add(tags_row)
            session.flush()
        measurement_row = measurement.Measurement(measurement=record['measurement'], timestamp=record['timestamp'],
                                                  energy=record[value_str], tags_id=tags_row.id)
        session.add(measurement_row)
        session.flush()


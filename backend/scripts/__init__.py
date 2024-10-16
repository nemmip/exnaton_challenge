from backend.models.session import get_session
from populate import populate_data, get_data_set


def main():
    session = get_session()
    try:
        set_1 = get_data_set("95ce3367-cbce-4a4d-bbe3-da082831d7bd")
        set_2 = get_data_set("1db7649e-9342-4e04-97c7-f0ebb88ed1f8")
        populate_data(session, set_1, "0100011D00FF")
        populate_data(session, set_2, "0100021D00FF")
    except Exception as e:
        session.rollback()
        print('Unable to populate tables', repr(e))
    else:
        session.commit()


if __name__ == '__main__':
    main()

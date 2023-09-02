import logging

from .server import NewAPI

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format={'timestamp': '%(asctime)s', 'level': '%(levelname)s', 'message': '%(message)s'}.
        handlers=[logging.StreamHandler()]
    )
    app = NewAPI()
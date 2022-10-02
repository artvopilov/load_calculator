from flask import Flask, request

from src.api.constants import AUTO_CONTAINERS
from src.api.request_parser import RequestParser
from src.api.response_builder import ResponseBuilder
from src.items.item_fabric import ItemFabric
from src.loading.loader import Loader
from src.logger.dummy_logger import DummyLogger

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return "<h1>This is TLG Load Calculator API!</h1>" \
           "The API supports following routes:" \
           "<ol>" \
           "    <li>[GET] /</li>" \
           "    <li>[POST] /calculate</li>" \
           "</ol>"


@app.route('/calculate', methods=['POST'])
def calculate():
    request_parser = RequestParser()
    request_data = request_parser.parse(request)

    container_params_to_count = request_data.container_params_to_count
    if not container_params_to_count:
        container_params_to_count = {c: -1 for c in AUTO_CONTAINERS}

    item_fabric = ItemFabric()
    logger = DummyLogger()

    loader = Loader(container_params_to_count, request_data.shipment_params_to_count, request_data.loading_type,
                    item_fabric, logger)
    loaded_containers = loader.load()

    response_builder = ResponseBuilder()
    return response_builder.build(loaded_containers, loader.get_left_shipments_counts())


if __name__ == '__main__':
    app.run()

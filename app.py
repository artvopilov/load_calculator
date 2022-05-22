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
    shipment_counts = request_parser.parse_shipment_counts(request)
    container_counts = request_parser.parse_container_counts(request)

    if not container_counts:
        container_counts = {c: -1 for c in AUTO_CONTAINERS}

    item_fabric = ItemFabric()
    logger = DummyLogger()

    loader = Loader(container_counts, shipment_counts, item_fabric, logger)
    loaded_containers = loader.load()

    response_builder = ResponseBuilder()
    return response_builder.build(loaded_containers, loader.get_left_shipments_counts())

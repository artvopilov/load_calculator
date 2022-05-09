from flask import Flask, request

from src.api.constants import AUTO_CONTAINERS
from src.loading.container_selection_type import ContainerSelectionType
from src.loading.container_selector import ContainerSelector
from src.items.item_fabric import ItemFabric
from src.loading.loader import Loader
from src.api.request_parser import RequestParser
from src.api.response_builder import ResponseBuilder
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

    container_selector = ContainerSelector()
    item_fabric = ItemFabric()
    logger = DummyLogger()

    container_selection_type = ContainerSelectionType.FIXED if container_counts else ContainerSelectionType.AUTO
    loader = Loader(container_counts, AUTO_CONTAINERS, container_selection_type,
                    shipment_counts, item_fabric, container_selector, logger)
    loader.load()

    response_builder = ResponseBuilder()
    return response_builder.build(loader.containers, loader.shipments_counts)
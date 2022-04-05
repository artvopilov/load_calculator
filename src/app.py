from flask import Flask, request

from loading.container_selector import ContainerSelector
from items.item_fabric import ItemFabric
from loading.loader import Loader
from api.request_parser import RequestParser
from api.response_builder import ResponseBuilder
from log.dummy_logger import DummyLogger

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "<p>This is Load Calculator!</p>"


@app.route('/calculate', methods=['POST'])
def calculate():
    item_fabric = ItemFabric()
    request_parser = RequestParser(item_fabric)

    shipment_counts = request_parser.parse_shipment_counts(request)
    container_counts = request_parser.parse_container_counts(request)

    container_selector = ContainerSelector()
    logger = DummyLogger()

    loader = Loader(container_counts, shipment_counts, item_fabric, container_selector, logger)
    loader.load()

    response_builder = ResponseBuilder()
    return response_builder.build(loader.containers, loader.shipments_counts)


if __name__ == '__main__':
    app.run(host='0.0.0.0')



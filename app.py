from flask import Flask, request
from loguru import logger

from src.api.request_parser import RequestParser
from src.api.response_builder import ResponseBuilder
from src.loading.loader_factory import LoaderFactory

logger.remove()
logger.add('logs/{time:YYYY-MM-DD}_info.log', level='INFO', rotation='00:00', retention=90)
logger.add('logs/{time:YYYY-MM-DD}_debug.log', level='DEBUG', rotation='00:00', retention=7)

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

    loader_factory = LoaderFactory()
    loader = loader_factory.create(
        request_data.shipment_params,
        request_data.container_params,
        request_data.loading_type_name
    )
    loader.load()

    response_builder = ResponseBuilder()
    return response_builder.build(loader.containers, loader.shipment_params)


if __name__ == '__main__':
    app.run()

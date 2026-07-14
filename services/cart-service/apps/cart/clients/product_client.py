import sys
import os
import grpc

_PROTO_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'shared', 'proto')
)
if _PROTO_DIR not in sys.path:
    sys.path.insert(0, _PROTO_DIR)

import product_pb2
import product_pb2_grpc

_target = os.environ.get('PRODUCT_GRPC_HOST', 'localhost:50051')
_channel = grpc.insecure_channel(_target)
_stub = product_pb2_grpc.ProductServiceStub(_channel)


def get_products_by_ids(ids: list[int]) -> list:
    response = _stub.GetProducts(product_pb2.GetProductsRequest(ids=ids))
    return list(response.products)

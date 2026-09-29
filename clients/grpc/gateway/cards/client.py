from grpc import Channel

from clients.grpc.client import GRPCClient
from clients.grpc.gateway.client import build_gateway_grpc_client

from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import IssuePhysicalCardRequest, IssuePhysicalCardResponse
from contracts.services.gateway.cards.rpc_issue_virtual_card_pb2 import IssueVirtualCardRequest, IssueVirtualCardResponse
from contracts.services.gateway.cards.cards_gateway_service_pb2_grpc import CardsGatewayServiceStub


class CardsGatewayGRPCClient(GRPCClient):
    def __init__(self, channel: Channel):
        super().__init__(channel)

        self.stub = CardsGatewayServiceStub(channel)

    def issue_physical_card_api(self, request: IssuePhysicalCardRequest) -> IssuePhysicalCardResponse:
        return self.stub.IssuePhysicalCard(request)

    def issue_virtual_card_api(self, request: IssueVirtualCardRequest) -> IssueVirtualCardResponse:
        return self.stub.IssueVirtualCard(request)

    def issue_physical_card(self, account_id: str, user_id: str) -> IssuePhysicalCardResponse:
        request = IssuePhysicalCardRequest(account_id = account_id, user_id=user_id)

        return self.stub.IssuePhysicalCard(request)

    def issue_virtual_card(self, account_id: str, user_id: str) -> IssueVirtualCardResponse:
        request = IssueVirtualCardRequest(account_id = account_id, user_id=user_id)

        return self.stub.IssueVirtualCard(request)

def build_cards_gateway_grpc_client() -> CardsGatewayGRPCClient:
    return CardsGatewayGRPCClient(channel=build_gateway_grpc_client())
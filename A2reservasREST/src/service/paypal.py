from ..settings import PaypalConfig
from httpx import AsyncClient
from typing import Any


class PaypalService:
    """From https://developer.paypal.com/docs/checkout/standard/integrate/"""

    base_url : str
    client_id: str
    app_secret: str

    def __init__(self, conf: PaypalConfig) -> None:
        self.base_url = conf.url
        self.client_id = conf.clientid
        self.app_secret = conf.secret

    async def __get_access_token(self, client: AsyncClient) -> str:
        response = await client.post(
            "/v1/oauth2/token",
            data={"grant_type": "client_credentials"},
            auth=(self.client_id,self.app_secret)
        )
        payload = response.json()
        return payload['access_token']

    async def capture_order(self, order_id: str) -> dict[str, Any]:
        async with AsyncClient(base_url=self.base_url) as client: 
            token = await self.__get_access_token(client)
            response = await client.post(
                f"/v2/checkout/orders/{order_id}/capture",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                }
            )
        return response.json()
        
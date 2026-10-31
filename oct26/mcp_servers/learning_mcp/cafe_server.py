from mcp.server import MCPServer
from cafe_data import MENU, COUPONS
from pydantic import BaseModel


mcp = MCPServer(
    "Charminar Cafe",
    instructions="Order food from Charminar Cafe in Hyderabad: read the menu, place orders, apply coupons, track delivery.")


ORDERS: dict[str, dict] = {}


@mcp.resource("cafe://menu")
def menu_card() -> str:
    """
    The full charminar cafe menu card with prices, veg/non-veg and spice level
    """
    lines = ["CHARMINAR CAFE  MENU  "]
    for name, item in MENU.items():
        tag = "veg" if item["veg"] else "non-veg"
        spice = f"spice {item['spicy']/4}" if item["spicy"] else "mild"
        lines.append(f"{name.title():<20} Rs {item['price']:>4}  {tag:<8}  {spice}")
    return "\n".join(lines)

def todays_special() -> str:
    pass

def cafe_policies() -> str:
    pass

@mcp.resource("cafe://order/{order_id}")
def order_reciept(order_id:str) -> str:
    pass

class OrderLine(BaseModel):
    item: str
    quantity: int

class OrderConfirmation(BaseModel):
    order_id: str
    total_rupees: int|float
    eta: str
    message: str

class OrderStatus(BaseModel):
    order_id: str
    status: str
    minutes_left: int

@mcp.tool()
def place_order(customer:str, items: list[OrderLine], table_no: str) -> OrderConfirmation:
    pass

@mcp.tool()
def apply_coupon(order_id: str, code: str) -> OrderConfirmation:
    pass

@mcp.tool()
def track_order(order_id:str) -> OrderStatus:
    pass




if __name__ == "__main__":
    mcp.run("stdio")
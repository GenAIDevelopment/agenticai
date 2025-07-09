"""This module will have mcp server to generate sales data
"""

from typing import Literal
from mcp.server.fastmcp import FastMCP
from utils import get_database_connection

mcp = FastMCP("data-generator")


# @mcp.tool()
# def create_user():
#     pass


@mcp.tool()
def create_product(
        name: str,
        description: str,
        price: float,
        stock_quantity: int,
        category_id: int = 1,
        image_url: str = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/640px-Image_not_available.png") -> Literal["Success", "Failed"]:
    """Creates  a product

    Returns:
        str: Success if saved false otherwise
    """
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        insert_product_sql = f"INSERT INTO products (name, description, price, stock_quantity, category_id, image_url) VALUES ('{name}', '{description}', {price}, {stock_quantity}, {category_id}, '{image_url}')"
        cursor.execute(insert_product_sql)
        connection.commit()
    except Exception:
        return "Failed"
    return "Success"


# @mcp.tool()
# def create_category():
#     pass


@mcp.resource(uri="products://latest")
def get_products():
    """This method gets the latest product
    """
    connection = get_database_connection()
    cursor = connection.cursor()
    latest_product_sql = 'SELECT * FROM `products` ORDER BY product_id DESC LIMIT 1;'
    cursor.execute(latest_product_sql)
    products = cursor.fetchall()
    product = products[0]
    message = f"{product[1]}, {product[2]}"
    return message



# @mcp.resource(uri="users://latest")
# def get_users():
#     pass


# @mcp.resource(uri="categories://latest")
# def get_categories():
#     pass
if __name__ == '__main__':
    mcp.run(transport='stdio')

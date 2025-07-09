"""This module will have utilities
"""
from dotenv import load_dotenv
import os
import mysql.connector
from typing import Union
#from mysql.connector.pooling import PooledMySQLConnection, MySQLConnectionAbstract


def get_database_connection(): # -> Union[PooledMySQLConnection, MySQLConnectionAbstract]:
    """This method connects to the mysql database

    Returns:
        Union[PooledMySQLConnection, MySQLConnectionAbstract]: _description_
    """
    load_dotenv()
    connection = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    return connection


if __name__ == '__main__':
    connection = get_database_connection()
    cursor = connection.cursor()
    # name = 'Sony PlayStation5 Gaming Console'
    # description = 'Slim Design: With PS5, players get powerful gaming technology packed inside a sleek and compact console design. 1TB of Storage: Keep your favorite games ready and waiting for you to jump in and play with 1TB of SSD storage built in. Ultra-High Speed SSD: Maximize your play sessions with near instant load times for installed PS5 games.'
    # price = 54990
    # stock_quantity = 10
    # category_id = 1
    # image_url = "https://m.media-amazon.com/images/I/51Ex3GcYMIL._SL1000_.jpg"

    # insert_product_sql = f"INSERT INTO products (name, description, price, stock_quantity, category_id, image_url) VALUES ('{name}', '{description}', {price}, {stock_quantity}, {category_id}, '{image_url}')"
    # cursor.execute(insert_product_sql)
    # connection.commit()
    latest_product_sql = 'SELECT * FROM `products` ORDER BY product_id DESC LIMIT 1;'
    cursor.execute(latest_product_sql)
    products = cursor.fetchall()
    for product in products:
        print(product)

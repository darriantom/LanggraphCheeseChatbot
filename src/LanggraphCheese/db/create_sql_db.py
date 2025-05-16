import json
import pymysql
from config import settings, CheeseData

class CreateSqlDB:
    def __init__(self):
        self.config = {
            "host": settings.DB_HOST,
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "db": settings.DB_NAME,
            "port": settings.DB_PORT,
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
            "connect_timeout": 10,
            "read_timeout": 10,
            "write_timeout": 10,
            "client_flag": pymysql.constants.CLIENT.MULTI_STATEMENTS
        }
        self.initialize()

    def _get_connection(self):
        return pymysql.connect(**self.config)

    def initialize(self):
        """Create the cheese data table if it doesn't exist"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS cheese_data (
                    id INT PRIMARY KEY,
                    showimage VARCHAR(255),
                    name VARCHAR(255),
                    brand VARCHAR(255),
                    category VARCHAR(255),
                    itemcount_case VARCHAR(255),
                    itemcount_each VARCHAR(255),
                    dimension_case VARCHAR(255),
                    dimension_each VARCHAR(255),
                    weight_case DECIMAL(10,2),
                    weight_each DECIMAL(10,2),
                    image TEXT,
                    related VARCHAR(255),
                    price_case DECIMAL(10,2),
                    price_each DECIMAL(10,2),
                    price_per_lb DECIMAL(10,2),
                    sku VARCHAR(255),
                    wholesale VARCHAR(255),
                    out_of_stock BOOLEAN,
                    product_url VARCHAR(255),
                    priceorder INT,
                    popularityorder INT
                )
                """)
            connection.commit()
        finally:
            connection.close()

    def insert_cheese(self, cheese: CheeseData, i):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO cheese_data 
                        (id, showimage, name, brand, category, itemcount_case, itemcount_each, dimension_case, dimension_each,
                        weight_case, weight_each, image, related, price_case, price_each, price_per_lb, sku, wholesale,
                        out_of_stock, product_url, priceorder, popularityorder)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                cursor.execute(sql, (
                    i,
                    cheese.get('showimage', ''),
                    cheese.get('name', ''),
                    cheese.get('brand', ''),
                    cheese.get('category', ''),
                    cheese.get('itemcount_case', ''),
                    cheese.get('itemcount_each', ''),
                    cheese.get('dimension_case', ''),
                    cheese.get('dimension_each', ''),
                    cheese.get('weight_case', 0.0),
                    cheese.get('weight_each', 0.0),
                    cheese.get('image', ''),
                    cheese.get('related', ''),
                    cheese.get('price_case', 0.0),
                    cheese.get('price_each', 0.0),
                    cheese.get('price_per_lb', 0.0),
                    cheese.get('sku', ''),
                    cheese.get('wholesale', ''),
                    cheese.get('out_of_stock', False),
                    cheese.get('product_url', ''),
                    cheese.get('priceorder', 0),
                    cheese.get('popularityorder', 0),
                ))
            connection.commit()
        finally:
            connection.close()

mysql_db = CreateSqlDB()

with open('cheese_product_sql.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
        
        # Process each product in the JSON
i = 0
for cheese in data:
    print(cheese.get('sku'))
    # mongodb.insert_cheese(cheese)
    mysql_db.insert_cheese(cheese, i)
    i+=1
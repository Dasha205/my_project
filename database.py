import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        # Подключение к MySQL (ЗАМЕНИТЕ НА СВОИ ДАННЫЕ)
        self.conn = mysql.connector.connect(
            host="localhost",           # или IP вашего сервера
            port=3306,                  # стандартный порт MySQL
            database="ваша_база_данных", # имя вашей БД в DBeaver
            user="ваш_логин",            # ваш пользователь
            password="ваш_пароль"        # ваш пароль
        )
        self.cursor = self.conn.cursor()
    
    def get_customers(self):
        """Возвращает список всех заказчиков"""
        self.cursor.execute("SELECT DISTINCT customer FROM your_orders_table ORDER BY customer")
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_orders(self, customer=None, sort_by=None, sort_order="ASC"):
        """Возвращает заказы с фильтрацией и сортировкой"""
        query = "SELECT customer, city, phone, order_date, order_sum FROM your_orders_table WHERE 1=1"
        params = []
        
        if customer and customer != "Все" and customer != "":
            query += " AND customer = %s"
            params.append(customer)
        
        if sort_by == "customer":
            query += f" ORDER BY customer {sort_order}"
        elif sort_by == "date":
            query += f" ORDER BY order_date {sort_order}"
        elif sort_by == "sum":
            query += f" ORDER BY order_sum {sort_order}"
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self):
        self.cursor.close()
        self.conn.close()

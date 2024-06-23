from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():

    @staticmethod
    def getState():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct (Country)
                    from go_retailers"""
        cursor.execute(query,)
        for row in cursor:
            result.append(row['Country'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct(extract(year from `Date`)) as year
                    from go_daily_sales"""
        cursor.execute(query, )
        for row in cursor:
            result.append(row['year'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNode(country):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers
                    where Country = %s """
        cursor.execute(query, (country,))
        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdge(country, year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select t1.r1, t2.r2, COUNT(distinct(t1.p1)) as peso
                    from (select gr.Retailer_code as r1, Product_number as p1
                            from go_daily_sales gds, go_retailers gr 
                            where gr.Retailer_code = gds.Retailer_code and gr.Country = %s and extract(year from gds.`Date`) = %s) t1,
                        (select gr.Retailer_code as r2, Product_number as p2
                            from go_daily_sales gds, go_retailers gr 
                            where gr.Retailer_code = gds.Retailer_code and gr.Country = %s and extract(year from gds.`Date`) = %s) t2
                    where t1.p1 = t2.p2 and t1.r1 < t2.r2
                    group by t1.r1, t2.r2"""
        cursor.execute(query, (country, year, country, year,))
        for row in cursor:
            result.append((row['r1'],
                           row['r2'],
                           row['peso']))

        cursor.close()
        conn.close()
        return result

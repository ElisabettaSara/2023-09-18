from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():

    @staticmethod
    def getNazione():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct Country 
                    from go_retailers gr """
        cursor.execute(query, )
        for row in cursor:
            result.append(row['Country'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAnno():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(`Date`) as anno
                    from go_daily_sales gds """
        cursor.execute(query, )
        for row in cursor:
            result.append(row['anno'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(nazione):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers gr 
                    where gr.Country =%s """
        cursor.execute(query, (nazione, ))
        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(nazione, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select gr1.rc1 as n1, gr2.rc2 as n2, count(*) as peso
                    from(select gds.Retailer_code as rc1, Product_number as pn1
                        from go_daily_sales gds,go_retailers gr 
                        where gds.Retailer_code = gr.Retailer_code 
                            and gr.Country =%s
                            and year(gds.`Date` )=%s) gr1,
                        (select gds.Retailer_code as rc2, gds.Product_number as pn2
                        from go_daily_sales gds,go_retailers gr 
                        where gds.Retailer_code = gr.Retailer_code 
                            and gr.Country =%s
                            and year(gds.`Date` )=%s) gr2
                where gr1.pn1 = gr2.pn2 and gr1.rc1<gr2.rc2 
                group by gr1.rc1, gr2.rc2 """
        cursor.execute(query, (nazione,anno, nazione, anno,))
        for row in cursor:
            result.append((row['n1'], row['n2'], row['peso']))

        cursor.close()
        conn.close()
        return result

import psycopg2,pandas


mydb = psycopg2.connect(database="kannur_corporation", 
                              user="analytics_view", 
                              password="Ulgis@1Ults", 
                              host="103.133.180.27", 
                              port="5432")

def execute_querry(querry,connection=mydb):
    q = pandas.read_sql_query(querry,connection)
    return q


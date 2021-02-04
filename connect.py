import psycopg2,pandas


mydb = psycopg2.connect(database="kannur_corporation", 
                              user="analytics_view", 
                              password="", 
                              host="", 
                              port="5432")

def execute_querry(querry,connection=mydb):
    q = pandas.read_sql_query(querry,connection)
    return q


import mysql.connector 
def allbatchs(dbname):
    my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database=dbname)
    cursor=my.cursor()
    cursor.execute("show tables")
    data=cursor.fetchall()
    for i in range(len(data)):
        tablename=data[i][0]
        cursor.execute(f"select CGPA from {tablename}")
        column=cursor.fetchall()
        print(column)
        ra=[]
        for j in range(len(column)):
            value=column[j][0]
            if value=='nan':
                continue
            ra.append(value)
        # print(ra)
        return max(ra)
    
# allbatchs("csm")
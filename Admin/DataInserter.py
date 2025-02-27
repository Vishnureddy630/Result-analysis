import mysql.connector
import pandas as pd
import numpy as np
my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database="civil")
cursor=my.cursor()
def creating_db(dbname):
    try:
        # Creating database if not exists
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishnu@123"
        ) as mydb:
            with mydb.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}`")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return 



def creating_table(dbname,tablename):
    try:
        # Creating database if not exists
        tablename = tablename.replace("-", "_")
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishnu@123",
            database=dbname
        ) as mydb:
            with mydb.cursor() as cursor:
                # cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}`")
                create_table_query = f"CREATE TABLE IF NOT EXISTS `{tablename}` (Roll_No VARCHAR(100), Name VARCHAR(300), Section CHAR(100),CGPA VARCHAR(5))"
                cursor.execute(create_table_query)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return 
    



def Regular(dbname,address,semister,Status,BatchYear,Month,examyear):
    creating_db(dbname)
    creating_table(dbname,BatchYear)

    #taking the section by sheets
    file_path=address
    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names
    print(sheet_names)
    sheets=sheet_names[0]

    for section in sheet_names:
        dfs = pd.read_excel(excel_file, sheet_name=section)
        print(type(dfs))

        #createing the column names in the table  
        column_names=[]  
        
        # keping the unnamed insted of the space
        for name in dfs.columns.tolist():
            if "Unnamed" in str(name) :
                column_names.append("")
            else:
                column_names.append(name)
        count=0

        for index, row in dfs.iterrows():
            temp=row.to_list()
            for i in range(len(temp)):
                if  np.nan == temp[i] or "nan" in str(temp[i]):
                    continue
                if ""==column_names[i]:
                    column_names[i]=str(temp[i])
                else:
                    column_names[i]=str(column_names[i])+"_"+str(temp[i])
            count+=1
            if count==2:
                break
            # print(temp)
        print(column_names)
        

        try:
            with mysql.connector.connect(
                host="localhost",
                user="root",
                password="vishnu@123",
                database=dbname
            ) as db_connection:

                # Creating a cursor object using the cursor() method
                cursor = db_connection.cursor()
                print("Table function activated")
                # Format batchyear for table name
                
                BatchYear=BatchYear.replace("-","_")
              
                
                column_new_name=[]
                for i in range(1,len(column_names)-1):
                    testvalue=column_names[i].split(" ")
                    if len(testvalue) > 0:
                        column_names[i]=column_names[i].replace(" ","$")
                    column = column_names[i] + "_" + Month + "_" + semister + "_" + Status+"_"+examyear
                    try:
                        if column_names[i]=="SGPA":
                            column=column_names[i]+"_" +semister
                            column_new_name.append(column)
                            cursor.execute("ALTER TABLE %s ADD COLUMN %s varchar(20)" %(BatchYear,column))
                        else:
                            column_new_name.append(column_names[i]+"_"+Month+"_"+semister+"_"+Status+"_"+examyear)
                            cursor.execute("ALTER TABLE %s ADD COLUMN %s varchar(20)" %(BatchYear,column))
                            
                    except Exception as e:
                        print(e)
                print("Table column are successfully created!")
                column_new_name.append("CGPA")

                # Inserting data into the table
                try:
                    count=0
                    for index, row in dfs.iterrows():
                        count+=1
                        if count<=2:
                            continue
                        row_elements=row.to_list()   
                        # print(row_elements)
                        rollno=row_elements[0]                 
                        try:
                            for i in range(1,len(row_elements)):
                                
                                # constrains for the value by this we can change the value as per the data we get form the sheet
                                if row_elements[i]==np.nan:
                                    row_elements[i]="T"
                                
                                # checking the roll no if not we just add the roll no to the database and this we do because there may be lateral entry students
                                cursor = db_connection.cursor()
                                cursor.execute(f"SELECT  CASE  WHEN EXISTS (SELECT 1 FROM {BatchYear} WHERE Roll_No = '{rollno}')         THEN '1'         ELSE '0'   END AS result")
                                result = cursor.fetchall()
                                
                                if int(result[0][0]):
                                    cursor.execute("UPDATE `%s` SET `%s` = '%s' WHERE `Roll_No` = '%s'" % (BatchYear, column_new_name[i-1], row_elements[i], rollno))
                                else:
                                    cursor = db_connection.cursor()
                                    query = f"INSERT INTO `{BatchYear}` (Roll_No) VALUES (%s)"
                                    cursor.execute(query, (row_elements[0],))
                                    db_connection.commit()
                                    
                                    cursor.execute("UPDATE `%s` SET `%s` = '%s' WHERE `Roll_No` = '%s'" % (BatchYear,column_new_name[i-1], row_elements[i], row_elements[0]))
                                cursor.execute("UPDATE `%s` SET `%s` = '%s' WHERE `Roll_No` = '%s'" % (BatchYear, "Section", section, row_elements[0]))
                        except Exception as e:
                            print(f"inner: {e}"+str(row_elements[i]),row_elements[i],column_new_name[i-1])
                        
                except mysql.connector.Error as erro:
                    print("out "+erro)
                db_connection.commit()
                print(cursor.rowcount, "Record inserted successfully into table")

        except mysql.connector.Error as error:
            print(error)
            # pass

def Supplementary(dbname,filename,semister,Status,BatchYear,Month,examyear):
    #taking the section by sheets
    file_path=filename
    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names
    print(sheet_names)
    sheets=sheet_names[0]

    for section in sheet_names:
        dfs = pd.read_excel(excel_file, sheet_name=section)
        print(type(dfs))

        #createing the column names in the table  
        column_names=[]  
        
        # keping the unnamed insted of the space
        for name in dfs.columns.tolist():
            if "Unnamed" in str(name) :
                column_names.append("")
            else:
                column_names.append(name)
        count=0

        for index, row in dfs.iterrows():
            temp=row.to_list()
            for i in range(len(temp)):
                if  np.nan == temp[i] or "nan" in str(temp[i]):
                    continue
                if ""==column_names[i]:
                    column_names[i]=str(temp[i])
                else:
                    column_names[i]=str(column_names[i])+"_"+str(temp[i])
            count+=1
            if count==2:
                break
            # print(temp)
        print(column_names)
        

        try:
            with mysql.connector.connect(
                host="localhost",
                user="root",
                password="vishnu@123",
                database=dbname
            ) as db_connection:

                # Creating a cursor object using the cursor() method
                cursor = db_connection.cursor()
                print("Table function activated")
                # Format batchyear for table name
                
                BatchYear=BatchYear.replace("-","_")
              
                
                column_new_name=[]
                for i in range(1,len(column_names)-1):
                    testvalue=column_names[i].split(" ")
                    if len(testvalue) > 0:
                        column_names[i]=column_names[i].replace(" ","$")
                    column = column_names[i] + "_" + Month + "_" + semister + "_" + Status+"_"+examyear
                    try:
                        if column_names[i]=="SGPA":
                            column=column_names[i]+"_" +semister
                            column_new_name.append(column)
                            # cursor.execute("ALTER TABLE %s ADD COLUMN %s varchar(20)" %(BatchYear,column))
                        else:
                            cursor.execute("ALTER TABLE %s ADD COLUMN %s varchar(20)" %(BatchYear,column))
                            column_new_name.append(column_names[i]+"_"+Month+"_"+semister+"_"+Status+"_"+examyear)
                    except Exception as e:
                        print(e)
                print("Table column are successfully created!")
                column_new_name.append("CGPA")

                # Inserting data into the table
                try:
                    count=0
                    for index, row in dfs.iterrows():
                        count+=1
                        if count<=2:
                            continue
                        row_elements=row.to_list()   
                        # print(row_elements)
                        rollno=row_elements[0]                 
                        try:
                            for i in range(1,len(row_elements)):
                                
                                # constrains for the value by this we can change the value as per the data we get form the sheet
                                if row_elements[i]==np.nan:
                                    row_elements[i]="T"
                                
                                # checking the roll no if not we just add the roll no to the database and this we do because there may be lateral entry students
                                cursor = db_connection.cursor()
                                cursor.execute(f"SELECT  CASE  WHEN EXISTS (SELECT 1 FROM {BatchYear} WHERE Roll_No = '{rollno}')         THEN '1'         ELSE '0'   END AS result")
                                result = cursor.fetchall()
                                
                                if int(result[0][0]):
                                    cursor.execute("UPDATE `%s` SET `%s` = '%s' WHERE `Roll_No` = '%s'" % (BatchYear, column_new_name[i-1], row_elements[i], rollno))
                                else:
                                    cursor = db_connection.cursor()
                                    query = f"INSERT INTO `{BatchYear}` (Roll_No) VALUES (%s)"
                                    cursor.execute(query, (row_elements[0],))
                                    db_connection.commit()
                                    
                                    cursor.execute("UPDATE `%s` SET `%s` = '%s' WHERE `Roll_No` = '%s'" % (BatchYear,column_new_name[i-1], row_elements[i], row_elements[0]))
                                cursor.execute("UPDATE `%s` SET `%s` = '%s' WHERE `Roll_No` = '%s'" % (BatchYear, "Section", section, row_elements[0]))
                        except Exception as e:
                            print(f"inner: {e}"+str(row_elements[i]))
                        
                except mysql.connector.Error as erro:
                    print("out "+erro)
                db_connection.commit()
                print(cursor.rowcount, "Record inserted successfully into table")

        except mysql.connector.Error as error:
            print(error)
            # pass

def CreatingLectureTable(dbname,tablename):
    try:
        # Creating database if not exists
        my=mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishnu@123",
            database=dbname
        ) 
        cursor=my.cursor()
        # cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}`")
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{tablename}` (Employee_Name  VARCHAR(100),Dept VARCHAR(100),	Emp_Id VARCHAR(100))"
        cursor.execute(create_table_query)
        

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return 
    

def LectureDataEntry(filepath):
    creating_db('Lecture')
    CreatingLectureTable('Lecture','Data')
    my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database='Lecture' ) 
    cursor=my.cursor()
    excel_file = pd.ExcelFile(filepath)
    sheet_names = excel_file.sheet_names
    print(sheet_names)
    sheets=sheet_names[0]

    for section in sheet_names:
        dfs = pd.read_excel(excel_file, sheet_name=section)
        for name, row  in dfs.iterrows():
            rows=row.to_list() 
            try:
                query = f"INSERT INTO data (Employee_Name,Dept,Emp_Id ) VALUES (%s,%s,%s)"
                cursor.execute(query, (rows[0],rows[1],str(int(rows[2]))))
                my.commit()
            except Exception as e:
                print('error occured ',e)
            


# LectureDataEntry('C:/Users/global ed/Desktop/test/RS/Copy of Faculty_Thumb_Code__Report(1).xlsx')

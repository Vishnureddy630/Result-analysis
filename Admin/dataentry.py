import mysql.connector
import mysql.connector
import pandas as pd


def Regular(dbname,address,semister,Status,BatchYear,Month,examyear):
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
            df=pd.read_excel(address)
            column_to_delete = 'Name'
            df = df.drop(columns=[column_to_delete])
            column_to_delete = 'Section'
            df = df.drop(columns=[column_to_delete])
            
            column_name=list(df) 
            column_new_name=[]
            for i in range(1,len(column_name)-1):
                column = column_name[i] + "_" + Month + "_" + semister + "_" + Status+"_"+examyear
                if column_name[i]=="SGPA":
                    column=column_name[i]+"_" +semister
                    column_new_name.append(column)
                    cursor.execute("ALTER TABLE %s ADD COLUMN %s varchar(5)" %(BatchYear,column))
                else:
                    cursor.execute("ALTER TABLE %s ADD COLUMN %s varchar(2)" %(BatchYear,column))
                    column_new_name.append(column_name[i]+"_"+Month+"_"+semister+"_"+Status+"_"+examyear)
            print("Table column are successfully created!")
            column_new_name.append("CGPA")
            # Inserting data into the table
            try:
                for index, row in df.iterrows():
                    row_elements=[]
                    row_elements.extend(row)
                    rollno=row_elements.pop(0)
                    print(len(column_new_name),len(row_elements))
                    sgpa=row_elements[-2]
                    try:
                        for i in range(len(row_elements)):
                            if row_elements[i]=="nan":
                                row_elements[i]="mf"
                            cursor.execute("UPDATE `%s` SET `%s` = '%s' WHERE `Roll_No` = '%s'" % (BatchYear, column_new_name[i], row_elements[i], rollno))
                            # print(len(column_new_name[i]),len(row_elements[i]))
                    except Exception as e:
                        print(f"Error: {e}")
                    # cursor.execute("UPDATE `%s` SET `%s` = '%s' WHERE `Roll_No` = '%s'" % (BatchYear, column_new_name[-2], sgpa, rollno))
                    # print(row_values)
            except mysql.connector.Error as erro:
                print(erro)
            db_connection.commit()
            print(cursor.rowcount, "Record inserted successfully into table")

    except mysql.connector.Error as error:
        print(error)
        # pass

def Supplementary(dbname,filename,semister,Status,BatchYear,Month,examyear):
    try:
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishnu@123",
            database=dbname
        ) as db_connection:
            address=filename
            # Creating a cursor object using the cursor() method
            cursor = db_connection.cursor()
            print("Table function activated")
            # Format batchyear for table name
            
            BatchYear=BatchYear.replace("-","_")
            df=pd.read_excel(address)
            column_to_delete = 'Name'
            df = df.drop(columns=[column_to_delete])
            column_to_delete = 'Section'
            df = df.drop(columns=[column_to_delete])
            
            column_name=list(df) 
            column_new_name=[]
            for i in range(1,len(column_name)-1):
                column = column_name[i] + "_" + Month + "_" + semister + "_" + Status + "_" + examyear
                if column_name[i]=="SGPA":
                    column=column_name[i]+"_" +semister
                    column_new_name.append(column)
                else:
                    cursor.execute("ALTER TABLE %s ADD COLUMN %s varchar(2)" %(BatchYear,column))
                    column_new_name.append(column_name[i]+"_"+Month+"_"+semister+"_"+Status+"_"+examyear)
            print("Table column are successfully created!")
            column_new_name.append("CGPA")
            # Inserting data into the table
            print(column_new_name)
            try:
                for index, row in df.iterrows():
                    row_elements=[]
                    row_elements.extend(row)
                    rollno=row_elements.pop(0)
                    print(len(column_new_name),len(row_elements))
                    sgpa=row_elements[-2]
                    try:
                        for i in range(len(row_elements)):
                            if row_elements[i]=="nan":
                                row_elements[i]="mf"
                            cursor.execute("UPDATE `%s` SET `%s` = '%s' WHERE `Roll_No` = '%s'" % (BatchYear, column_new_name[i], row_elements[i], rollno))
                            # print(len(column_new_name[i]),len(row_elements[i]))
                    except:
                        pass
                    # cursor.execute("UPDATE `%s` SET `%s` = '%s' WHERE `Roll_No` = '%s'" % (BatchYear, column_new_name[-2], sgpa, rollno))
                    # print(row_values)
            except mysql.connector.Error as erro:
                print(erro)
            db_connection.commit()
            print(cursor.rowcount, "Record inserted successfully into table")

    except mysql.connector.Error as error:
        print(error)
        # pass

def create_table_insert_data(dbname, filename, batchyear):
    try:
        # Establishing a connection to the MySQL database
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishnu@123",
            database=dbname
        ) as db_connection:

            # Creating a cursor object using the cursor() method
            cursor = db_connection.cursor()

            # Format batchyear for table name
            batchyear = batchyear.replace("-", "_")

            # Creating a table in MySQL database
            create_table_query = f"CREATE TABLE IF NOT EXISTS `{batchyear}` (Roll_No VARCHAR(11), Name VARCHAR(100), Section CHAR(1),CGPA VARCHAR(5))"
            cursor.execute(create_table_query)
            print("Table created successfully!")

            # Inserting data into the table
            try:
                df = pd.read_excel(filename)
                for index, row in df.iterrows():
                    row_values = (str(row['Roll No']), str(row['Name']), str(row['Section']),str(row['CGPA']))
                    insert_query = f"INSERT INTO `{batchyear}` (Roll_No, Name, Section,CGPA) VALUES (%s, %s, %s, %s)"
                    cursor.execute(insert_query, row_values)
                    print(row_values)
            except mysql.connector.Error as erro:
                print(erro)
            db_connection.commit()
            print(cursor.rowcount, "Record inserted successfully into table")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Closing the cursor & connection
        cursor.close()

def creating_db_basic_details(dbname, batchyear, filename):
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

    # Calling function to create table and insert data
    create_table_insert_data(dbname, filename, batchyear)

# Example usage:
# creating_db_basic_details("mydatabase", "2023-2024", "data.xlsx")

import mysql.connector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import numpy as np

def details(rollno,barnch):
    my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database=barnch)
    cursor=my.cursor()
    cursor.execute("show tables")
    data=cursor.fetchall()
    # the exception will shure come becaues the table will iterate till the no of table the database have
    try:
        # this below loop is use to find the correct table for the correct table name of the roll no
        for tablename in data:
            cursor.execute(f"SELECT Name,Roll_No,Section,CGPA FROM {tablename[0]} WHERE Roll_No= %s ", (rollno,))
            data = cursor.fetchall()
            dataa=[]
            for i in data:
                dataa.extend(i)
    except Exception as error:
        print(error)
    print(dataa)
    return dataa

def generate_plot(dat):
    # Creating the dataset
    print("hellow man",dat)
    data={}
    co=1
    for i in range(len(dat)):
        key="Semister :"+str(co)
        value=float(dat[i])
        data[key]=value
        co+=1
    print(data)
    courses = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots(figsize=(8, 5))

    # Defining bar positions
    bar_width = 0.5
    bar_positions = np.arange(len(courses))

    # Creating the vertical bar plot with reduced width and closer spacing
    bars = ax.bar(bar_positions, values, width=bar_width)
    ax.set_xlabel("Semisters")
    ax.set_ylabel("SGPA")
    ax.set_title("Based on the SGPA")

    # Setting y-axis range from 1 to 10
    ax.set_ylim(1, 10)

    # Adding values on the bars with increased font size
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value}', 
                ha='center', va='bottom', fontsize=12, weight='bold')

    # Setting x-ticks to be in the center of the bars
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(courses)

    # Changing the figure title
    fig.suptitle("SGPA ", fontsize=16, fontweight='bold')


    # Convert plot to image
    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plot_img = base64.b64encode(img_stream.getvalue()).decode()
    plt.close()

    return plot_img

def results(dbname,rollno):
    try:
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishnu@123",
            database=dbname
        ) as db_connection:

            # Creating a cursor object using the cursor() method
            cursor = db_connection.cursor()
            # print("Table function activated")
            # Format batchyear for table name
            tablenames=[]
            try :
                cursor.execute("show tables")
                tables = cursor.fetchall()
                # Process the rows
                for table in tables:
                    # print(row)
                    k=str(table)
                    k=k.replace("(","")
                    k=k.replace(")","")
                    k=k.replace("'","")
                    k=k.replace(",","")
                    tablenames.append(k)
            except Exception as e:
                print(e)
            print(tablenames)
            try:
                for i in range(len(tablenames)):
                    try:
                        # k=f"select * from {tablenames[i]} where  Roll_No = %s"
                        # cursor.execute(k,(rollno,))
                        # data = cursor.fetchall()
                        print(type(tablenames[i]))
                        print(tablenames[i])
                        table=tablenames[i]
                        query=f"desc {tablenames[i]}"
                        cursor.execute(query)
                        column_description=cursor.fetchall()
                        
                        count=0
                        semister = [[] for _ in range(8)] 
                        indexs=[[] for _ in range(8)] 
                        # print(indexs)
                        try:
                            for i in column_description:
                                # print(i)
                                val=str(i[0])
                                # print(type(val))
                                count+=1
                                if count<=4:
                                    continue
                                if "SGPA" in val:
                                    h,j=val.split("_")
                                else:
                                    h,i,k,j,l,m=val.split("_")
                                if "I" == j:
                                    semister[0].append(val)
                                    print(val)
                                    if "SGPA" in val:
                                        index=len(semister[0])-1
                                        # print(semister)
                                        indexs[0].append(index)
                                elif "II" == j:
                                    semister[1].append(val)
                                    if "SGPA" in val:
                                        index=len(semister[1])-1
                                        indexs[1].append(index)
                                elif "III"==j:
                                    semister[2].append(val)
                                    if "SGPA" in val:
                                        index=len(semister[2])-1
                                        indexs[2].append(index)
                                elif "IV"==j:
                                    semister[3].append(val)
                                    if "SGPA" in val:
                                        index=len(semister[3])-1
                                        indexs[3].append(index)
                                elif "V"==j:
                                    semister[4].append(val)
                                    if "SGPA" in val:
                                        index=len(semister[4])-1
                                        indexs[4].append(index)
                                elif "VI"==j:
                                    semister[5].append(val)
                                    if "SGPA" in val:
                                        index=len(semister[5])-1
                                        indexs[5].append(index)
                                elif "VII"==j:
                                    semister[6].append(val)
                                    if "SGPA" in val:
                                        index=len(semister[6])-1
                                        indexs[6].append(index)
                                elif "VIII"==j:
                                    semister[7].append(val)
                                    if "SGPA" in val:
                                        index=len(semister[7])-1
                                        indexs[7].append(index)
                                # print(indexs)
                        except Exception as e:
                            print(e)
                        # print(len(semister))
                        # print(len(indexs))
                        no_of_semister=0
                        for i in semister:
                            if len(i)!=0:
                                no_of_semister+=1
                        # print("no of semister",indexs)
                        for i in range(len(semister)):
                            ele=indexs[i][0]
                            sgp=str(semister[i].pop(ele))
                            semister[i].append(sgp)
                            if i==no_of_semister-1:
                                break
                        # print("jklsdjfkljsalkfjsldjfjsljfdklsjsdklfsdjklfjklfjkldfjkldfjfkl")
                        
                        full_table_data = []
                        # print(semister)
                        count=0
                        no_of_semister=["I","II","III","IV","V","VI","VII","VIII"]
                        update=0
                        sgpa_graph=[]
                        # print(semister)
                        for i in semister:
                            # print("the semister no is",count)
                            k=[]
                            sno=1
                            for j in i:
                                
                                if count==0:
                                    # print("ahi")
                                   
                                    k=["S. No.","Subjects code","Subject name","grade","SGPA","month year",no_of_semister[update]]
                                    full_table_data.append(k)
                                    update+=1
                                    count+=1
                                    # print(full_table_data)
                                cursor.execute(f"SELECT {j} FROM {table} WHERE Roll_No=%s ", (rollno,))
                                data = cursor.fetchall()
                                # print(list(data[0])[0])
                                if list(data[0])[0]==None:
                                    continue
                                if "SGPA" in j:
                                    sg,se=j.split("_")
                                    # print(data[0][0])
                                    if data[0][0]== "nan":
                                        kk=0
                                        ppr=[sno,sg,se,kk]
                                        sgpa_graph.append(ppr)
                                    else:
                                        ppr=[sno,sg,se,data[0][0]]
                                        sgpa_graph.append(ppr)
                                    full_table_data.append(ppr)
                                    
                                    # print(full_table_data)
                                    k=["S. No.","Subjects code","Subject name","grade","SGPA","month year",no_of_semister[update]]
                                    full_table_data.append(k)
                                    update+=1
                                    
                                else:
                                    if full_table_data[-1][0]=="S. No.":
                                        pp,qq,rr,ss,tt,uu=j.split("_")
                                        monyea=f"({rr} {uu})"
                                        full_table_data[-1].append(monyea)
                                    subjectcode,subjectname,month,semisterno,typ,examyear=j.split("_")
                                    check="not there "
                                    if 1:
                                        for k in range(len(full_table_data)):
                                            if full_table_data[k][1]==subjectcode:
                                                full_table_data[k][-3]=data[0][0]
                                                full_table_data[k][-2]=month+" "+examyear
                                                full_table_data[k][-1]=int(full_table_data[k][-1])+1
                                                check="is is there"
                                    if check=="not there ":                                   
                                        pp=[sno,subjectcode,subjectname,month,semisterno,typ]
                                        st=data[0][0]
                                        montyear= month+" "+examyear
                                        pp.append(st)
                                        pp.append(montyear)
                                        pp.append(0)
                                        full_table_data.append(pp)
                                sno+=1
                                        # print(full_table_data)
                                
                                
                        # print(full_table_data)
                        print("graph values are",sgpa_graph)
                        data=[]
                        #removing the subject code column form the table please
                        if "S. No."==full_table_data[-1][0]:
                            del full_table_data[-1]
                        print(full_table_data)
                        print(sgpa_graph)
                        for i in sgpa_graph:
                            data.append(i[-1])
                        print(data)

                        # Extract y values
                        # y_values = [item[1] for item in data]
                        print("it came near the graph")
                        graph=generate_plot(data)
                        print(full_table_data)
                        if "Subjects" in full_table_data[-1]:
                            print("hai")
                        maxlen=len(full_table_data)-1
                        for i in range(len(full_table_data)):
                            if maxlen==i:
                                if full_table_data[maxlen][0]=="Subjects":
                                    del full_table_data[maxlen]
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
            db_connection.commit()

    except mysql.connector.Error as error:
        print(error)
    # j=0
    cursor.close()
    
    return full_table_data,details(rollno),graph
        # pass
# dbname="csm"
# rollno='21641A6694'
# results(dbname,rollno)
def semister_wise(batch):
    try:
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishnu@123",
            database="csm"
        ) as db_connection:

            # Creating a cursor object using the cursor() method
            cursor = db_connection.cursor()
            # print("Table function activated")
            # Format batchyear for table name
            tablenames=[]
            try :
                cursor.execute(f"desc table {batch}")
                tables = cursor.fetchall()
                # Process the rows
                column_name=[]
                for table in tables:
                    column_name.extend(table[0])
                    pass
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    cursor.close()
    
def results2(dbname,rollno):
    try:
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishnu@123",
            database=dbname
        ) as db_connection:

            # Creating a cursor object using the cursor() method
            cursor = db_connection.cursor()
            # print("Table function activated")
            # Format batchyear for table name
            tablenames=[]
            try :
                # trying to get the all the tables 
                cursor.execute("show tables")
                tables = cursor.fetchall()
                # Process the rows
                for table in tables:
                    # print(row)
                    k=str(table)
                    k=k.replace("(","")
                    k=k.replace(")","")
                    k=k.replace("'","")
                    k=k.replace(",","")
                    tablenames.append(k)
            except Exception as e:
                print(e)
            print(tablenames)
            try:
                # getting the each table schema
                for i in range(len(tablenames)):
                    try:
                     
                        print(type(tablenames[i]))
                        print(tablenames[i])
                        table=tablenames[i]
                        query=f"desc {tablenames[i]}"
                        cursor.execute(query)
                        column_description=cursor.fetchall()
                        
                        count=0
                        semister = [[] for _ in range(8)] 
                        index =[[] for _ in range(8)] 
                        # print(indexs)
                        try:
                            for i in column_description:
                                # print(i)
                                val=str(i[0])
                                # print(type(val))
                                count+=1
                                if count<=4:
                                    continue
                                if "SGPA" in val:
                                    h,j=val.split("_")
                                else:
                                    g,h,i,k,j,l,m=val.split("_")
                                # to clasify the semister and also 
                                if "I" == j:
                                    semister[0].append(val)
                                    print(val)
                                    if 'SGPA' in val:
                                        inde=len(semister[0])-1
                                        index[0].append(inde)
                                  
                                elif "II" == j:
                                    semister[1].append(val)
                                    if 'SGPA' in val:
                                        inde=len(semister[1])-1
                                        index[1].append(inde)
                                  
                                elif "III"==j:
                                    semister[2].append(val)
                                    if 'SGPA' in val:
                                        inde=len(semister[2])-1
                                        index[2].append(inde)
                                    
                                elif "IV"==j:
                                    semister[3].append(val)
                                    if 'SGPA' in val:
                                        inde=len(semister[3])-1
                                        index[3].append(inde)
                                    
                                elif "V"==j:
                                    semister[4].append(val)
                                    if 'SGPA' in val:
                                        inde=len(semister[4])-1
                                        index[4].append(inde)
                                   
                                elif "VI"==j:
                                    semister[5].append(val)
                                    if 'SGPA' in val:
                                        inde=len(semister[5])-1
                                        index[5].append(inde)
                                    
                                elif "VII"==j:
                                    semister[6].append(val)
                                    if 'SGPA' in val:
                                        inde=len(semister[6])-1
                                        index[6].append(inde)
                                    
                                elif "VIII"==j:
                                    semister[7].append(val)
                                    if 'SGPA' in val:
                                        inde=len(semister[7])-1
                                        index[7].append(inde)
                                   
                                # print(indexs)
                        except Exception as e:
                            print(e)
                        print(semister)
                    

                        # calculating the no of semisters and deleting the empty semisters
                        
                        for item in semister[:]:
                            if item == []:
                                semister.remove(item)
                            
                        
                        for i in range(len(semister)):
                            ele=index[i][0]
                            sgp=str(semister[i].pop(ele))
                            semister[i].append(sgp)
                            
       
                       
                        print(semister)
                        
                        
                        full_table_data = []
                        
                        count=0
                        no_of_semister=["I","II","III","IV","V","VI","VII","VIII"]
                        update=0
                        sgpa_graph=[]
                        # print(semister)
                        for i in semister:
                            # print("the semister no is",count)
                            k=[]
                            sno=1
                            for j in i:
                                
                                if count==0:
                                    # print("ahi")
                                   
                                    k=["S. No.","Subjects code","Subject name","grade","SGPA","month year",no_of_semister[update]]
                                    full_table_data.append(k)
                                    update+=1
                                    count+=1
                                    # print(full_table_data)
                                cursor.execute(f"SELECT {j} FROM {table} WHERE Roll_No=%s ", (rollno,))
                                data = cursor.fetchall()
                                # print(list(data[0])[0])
                                if list(data[0])[0]==None:
                                    continue
                                if "SGPA" in j:
                                    sg,se=j.split("_")
                                    # print(data[0][0])
                                    if data[0][0]== "nan":
                                        kk=0
                                        ppr=[sno,sg,se,kk]
                                        sgpa_graph.append(ppr)
                                    else:
                                        ppr=[sno,sg,se,data[0][0]]
                                        sgpa_graph.append(ppr)
                                    full_table_data.append(ppr)
                                    
                                    # print(full_table_data)
                                    k=["S. No.","Subjects code","Subject name","grade","SGPA","month year",no_of_semister[update]]
                                    full_table_data.append(k)
                                    update+=1
                                    
                                else:
                                    if full_table_data[-1][0]=="S. No.":
                                        nn,pp,qq,rr,ss,tt,uu=j.split("_")
                                        monyea=f"({rr} {uu})"
                                        full_table_data[-1].append(monyea)
                                    lecturer_id,subjectname,subjectcode,month,semisterno,typ,examyear=j.split("_")
                                    check="not there "
                                    if 1:
                                        for k in range(len(full_table_data)):
                                            if full_table_data[k][1]==subjectcode:
                                                # print(full_table_data[k])
                                                # print(full_table_data[k-1][-3])
                                                
                                                if full_table_data[k][-3] in  ['O','A+','A','B+','B','C']:
                                                    check="is is there"
                                                elif full_table_data[k][-3] in  ['M','Ab'] or full_table_data[k-1][-3] ==np.nan:
                                                    full_table_data[k][-3]=data[0][0]
                                                    full_table_data[k][-2]=month+" "+examyear
                                                    full_table_data[k][-1]=int(full_table_data[k][-1])+1
                                                    check="is is there"
                                                    
                                                else:
                                                    full_table_data[k][-3]=data[0][0]
                                                    full_table_data[k][-2]=month+" "+examyear
                                                    full_table_data[k][-1]=int(full_table_data[k][-1])+1
                                                    check="is is there"
                                    if check=="not there ":                                   
                                        pp=[sno,subjectcode,subjectname,month,semisterno,typ]
                                        st=data[0][0]
                                        montyear= month+" "+examyear
                                        pp.append(st)
                                        pp.append(montyear)
                                        pp.append(0)
                                        full_table_data.append(pp)
                                sno+=1
                                        # print(full_table_data)
                                
                                
                        # print(full_table_data)
                        print("graph values are",sgpa_graph)
                        data=[]
                        #removing the subject code column form the table please
                        if "S. No."==full_table_data[-1][0]:
                            del full_table_data[-1]
                        print("ist me")
                        print(full_table_data)
                        print(sgpa_graph)
                        for i in sgpa_graph:
                            data.append(i[-1])
                        print(data)

                        # Extract y values
                        # y_values = [item[1] for item in data]
                        print("it came near the graph")
                        graph=generate_plot(data)
                        print(full_table_data)
                        if "Subjects" in full_table_data[-1]:
                            print("hai")
                        maxlen=len(full_table_data)-1
                        for i in range(len(full_table_data)):
                            if maxlen==i:
                                if full_table_data[maxlen][0]=="Subjects":
                                    del full_table_data[maxlen]
                        print("jao")
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
            db_connection.commit()

    except mysql.connector.Error as error:
        print(error)
    # j=0
    cursor.close()
    print(full_table_data)
    return full_table_data,details(rollno,dbname),graph
        # pass
# dbname="civil"
# rollno='13641A0569'
# results2(dbname,rollno)
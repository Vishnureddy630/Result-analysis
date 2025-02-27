import mysql.connector 
def all_data(batch):
    my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database="csm")
    cursor=my.cursor()
    cursor.execute(f"desc {batch}")
    column_name=[]
    data=cursor.fetchall()
    # print(data)
    for i in data:
        column_name.append(i[0])
    semister=[[],[],[],[],[],[],[],[]]
    for m in column_name:
        if m=="Roll_No"  :
            continue
        p=[]
        p=m.split("_")
        # print(p)
        if p[0]=="SGPA" or p[0]=="Roll_No"  or p[0]=="Name" or p[0]=="Section" or p[0]=="CGPA":
            continue
        # print(m)
        if p[3]=="I":
            semister[0].append(m)
        elif p[3]=="II":
            semister[1].append(m)
        elif p[3]=="III":
            semister[2].append(m)
        
    wholedata=[]
    cursor.execute(f"SELECT DISTINCT Section FROM {batch}")
    data0=cursor.fetchall()
    section=[]
    for i in data0:
        section.append(i[0])
    # section_wise_data={}
    # for j in section:
    # print(semister)
    section.append("")
    for sec in section:
        if sec:
            print("CSM-",sec)
        else:
            print("CSM cumilative")
        print("subject code","subject name","semister","monthe year","total strength","qualified","fail","absent")
        for i in semister:
            for ij in i:
                if sec:
                    cursor.execute(f"select {ij} from {batch} where Section='{sec}'")
                else:
                    cursor.execute(f"select {ij} from {batch} ")
                data1=cursor.fetchall()
                val=[]
                fail=0
                qulified=0
                absent=0
                total=0
                for j in data1:
                    m=j[0]
                    val.append(j[0])
                    if m=="O" or m=="A+" or m=="A" or m=="B+" or m=="B" or m=="C":
                        qulified+=1
                        # elif m=="AB":
                    elif m=="P":
                        continue
                    else:
                        absent+=1
                    total+=1
                su=[]
                su=ij.split("_")
                k=[]
                k=[su[0],su[1],su[3],su[4],su[2],su[5],total,qulified,total-qulified,absent]
                wholedata.append(k)

                print(su[0],su[1],su[3],su[4],su[2],su[5],total,qulified,total-qulified,absent)
    # print(wholedata)
                
# all_data("2021_2025")
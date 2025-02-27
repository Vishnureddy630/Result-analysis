import mysql.connector

def profile(leacturerid):
    totaldata={}
    # this is used for the all branchs data of leacture to get the irrespctive of branchs
    my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123")
    cursor=my.cursor()
    cursor.execute(f"show databases ")
    tempbranchs = cursor.fetchall()
    
    branchs=[]
    for bran in tempbranchs:
        branchs.append(bran[0])
    
    # print(branchs)  

    for branch in branchs:      
        my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database=branch)
        cursor=my.cursor()
        try:
            # this is for use to get the tables names in database 
            # remember each database is a branch and each table is a dedecated to the a batchs
            cursor.execute(f"show tables ")
            batchs = cursor.fetchall()
            
            batchss=[]
            for seee in batchs:
                batchss.append(seee[0])
            
            for b in batchss:
                # print(b)
                # getting  the section 
                
                cursor.execute(f"select DISTINCT Section from "+b+"")
                sections = cursor.fetchall()

                # getting the coulmn names
                cursor.execute(f"desc {b}")
                tempcolumn= cursor.fetchall()

                # filtering the column names removing the column which the leacture didn't thought
                column=[]
                for i in tempcolumn:
                    if leacturerid in i[0]:
                        column.append(i[0])
                # print(column)

                grades=['O','A+','A','B+','B','C','AB','M','F']
                
                data={}
                for s in sections:
                    for c in column:
                        # print(c)
                        templist=[]
                        totalstudents=0
                        Passed=0
                        for g in grades:
                            cursor.execute(f"select count(*) from  {b} where {c}='{g}' and Section='{s[0]}' ")
                            count= cursor.fetchall()
                            templist.append(count[0][0])
                            if g in ['AB','M','F']:
                                totalstudents+=count[0][0]
                            else:
                                Passed+=count[0][0]
                                totalstudents+=count[0][0]
                        templist.append(Passed)
                        templist.append(totalstudents)
                        passper=(Passed/totalstudents)*100
                        templist.append(passper)
                        data[c+"_"+str(s[0])]=templist
                # print(data)
                if data=={}:
                    continue
                totaldata[branch+"  "+b]=data
        except Exception as e:
            # print( e)
            pass
    # print(totaldata)
    htmlcode=""
    htmlcode+="<table>"
    htmlcode+="<thead>"
    htmlcode+="<tr>"
    htmlcode+="<th>Branch</th><th>Subject</th><th>Section</th>"
    grades=['O','A+','A','B+','B','C','AB','M','F','Passed','Total','Pass%']
    for g in grades:
        htmlcode+="<th>"+g+"</th>"
    htmlcode+="</tr>"
    htmlcode+="</thead>"
    for branch, subjects in totaldata.items():
        for subject, values in subjects.items():
            htmlcode += "<tr>"
            htmlcode += f"<td>{branch}</td>"
            htmlcode += f"<td>{subject}</td>"
            htmlcode += f"<td>{values[0]}</td>"  # Assuming section is the first value in the list
            for value in values[1:]:
                htmlcode += f"<td>{value}</td>"
            htmlcode += "</tr>"

    htmlcode += "</tbody>"
    htmlcode += "</table>"   
    return htmlcode 
   
    
leacturerid='4046'
branch='civil'
print(profile(leacturerid) )
    
    




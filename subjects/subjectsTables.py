import mysql.connector
import numpy as np
def subjectscumilative(branch,batch,semister):
    my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database=branch)
    cursor=my.cursor()
    try:
        print(batch)
       
        # this is for use to get column names form the tables
        cursor.execute(f"desc "+batch+"")
        data = cursor.fetchall()
    
        # firts filtering (removing the Roll_No,Name,Section,CGPA,Supplementary and unrelated semister from the columnames)
        columnnames=[]
        for i in data:
            if i[0] in 'Roll_No Name Section CGPA':
                continue
            else:
                # print(i[0])
                colum=[]
                colum=i[0].split("_")
                if len(colum)==2 or colum[-2]=='Supplementary' or colum[-3]!=semister:
                    continue
                columnnames.append(i[0])
        print(columnnames)
        
        grades=['O','A+','A','B+','B','C','AB','M','F']
        
        
        data={}     
        # This loop is for the columnames respectively
        for i in columnnames:
            totalstudents=0
            Passed=0
            # This loop is for the grades
            for grade in grades:
                try:
                    val=""
                    cursor.execute(f"SELECT COUNT(*) AS TABLEE FROM {batch} WHERE {i}='{grade}' ")
                    countofgrades = cursor.fetchall()
                    val=countofgrades[0][0]
                    if i in data:
                        data[i].append(str(val))
                        # data[i]=data[i]+"_"+str(countofgrades[0][0])
                    else:
                        data[i]=[str(val)]
                    # print(i,grade,countofgrades,data[i])
                    if grade in ['AB','M','F']:
                        totalstudents+=val
                    else:
                        Passed+=val
                        totalstudents+=val
                except Exception as e:
                    print("inised",e)
            try:
                data[i].append(str(Passed))
                data[i].insert(0,str(totalstudents))
                passper=(Passed/totalstudents)*100
                data[i].append(int(passper))
            except Exception as e:
                print(e)
        key=[]
        for i in data:
            key.append(i)
        grades=['Candidates','O','A+','A','B+','B','C','AB','M','F','Passed','Pass%']
            
        values=[[] for _ in range(len(grades)+1)] 
        
        # for columnnames 

        values[0].append('Item')
        for c in columnnames: 
            subject=c.split('_')   
            values[0].append(subject[1].replace('$'," "))
            # print(count,c)

        count=1
        # appending the grades
        for pp in grades:
            values[count].append(pp)
            count+=1
            
            

        # appending the value to the list 
        for v  in  key:
            count=1
            for d in data[v]:
                values[count].append(d)
                count+=1  
        print(values)
        count=0
        htmlcodefortable=""
        htmlcodefortable+="<table>"
        for i in values:
            
            if count==0:
                htmlcodefortable+="<thead>"
                htmlcodefortable+="<tr>"
                for j in i:
                    htmlcodefortable+="<th>"+str(j)+"</th>"    
                htmlcodefortable+="</tr>"
                htmlcodefortable+="<thead>"
                count+=1
            else:
                htmlcodefortable+="<tr>"
                for j in i:
                    htmlcodefortable+="<td>"+str(j)+"</td>"    
                htmlcodefortable+="</tr>"
            
        htmlcodefortable+="</table>" 

    except Exception as e:
        print(e)
    return htmlcodefortable



# branch='civil'
# batch='2021_2025'
# semister='I'
# subjectscumilative(branch,batch,semister)




def subjects(branch,batch,semister):
    my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database=branch)
    cursor=my.cursor()
    try:
        print(batch)
        # this is for use to get the section names in the table form the tables
        cursor.execute(f"select DISTINCT Section from "+batch+"")
        section = cursor.fetchall()
        print(section)
        sections=[]
        for seee in section:
            sections.append(seee[0])
        sections = sorted(sections)
        # this is for use to get column names form the tables
        cursor.execute(f"desc "+batch+"")
        data = cursor.fetchall()
    
        # firts filtering (removing the Roll_No,Name,Section,CGPA,Supplementary and unrelated semister from the columnames)
        columnnames=[]
        for i in data:
            if i[0] in 'Roll_No Name Section CGPA':
                continue
            else:
                # print(i[0])
                colum=[]
                colum=i[0].split("_")
                if len(colum)==2 or colum[-2]=='Supplementary' or colum[-3]!=semister:
                    continue
                columnnames.append(i[0])
        # print(columnnames)
        grades=['O','A+','A','B+','B','C','AB','M','F']
        totaldata={}
        
        subjectsdata=[]
        # This loop is for the respective section as we got and want
        for sec in sections:
            data={}
            # This loop is for the columnames respectively
            for i in columnnames:
                totalstudents=0
                Passed=0
                # This loop is for the grades
                for grade in grades:
                    try:
                        val=""
                        cursor.execute(f"SELECT COUNT(*) AS TABLEE FROM {batch} WHERE {i}='{grade}' AND section='{sec}'")
                        countofgrades = cursor.fetchall()
                        val=countofgrades[0][0]
                        if i in data:
                            data[i].append(str(val))
                            # data[i]=data[i]+"_"+str(countofgrades[0][0])
                        else:
                            data[i]=[str(val)]
                        print(i,grade,countofgrades,data[i])
                        if grade in ['AB','M','F']:
                            totalstudents+=val
                        else:
                            Passed+=val
                            totalstudents+=val
                    except Exception as e:
                        print("inised",e)
                try:
                    data[i].append(str(Passed))
                    data[i].append(str(totalstudents))
                    passper=(Passed/totalstudents)*100
                    data[i].append(passper)
                except Exception as e:
                    print(e)
            """Adding the nested list with the main key is subject name if it exist the atomaticaly the value will
             be added to the nested list and if the value is not there then also the value is added and we do this
             for gathering the same subject marks and data togethter"""
            for jj in data:
                column=jj.split("_")
                if column[2] in totaldata:
                    totaldata[column[2]][jj+"_"+str(sec)]=data[jj]
                else:
                    totaldata[column[2]]={jj+"_"+str(sec):data[jj]}
                  

        htmlcodefortable=""
        htmlcodefortable=subjectscumilative(branch,batch,semister)
        for i in totaldata:
            htmlcodefortable+="<table>"
            htmlcodefortable+="<thead>"
            lecturername=[]
            sectionnames=[]
            key=[]
            for k in totaldata[i]:
                # print(k,totaldata[i][k])
                data=k.split("_")
                lecturername.append(data[0])
                sectionnames.append(data[-1])
                key.append(k)
            htmlcodefortable+="<thead>"
            htmlcodefortable+="<tr>"
            htmlcodefortable+="<th>"+str(data[1]).replace('$'," ")+"</th>"
            
            for sect in sectionnames:
                htmlcodefortable+="<th>Section-"+sect+"</th>"
            htmlcodefortable+="<th>All</th>"
            htmlcodefortable+="</tr>"
            htmlcodefortable+="<tr>"
            htmlcodefortable+="<th>Teacher</th>"


            my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database='lecture')
            cursor=my.cursor()
            for lect in lecturername:
                cursor.execute(f"SELECT DISTINCT Employee_Name FROM data WHERE Emp_Id='{lect}'")
                name = cursor.fetchall()
                htmlcodefortable+="<th>"+str(name[0][0])+"</th>"
            htmlcodefortable+="<th>---</th>"
            htmlcodefortable+="</tr>"            
            htmlcodefortable+="</thead>"
            grades=['O','A+','A','B+','B','C','AB','M','F','Passed','Total','Pass%']
            
            values=[[] for _ in range(len(grades)+1)] 
            count=0
            # appending the grades
            for pp in grades:
                values[count].append(pp)
              
                count+=1

            # appending the value to the list 
            for v  in  key:
                count=0
                for d in totaldata[i][v]:
                    values[count].append(d)
                    count+=1

            
            print("the length",len(values))
            print(values)
            for mm_index, mm in enumerate(values):  # Get the index of the outer list
                countt = 0
                sum=0
                for nn_index, nn in enumerate(mm):  # Get the index of the inner list
                    if countt < 1:
                        pass  # Skip the first two elements
                    else:
                        values[mm_index][nn_index] = int(values[mm_index][nn_index])  # Modify the element
                        sum+=int(values[mm_index][nn_index]) 
                    countt += 1
                values[mm_index].append(sum)
            for p in values:
                htmlcodefortable+="<tr>"
                
                for q in p:
                    htmlcodefortable+="<td>"+str(q)+"</td>"
                    # print(q)
                
                htmlcodefortable+="</tr>"
                print(p)
            
            htmlcodefortable+="</table>"
        # print(sectionnames,lecturername,key)
        # print(htmlcodefortable)
        return htmlcodefortable,semister,batch
    except Exception as error:
        print(error)
    
    pass


# '''
# Pass_Percentage=( Total_Number_of_Students/Number_of_Passed_Students)*100'''
# branch='civil'
# batch='2021_2025'
# semister='I'
# subjects(branch,batch,semister)


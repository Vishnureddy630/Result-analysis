import mysql.connector
import numpy as np
def faculty(branch):
    my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database=branch)
    cursor=my.cursor()
    # this shows the no of the tables in the database 
    cursor.execute("show tables")
    data=cursor.fetchall()
    lecturedata={}
    # the exception will share come becaues the table will iterate till the no of table the database have
    try:
        # this loop is use to get column names 
        for tablename in data:
            print(tablename[0])
            cursor.execute(f"desc "+tablename[0]+"")
            data = cursor.fetchall()
            # print(data)

            
            # firts filtering (removing the Roll_No,Name,Section,CGPA,Supplementary from the columnames)
            for i in data:
                if i[0] in 'Roll_No Name Section CGPA':
                    continue
                else:
                    # print(i[0])
                    colum=[]
                    colum=i[0].split("_")
                    if len(colum)==2 or colum[-2]=='Supplementary':
                        continue
                    
                    # getting the pass percentage of the each column or each lecturar
                    cursor.execute(f"select "+i[0]+" from  "+tablename[0]+" ")
                    rowvalues = cursor.fetchall()
                    # print(rowvalues)

                    # getting trouble to get the nan vlaues are non subject students according to the database table 
                    pass_student=0
                    total_section=0
                    for j in rowvalues:
                        if j[0]==np.nan:
                            continue
                        elif j[0] !='AB' or j[0] !='F'  or j[0]!='M' :
                            pass_student+=1
                        total_section+=1
                    
                    """First one is the no of student pass and second one is no of student in the section 👇🏼 
                    and also removing or adding the values if the key is exist.  for the same branchs
                     and also remember one thing that the dictonary is from the out of the loop this means 
                    all the sections and all the batchs data will be taken here so this is correct and also
                      replacing the column name with the lecturerid insted"""
                    lecturerid=i[0].split("_")
                    
                    if lecturerid[0] in lecturedata:
                        datafromdict=lecturedata[lecturerid[0]].split("_")
                        lecturedata[lecturerid[0]]=""+str(datafromdict[0]+pass_student)+"_"+str(datafromdict[1]+total_section)+""
                    else:
                        lecturedata[lecturerid[0]]=""+str(pass_student)+"_"+str(total_section)+""
            
            my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database="lecture")
            cursor=my.cursor()
            lecturedatalist=[]
            for va in lecturedata:
                # print(va,lecturedata[va])
                data=lecturedata[va].split("_")
                cursor.execute("select Employee_Name from data where Emp_Id="+va+"")
                lecturername=cursor.fetchall()
                lecturedata[va]=str(lecturername[0][0])+"_"+str(va)+"_"+str(lecturedata[va])+"_"+str((int(data[0])/int(data[1]))*100)
                # print(lecturedata[va])
                lecturedatalist.append(lecturedata[va].split("_"))
        
        # Sorting by the last element (as a float) in descending order
        sorted_data_desc = sorted(lecturedatalist, key=lambda x: float(x[-1]), reverse=True)

        # Output the sorted data
        top10=[]
        count=0
        for item in sorted_data_desc:
            count+=1
            top10.append(item)
            print(count,item)
            if count==10:
                break
            
            
        # print(top10)
        n=10
        count=0
        leaderbordhtmlcode=""
        for i in range(1,n+1):
            leaderbordhtmlcode+="<div class='row'>"
            for j in range(i):
                leaderbordhtmlcode+="<div class='card'>"
                print(top10[count],end="  ")
                leaderbordhtmlcode+="<div ><img style='border: solid; border-radius: 50%; width: 100px;' src='data:image/jpeg;base64,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' alt='lecturer image'></div>"
                leaderbordhtmlcode+="<h3>Rank :"+str(count+1)+"</h3>"
                leaderbordhtmlcode+="<p>"+str(top10[count][0])+"</p>"
                leaderbordhtmlcode+="<p> Id:"+str(top10[count][1])+"</p>"
                leaderbordhtmlcode+="<p>No of Students passed / Total No of students"+str(top10[count][2])+"/"+str(top10[count][3])+"</p>"
                leaderbordhtmlcode+="<h3>Pass %:"+str(top10[count][-1])+"</h3>"
                leaderbordhtmlcode+="</div>"
                count+=1
            leaderbordhtmlcode+="</div>"
            if i==4:
                break    
            print("\n")
        
        rows=""
        for k in range(len(sorted_data_desc)):
            rows+="<tr>"
            rows+="<td>"+str(k+1)+"</td>"
            rows+="<td>"+str(sorted_data_desc[k][0])+"</td>"
            rows+="<td>"+str(sorted_data_desc[k][1])+"</td>"
            rows+="<td>"+str(sorted_data_desc[k][2])+"</td>"
            rows+="<td>"+str(sorted_data_desc[k][3])+"</td>"
            rows+="<td>"+str(sorted_data_desc[k][4])+"</td>"
            rows+="</tr>"

                    
        return leaderbordhtmlcode,rows
    except Exception as error:
        print(error)
    
    pass


# '''
# Pass_Percentage=( Total_Number_of_Students/Number_of_Passed_Students)*100'''
# branch='Mech'
# faculty(branch)
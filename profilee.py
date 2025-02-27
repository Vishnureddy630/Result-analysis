import mysql.connector
def detailsofleacturerf(leacturerid):
    import mysql.connector

    # Connect to the database
    my = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vishnu@123",
        database='lecture'
    )

    cursor = my.cursor()

    # Execute the query
    cursor.execute(f"SELECT DISTINCT * FROM data WHERE Emp_Id={leacturerid}")

    # Fetch all the data
    data = cursor.fetchall()

    # Get the column names
    column_names = [i[0] for i in cursor.description]

    # Combine column names and values
    datapro=[]
    result = []
    for row in data:
        datapro.extend(row)
        result.append(dict(zip(column_names, row)))

    # Print the results
    for item in result:
        print(item)

    # Close the cursor and connection
    cursor.close()
    my.close()

    htmlcode=""
    htmlcode+="<div class='profile-header'>"
    htmlcode+="<img src='https://pbs.twimg.com/media/EZYX2gkWAAES12y.jpg' alt='Lecturer Photo'>"
    htmlcode+="<div><h1>"+datapro[0]+"</h1><h2>"+datapro[1]+"</h2><h1>"+datapro[2]+"</h1></div></div>"
    if datapro[3]== None:
        htmlcode+=" <div class='profile-section'><h3>About Me</h3><p>Dr. John Doe has over 15 years of experience in the field of computer science. He specializes in artificial intelligence,machine learning, and software engineering. He has published numerous research papers in top journals and has been awarded  multiple grants for his work on intelligent systems. </p> </div>"
    else:
        htmlcode+=" <div class='profile-section'><h3>About Me</h3><p>"+str(datapro[3])+"</p> </div>"
    if datapro[4]== None:
        htmlcode+=" <div class='profile-section'><h3>Education</h3><p><strong>Ph.D. in Computer Science</strong> - University of Technology, 2008</p>  <p><strong>M.S. in Software Engineering</strong> - State University, 2004</p>  <p><strong>B.S. in Computer Science</strong> - City University, 2002</p>       </div>"
    else:
        htmlcode+=" <div class='profile-section'><h3>Education</h3>"
        dicto=datapro[4]
        for i in dicto:
            htmlcode+="<p><strong>"+str(i)+"</strong>"+str(dicto[i])+"</p>"
        htmlcode+="</div>"
    
    if datapro[5]== None:
        htmlcode+=" <div class='profile-section'><h3>Research Interests</h3><p> Artificial Intelligence, Machine Learning, Data Science, Software Engineering, Intelligent Systems, Natural Language Processing.    </p> </div>"
    else:
        htmlcode+=" <div class='profile-section'><h3>Research Interests</h3><p>"+str(datapro[5])+"</p> </div>"
    if datapro[6]== None:
        htmlcode+="<div class='profile-section'> <h3>Courses Taught</h3>         <p>     <ul>        <li>Introduction to Artificial  Intelligence</li> <li>Advanced Machine Learning</li>   <li>Data Structures and Algorithms</li>  <li>Software Engineering Principles</li> </ul></p></div> "        
    else:
        htmlcode+=" <div class='profile-section'><h3>Courses Taught</h3>"
        da=datapro[6]
        htmlcode+="<p><ul>"
        for i in da:
            htmlcode+="<li>"+str(i)+"</li>"                       
        htmlcode+="</ul></p>"
        htmlcode+="</div>"
    if datapro[7]== None:
        htmlcode+=" <div class='profile-section contact-info'> <h3>Contact Information</h3> <p>Email: <a href='mailto:johndoe@university.edu'>johndoe@university.edu</a></p> <p>Phone: (123) 456-7890</p>  <p>Office: Room 123, Department of Computer Science</p>   </div>"
    else:
        htmlcode+=" <div class='profile-section contact-info'><h3>Contact Information</h3>"
        da=datapro[7]
        htmlcode+=" <p>Email: <a href='mailto:"+str(da[0])+"'>"+str(da[0])+"</a></p>"
        htmlcode+="<p>Phone:"+str(da[1])+"</p>  <p>"
        htmlcode+=" <p>Office: "+str(da[2])+"</p> "
        htmlcode+="</div>"
    # print(datapro)
    return htmlcode

    
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
                    if  'Supplementary' in i[0]:
                        continue
                    if leacturerid in i[0] :
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
                        templist.append(f"{passper:.2f}%")
                        data[c+"$"+str(s[0])]=templist
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
            va=subject.split("$")
            htmlcode += f"<td>{va[0]}</td>"
            htmlcode += f"<td>{va[1]}</td>"
            htmlcode += f"<td>{values[0]}</td>"  # Assuming section is the first value in the list
            for value in values[1:]:
                htmlcode += f"<td>{value}</td>"
            htmlcode += "</tr>"

    htmlcode += "</tbody>"
    htmlcode += "</table>"  
    # Close the cursor and connection
    cursor.close()
    my.close() 
    return htmlcode ,detailsofleacturerf(leacturerid)
   
    
# leacturerid='4046'

# # print(profile(leacturerid) )

# detailsofleacturerf(leacturerid)
    
    




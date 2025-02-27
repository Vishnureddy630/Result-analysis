import mysql.connector 
import matplotlib.pyplot as plt
import numpy as np
import base64
import io

import pandas as pd
def lectureperformance(branch,table,section):
    my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database=branch)
    cursor=my.cursor()
    cursor.execute(f"desc {table}")
    data=cursor.fetchall()
   
    
    semister=[[],[],[],[],[],[],[],[]]
    fortable=[]
    # print(data)
    
    for i in data:      
        if 'Roll_No' in i[0] or 'Name' in i[0] or 'Section' in i[0] or 'CGPA' in i[0]  or 'SGPA' in i[0]:
            continue
        'make the filter to make it come in semister wise like seminste 1 next 2 next 3 and so............'
        temp=[]
        '4046_Mathematics_B20CS37_Oct_II_Regular_2021'
        val=i[0].split("_")
        if val[-2]!="Regular":
            continue
        # print(val)
        s=val[-3]
        # print(s)
        if s=="I":
            semister[0].append(i[0])
        elif s=="II":
            semister[1].append(i[0])
        elif s=="III":
            semister[2].append(i[0])
        elif s=="IV":
            semister[3].append(i[0])
        elif s=="V":
            semister[4].append(i[0])
        elif s=="VI":
            semister[5].append(i[0])
        elif s=="VII":
            semister[6].append(i[0])
        elif s=="VIII":
            semister[7].append(i[0])

    

    # print(columnnames)
    
    data=[]
    
    # print(len(data[0]))
    grades=['O','A+','A','B+','B','C','AB','M','F']
    count=0
    semi=["I","II","III","IV","V","Vi","VII","VIII"]
    for j in semister:
        # print(j)
        temp=[]   
        if not j:
            continue
        temp.append(['Lecturar Name','Subject Name','subject code','Total Strength','O','A+','A','B+','B','C','AB','M','F','Passed','Pass %',str(semi[count])])
        my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database=branch)
        cursor=my.cursor()
        for i in j:
            # column names are taken 
            # print(i)
            if i==[]:
                continue
            # print(i)
            tempro=[]
            '4046_Mathematics_B20CS37_Oct_II_Regular_2021'
            # print(i)
            # spliting the data and making it for the table
            val=i.split("_")
            tempro.append(val[0])
            tempro.append(val[1])
            tempro.append(val[2])
             
            # getting the no of grades 
            passpeople=0
            totalmembers=0
            for jj in grades:
                if section=="ALL":
                    cursor.execute(f"SELECT COUNT(*) AS TABLEE FROM 2021_2025 WHERE {i}='{jj}'")
                    tempro.append(cursor.fetchall()[0][0])

                else:
                    cursor.execute(f"SELECT COUNT(*) AS TABLEE FROM 2021_2025 WHERE {i}='{jj}' and section='{section}'")
                    tempro.append(cursor.fetchall()[0][0])
                totalmembers+=tempro[-1]
                if jj=='AB'or jj=='M' or jj=='F':
                    continue
                passpeople+=tempro[-1]
            print(totalmembers)
            # total value
            tempro.insert(3,totalmembers)

            # pass value
            tempro.append(passpeople)
            # pass %
            tempro.append(int((passpeople/totalmembers)*100))
            
            
            temp.append(tempro)
            

            

        # changing the punchi id with the respected names 
        my=mysql.connector.connect(host="localhost",user="root",password="vishnu@123",database='lecture')
        cursor=my.cursor()
        co=0
        print(temp)
        for i in temp:
            if i[0]=="Lecturar Name":
                continue
            cursor.execute(f"select  Employee_Name from data where Emp_Id='{i[0]}'")
            val=cursor.fetchall()
            # print(val)
            co+=1
            temp[co][0]=val[0][0]  
        
       
        # data.append(['Lecturar Name','Subject Name','subject code','Total Strength','O Grade','A+ Grade','A Grade','B+ Grade','B Grade','C Grade','AB Grade','M Grade','Fail Grade','Passed','Pass %',str(semi[count])])
        co+=1
        if not temp:
            continue
        
        data.append(temp)
        # fortable.append()

    
    
    # arranging the data in the table formate as we asumed
    # print(len(['Lecturar Name','Subject Name','subject code','Total Strength','O Grade','A+ Grade','A Grade','B+ Grade','B Grade','C Grade','AB Grade','M Grade','Fail Grade','Passed','Pass %']))
    
    # tablelist=[[],[],[],[],[],[],[],[],[],[],[],[],[]]
    # print(len(tablelist))
    # cou=0
    # for i in data:
    #     if cou==0:
    #         cou+=1
    #         continue
    #     for j in range(len(i)):
    #         # print(len(i))
    #         # print(j)
    #         if j==0:
    #             tablelist[0].append(i[0])
    #         elif j==1:
    #             tablelist[1].append(i[1])
    #         elif j==2:
    #             tablelist[2].append(i[2])
    #         elif j==3:
    #             tablelist[3].append(i[3])
    #         elif j==4:
    #             tablelist[4].append(i[4])
    #         elif j==5:
    #             tablelist[5].append(i[5])
    #         elif j==6:
    #             tablelist[6].append(i[6])
    #         elif j==7:
    #             tablelist[7].append(i[7])
    #         elif j==8:
    #             tablelist[8].append(i[8])
    #         elif j==9:
    #             tablelist[9].append(i[9])
    #         elif j==10:
    #             tablelist[10].append(i[10])
    #         elif j==11:
    #             tablelist[11].append(i[11])
    #         elif j==12:
    #             tablelist[12].append(i[12])
            
          
    # print(tablelist)
    # print("/n")
    # print(data)
    # print(len(data))
    fortable.extend(data)
    # print(fortable)
    datasets=data
    print("the datasets")
    
    print(datasets)
    # Create a figure with multiple subplots (one for each dataset)

    num_datasets = len(datasets)
    fig, axes = plt.subplots(nrows=num_datasets if num_datasets > 1 else 1,
                             ncols=1,
                             figsize=(50, max(num_datasets * 6, 6)))

    # Ensure axes is always an array for consistent access
    if num_datasets == 1:
        axes = [axes]

    # Loop through each dataset and create a bar graph
    for ax_idx in range(num_datasets):
        data = datasets[ax_idx]
        
        # Extracting relevant data
        subjects = [row[1] for row in data[1:]] # Subject names
        lecturers = [row[0] for row in data[1:]] # Lecturer names
        grades = np.array([row[4:13] for row in data[1:]]) # Extract grades for each subject

        # Set the width of the bars
        bar_width = .1

        # Set positions of bar groups on x-axis
        x = np.arange(len(subjects))

        # Create bars for each grade
        for i in range(grades.shape[1]):
            bars = axes[ax_idx].bar(x + i * bar_width , grades[:, i], width=bar_width,
                              label=f'{data[0][4 + i]}') # Using header names for labels
            
            # Add text annotations for each bar
            for j in range(len(bars)):
                height = bars[j].get_height()
                axes[ax_idx].text(bars[j].get_x() + bars[j].get_width()/2 - bar_width/4,
                            height,
                            str(int(height)),
                            ha='center',
                            va='bottom',
                            fontsize=8)
                axes[ax_idx].text(bars[j].get_x() + bars[j].get_width()/2 - bar_width/4,
                            height + (height * -1), 
                            data[0][4 + i], 
                            ha='center',
                            va='bottom',
                            fontsize=10)

        # Add subject names and lecturer names with proper spacing to avoid overlap
        for i in range(len(subjects)):
            axes[ax_idx].text(x[i] - bar_width/2 + (bar_width / len(grades))/2,
                        -3,
                        subjects[i], 
                        ha='center',
                        va='top',
                        fontsize=10)
            
            axes[ax_idx].text(x[i] - bar_width/2 + (bar_width / len(grades))/2,
                        -10.0,
                        lecturers[i], 
                        ha='center',
                        va='top',
                        fontsize=10)

        # Adding labels and title for each subplot
        # axes[ax_idx].set_xlabel('Subjects')
        axes[ax_idx].set_ylabel('Number of Students')
        axes[ax_idx].set_title(f'Grade Distribution ({ax_idx + 1})')
        axes[ax_idx].set_xticks(x)
        axes[ax_idx].set_xticklabels(['' for _ in range(len(subjects))]) # Remove x-tick labels
        axes[ax_idx].legend(title='Grades')

    # Adjust spacing between subplots
     # Add a legend
    plt.legend()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Clear the plot to avoid overlap in future plots
    plt.clf()


    table=[]
    for i in fortable:
        for j in i:
            table.append(j)
    # print(table)    
    return table,plot_url
        

# lectureperformance('Mech','2021_2025','Sheet1','Regular')


from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
import DataInserter as de
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("DataInserter.html")

@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    # getting the values form the javascript and we are not using the form to get the values form the direct html
    file = request.files['file']
    semester = request.form.get('Semister')
    status = request.form.get('Status')
    batch_year = request.form.get('BatchYear')
    month = request.form.get('Month')
    exam_year = request.form.get('examyear')
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Process the file (for now, just print its name)
    df=pd.read_excel(file)
    
    # checking the data is in correct formate as per requeryment
    data =df.columns.tolist()
    excel_file = pd.ExcelFile(file)

    # getting the sheets name sheet name == section name
    # note : each sheet is considered as a section from a baranch
    sheet_names = excel_file.sheet_names
    
    
    fortheif=0
    bigmessage={}
    rows=""
    for section in sheet_names:
        tempmessage=["","",""]
       
        dfs = pd.read_excel(excel_file, sheet_name=section)
        
        # createing the column names in the table  for this sheet / this section 
        column_names=[]  
        count=0
       
        for name in dfs.columns.tolist():
            
            if "Unnamed" in str(name) :
                if count<1:
                    column_names.append("")
                    count+=1
                    continue
                count+=1
                column_names.append("")
            else:
                column_names.append(name)
        
        count=0
        for index, row in dfs.iterrows():
            temp=row.to_list()    
            minicount=0
            for i in range(len(temp)):
                if  np.nan == temp[i] or "nan" in str(temp[i]) or 'Unnamed' in str(temp[i]):
                    column_names[i]=str(column_names[i])+"_"
                    continue
               
                column_names[i]=str(column_names[i])+"_"+str(temp[i])
            count+=1
            if count==2:
                break

        #  removing the underscro(_) from rollno,sgpa & cgpa 
        for i in range(len(column_names)):
            if i==0 or i==len(column_names)-2 or i==len(column_names)-1:
                column_names[i]=str(column_names[i]).replace("_","")
            
       

        #  checking the missing lecture id or subject code or subject name 
        # we are giving the user the cell name as per the excel sheet

        Abc=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        for i in range(len(column_names)):
            if i<0 or i==len(column_names)-1 or i==len(column_names)-2:
                continue
            arr=list(column_names[i].split("_"))
            value=0
            for j in arr:
                # value+=1
                print(j)
                if len(j)<1:
                    if value==0:
                        # emptylectureno+=str(i)
                        # missing lecturer id is taken here
                        tempmessage[0]+="   "+Abc[i]+str(value+1)
                        fortheif+=1
                    elif value==1:
                        # subjectname+=str(i)
                        # missing subject name  is taken here 
                        tempmessage[1]+="   "+Abc[i]+str(value+1)
                        fortheif+=1
                    elif value==2:
                        # subjectcode+=str(i)
                        # missing subject code is taken here
                        tempmessage[2]+="   "+Abc[i]+str(value+1)
                        fortheif+=1
                    
                value+=1
        
        if section not in bigmessage:
            bigmessage[section]=''
        bigmessage[section]=tempmessage
        onerow="<td style='border: 1px solid black; padding: 8px;'>"+section+"</td>"
        for i in range(len(tempmessage)):
            onerow+="<td style='border: 1px solid black; padding: 8px;'>"+tempmessage[i]+"</td>"
          
        rows+="<tr>"+onerow+"</tr>"
      
      
    if fortheif>0:
        # table is created if it have the missig column name in the sheet
        table="<aside align='right'><button onclick='closeModal()' class='close'>X</button></aside><table style='border-collapse: collapse; width: 350px; border: 1px solid black;'>        <thead style='border: 1px solid black; padding: 8px;'>            <tr >                <th style='border: 1px solid black; padding: 8px;'>Section/sheet name</th>                <th style='border: 1px solid black; padding: 8px;'>lecture id</th>                <th style='border: 1px solid black;'>Subject Name </th>                <th style='border: 1px solid black; padding: 8px;'>Subject code</th>            </tr>        </thead>        <tbody>"+rows+"       </tbody>    </table>"
        return jsonify({'message':table})
    else:
        # if we dont have any missing values(lectureid,subject name ,subject code) we will get into it and call function form the other file and insert the data in the database mysql
        dbname="civil"
        if status=='Regular':
            de.Regular(dbname,file,semester,status,batch_year,month,exam_year)
        else:
            de.Supplementary(dbname,file,semester,status,batch_year,month,exam_year)
            
        return jsonify({'message':"<p>everything is clear data is inserted sucessfully</p><button class='ok' onclick='closeModal()'>ok</button>"})


if __name__ == '__main__':
    app.run(debug=True)

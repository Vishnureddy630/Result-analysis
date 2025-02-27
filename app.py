from flask import Flask, render_template, request,jsonify

import fetchdata as fet
import semister_wise as sw
import semister_wise_section_data1 as sw1
import faculty as fe
import profilee as pe


import subjects.subjectsTables as sT 
import webbrowser
import tkinter as tk
from tkinter import filedialog
import threading

import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64

import allbatchs as al


dbname="civil"


def get_filename():
    root = tk.Tk()
    root.withdraw()  # Hide the window
    # root.deiconify()
    filename = filedialog.askopenfilename()
    root.destroy()  # Destroy the hidden window
    return filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html', error_message=None)

@app.route('/login', methods=['POST'])
def login():
    type_user=request.form['user']
    global filename
    if type_user=="admin":
        filename = get_filename()
        print(filename)
        return render_template("existing data.html",filename=filename)
    else:
        global user_info
        got_username = request.form['username']
        got_password = request.form['password']
        user_info={} 
        user_info['Name'] = got_username
        user_info['Roll_no']=got_password
        user_info['Branch']='csm'
       
        return render_template('Home.html',user_info=user_info)

@app.route('/close', methods=['POST'])
def close():
    return render_template('login.html', error_message=None)

@app.route('/capture')
def forwardsheduling():
    button_value = request.args.get('button')
    print(f'Button clicked: {button_value}')
    if button_value=='data_entry':
        return render_template('Data options.html')
    elif button_value=="Student":
        return render_template('enter_roll_no.html') 
    elif button_value=="Section wise"   :
        batch_options = sw.bathcs(dbname)  
        return render_template("semister_details.html",batch_options=batch_options)
    elif button_value == "Batchs":
        
        # Data for the plot
        value=al.allbatchs("csm")
        y = [float(value)]
        x = range(1, len(y) + 1)

        # Create a Matplotlib figure
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plotting the points with a line and filling the area under the curve
        ax.plot(x, y, color='blue', linewidth=2, linestyle='-', marker='o', markersize=8)
        ax.fill_between(x, y, color='skyblue', alpha=0.5)

        # Adding value annotations on each dot
        for i, (xi, yi) in enumerate(zip(x, y)):
            ax.text(xi, yi, f'{yi:.1f}', fontsize=13, va='bottom', color='black')

        # Placing names below the x-axis
        names = [f'Point {i}' for i in x]
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right')

        # Setting x and y axis range with padding on the x-axis
        ax.set_ylim(0, 10)
        ax.set_xlim(0.5, len(y) + 0.5)

        # Setting y-ticks to show every integer value
        ax.set_yticks(range(0, 11, 1))

        # Adding grid lines
        ax.grid(which='both', color="black", linestyle='-', linewidth=0.5, alpha=0.5)

        # Naming the x axis
        ax.set_xlabel('batchs', color='white')
        # Naming the y axis
        ax.set_ylabel('CGPA', color='white')

        # Giving a title to the graph
        ax.set_title('CGPA GROWTH OF THE STUDENTS BY BATCHS', color='white')

        # Hiding top and right spines for a cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Adjusting subplot parameters for reduced margins
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)

        # Saving the plot to a BytesIO object
        img = io.BytesIO()
        FigureCanvas(fig).print_png(img)
        plt.close(fig)

        # Encode the image in base64
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        return render_template('graphOfAllBatchs.html',user_info=user_info,plot_img=img_base64)        
        # return render_template("page_Not_Avalibale.hta")
    elif button_value == "Faculty":
        
        branch=dbname
        htmlcode,rows=fe.faculty(branch)
        return render_template("leaderbord.html",htmlcode=htmlcode,rows=rows)
    elif button_value == "Semister":
        return render_template("page_Not_Avalibale.hta")
    elif button_value == "Subject":
        # return render_template("subject/test.html")
        batch_options = sw.bathcs(dbname)  
        return render_template("subject/details.html",batch_options=batch_options)
    elif button_value=="Profile":
        # return render_template('profile/detailsdemo.html') 
        return render_template('profile/profileid.html') 


@app.route('/subjectanalysis',methods=['POST'])
def subjectanalysis():
    global selected_batches
    global Semister
    Semister = request.form['Semister']
    
    selected_batches = request.form.getlist('batch')
    
    
    # print(selected_batches[0],section)
    if  selected_batches[0]=="None" : #or regulation[0]=="None"
        error="Fill all necessary details"
        batch_options = sw.bathcs()
        return render_template("semister_details.html",error=error,batch_options=batch_options)   
    
    else: 
        dbname='civil'       
        htmlcode,s,ba=sT.subjects(dbname,selected_batches[0],Semister)
        print(s)
        return render_template("subject/table.html",htmlcode=htmlcode,s=s,ba=ba)



@app.route('/Select batch',methods=['POST'])
def select_batch():
    global selected_batches
    global section
    section = request.form['sec']
    # checkbox_value = request.form['my_checkbox'] if 'my_checkbox' in request.form else 'Not Checked'
    selected_batches = request.form.getlist('batch')
    # regulation = request.form.getlist('Regulation')
    
    print(selected_batches[0],section)
    if section=="" or selected_batches[0]=="None" : #or regulation[0]=="None"
        error="Fill all necessary details"
        batch_options = sw.bathcs(dbname)
        return render_template("semister_details.html",error=error,batch_options=batch_options)   
    # elif section=="ALL":
    #     data,imge=sw1.cumilative(selected_batches[0],regulation[0])
    #     return render_template("cumilative_semisterwise_section_table.html",data=data,section=section,imge=imge)
    else: 
        # data,imge=sw1.all_data(selected_batches[0],section,regulation[0])
        print(select_batch)
        data,imge=sw1.lectureperformance(dbname,selected_batches[0],section)
        # return render_template("sectionwise1.html",data=data,section=section,imge=imge)
        return render_template("sectionwise2.html",data=data,section=section,imge=imge)

    

@app.route('/roll_no',methods=['POST'])
def roll_no():
    # dbname="civil"
    # dbname="civil"
    rollNumber= request.form['rollNumber']
    
    items,Name_Section_Cgpa,image_base64=fet.results2(dbname,rollNumber)
    actual_no_of_semister=[]

    # print("recived data",data)
    return render_template("student_results.html",items=items,Name_Section_Cgpa=Name_Section_Cgpa,image_base64=image_base64)


@app.route('/profile', methods=['POST'])
def profile():    
    # getting the values form the javascript and we are not using the form to get the values form the direct html
    table="end of the profile"
    idd = request.form.get('LecturerId')
    htmlcode,code=pe.profile(idd)
    return jsonify({'message':htmlcode,"code":code})

     
@app.route('/backseduling')
def backseduling():
    button_value = request.args.get('button')
    print(f'Button clicked: {button_value}')
    if button_value=='results':
        return render_template('enter_roll_no.html')
    elif button_value=="enter_roll_no":
        return render_template('Home.html',user_info=user_info)   
    elif button_value=="home":
        return render_template('login.html')  
    elif button_value=="calendar" :
        return render_template('Home.html',user_info=user_info)   
    elif button_value=="semister":
        batch_options = sw.bathcs(dbname) 
        return render_template('semister_details.html',batch_options=batch_options) 
    elif button_value=="semister_details":
        return render_template('Home.html',user_info=user_info)   
    elif button_value=="sectionwise":
        batch_options = sw.bathcs(dbname) 
        return render_template('semister_details.html',batch_options=batch_options) 
    elif button_value=="leaderbord":
        batch_options = sw.bathcs(dbname) 
        return render_template('Home.html',user_info=user_info)   

def open_browser():
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True)
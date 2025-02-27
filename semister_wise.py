import mysql.connector 
import base64
import io
import matplotlib.pyplot as plt
import numpy as np
def generate_plot(column_name,value,n_number_of_studetns,section):
    # Data for the graph
    categories=[]
    values=[]
    for e in value:
        m=[e,n_number_of_studetns-e]
        values.append(m)
    print(values)
    
    for ele in column_name:
        k,se=ele.split("_")
        k="Semister :"+se
        categories.append(k)
    print(categories)
    # Labels for the sets
    things = ['Pass', 'Fail']

    # Define a professional color palette
    colors = ['#4E79A7', '#F28E2B']  # Blue and orange

    num_categories = len(categories)
    num_values = len(things)

    # Define the bar width
    bar_width = 0.8 / num_values  # Adjust the width to fit within the category

    # Create the positions for the bars
    r = np.arange(num_categories)
    bar_positions = [r + i * bar_width for i in range(num_values)]

    # Create the bar graph with specified colors
    for i in range(num_values):
        plt.bar(bar_positions[i], [v[i] for v in values], width=bar_width, label=f'{things[i]}', color=colors[i])

    # Add labels and title
    plt.xlabel('Semisters')
    plt.ylabel('Number of students')
    if section==None:
        titl=f'Cumilative of CSM ({n_number_of_studetns})'
        
    else:
        titl=f'Number of Students passed in :CSM- {section} ({n_number_of_studetns})'
    plt.title(titl)
    
    # Center x-ticks
    plt.xticks([r + bar_width * (num_values - 1) / 2 for r in range(num_categories)], categories)

    # Set y-axis range if needed
    plt.ylim(0, n_number_of_studetns)  # Adjust the range based on your data

    # Add values on top of the bars
    for i in range(num_values):
        for j in range(num_categories):
            height = values[j][i]
            plt.text(bar_positions[i][j] + bar_width / 2, height, f'{height}', ha='center', va='bottom')

    # Add a legend
    plt.legend()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Clear the plot to avoid overlap in future plots
    plt.clf()
    return plot_url

def semister_wise(batch,section):
    try:
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishnu@123",
            database="csm"
        ) as db_connection:
            print(batch[0])
            # Creating a cursor object using the cursor() method
            cursor = db_connection.cursor()
            # print("Table function activated")
            # Format batchyear for table name
            batch_name=batch[0]
            tablenames=[]
            try :
                cursor.execute(f"desc {batch_name}")
                tables = cursor.fetchall()
                column_name=[]

                for table in tables:
                    k=table[0]
                    if "SGPA" in k:
                        column_name.append(k)
                cursor.execute(f"select Section from {batch_name}")
                section_data = cursor.fetchall()
                n_sections=[]
                for i in section_data:
                    if i[0] in n_sections:
                        pass
                    else:
                        n_sections.append(i[0])
                print(n_sections)
                images=[]
                for section in n_sections:
                    # print(column_name)
                    whole_column_data={}
                    value=[]
                    for i in range(len(column_name)):
                        value.append(0)
                    k=0
                    print("ha")
                    for i in column_name:
                        print(section)
                        if section:
                            cursor.execute(f"SELECT {i} FROM {batch_name} WHERE Section= %s ",(section,))
                            
                        else:
                            cursor.execute(f"SELECT {i} FROM {batch_name}")
                        data = cursor.fetchall()
                        
                        co=[]
                        
                        count=0
                        for j in data:
                            if j[0]=="nan" or j[0]==None:
                                pass
                            else:
                                count+=1
                            co.append(j[0])
                            # print(co)
                        print(value)
                        value[k]=count
                        
                        n_number_of_studetns=len(co)
                        k+=1
                    
                    print(column_name,value,n_number_of_studetns,section)
                    images.append(generate_plot(column_name,value,n_number_of_studetns,section))
                    value=[]
                    n_number_of_studetns=0
                    for i in range(len(column_name)):
                        value.append(0)
                    k=0
                    for i in column_name:
                        cursor.execute(f"SELECT {i} FROM {batch_name}")
                        data = cursor.fetchall()
                        co=[]                        
                        count=0
                        for j in data:
                            if j[0]=="nan" or j[0]==None:
                                pass
                            else:
                                count+=1
                            co.append(j[0])
                            # print(co)
                        print(value)
                        value[k]=count
                        
                        n_number_of_studetns=len(co)
                        k+=1
                section=None
                print(column_name,value,n_number_of_studetns)
                images.append(generate_plot(column_name,value,n_number_of_studetns,section))
             
                return images
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
# semister_wise("2021_2025")

def bathcs(dbname):
    with mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishnu@123",
            database=dbname
        ) as db_connection:

            
            cursor = db_connection.cursor()
            # print("Table function activated")
            # Format batchyear for table name
            tablenames=[]
            try :
                cursor.execute("show tables")
                fetch_data=cursor.fetchall()
                lis=[]
                {"value": "None", "label": "None"},
                for i in fetch_data:
                    m={}
                    m["value"]=i[0]
                    m["label"]=i[0]
                    lis.append(m)
                print(lis)
            except Exception as e:
                pass
    return lis

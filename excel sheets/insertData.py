import pandas as pd
excel_file = 'C:/Users/global ed/Desktop/result analysis/excel sheets/final templates.xlsx'
file_path=excel_file
excel_file = pd.ExcelFile(file_path)
sheet_names = excel_file.sheet_names
print(sheet_names)
sheets=sheet_names[0]
for sheets in sheet_names:
    dfs = pd.read_excel(excel_file, sheet_name=sheets)
    print(type(dfs))
    column_names=[]
    
    k=dfs
    
    column_names.append(dfs.columns.tolist())
    count=0
    print(len(column_names))
    for index, row in dfs.iterrows():
        # temp=[]
        temp=row.to_list()
        for i in range(len(temp)-1):
            if "Unnamed" in str(temp[i]) or "nan" in str(temp[i]):
                continue
            column_names[0][i]=str(column_names[0][i])+"_"+str(temp[i])
        count+=1
        if count==2:
            break
        # print(temp)
    print(column_names)
    










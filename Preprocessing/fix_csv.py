# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:32:24 2019

@author: JayT
"""

import pandas as pd
import math
import os
import glob

def split_columns(data_file):    
    # Delimiter
    data_file_delimiter = ','
    
    # The max column count a line in the file could have
    largest_column_count = 0
    
    # Loop the data lines
    with open(data_file, 'r') as temp_f:
        # Read the lines
        lines = temp_f.readlines()
        for l in lines:
            # Count the column count for the current line
            column_count = len(l.split(data_file_delimiter)) + 1
    
            # Set the new most column count
            largest_column_count = column_count if largest_column_count < column_count else largest_column_count
    
    # Close file
    temp_f.close()
    
    # Generate column names (will be 0, 1, 2, ..., largest_column_count - 1)
    column_names = [i for i in range(0, largest_column_count)]
    
    # Read csv
    df = pd.read_csv(data_file, header=None, delimiter=data_file_delimiter, names=column_names)
    
    return df

def get_Moriarty(path):
    df=split_columns(os.path.join(path,'Moriarty.csv'))
    col_to_split=3
    df_col=len(df.columns)
    print(df_col)
    n_cols=9
    with open((os.path.join(path,'New_Moriarty.csv')), 'w+') as f:    
        for index,row in df.iterrows():
            toModify=False
            check=df_col-1
            while(check>n_cols-1 and not toModify):
                try:
                    if(isinstance(row[check],str)):
                        toModify=True
                    elif(not math.isnan(row[check])):
                        toModify=True
                    else: 
                        check=check-1
                except:
                    None
            if(toModify): 
                new_value=""
                for i in range(col_to_split-1,col_to_split+df_col-n_cols-1):
                    new_value+=str(row[i])+" "
                
                    
                new_row=""
                for i in range(0,col_to_split-1):
                    if(not row[i]=='nan'):
                     new_row+=str(row[i])+","
                   
                
                new_row+=new_value[:-1]
                
                for x in range(df_col-check+col_to_split-1,df_col):
                    try:
                        if(not (math.isnan(row[x]))):
                            new_row+=","+str(row[x])
                    except:
                        new_row+=","+str(row[x])

                f.write(new_row+"\n")
                        
            else:
                new_values=[' '.join(str(ele).split()) for ele in row]
                final_value=""
                for value in new_values:
                    if(not value=='nan'):
                        final_value+=value+","
                f.write(final_value[:-1]+"\n")
            
                
def get_Broadcasts(path):

    df=split_columns((os.path.join(path,'AllBroadcasts.csv')))
    
    with open((os.path.join(path,'NOExtrasBroadcast.csv')), 'w+') as f,open((os.path.join(path,'Extras.csv')), 'w+') as f_extras:
        
        for index,row in df.iterrows():
            index_action=13
            index_timestamp=14
            try:
                while(math.isnan(row[index_timestamp])):
                    index_action=index_action-1
                    index_timestamp=index_timestamp-1
            except:
                f.write(str(row[0])+","+str(row[1])+","+str(row[index_action])+","+str(row[index_timestamp])+"\n")
                extras=2
                string_extras=""
                while(extras<index_action):
                    string_extras+=str(row[extras])
                    extras+=1
                f_extras.write(string_extras)
                f_extras.write("\n")
                
    broadcast1 = pd.read_csv(os.path.join(path,'NOExtrasBroadcast.csv'),usecols=['UserId','UUID'])
    extras=pd.read_csv(os.path.join(path,'Extras.csv'))
    broadcast2=pd.read_csv(os.path.join(path,'NOExtrasBroadcast.csv'),usecols=['Action','timestamp'])

    new_broadcast=pd.concat([broadcast1,extras,broadcast2],axis=1)
    new_broadcast.to_csv(os.path.join(path,'New_AllBroadcasts.csv'),index=False)  
    os.chdir(path)    
    os.remove('NOExtrasBroadcast.csv')
    os.remove('Extras.csv')

def split_cols(path):
    df=split_columns(os.path.join(path,'AppPackages.csv'))
    col_to_split=10
    df_col=len(df.columns)
    print(df_col)
    n_cols=13
    with open((os.path.join(path,'New_AppPackages.csv')), 'w+') as f:
        
        for index,row in df.iterrows():
            print(index)
            toModify=False
            check=df_col-1
            while(check>n_cols-1 and not toModify):
                try:
                    if(not math.isnan(float(row[check]))):
                        toModify=True
                    else: 
                        check=check-1
                except:
                    if(len(row[check].split("."))>2): check=check-1
            if(toModify): 
                new_value=""
                for i in range(col_to_split-1,col_to_split+df_col-n_cols):
                    new_value+=str(row[i])+" "
                
                new_row=""
                for i in range(0,col_to_split-1):
                    if(not row[i]=='nan'):
                     new_row+=str(row[i])+","
                    
                new_row+=new_value[:-1]
                
                for x in range(df_col-check+col_to_split,df_col):
                    try:
                        if(not (math.isnan(row[x]))):
                            new_row+=","+str(row[x])
                    except:
                        new_row+=","+str(row[x])

                f.write(new_row+"\n")
                        
            else:
                new_values=[' '.join(str(ele).split()) for ele in row]
                final_value=""
                size=0
                for value in new_values:
                    if(size<n_cols):
                        size+=1
                        if(not value=='nan'):
                            final_value+=value+","
                        else:final_value+=","
                print(final_value[:-1])
                f.write(final_value[:-1]+"\n")


def get_AppPackages(path,n_cols,col_to_split):
    df=split_columns((os.path.join(path,'AppPackages.csv')))
    with open((os.path.join(path,'New_AppPackages.csv')), 'w+') as f:
        
        for index,row in df.iterrows():
            if(index>0):
                str_value=""
                for i in range (0,col_to_split-1):
                    str_value+=str(row[i]).replace(" ","")+","
                i=len(df.columns)-1
                donecols=0
                mid_string=""
                while(donecols<(n_cols-col_to_split)):
                    try:
                        if(not math.isnan(row[i])):
                            mid_string=str(row[i]).replace(" ","")+","+mid_string
                            donecols+=1
                    except:
                        mid_string=str(row[i]).replace(" ","")+","+mid_string
                        donecols+=1
                    i=i-1
                
                col_to_split_string=""
                for x in range(col_to_split-1,i+1):
                    col_to_split_string+=str(row[x]).replace(" ","")
                col_to_split_string+=","
                no_col_to_split_string=(str_value+mid_string[:-1])
                final_string=""
                size=0
                for value in no_col_to_split_string.split(","):
                    if(size==col_to_split-1):
                        final_string+=col_to_split_string
                    final_string+=value+","
                    size+=1
                f.write(final_string[:-1]+"\n")
            else:
                head_string=""
                for value in row:
                    try:
                        if(not math.isnan(value)):
                            head_string+=value+","
                    except:
                        head_string+=value+","
                f.write(head_string[:-1]+"\n")
                    
                
    
def merge_nt(path):
    os.chdir(path)
    with open(path+'\\merged_file.nt','w+') as new_file, open(path+'\\target_file.nt','w+') as target_file:
        for file in glob.glob("*.nt"):
            if(not file=='merged_file.nt' and not file=='target_file.nt' and not 'schema' in file):
                print(file)
                f=open(file)
                for line in f:
                    if(not line=='\n'):
                        if('actiontype' in line):
                            target_file.write(line)
                        elif(not 'http://example.org/Class' in line):
                            new_file.write(line)  
                            
def split_applications(path):
    df = pd.read_csv(path,delimiter=",")
    with open("D:\\completo\\output\\Csv\\applications_to_use.csv","w+",encoding="utf-8") as f:
        header=list(df.columns.values)
        header_string=""
        for h in header:
            header_string+=h+","
        f.write(header_string[:-1]+"\n")
        for index,row in df.iterrows():
            newrow=""
            index=0
            for value in row:
                try:
                    if(math.isnan(value)):
                        newrow+="NULL,"
                    elif(index==1):
                        newrow+=str(int(value))+","
                    else:  
                        newrow+=str(value)+","
                except:
                    newrow+=value+","
                index+=1
            f.write(newrow[:-1]+"\n")
    
def reduce_csv(path,filename,seconds):
    current_uuid=0
    current_seconds=0
    lastuuid=0
    with open(os.path.join(path,filename+".csv"),"r+",encoding="utf-8") as f:
        with open(os.path.join(path,filename+"_"+str(seconds)+".csv"),"w+",encoding="utf-8") as f_new:
            f_new.write(f.readline())
            for line in f:
                if(current_uuid==0 and current_seconds==0):
                    current_uuid=int(line.split(",")[1])
                    lastuuid=current_uuid
                    f_new.write(line)
                elif(current_uuid==int(line.split(",")[1]) and (current_seconds>=seconds*1000 or current_seconds==0)):
                    f_new.write(line)
                elif(not current_uuid==int(line.split(",")[1])):
                    current_seconds=abs(lastuuid-int(line.split(",")[1]))
                    current_uuid=int(line.split(",")[1])
                    if(current_seconds>=seconds*1000):
                        lastuuid=current_uuid
                        f_new.write(line)
                   
  
#reduce_csv("D:\completo\PER ECLIPSE","Applications",1200)   
#reduce_csv("D:\completo\PER ECLIPSE","T2",60)      
#reduce_csv("D:\completo\PER ECLIPSE","T4",60)      
   
#path="D:\\completo\\"
#get_AppPackages(path,13,10)
#get_Broadcasts(path)
#get_Moriarty(path)
merge_nt("D:\\Big Data\\Data\\Sherlock Dataset\\Sample Dataset\\OpenKEonSpark\\Discretized one target relation\\Equal width\\Output nt")
#n_rows=2000000
#df=pd.read_csv("D:\\completo\\output\\Csv\\Complete_Applications.csv",delimiter=",",nrows=n_rows)
#df.to_csv("D:\\completo\\output\\Csv\\Complete_Applications_"+str(n_rows)+".csv",index=False)  

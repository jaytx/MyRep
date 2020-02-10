# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 15:44:32 2019

@author: JayT
"""
import pandas as pd
import math
import os
import numpy as np
import numbers
import decimal
import glob

class Error(LookupError):
    '''raise this when there's a lookup error for my app'''
                    
def discretizehertz(file_name,attribute,data,arrayvalue,output_folder):
    new_mapvalue={}
    for value in arrayvalue:
        if(isinstance(value,str) and "MHz" in value):
            new_mapvalue.update({str(int(value.split("MHz")[0])/1000)+"GHz" : value})
        elif(isinstance(value,str)):
            new_mapvalue.update({value.replace(" ",""): value})
    
    new_column=[]
    for value in data:
        try:
            math.isnan(value)
            new_column.append(value)
        except TypeError:
            new_column.append(new_mapvalue.get(value))


    print("Cpu Hertz Discretized.")     
    df = pd.DataFrame({attribute : new_column})
    df.to_csv(output_folder+'Single Column\\'+file_name+'\\'+attribute+'.csv',index=False)  
              
    print("Number of lines: "+str(len(list(df.index))))      
    print("Done. \n")
                
    return new_column
    
                        
def create_bin_frequency(data, bins):
    split = np.array_split(np.sort(data), bins)
    cutoffs = [x[-1] for x in split]
    cutoffs = cutoffs[:-1]
    discrete = np.digitize(data, cutoffs, right=True)
    return discrete, cutoffs

def convert_to_int(data,attribute,output_folder,file_name):
    new_values=[]
    print("Decimal to int...")
    for value in data:
        try:
            value=float(value)
            if(not math.isnan(value)):
                new_values.append(round(value,2))
            else:
                new_values.append(value)
        except: 
            new_values.append(value)
    
    df = pd.DataFrame({attribute : new_values})
    df.to_csv(output_folder+'Single Column\\'+file_name+'\\'+attribute+".csv",index=False)  
              
    print("Number of lines: "+str(len(list(df.index))))      
    print("Done. \n")
    
    return new_values 
    
def create_intervall(algorithm,file_name,min_number,max_number,single_value_list,max_number_of_values,tollerance,data,attribute,output_folder):
    array_intervall=[]
    new_values=[]
    print("MIN : "+ str(int(min_number)))
    print("MAX : "+ str(int(max_number))) 
    f=open(os.path.join(output_folder,algorithm+"_list_intervals.txt"),"a+")
    if(algorithm=="width"):
        try:
            print("Discretizing data with equal width algortihm...")
            interval=round((max_number-(min_number))/max_number_of_values)
            print("INTERVALL: "+str(int(interval)))
            current_min=min_number
            current_max=current_min+interval
            
            print("Generating intervalls...")
            while(current_max<=max_number):
                #if(current_max+interval>max_number): current_max=int(max_number)
                print(str(int(current_min))+"-"+str(int(current_max)))
                f.write(str(int(current_min))+"-"+str(int(current_max))+ "\n")
                array_intervall.append(str(int(current_min))+"-"+str(int(current_max)))
                current_min=current_max+1
                current_max+=(interval+1)
                if(current_min<max_number and current_max>max_number):
                    current_max=max_number
                elif(current_min==max_number):
                    print(str(int(current_min))+"-"+str(int(current_max)))
                    f.write(str(int(current_min))+"-"+str(int(current_max))+ "\n")
                    array_intervall.append(str(int(current_min))+" - "+str(int(current_max)))
             
            print("Intervals for "+attribute+" created.")
            print("Discretizing values...")
            size=0
            last_perc=0
            for value in data:
                perc=round(size/len(data)*100)
                if(int(perc)>(int(last_perc))+4): 
                    print("Percentage of discretized attributes of "+attribute+" : "+str(perc)+"%")
                    last_perc=perc
                boolean=False
                size=size+1
                try:
                    for inter in range(0,len(array_intervall)):
                        min_v,max_v=array_intervall[inter].split("-")
                        if(int(value)>=int(min_v) and int(value)<=int(max_v)): 
                            new_values.append(str(array_intervall[inter]))
                            boolean=True
                    if(not boolean):
                        raise Error("MISSED VALUE: "+str(value))
                except:
                    new_values.append(value)
        except TypeError:
            print("String Type, no discretization.")
            new_values=data
        
    elif(algorithm=="frequency"):
        num_interval=100
        array_intervall=[]
        discrete_dat, cutoff = create_bin_frequency(data, num_interval)
        print("Discretizing data with equal frequency algortihm...")
        interval_created=0
        for value in single_value_list:
            try:
                if(value==cutoff[0]): 
                    array_intervall.append(str(round(min_number,3)) + "-" + str(round(value,3)))
                    print(str(round(min_number,3)) + "-" + str(round(value,3)))
                    f.write(str(round(min_number,3)) + "-" + str(round(value,3))+"\n")
                    min_number=round(value,3)+(0.001)
                    interval_created+=1
                    del(cutoff[0])
            except IndexError:
                array_intervall.append(str(round(min_number,3)) + "-" + str(round(max_number,3)))
                print(str(round(min_number,3)) + "-" + str(round(max_number,3)))
                f.write(str(round(min_number,3)) + "-" + str(round(max_number,3))+"\n")
                interval_created+=1
                break  
         
        print("Intervals for "+attribute+" created.")
        print("Discretizing values...")
        f.write("intervall created: "+str(interval_created)+"\n")
        size=0
        last_perc=0
        for value in data:
            perc=round(size/len(data)*100)
            if(int(perc)>(int(last_perc))+4): 
                print("Percentage of discretized attributes of "+attribute+" : "+str(perc)+"%")
                last_perc=perc
            boolean=False
            size=size+1
            try:
                if(not math.isnan(value)):
                    for inter in range(0,len(array_intervall)):
                        min_v,max_v=array_intervall[inter].split("-")
                        if(round(value,3)>=float(min_v) and round(value,3)<=float(max_v)): 
                            new_values.append(str(array_intervall[inter]))
                            boolean=True
                    if(not boolean):
                        raise Error("MISSED VALUE: "+str(value))
                else:
                    new_values.append(value)
            except:
                new_values.append(value)
                       
    
    df = pd.DataFrame({attribute : new_values})
    df.to_csv(output_folder+'Single Column\\'+file_name+'\\'+attribute+'.csv',index=False)  
              
    print("Number of lines: "+str(len(list(df.index)))) 
    f.write("Number of lines: "+str(len(list(df.index))))
    f.close()    
    print("Done. \n")
    
    return new_values   


def discretize_dataset(prefix_file,file_names,algorithm,attributes_to_avoid,input_folder,output_folder,max_number_of_values,tollerance):
    attributes_discarded=[]
    for file_name in file_names:
        if(not (os.path.isdir(output_folder+"Single Column\\"+file_name))): os.mkdir(output_folder+"Single Column\\"+file_name)
        print("=========================Discretizing "+file_name+"=========================")
        data = pd.read_csv(input_folder+file_name,delimiter=",")
        
        attributes=data.columns.tolist()
       
        for attribute in attributes:
            for attr in attributes_to_avoid:
                if(attr in attribute.lower()):
                    try:
                        attributes.remove(attribute)
                    except:
                        None

        if('UUID' in attributes): attributes.remove('UUID')  #previous loop skip these attributes, need to specify
        if('time_lapse' in attributes): attributes.remove('time_lapse')
        if('uuid' in attributes): attributes.remove('uuid')
        if('pid' in attributes): attributes.remove('pid')
        if('SessionID' in attributes): attributes.remove('SessionID')
        if('CellTower_Cid' in attributes): attributes.remove('CellTower_Cid')
        if('TimeStemp' in attributes): attributes.remove('TimeStemp')
        if('sessionid' in attributes): attributes.remove('sessionid')
        if('celltower_cid' in attributes): attributes.remove('celltower_cid')
        if('timestamp' in attributes): attributes.remove('timestamp')
        

        values_dict={}
        for attribute in attributes:
            data1=data[attribute]
            if(data[attribute].nunique()>1):
                print("=========================Discretizing "+attribute+"=========================")
                #data2.to_csv('C:\\Users\\JayT\\Desktop\\Single Column\\T1\\'+attribute+'.csv')
                #print(data2)
                data2=[]
                for value_data in data1:
                    if(isinstance(value_data,str)):
                        data2.append(value_data.replace(" ", ""))
                    else: data2.append(value_data)
                #print(arrayvalue)
                if(algorithm=="int"):
                    values_dict.update({attribute: convert_to_int(data2,attribute,output_folder,file_name)}) 
                elif(file_name=='T4' and attribute=='CpuHertz'):
                    arrayvalue=data[attribute].unique()
                    values_dict.update({attribute :discretizehertz(file_name,attribute,data2,arrayvalue,output_folder)})
                else:
                    print("Number of values: "+str(data[attribute].nunique()))
                    if(data[attribute].nunique()>max_number_of_values+tollerance):
                        #arrayvalue=get_values(data,attribute)
                        arrayvalue=data[attribute].unique()
                        i=0
                        while i<len(arrayvalue):
                          try:
                            arrayvalue[i]=float(arrayvalue[i])   
                          except:
                            if((arrayvalue[i]=='""' or arrayvalue[i]=="Null" or arrayvalue[i]=='\\N') and (algorithm=='width' or algorithm=='frequency')):
                              arrayvalue[i]=float(0)
                          i=i+1
                        if(isinstance(max(arrayvalue),numbers.Number) and max(arrayvalue)<=max_number_of_values+tollerance):
                            values_dict.update({attribute: convert_to_int(data2,attribute,output_folder,file_name)})
                        elif(isinstance(max(arrayvalue),numbers.Number)):
                            arrayvalue.sort()
                            values_dict.update({attribute : create_intervall(algorithm,file_name,min(arrayvalue),max(arrayvalue),arrayvalue,max_number_of_values,tollerance,data2,attribute,output_folder)})
                    elif(not(data[attribute].nunique()==1)):
                        print("No Discretization needed. \n")
                        values_dict.update({attribute : data2})
                        df = pd.DataFrame({attribute : data2})
                        df.to_csv(output_folder+'Single Column\\'+file_name+'\\'+attribute+".csv",index=False) 
            else: 
                attributes_discarded.append(attribute)
                print("Only one value, attribute "+str(attribute)+" discarded.")
        try:
            df = pd.DataFrame(values_dict)
            df.to_csv(output_folder+'Csv\\'+prefix_file+file_name,index=False)  
        except ValueError:
            for key in values_dict:
                print("Lenght of "+str(key)+": "+str(len(values_dict.get(key))))
                raise Error("Lenght of columns are not the same, check generated intervals")
                
    print("List of attributes discarded: ")
    print(attributes_discarded)
                
 
    
def run_export(prefix_file,algorithm,input_folder,output_folder):
    file_names=[] 

    attributes_to_avoid=['timestamp','date','version','id','timestemp','time_lapse','time_unix','userid','ssid','uid']
    
    os.chdir(input_folder)    
    for file in glob.glob("*.csv"):
        file_names.append(file)
    print(file_names)
    if(not (os.path.isdir((os.path.join(output_folder,"Csv"))))): os.mkdir(os.path.join(output_folder,"Csv"))
    if(not (os.path.isdir((os.path.join(output_folder,"Output nt"))))): os.mkdir(os.path.join(output_folder,"Output nt"))
    if(not (os.path.isdir((os.path.join(output_folder,"Single Column"))))) : os.mkdir(os.path.join(output_folder,"Single Column"))
    if(algorithm==""): max_number_of_values=9999999999999999
    else:max_number_of_values=10000
    tollerance=2500
    discretize_dataset(prefix_file,file_names,algorithm,attributes_to_avoid,input_folder,output_folder,max_number_of_values,tollerance)

   
    
#split_applications("C:\\Users\\JayT\\Desktop\\Big Data\\Data\\Sherlock Dataset\\Original Dataset\\Applications.csv")

"""
algorithm="width" #set width to use equal width or frequency to use equal frequency , or set "" to not perform discretization
input_folder="D:\\Big Data\\Data\\Sherlock Dataset\\Sample Dataset\\Comparison\\Csv Translated\\"  # path to CSV files
output_folder="D:\\Big Data\\Data\\Sherlock Dataset\\Sample Dataset\\OpenKEonSpark\\Discretized one target relation\\Equal width\\"   #set path where to save data
prefix_file="Sample_Width_"
run_export(prefix_file,algorithm,input_folder,output_folder)
"""
#merge_nt('C:\\Users\\JayT\\Desktop\\Big Data\\Data\\Sherlock Dataset\\Discretized\\Equal width\\Output nt\\')
#data = pd.read_csv("C:\\Users\\JayT\\Desktop\\Big Data\\Data\\Sherlock Dataset\\Dataset to use\\T2.csv",delimiter=",")
#data2=data['pressure_MIDDLE_SAMPLE']
#convert_to_int(data2,"pressure_MIDDLE_SAMPLE","C:\\Users\\JayT\\Desktop\\","test")
"""
data = pd.read_csv("C:\\Users\\JayT\\Desktop\\Big Data\\Data\\Sherlock Dataset\\Dataset to use\\T2.csv",delimiter=",")
data2=data['LinearAcceleration_z_VAR_FFT']
i=0
arrayvalue=data['LinearAcceleration_z_VAR_FFT'].unique()
while i<len(arrayvalue):
  try:
    #arrayvalue[i]=float(arrayvalue[i])   
    if(math.isnan(arrayvalue[i])):arrayvalue[i]=float(0)
  except:
    if(arrayvalue[i]=='""' or arrayvalue[i]=="Null"):
      arrayvalue[i]=float(0)
  i=i+1

arrayvalue=list(set(arrayvalue))
arrayvalue.sort()
max_number_of_values=10000
tollerance=2500
df=create_intervall("frequency",'T2',min(arrayvalue),max(arrayvalue),arrayvalue,max_number_of_values,tollerance,data2,'LinearAcceleration_z_VAR_FFT',"C:\\Users\\JayT\\Desktop\\")
"""

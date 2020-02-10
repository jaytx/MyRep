# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:35:06 2019

@author: JayT
"""

import pandas as pd
def translate_sherlock_from_dump(path,file,std):
    values_array=[]
    map_index={}
    create_table=False
    read_values=False
    index_table=0
    header=""
    print("Reading rows...")
    table=""
    if(std):
        with open(path+file, 'r',encoding="utf-8") as original:
            for line in original:
                if(create_table):
                    if(not ");" in line): 
                        header+=line.split(" ")[4].replace('"',"")+","
                    else: 
                        create_table=False
                        values_array[index_table][1].append(header[:-1]+"\n")
                        header=""
                if(read_values and line=="\.\n"):
                    read_values=False
                elif(read_values):
                    values=line.split("\t")
                    value_row=""
                    for i in range(0,len(values)):
                        value_row+=values[i]+","
                        
                    value_row=value_row[:-1]                    
                    values_array[map_index.get(table)][1].append(value_row.replace(" ",""))   
                if("CREATE TABLE public." in line):
                    values_array.append([(line.split("public.")[1]).split('(')[0].strip(" "),[]])
                    map_index.update({ (line.split("public.")[1]).split('(')[0].strip(" ") : (len(values_array)-1)})
                    index_table=map_index.get((line.split("public.")[1]).split('(')[0].strip(" "))
                    create_table=True    
                elif("COPY public." in line):
                    read_values=True
                    table=line.split("COPY public.")[1].split("(")[0].replace(" ","")
    else:
        with open(path+file, 'r',encoding="utf-8") as original:
            for line in original:
                if(create_table):
                    if(not ");" in line): 
                        header+=line.split(" ")[4].replace('"',"")+","
                    else: 
                        create_table=False
                        values_array[index_table][1].append(header[:-1]+"\n")
                        header=""
                if(read_values and line=="\.\n"):
                    read_values=False
                elif(read_values):
                    values=line.split("\t")
                    value_row=""
                    for i in range(0,len(values)):
                        value_row+=values[i]+","
                        
                    value_row=value_row[:-1]
                    
                    values_array[map_index.get(table)][1].append(value_row.replace(" ",""))   
                if("CREATE TABLE pre." in line):
                    values_array.append([(line.split("pre.")[1]).split('(')[0].strip(" "),[]])
                    map_index.update({ (line.split("pre.")[1]).split('(')[0].strip(" ") : (len(values_array)-1)})
                    index_table=map_index.get((line.split("pre.")[1]).split('(')[0].strip(" "))
                    create_table=True    
                elif("COPY pre." in line):
                    read_values=True
                    table=line.split("COPY pre.")[1].split("(")[0].replace(" ","")
                    

    print("Read all rows.")
            
    for attribute,list_value in values_array:
        with open(path+attribute+".csv",'w+',encoding="utf-8") as writef:
            for row in list_value:
                writef.write(row.replace('"',""))

    
def switch_for_file(table):
    switcher = {
        "1": "PROVA",
        "allbroadcastprobe": "UserId,UUID,Extras,Action,timestamp",
        "application": "February",
        "apppackages": "UserId,UUID,Action,AppPackage,AppUID,App_Name,InstallSrc,InstallTime,PackageHASH,Permissions,versionName,versionCode,sherlock_version",
        "bluetooth": "UserID,UUID,Bluetooth_appearance,Bluetooth_class,Bluetooth_mAddress,Bluetooth_mRemoteBrsf,Bluetooth_mValueNREC,Bluetooth_mValueWBS,Bluetooth_name,Bluetooth_rssi,Bluetooth_timestamp",
        "call": "UserId,UUID,Address,Date,Duration,FromContacts,Type",
        "moriartyprobe": "UserId,UUID,Details,Action,ActionType,SessionType,Version,SessionID,behavior",
        "screenon": "UserID,UUID,ScreenOn,Timestamp",
        "sms": "UserId,UUID,Address,ContainsURL,Date,FromContacts,Type",
#INSERIRE NULL IN COLONNA 5        "t0": "UserId,UUID,Version,Telephoney_deviceId,Telephoney_deviceSoftwareVersion,Telephoney_networkCountryIso,Telephoney_networkOperator,Telephoney_networkOperatorName,Telephoney_networkType,Telephoney_phoneType,Telephoney_simCountryIso,Telephoney_simOperator,Telephoney_simOperatorName,Telephoney_simSerialNumber,Telephoney_simState,Telephoney_subscriberId,Telephoney_hassIccCard,Telephoney_timestemp,Hardware_wifiMac,Hardware_bluetoothMac,Hardware_androidId,Hardware_brand,Hardware_model,Hardware_deviceId,SystemInfo_OS_version,SystemInfo_Baseband_version,SystemInfo_SDK,SystemInfo_KernelInfo,SystemInfo_timestemp",
        "t1": "UserID,UUID,Version,GooglePlayLoc_Speed,GooglePlayLoc_mAccuracy,5-means_geo,10-means_geo,25-means_geo,50-means_geo,75-means_geo,100-means_geo,5-means_geo_HourOfDay,25-means_geo_HourOfDay,100-means_geo_HourOfDay,5-means_geo_DayOfWeek,25-means_geo_DayOfWeek,100-means_geo_DayOfWeek,GooglePlayLoc_timestamp,CellTower_Cid,CellTower_lac,CellTower_psc,CellTower_timestamp,CellTower_type,Status_AlarmVol,Status_BrightnessMode,Status_Brightness_file,Status_Brightness_settings,Status_DtmfVol,Status_MusicVol,Status_NotificationVol,Status_Orientation,Status_RingerMode,Status_RingtoneVol,Status_SystemVol,Status_VoiceCallVol,Status_timestamp",
        "t2": "UserID,UUID,Version,TimeStemp,AccelerometerStat_x_DC_FFT,AccelerometerStat_x_FIRST_IDX_FFT,AccelerometerStat_x_FIRST_VAL_FFT,AccelerometerStat_x_FOURTH_IDX_FFT,AccelerometerStat_x_FOURTH_VAL_FFT,AccelerometerStat_x_MEAN,AccelerometerStat_x_MEAN_FFT,AccelerometerStat_x_MEDIAN,AccelerometerStat_x_MEDIAN_FFT,AccelerometerStat_x_SECOND_IDX_FFT,AccelerometerStat_x_SECOND_VAL_FFT,AccelerometerStat_x_THIRD_IDX_FFT,AccelerometerStat_x_THIRD_VAL_FFT,AccelerometerStat_x_VAR,AccelerometerStat_x_VAR_FFT,AccelerometerStat_y_DC_FFT,AccelerometerStat_y_FIRST_IDX_FFT,AccelerometerStat_y_FIRST_VAL_FFT,AccelerometerStat_y_FOURTH_IDX_FFT,AccelerometerStat_y_FOURTH_VAL_FFT,AccelerometerStat_y_MEAN,AccelerometerStat_y_MEAN_FFT,AccelerometerStat_y_MEDIAN,AccelerometerStat_y_MEDIAN_FFT,AccelerometerStat_y_SECOND_IDX_FFT,AccelerometerStat_y_SECOND_VAL_FFT,AccelerometerStat_y_THIRD_IDX_FFT,AccelerometerStat_y_THIRD_VAL_FFT,AccelerometerStat_y_VAR,AccelerometerStat_y_VAR_FFT,AccelerometerStat_z_DC_FFT,AccelerometerStat_z_FIRST_IDX_FFT,AccelerometerStat_z_FIRST_VAL_FFT,AccelerometerStat_z_FOURTH_IDX_FFT,AccelerometerStat_z_FOURTH_VAL_FFT,AccelerometerStat_z_MEAN,AccelerometerStat_z_MEAN_FFT,AccelerometerStat_z_MEDIAN,AccelerometerStat_z_MEDIAN_FFT,AccelerometerStat_z_SECOND_IDX_FFT,AccelerometerStat_z_SECOND_VAL_FFT,AccelerometerStat_z_THIRD_IDX_FFT,AccelerometerStat_z_THIRD_VAL_FFT,AccelerometerStat_z_VAR,AccelerometerStat_z_VAR_FFT,AccelerometerStat_COV_y_x,AccelerometerStat_COV_z_x,AccelerometerStat_COV_z_y,GyroscopeStat_x_DC_FFT,GyroscopeStat_x_FIRST_IDX_FFT,GyroscopeStat_x_FIRST_VAL_FFT,GyroscopeStat_x_FOURTH_IDX_FFT,GyroscopeStat_x_FOURTH_VAL_FFT,GyroscopeStat_x_MEAN,GyroscopeStat_x_MEAN_FFT,GyroscopeStat_x_MEDIAN,GyroscopeStat_x_MEDIAN_FFT,GyroscopeStat_x_SECOND_IDX_FFT,GyroscopeStat_x_SECOND_VAL_FFT,GyroscopeStat_x_THIRD_IDX_FFT,GyroscopeStat_x_THIRD_VAL_FFT,GyroscopeStat_x_VAR,GyroscopeStat_x_VAR_FFT,GyroscopeStat_y_DC_FFT,GyroscopeStat_y_FIRST_IDX_FFT,GyroscopeStat_y_FIRST_VAL_FFT,GyroscopeStat_y_FOURTH_IDX_FFT,GyroscopeStat_y_FOURTH_VAL_FFT,GyroscopeStat_y_MEAN,GyroscopeStat_y_MEAN_FFT,GyroscopeStat_y_MEDIAN,GyroscopeStat_y_MEDIAN_FFT,GyroscopeStat_y_SECOND_IDX_FFT,GyroscopeStat_y_SECOND_VAL_FFT,GyroscopeStat_y_THIRD_IDX_FFT,GyroscopeStat_y_THIRD_VAL_FFT,GyroscopeStat_y_VAR,GyroscopeStat_y_VAR_FFT,GyroscopeStat_z_DC_FFT,GyroscopeStat_z_FIRST_IDX_FFT,GyroscopeStat_z_FIRST_VAL_FFT,GyroscopeStat_z_FOURTH_IDX_FFT,GyroscopeStat_z_FOURTH_VAL_FFT,GyroscopeStat_z_MEAN,GyroscopeStat_z_MEAN_FFT,GyroscopeStat_z_MEDIAN,GyroscopeStat_z_MEDIAN_FFT,GyroscopeStat_z_SECOND_IDX_FFT,GyroscopeStat_z_SECOND_VAL_FFT,GyroscopeStat_z_THIRD_IDX_FFT,GyroscopeStat_z_THIRD_VAL_FFT,GyroscopeStat_z_VAR,GyroscopeStat_z_VAR_FFT,GyroscopeStat_COV_y_x,GyroscopeStat_COV_z_x,GyroscopeStat_COV_z_y,MagneticField_x_DC_FFT,MagneticField_x_FIRST_IDX_FFT,MagneticField_x_FIRST_VAL_FFT,MagneticField_x_FOURTH_IDX_FFT,MagneticField_x_FOURTH_VAL_FFT,MagneticField_x_MEAN,MagneticField_x_MEAN_FFT,MagneticField_x_MEDIAN,MagneticField_x_MEDIAN_FFT,MagneticField_x_SECOND_IDX_FFT,MagneticField_x_SECOND_VAL_FFT,MagneticField_x_THIRD_IDX_FFT,MagneticField_x_THIRD_VAL_FFT,MagneticField_x_VAR,MagneticField_x_VAR_FFT,MagneticField_y_DC_FFT,MagneticField_y_FIRST_IDX_FFT,MagneticField_y_FIRST_VAL_FFT,MagneticField_y_FOURTH_IDX_FFT,MagneticField_y_FOURTH_VAL_FFT,MagneticField_y_MEAN,MagneticField_y_MEAN_FFT,MagneticField_y_MEDIAN,MagneticField_y_MEDIAN_FFT,MagneticField_y_SECOND_IDX_FFT,MagneticField_y_SECOND_VAL_FFT,MagneticField_y_THIRD_IDX_FFT,MagneticField_y_THIRD_VAL_FFT,MagneticField_y_VAR,MagneticField_y_VAR_FFT,MagneticField_z_DC_FFT,MagneticField_z_FIRST_IDX_FFT,MagneticField_z_FIRST_VAL_FFT,MagneticField_z_FOURTH_IDX_FFT,MagneticField_z_FOURTH_VAL_FFT,MagneticField_z_MEAN,MagneticField_z_MEAN_FFT,MagneticField_z_MEDIAN,MagneticField_z_MEDIAN_FFT,MagneticField_z_SECOND_IDX_FFT,MagneticField_z_SECOND_VAL_FFT,MagneticField_z_THIRD_IDX_FFT,MagneticField_z_THIRD_VAL_FFT,MagneticField_z_VAR,MagneticField_z_VAR_FFT,MagneticField_COV_y_x,MagneticField_COV_z_x,MagneticField_COV_z_y,Pressure_DC_FFT,Pressure_FIRST_IDX_FFT,Pressure_FIRST_VAL_FFT,Pressure_FOURTH_IDX_FFT,Pressure_FOURTH_VAL_FFT,Pressure_MEAN,Pressure_MEAN_FFT,Pressure_MEDIAN,Pressure_MEDIAN_FFT,Pressure_SECOND_IDX_FFT,Pressure_SECOND_VAL_FFT,Pressure_THIRD_IDX_FFT,Pressure_THIRD_VAL_FFT,Pressure_VAR,Pressure_VAR_FFT,OrientationProbe_azimuth_MEAN,OrientationProbe_azimuth_MEDIAN,OrientationProbe_azimuth_MIDDLE_SAMPLE,OrientationProbe_pitch_MEAN,OrientationProbe_pitch_MEDIAN,OrientationProbe_pitch_MIDDLE_SAMPLE,OrientationProbe_roll_MEAN,OrientationProbe_roll_MEDIAN,OrientationProbe_roll_MIDDLE_SAMPLE,RotationVector_cosThetaOver2_MEAN,RotationVector_cosThetaOver2_MEDIAN,RotationVector_cosThetaOver2_MIDDLE_SAMPLE,RotationVector_xSinThetaOver2_MEAN,RotationVector_xSinThetaOver2_MEDIAN,RotationVector_xSinThetaOver2_MIDDLE_SAMPLE,RotationVector_ySinThetaOver2_MEAN,RotationVector_ySinThetaOver2_MEDIAN,RotationVector_ySinThetaOver2_MIDDLE_SAMPLE,RotationVector_zSinThetaOver2_MEAN,RotationVector_zSinThetaOver2_MEDIAN,RotationVector_zSinThetaOver2_MIDDLE_SAMPLE,LinearAcceleration_COV_y_x,LinearAcceleration_COV_z_x,LinearAcceleration_COV_z_y,LinearAcceleration_x_DC_FFT,LinearAcceleration_x_FIRST_IDX_FFT,LinearAcceleration_x_FIRST_VAL_FFT,LinearAcceleration_x_FOURTH_IDX_FFT,LinearAcceleration_x_FOURTH_VAL_FFT,LinearAcceleration_x_MEAN,LinearAcceleration_x_MEAN_FFT,LinearAcceleration_x_MEDIAN,LinearAcceleration_x_MEDIAN_FFT,LinearAcceleration_x_MIDDLE_SAMPLE,LinearAcceleration_x_SECOND_IDX_FFT,LinearAcceleration_x_SECOND_VAL_FFT,LinearAcceleration_x_THIRD_IDX_FFT,LinearAcceleration_x_THIRD_VAL_FFT,LinearAcceleration_x_VAR,LinearAcceleration_x_VAR_FFT,LinearAcceleration_y_DC_FFT,LinearAcceleration_y_FIRST_IDX_FFT,LinearAcceleration_y_FIRST_VAL_FFT,LinearAcceleration_y_FOURTH_IDX_FFT,LinearAcceleration_y_FOURTH_VAL_FFT,LinearAcceleration_y_MEAN,LinearAcceleration_y_MEAN_FFT,LinearAcceleration_y_MEDIAN,LinearAcceleration_y_MEDIAN_FFT,LinearAcceleration_y_MIDDLE_SAMPLE,LinearAcceleration_y_SECOND_IDX_FFT,LinearAcceleration_y_SECOND_VAL_FFT,LinearAcceleration_y_THIRD_IDX_FFT,LinearAcceleration_y_THIRD_VAL_FFT,LinearAcceleration_y_VAR,LinearAcceleration_y_VAR_FFT,LinearAcceleration_z_DC_FFT,LinearAcceleration_z_FIRST_IDX_FFT,LinearAcceleration_z_FIRST_VAL_FFT,LinearAcceleration_z_FOURTH_IDX_FFT,LinearAcceleration_z_FOURTH_VAL_FFT,LinearAcceleration_z_MEAN,LinearAcceleration_z_MEAN_FFT,LinearAcceleration_z_MEDIAN,LinearAcceleration_z_MEDIAN_FFT,LinearAcceleration_z_MIDDLE_SAMPLE,LinearAcceleration_z_SECOND_IDX_FFT,LinearAcceleration_z_SECOND_VAL_FFT,LinearAcceleration_z_THIRD_IDX_FFT,LinearAcceleration_z_THIRD_VAL_FFT,LinearAcceleration_z_VAR,LinearAcceleration_z_VAR_FFT,AccelerometerStat_x_MIDDLE_SAMPLE,AccelerometerStat_y_MIDDLE_SAMPLE,AccelerometerStat_z_MIDDLE_SAMPLE,GyroscopeStat_x_MIDDLE_SAMPLE,GyroscopeStat_y_MIDDLE_SAMPLE,GyroscopeStat_z_MIDDLE_SAMPLE,MagneticField_x_MIDDLE_SAMPLE,MagneticField_y_MIDDLE_SAMPLE,MagneticField_z_MIDDLE_SAMPLE,pressure_MIDDLE_SAMPLE",
        "t3": "Userid,UUID,Version,Audio_diffSecs,Audio_l1Norm,Audio_l2Norm,Audio_linfNorm,AudPSD_AcrossFreqBands0,AudPSD_AcrossFreqBands1,AudPSD_AcrossFreqBands2,AudPSD_AcrossFreqBands3,Audio_mfccs0,Audio_mfccs1,Audio_mfccs2,Audio_mfccs3,Audio_mfccs4,Audio_mfccs5,Audio_mfccs6,Audio_mfccs7,Audio_mfccs8,Audio_mfccs9,Audio_mfccs10,Audio_mfccs11,Audio_timestemp,Light_accuracy,Light_lux,Light_timestamp",
        "t4": "Userid,UUID,Version,traffic_mobilerxbytes,traffic_mobilerxpackets,traffic_mobiletxbytes,traffic_mobiletxpackets,traffic_totalrxbytes,traffic_totalrxpackets,traffic_totaltxbytes,traffic_totaltxpackets,traffic_totalwifirxbytes,traffic_totalwifirxpackets,traffic_totalwifitxbytes,traffic_totalwifitxpackets,traffic_timestamp,battery_charge_type,battery_current_avg,battery_health,battery_icon_small,battery_invalid_charger,battery_level,battery_online,battery_plugged,battery_present,battery_scale,battery_status,battery_technology,battery_temperature,battery_timestamp,battery_voltage,cpuhertz,cpu_0,cpu_1,cpu_2,cpu_3,total_cpu,totalmemory_freesize,totalmemory_max_size,totalmemory_total_size,totalmemory_used_size,memtotal,Memfree,buffers,cached,swapcached,active,inactive,active_anon,inactive_anon,active_file,inactive_file,unevictable,mlocked,hightotal,highfree,lowtotal,lowfree,swaptotal,swapfree,dirty,writeback,anonpages,mapped,shmem,slab,sreclaimable,sunreclaim,kernelstack,pagetables,commitlimit,committed_as,vmalloctotal,vmallocused,vmallocchunk,msmgpio_cpu0,msmgpio_sum_cpu123,wcd9xxx_cpu0,wcd9xxx_sum_cpu123,pn547_cpu0,pn547_sum_cpu123,cypress_touchkey_cpu0,cypress_touchkey_sum_cpu123,synaptics_rmi4_i2c_cpu0,synaptics_rmi4_i2c_sum_cpu123,sec_headset_detect_cpu0,sec_headset_detect_sum_cpu123,flip_cover_cpu0,flip_cover_sum_cpu123,home_key_cpu0,home_key_sum_cpu123,volume_down_cpu0,volume_down_sum_cpu123,volume_up_cpu0,volume_up_sum_cpu123,companion_cpu0,companion_sum_cpu123,slimbus_cpu0,slimbus_sum_cpu123,function_call_interrupts_cpu0,function_call_interrupts_sum_cpu123,cpu123_intr_prs,tot_user,tot_nice,tot_system,tot_idle,tot_iowait,tot_irq,tot_softirq,ctxt,btime,processes,procs_running,procs_blocked,connectedwifi_ssid,connectedwifi_level,internal_availableblocks,internal_blockcount,internal_freeblocks,internal_blocksize,internal_availablebytes,internal_freebytes,internal_totalbytes,external_availableblocks,external_blockcount,external_freeblocks,external_blocksize,external_availablebytes,external_freebytes,external_totalbytes",
        "userpresentprobe": "userID,UUID,timestamp",
        "wifi": "UserID,UUID,SSID,Capabilities,Freq,Level"
    }
    return (switcher.get(table, "Invalid table"))    


def translate_from_original():
    path_dirs="C:\\Users\\JayT\\Desktop\\prova"
    output_dir="C:\\Users\\JayT\\Desktop\\"
    for dirs in os.walk(path_dirs):
        if(not path_dirs==dirs[0].replace("\\ ","\\\ ")):
            splitted=dirs[0].split("\\")
            file_name=splitted[len(splitted)-1]
            print(file_name)
            with open(output_dir+file_name+"_sampled.csv","w+") as f:
                f.write(switch_for_file(file_name))
                os.chdir(dirs[0])
                for file in glob.glob("*.*"):
                    with open(file,"r+") as f_or:
                        for line in f_or:
                            uuid=int(line.split("\t")[1])
                            if(uuid > 1467331200000 and uuid < 1470009600000):
                                f.write("\n"+line)   
    
    
    
    
#translate_sherlock_from_dump("D:\\Big Data\\Data\\Sherlock Dataset\\Sample Dataset\\Comparison\\","dump_sampledataset_mrsbc_preprocessed_10sec_no500rows.backup",True)
              
import csv
import os
import glob

os.chdir("D:\\Big Data\\Data\\Sherlock Dataset\\Sample Dataset\\Comparison\\Csv Translated Preprocessed\\Csv")
total=0
for file in glob.glob("*.csv"):
    with open(file,"r",encoding="utf-8") as f:
        fileObject = csv.reader(f,delimiter = ",")
        data = list(fileObject)
        row_count = len(data)
        print("Num of rows for "+str(file)+": "+str(row_count))
        total+=row_count
print("\nTotal of rows: "+str(total))

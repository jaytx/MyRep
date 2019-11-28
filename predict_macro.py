"""
@:param
    sys.argv[1]; path where dataset is located
    sys.argv[2]; path where the model is located
    sys.argv[3]; path to OpenKEonSpark/release/Base.so
    sys.argv[4]: embedding dimensionality
    sys.argv[5]: model to use (transe/transh/transr/transd)
"""

from Config import Config
from TransE import TransE
from TransH import TransH
from TransR import TransR
from TransD import TransD  
import sys
import os

def get_ckpt(p):
    ckpt = None
    with open(os.path.join(p,"checkpoint"), 'r') as f:
        first_line = f.readline()
        ckpt = first_line.split(':')[1].strip().replace('"', '').split('/')
        ckpt = ckpt[len(ckpt) - 1]
    return ckpt

for arg in sys.argv: print(arg, type(arg))

dataset_path = sys.argv[1]
model_path = sys.argv[2]
cpp_path = sys.argv[3]
dim = sys.argv[4]
model = sys.argv[5]
  
ckpt = get_ckpt(model_path)
con = Config(cpp_lib_path=cpp_path)
con.set_in_path(dataset_path)
con.set_test_triple_classification(True)
con.set_dimension(int(dim))
con.init()

if model.lower() == "transe": con.set_model_and_session(TransE)
elif model.lower() == "transh": con.set_model_and_session(TransH)
elif model.lower() == "transr": con.set_model_and_session(TransR)
else: con.set_model_and_session(TransD)
    
con.set_import_files(os.path.join(model_path, ckpt))

print("Testing triples...")
test_triples=[]

with open (os.path.join(dataset_path,'test2id.txt')) as f:
    f.readline()
    for line in f:
        triple=line.split(" ")
        test_triples.append([int(triple[0]),int(triple[1]),int(triple[2])])
        
entity_map={}
with open (os.path.join(dataset_path,'entity2id.txt')) as f_entity:
    f_entity.readline()
    for line in f_entity:
        entity=line.split("\t")
        if(len(entity[0].split('"'))>1):
            entity_map.update({int(entity[1].split("\n")[0]) : entity[0].split('"')[1]})
        else: entity_map.update({int(entity[1].split("\n")[0]) : entity[0]})
        
rel_map={}
with open((os.path.join(dataset_path,'relation2id.txt'))) as f_rel:
    f_rel.readline()
    for line in f_rel:
        line_splitted=line.split("\t")
        rel_map.update({int(line_splitted[1].split("\n")[0]) : line_splitted[0]})


#print(str(entity_map.get(triple[0]))+ " "+str(rel_map.get(triple[2]))+ " " + str(entity_map.get(triple[1])))
TP_m,TN_m,FP_m,FN_m,TP_b,TN_b,FP_b,FN_b=con.predict_triples_for_macro(test_triples,entity_map)  
print("=============Evaluation of malicious label=============")
accuracy_m = 1.0 * (TP_m + TN_m) / (TP_m + TN_m + FP_m + FN_m)

if( TP_m + FP_m ==0):
    precision_m=1
else:
    precision_m = 1.0 * TP_m / (TP_m + FP_m)
    
recall_m = 1.0 * TP_m / (TP_m + FN_m)

if(precision_m + recall_m ==0): 
    fmeasure_m=0
else:  
    fmeasure_m = (2 * precision_m * recall_m) / (precision_m + recall_m)
print("True Positive malicious: "+str(TP_m))
print("True Negative malicious: "+str(TN_m))
print("False Positive malicious: "+str(FP_m))
print("False Negative malicious: "+str(FN_m))
print("FPR malicious: "+str(FP_m/(FP_m+TN_m)))
print("TPR malicious: "+str(TP_m/(TP_m+FN_m)))
print("Accuracy malicious: "+ str(accuracy_m))
print("Precision malicious: "+ str(precision_m))
print("Recall malicious: " +str(recall_m))
print("Fmeasure malicious: "+str(fmeasure_m))

print("=============Evaluation of benign label=============")
accuracy_b = 1.0 * (TP_b + TN_b) / (TP_b + TN_b + FP_b + FN_b)

if( TP_b + FP_b ==0):
    precision_b=1
else:
    precision_b = 1.0 * TP_b / (TP_b + FP_b)
    
recall_b = 1.0 * TP_b / (TP_b + FN_b)

if(precision_b + recall_b ==0): 
    fmeasure_b=0
else:  
    fmeasure_b = (2 * precision_b * recall_b) / (precision_b + recall_b)
print("True Positive benign: "+str(TP_b))
print("True Negative benign: "+str(TN_b))
print("False Positive benign: "+str(FP_b))
print("False Negative benign: "+str(FN_b))
print("FPR benign: "+str(FP_b/(FP_b+TN_b)))
print("TPR benign: "+str(TP_b/(TP_b+FN_b)))
print("Accuracy benign: "+ str(accuracy_b))
print("Precision benign: "+ str(precision_b))
print("Recall benign: " +str(recall_b))
print("Fmeasure benign: "+str(fmeasure_b))

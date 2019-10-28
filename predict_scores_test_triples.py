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

with open (os.path.join(dataset_path,'test2id.txt')) as f:
    f.readline()
    for line in f:
        triple=line.split(" ")
        test_triples.append([int(triple[0]),int(triple[1]),int(triple[2])])

#print(str(entity_map.get(triple[0]))+ " "+str(rel_map.get(triple[2]))+ " " + str(entity_map.get(triple[1])))
TP,TN,FP,FN=con.predict_triples(test_triples,entity_map)  
print("True Positive: "+str(TP))
print("True Negative: "+str(TN))
print("False Positive: "+str(FP))
print("False Negative: "+str(FN))
print("FPR: "+str(FP/(FP+TN)))
print("TPR: "+str(TP/(TP+FN)))
accuracy = 1.0 * (TP + TN) / (TP + TN + FP + FN)
precision = 1.0 * TP / (TP + FP)
recall = 1.0 * TP / (TP + FN)
fmeasure = (2 * precision * recall) / (precision + recall)
print("Accuracy: "+ str(accuracy))
print("Precision: "+ str(precision))
print("Recall: " +str(recall))
print("Fmeasure: "+str(fmeasure))



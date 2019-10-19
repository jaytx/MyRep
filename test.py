"""
Once learned the embedding model, this script could be used to:
    use the model learnt (predict_head_entity, predict_tail_entity, predict_relation, predict_triple)
    evaluate test triple classification task:
        - precision, recall, accuracy, f-measure
        - ROC curve

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

os.environ['CUDA_VISIBLE_DEVICES']='-1'

for arg in sys.argv: print(arg, type(arg))

dataset_path = sys.argv[1]
model_path = sys.argv[2]
cpp_path = sys.argv[3]
dim = sys.argv[4]
model = sys.argv[5]



def get_ckpt(p):
    ckpt = None
    with open(os.path.join(p,"checkpoint"), 'r') as f:
        first_line = f.readline()
        ckpt = first_line.split(':')[1].strip().replace('"', '').split('/')
        ckpt = ckpt[len(ckpt) - 1]
    return ckpt

index_rel=[]

rel_map={}
with open((os.path.join(dataset_path,'relation2id.txt'))) as f_rel:
    f_rel.readline()
    for line in f_rel:
        line_splitted=line.split("\t")
        rel_map.update({int(line_splitted[1].split("\n")[0]) : line_splitted[0]})
                    
    
index_rel=[]
with open((os.path.join(dataset_path,'test2id.txt'))) as f:
    f.readline()
    for line in f:
        index=line.split(" ")[2].strip("\n")
        if(not int(index) in index_rel):
            index_rel.append(int(index))
        

rel_index=[]
for value in index_rel:
    rel_index.append([rel_map.get(value),value])

print("TARGET RELATION AND INDEX:")
print(rel_index)

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

con.test()

for relation,index in rel_index:
  print("Plotting ROC Curve for "+relation+"...")
  print("Index: "+str(index))
  print("Path name: "+str((os.path.join(model_path,'plot_'+str(relation)+'.png'))))
  con.plot_roc(rel_index=int(index), fig_name=(os.path.join(model_path,'plot_'+str(index)+'.png')))

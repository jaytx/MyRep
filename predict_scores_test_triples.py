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
    for line in f
    triple=line.split(" ")
    test_triples.append(triple[0],triple[2],triple[1])

for triple in test_triples:
    con.predict_triple(triple[0], triple[1], triple[2])  

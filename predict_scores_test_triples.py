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

for arg in sys.argv: print(arg, type(arg))

dataset_path = sys.argv[1]
model_path = sys.argv[2]
cpp_path = sys.argv[3]
dim = sys.argv[4]
model = sys.argv[5]
  
con = Config(cpp_lib_path=cpp_path)  
con.set_in_path(dataset_path)   
con.set_dimension(dim)   #embedding dimension
con.init()  
con.set_model_and_session(model)
con.set_import_files(model_path)
  
'''perform your operations'''   
con.predict_triple(0, 2, 1)  

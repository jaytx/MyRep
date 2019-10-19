echo "====================================== Parameters ======================================"
echo "Number of batches: $1"
echo "Embedding dimensionality: $2"
echo "Model to use: $3"
echo "Learning rate: $4"

echo "====================================== Start evaluation for batch $i ======================================"
	  python3 $WORK_DIR_PREFIX/test.py /content/drive/My\ Drive/DBpedia/1/0/ /content/drive/My\ Drive/DBpedia/1/0/model/ $WORK_DIR_PREFIX/release/Base.so $2 $3 | tee /content/drive/My\ Drive/DBpedia/1/0/res.txt

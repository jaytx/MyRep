echo "====================================== Parameters ======================================"
echo "Number of batches: $1"
echo "Embedding dimensionality: $2"
echo "Model to use: $3"
echo "Learning rate: $4"
echo "Target relation: $5"

echo "====================================== Start evaluation for batch $i ======================================"
	  echo "Evaluation with test"
	  python3 $WORK_DIR_PREFIX/test.py /content/drive/My\ Drive/DBpedia/0/1/ /content/drive/My\ Drive/DBpedia/0/1/model/ $WORK_DIR_PREFIX/release/Base.so $2 $3 $5 | tee /content/drive/My\ Drive/DBpedia/0/1/res.txt

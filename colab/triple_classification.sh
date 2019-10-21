echo "====================================== Parameters ======================================"
echo "Dataset Path:" $1
echo "Model Path:" $1
echo "Embedding dimensionality: $3"
echo "Model to use: $4"

echo "====================================== Start Triple Classification Evaluation for batch $i ======================================"
	  python3 $WORK_DIR_PREFIX/test.py $1 $2 $WORK_DIR_PREFIX/release/Base.so $3 $4 | tee $1/res.txt



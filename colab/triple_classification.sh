echo "====================================== Parameters ======================================"
echo "Embedding dimensionality: $1"
echo "Model to use: $2"

echo "====================================== Start Triple Classification Evaluation for batch $i ======================================"
	  #python3 $WORK_DIR_PREFIX/predict_scores_test_triples.py /content/drive/My\ Drive/DBpedia/1/0/ /content/drive/My\ Drive/DBpedia/1/0/model/ $WORK_DIR_PREFIX/release/Base.so $1 $2 | tee /content/drive/My\ Drive/DBpedia/1/0/model/res.txt
	  python3 $WORK_DIR_PREFIX/test.py /content/drive/My\ Drive/DBpedia/1/0/ /content/drive/My\ Drive/DBpedia/1/0/model/ $WORK_DIR_PREFIX/release/Base.so $1 $2 | tee /content/drive/My\ Drive/DBpedia/1/0/model/res.txt



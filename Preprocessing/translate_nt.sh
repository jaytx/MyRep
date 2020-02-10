dir=/mnt/d/Big\ Data/Data/Sherlock\ Dataset/Sample\ Dataset/OpenKEonSpark/Discretized\ one\ target\ relation/Equal\ width/Csv
for file in "$dir"/*.csv
do
	IFS="."
	read -ra ADDR <<<"${file##*/}"
	echo "Translating ${ADDR[0]} ..."
	echo "$file"
	python3 csv2rdf.py "$file" --outdata="${ADDR[0]}_data.nt" --outschema=${ADDR[0]}_schema.nt --tnamespace="http://example.com/${ADDR[0]}/" --schemanamespace="http://example.com/${ADDR[0]}/property/"
done

# update output files
# .update.sh

./parse_kraken2.py -k data/abscessus.tab -o output/abscessus.json
./parse_kraken2.py -k data/kansasii.tab -o output/kansasii.json
./parse_kraken2.py -k data/xenopi.tab -o output/xenopi.json
./parse_kraken2.py -k data/tb.tab -o output/tb.json
./parse_kraken2.py -k data/mixed.tab -o output/mixed.json
./parse_kraken2.py -k data/high.tab -o output/high.json
./parse_kraken2.py -k data/low.tab -o output/low.json
./parse_kraken2.py -k data/unclassified.tab -o output/unclassified.json

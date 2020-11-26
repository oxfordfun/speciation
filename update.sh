# update output files
# .update.sh

python parse_kraken2.py -k data/abscessus.tab -o output/abscessus.json
python parse_kraken2.py -k data/kansasii.tab -o output/kansasii.json
python parse_kraken2.py -k data/xenopi.tab -o output/xenopi.json
python parse_kraken2.py -k data/tb.tab -o output/tb.json
python parse_kraken2.py -k data/mixed.tab -o output/mixed.json
python parse_kraken2.py -k data/high.tab -o output/high.json
python parse_kraken2.py -k data/low.tab -o output/low.json
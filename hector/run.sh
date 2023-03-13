counter=0
while true ; do
    #use a counter for the number of extractions
    python3 xtractor.py
    counter=$((counter+1))
    echo "Extraction number $counter"
done
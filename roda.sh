for x in inputs/proc/all_*.txt 
do
    name=$(basename $x)
    echo $name 
    src/merge.py $x inputs/ > logs/${name}.txt 2> logs/${name}.err
done

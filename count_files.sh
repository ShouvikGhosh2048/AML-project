DIRECTORIES=( $(ls data/tsinghua/low-resolution) )

for DIRECTORY in "${DIRECTORIES[@]}"
do
    ls -1 data/tsinghua/low-resolution/$DIRECTORY | wc -l
done

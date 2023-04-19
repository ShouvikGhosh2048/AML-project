DIRECTORIES=( $(ls data/Images) )

for DIRECTORY in "${DIRECTORIES[@]}"
do
    ls -1 data/Images/$DIRECTORY | wc -l
done

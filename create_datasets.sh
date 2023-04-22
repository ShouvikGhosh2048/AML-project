DIRECTORIES=( $(ls data/tsinghua/low-resolution) )

rm -rf data/smaller_dataset
mkdir data/smaller_dataset
mkdir data/smaller_dataset/train
mkdir data/smaller_dataset/val

# for i in {1..1}
# do
#     echo $DIRECTORIES[$i]
#     find data/Images/$DIRECTORIES[$i] -maxdepth 1 -type f
# done

for DIRECTORY in "${DIRECTORIES[@]}"
do
    files=( $(ls data/tsinghua/low-resolution/$DIRECTORY) )

    # creating training dataset
    echo "Copying top 50 files from data/tsinghua/low-resolution/$DIRECTORY to data/smallar_dataset/train/$DIRECTORY"
    mkdir "data/smaller_dataset/train/$DIRECTORY"
    for i in {1..50}
    do
        cp data/tsinghua/low-resolution/$DIRECTORY/${files[i]} data/smaller_dataset/train/$DIRECTORY/${files[i]}
    done

    # creating validation dataset
    echo "Copying next 10 files from data/tsinghua/low-resolution/$DIRECTORY to data/smallar_dataset/val/$DIRECTORY"
    mkdir "data/smaller_dataset/val/$DIRECTORY"
    for i in {51..60}
    do
        cp data/tsinghua/low-resolution/$DIRECTORY/${files[i]} data/smaller_dataset/val/$DIRECTORY/${files[i]}
    done
done


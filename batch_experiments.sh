#!/usr/bin/env bash
for ((i=0;i<10;i++)); do
  python main.py "Colored City delta 0.$i seed 1" "Colored City" -n 3 --delta "0.$i" -q -s 32 32
  echo "Finished step with delta 0.$i"
done

python main.py "Colored City delta 1.0 seed 1" "Colored City" -n 3 --delta 1.0 -q -s 32 32
echo "Finished step with delta 1.0"

#for ((i=0;i<30;i++)); do
#  python main.py "Flowers Yellow and Red no params" "Flowers" "Flowers2" -n 3 --seed "$i" -q
#  echo "Flowers Yellow and Red no params $i"
#done

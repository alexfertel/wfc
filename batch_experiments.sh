#!/usr/bin/env bash
for ((i=0;i<10;i++)); do
  python main.py "AP Red Maze alpha 0.$i" "Red Maze" -n 2 --alpha "0.$i" -q --seed 10
  echo "Finished step with alpha 0.$i"
done

python main.py "AP Red Maze alpha 1.0" "Red Maze" -n 2 --alpha 1.0 -q --seed 10
echo "Finished step with alpha 1.0"

#for ((i=0;i<30;i++)); do
#  python main.py "Flowers Yellow and Red no params" "Flowers" "Flowers2" -n 3 --seed "$i" -q
#  echo "Flowers Yellow and Red no params $i"
#done

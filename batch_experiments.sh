#!/usr/bin/env bash
for ((i=0;i<10;i++)); do
  python main.py "Red Maze alpha 0.$i" "Red Maze" -n 2 --alpha "0.$i" -q &> /dev/null
  echo "Finished step with alpha $i"
done

python main.py "Red Maze alpha 1.0" "Red Maze" -n 2 --alpha 1.0 -q &> /dev/null
echo "Finished step with alpha 1.0"
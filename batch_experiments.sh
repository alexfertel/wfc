#!/usr/bin/env bash
for ((j=0;j<10;j++)); do
    echo "Gamma 0.$j"
    for ((i=0;i<10;i++)); do
      echo "Alpha 0.$i"
      python main.py "Qud gamma 0.$j alpha 0.$i" "Qud" -n 3 --delta "0.$j" --alpha "0.$i" -q
    done

    echo "Alpha 1"
    python main.py "Qud gamma 0.$j alpha 1" "Qud" -n 3 --delta "0.$j" -q
done

echo "Gamma 1"
python main.py "Qud gamma 1 alpha 1" "Qud" -n 3 -q

#for ((i=0;i<30;i++)); do
#  python main.py "Flowers Yellow and Red no params" "Flowers" "Flowers2" -n 3 --seed "$i" -q
#  echo "Flowers Yellow and Red no params $i"
#done

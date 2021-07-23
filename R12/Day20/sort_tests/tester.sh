for fl in $(ls *.inp)
  do ../icicle.py ../quicksort.txt < $fl && echo ''
done

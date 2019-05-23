for i in 1 2
do
   echo "started $i"
   python parsoid_crawler.py ru_params/ru_params_$i.json &
done

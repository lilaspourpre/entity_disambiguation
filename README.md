Current repository contains the commonly available code of **"Entity Disambiguation to Wikipedia for Languages with Different Corpora Volumes"** master thesis. 

Disambiguation model train-test architecture is under private ownership of ISP RAS.

1. Extract texts and graph

1.1 Generate json files with parameters

```
python3 params_computer.py
```

Target json file content:

```json
{
  "spliterator": "\t", 
  "directory": "./output_directory", 
  "host": "127.0.0.1", 
  "language": "be", 
  "symbol": "_", 
  "cat_name": "Вікіпедыя:", 
  "title2id": "be_title2id.txt"
}
```

1.2 Run parsoid crawler providing filename with generated parameters
```
python3 parsoid_crawler.py params.json
```

2. Run node2vec
```
usage: random_walks.py [-h] [-e <epochs>] [-l <sequence_length>] [-p <p>]
                       [-q <q>] [-s <print_every_sequence>] -i <input file> -t
                       <id2title file> -o <output file> -r <r>

Train sequence translation for wikification

optional arguments:
  -h, --help            show this help message and exit
  -e <epochs>           number of epochs (walks) through all nodes
  -l <sequence_length>  sequence length
  -p <p>                parameter for return probability, p >= 0
  -q <q>                parameter for unseen node probability, q >= 0
  -s <print_every_sequence>
                        print every s sequences
  -i <input file>       input jsonlines file
  -t <id2title file>    id2title file
  -o <output file>      output file
  -r <r>                spliterator, <t> for tab or <s> for space in id2title file
```
Lines format in input file:
```json
{
  "id": 73276,
  "links": [73311, 32019],
  "anchors": ["anchor1", "anchor2"], 
  "categories": [45, 884]
}
```
3. Add lemmas and tokens from Apertium:

```bash
 python3 apertium.py input_filename_jsonlines.json.gz output_filename_jsonlines.json.gz apertium-lang-directory
```
4. Generate dataset
5. Train model
6. Test model

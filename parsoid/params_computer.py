import json
import os

language = "hy"
n_splits = 30
dirname = "{}_params".format(language)
if not os.path.exists(dirname):
    os.makedirs(dirname)

for i in range(1, n_splits+1):
    params = {
        "title2id": "{}.id2title_cat.txt".format(language),
        "symbol": "_",
        "language": language,
        "cat_name":"Կատեգորիա:",
        "spliterator": "\t",
        "directory": "{}/data/{}".format(language, i),
        "host": "127.0.0.1"
    }
    with open("{0}/{0}_{1}.json".format(dirname, i), 'w', encoding='utf-8') as w:
        w.write(json.dumps(params))

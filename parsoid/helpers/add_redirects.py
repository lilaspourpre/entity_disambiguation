import os
# tail -n +0 be.id2title.txt > be.id2title_cat.txt
# tail -n +0 be.id2title.category.txt >> be.id2title_cat.txt
from parsoid_helper import load_title_to_id

language = 'uk'
directory = "nlpdocs\\UKWIKI"
t2i = "{}\\{}.id2title_cat.txt".format(directory, language)
title2id = load_title_to_id(t2i)
redirect2title = {}
unresolved = []
resolved = []

with open(os.path.join(directory, "{}.redirects.txt".format(language)), 'r', encoding='utf-8') as file:
    for line in file.read().split('\n'):
        if line != '':
            id_, title, redirect = line.split('\t')
            if title2id.get(redirect, None) == None:
                unresolved.append((title,redirect, []))
            else:
                resolved.append((title2id[redirect], title))
            redirect2title[title] = redirect


def vicious_cirle(title, redirect, prev):
    if title2id.get(redirect, None) != None:
        resolved.append((title2id[redirect], title))
    elif redirect2title.get(redirect, None) != None:
        if redirect2title[redirect] in prev:
            print(title, redirect, prev)
        else:
            unresolved.append((redirect, redirect2title[redirect], prev+[title]))
    else:
        pass
    unresolved.remove((title, redirect, prev))



while len(unresolved)>=1:
    print(len(resolved), len(unresolved), len(resolved)+len(unresolved))
    for title, redirect, prev in unresolved:
        vicious_cirle(title, redirect, prev)

print(len(resolved))

with open(t2i, 'a', encoding='utf-8') as wr:
    for id_, title in resolved:
        wr.write(str(id_)+'\t'+title+'\n')

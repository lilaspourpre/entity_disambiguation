import os
from collections import defaultdict

success = 0
error = 0
error2 = 0
all_ = 0
dict_ = defaultdict(dict)
language = "uk"
for x, y, z in os.walk("{}/data".format(language)):
    for i in z:
        success__ = 0
        error__ = 0
        error2__ = 0
        all__ = 0
        if i.startswith("success"):
            with open(os.path.join(x, i), 'r', encoding='utf-8')as f:
                for line in f:
                    success += 1
                    success__ += 1
            dict_[x]['success'] = success__
        # if i.startswith("error3"):
        #     with open(os.path.join(x, i), 'r', encoding='utf-8')as f:
        #         for line in f:
        #             error2 += 1
        #             error2__ += 1
        #     dict_[x]['error2'] = error2__
        if i.startswith("error"):
            with open(os.path.join(x, i), 'r', encoding='utf-8')as f:
                for line in f:
                    error += 1
                    error__ += 1
            dict_[x]['error'] = error__
        if i.startswith("{}.title2id".format(language)):
            with open(os.path.join(x, i), 'r', encoding='utf-8')as f:
                for line in f:
                    all_ += 1
                    all__ += 1
            dict_[x]['all'] = all__

for k,v in sorted(list(dict_.items())):
    print(k,v)

print(success, error, success+error, all_, all_-success-error)
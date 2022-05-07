import json
import pandas as pd

with open('data/factor_final.json', 'r') as f:
    fac_dict = json.load(f)
for k in fac_dict.keys():
    fac_dict[k] = pd.DataFrame(fac_dict[k])

fac_list = list(fac_dict[k].columns)
for fac in fac_list:
    exec('port_%s = {}' % fac)
    for i in range(1, 6):
        exec("port_%s['port_%s'] = {}" % (fac, i))


dateList = list(fac_dict.keys())
for date in dateList:
    temp = fac_dict[date]
    for fac in fac_list:
        l_1 = temp[temp[fac] >= temp[fac].quantile(0.8)].index.tolist()
        l_2 = [i for i in temp[temp[fac] >= temp[fac].quantile(0.6)].index.tolist() if i not in l_1]
        l_3 = [i for i in temp[temp[fac] >= temp[fac].quantile(0.4)].index.tolist() if i not in l_1 if i not in l_2]
        l_5 = temp[temp[fac] < temp[fac].quantile(0.2)].index.tolist()
        l_4 = [i for i in temp[temp[fac] < temp[fac].quantile(0.4)].index.tolist() if i not in l_5]
        for i in range(1, 6):
            exec("port_%s['port_%s'][date] = l_%s" % (fac, i, i))

for fac in fac_list:
    jsonObj = json.dumps(eval('port_%s' % fac))
    fileObj = open('data/port_%s.json' % fac, 'w', encoding='utf-8')
    fileObj.write(jsonObj)
    fileObj.close()
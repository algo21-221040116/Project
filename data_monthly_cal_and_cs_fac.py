import pandas as pd
import time
import json
'''
将处理好的daily数据转化为monthly的，并得到每个时间截面的cs factor
'''

if __name__ == '__main__':

    ### monthly data process
    ts = time.time()

    symbol_info = pd.read_csv('data/symbol_info.csv', index_col=0)
    for symbol in symbol_info.index.tolist():
        temp = pd.read_csv('data/data_daily/%s.csv' % symbol, parse_dates=True, index_col=0)
        tmp = temp.resample('m').last()
        for t in tmp.index:
            tp = temp[temp.index < t].iloc[-20:, [1, -1]]
            tmp.loc[t, 'PV_corr_avg_o'] = tp['PV_corr_daily'].mean()
            tmp.loc[t, 'PV_corr_std_o'] = tp['PV_corr_daily'].std()
        tmp.to_csv('data/data_monthly/%s.csv' % symbol)

    print('monthly data process done: ', time.time() - ts)



    ### cs factor process
    ts = time.time()

    with open('data/hs300_cleared_dict.json', 'r') as f:
        symbol_dict = json.load(f)

    dateList = list(symbol_dict.keys())

    cs_factor_dict = {}
    for date in dateList:
        print(date)
        cs_factor_df = pd.DataFrame()
        symbol_list = symbol_dict[date]
        for symbol in symbol_list:
            try:
                data = pd.read_csv('data/data_monthly/%s.csv' % symbol, parse_dates=True, index_col=0)
                cs_factor_df.loc[symbol, 'PV_corr_avg_o'] = data.loc[date, 'PV_corr_avg_o']
                cs_factor_df.loc[symbol, 'PV_corr_std_o'] = data.loc[date, 'PV_corr_std_o']
            except:
                # print(symbol, 'deleted')
                pass
        cs_factor_dict[date] = cs_factor_df.to_dict()

    jsonObj = json.dumps(cs_factor_dict)
    fileObj = open('data/cs_factor_dict.json', 'w', encoding='utf-8')
    fileObj.write(jsonObj)
    fileObj.close()

    print('cs factor process done: ', time.time() - ts)
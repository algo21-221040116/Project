import time
import pandas as pd
import numpy as np
import os
import multiprocessing
'''
将jq拉取的分钟数据merge，并同时计算每日PV_corr因子，将每日因子数据存入本地
'''

def fac_cal(symbol, data_arr, data):
    print(symbol)
    tmp = data_arr[data_arr[:, 0] == symbol]
    tmp = np.delete(tmp, 0, axis=1)
    tmp = pd.DataFrame(tmp, columns=data.columns)
    tmp.set_index(tmp['date'], inplace=True, drop=True)
    tmp.drop(columns=['date'], inplace=True)
    tmp.index = pd.to_datetime(tmp.index)

    tp = tmp.resample('d').last().dropna()
    for t in tp.index:
        tmp_arr = np.array(tmp.loc[tmp.index.date == t.date(), ['close', 'volume']].astype(float))

        if np.std(tmp_arr[:, 0]) != 0 and np.std(tmp_arr[:, 1]) != 0:
            tp.loc[t, 'PV_corr_daily'] = np.corrcoef(tmp_arr[:, 0], tmp_arr[:, 1])[0, 1]
    tp.to_csv('data/data_daily/%s.csv' % symbol)
    return tp


if __name__ == '__main__':

    ### merge data
    ts = time.time()

    symbol_info = pd.read_csv('data/symbol_info.csv', index_col=0)
    files = os.listdir('data/data_origin')
    data = pd.DataFrame()
    for file in files:
        temp = pd.read_csv('data/data_origin/%s' % file, index_col=0)
        temp.drop(columns=temp.columns[0], inplace=True)
        data = data.append(temp)
    print(data.shape)
    data = data.drop_duplicates()
    data.to_csv('minute_data_all.csv')
    print(data.shape)

    te = time.time()
    print('data merge: ', te - ts)



    ### factor calculation
    ts = time.time()

    data_arr = np.array(data.reset_index())

    ### single process
    for symbol in symbol_info.index.tolist():
        print(symbol)
        tmp = data_arr[data_arr[:, 0] == symbol]
        tmp = np.delete(tmp, 0, axis=1)
        # tmp = np.insert(tmp, 0, data.columns, axis=0)
        tmp = pd.DataFrame(tmp, columns=data.columns)
        tmp.set_index(tmp['date'], inplace=True, drop=True)
        tmp.drop(columns=['date'], inplace=True)
        tmp.index = pd.to_datetime(tmp.index)

        # t1 = time.time()
        tp = tmp.resample('d').last().dropna()
        for t in tp.index:
            tmp_arr = np.array(tmp.loc[tmp.index.date==t.date(), ['close', 'volume']].astype(float))
            # pv_corr = tmp.loc[tmp.index.date==t.date(), ['close', 'volume']].astype(float).corr().iloc[0, 1]
            # tp.loc[t, 'PV_corr_daily'] = pv_corr
            if np.std(tmp_arr[:, 0]) != 0 and np.std(tmp_arr[:, 1]) != 0:
                tp.loc[t, 'PV_corr_daily'] = np.corrcoef(tmp_arr[:, 0], tmp_arr[:, 1])[0, 1]
        # print(time.time() - t1)
        tp.to_csv('data/data_daily/%s.csv' % symbol)

    # ### multi process
    # pool = multiprocessing.Pool()
    # res_list = []
    # for symbol in symbol_info.index.tolist()[:20]:
    #     res_list.append(pool.apply_async(fac_cal, args=(symbol, data_arr, data)))
    # pool.close()
    # pool.join()
    # print('Sub-process done')
    #
    # for i in range(len(res_list)):
    #     res_list[i].get()

    te = time.time()
    print('factor calculation: ', te - ts)
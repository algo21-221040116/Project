import numpy as np
import pandas as pd
import json
import time
import statsmodels.api as sm
import jqdatasdk as jq
jq.auth('13350103318', '87654321wW')

if __name__ == '__main__':

    ts = time.time()

    symbol_info = pd.read_csv('data/symbol_info.csv', index_col=0)
    industry_list = symbol_info['industry'].drop_duplicates().tolist()
    ind_dummies = pd.DataFrame(index=symbol_info.index)
    for ind in industry_list:
        ind_symbol = symbol_info[symbol_info['industry'] == ind].index.tolist()
        ind_dummies.loc[ind_symbol, ind] = 1
    ind_dummies.fillna(0, inplace=True)

    with open('data/cs_factor_dict.json', 'r') as f:
        cs_factor = json.load(f)

    factor_final = {}
    for date in cs_factor.keys():
        print(date)
        temp = pd.DataFrame(cs_factor[date])

        ### get mkt cap
        q = jq.query(jq.valuation.code, jq.valuation.market_cap).filter(jq.valuation.code.in_(temp.index.tolist()))
        market_cap = jq.get_fundamentals(q, date=date)
        market_cap.set_index(market_cap['code'], inplace=True)
        del market_cap['code']
        temp = pd.merge(temp, market_cap, left_index=True, right_index=True, how='inner')

        temp = pd.merge(temp, ind_dummies, left_index=True, right_index=True, how='inner')
        # temp = np.array(temp)
        # model_avg = sm.OLS(temp[:, 0], temp[:, 2:]).fit()
        # model_std = sm.OLS(temp[:, 1], temp[:, 2:]).fit()
        model_avg = sm.OLS(temp.iloc[:, 0], temp.iloc[:, 2:]).fit()
        model_std = sm.OLS(temp.iloc[:, 1], temp.iloc[:, 2:]).fit()
        corr_avg = model_avg.resid
        corr_std = model_std.resid
        corr = (corr_avg - corr_avg.mean())/corr_avg.std() + (corr_std - corr_std.mean())/corr_std.std()
        res = pd.concat([corr_avg, corr_std, corr], axis=1)
        res.columns = ['PV_corr_avg', 'PV_corr_std', 'PV_corr']
        factor_final[date] = res.to_dict()

    jsonObj = json.dumps(factor_final)
    fileObj = open('data/factor_final.json', 'w', encoding='utf-8')
    fileObj.write(jsonObj)
    fileObj.close()

    print('cs factor process done: ', time.time() - ts)




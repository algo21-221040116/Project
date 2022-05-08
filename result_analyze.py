import matplotlib.pyplot as plt
import os
import pandas as pd
import pMatrix
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 4000)

if __name__ == '__main__':

    index = pd.read_csv(os.path.join('data', 'index.csv'), parse_dates=True, index_col=0)

    bt_start = '2016-12-31'
    bt_end = '2021-12-31'
    port_list = ['port_PV_corr_avg', 'port_PV_corr_std', 'port_PV_corr',
                 'port_Ret20', 'port_PV_corr_deRet20', 'port_PV_corr_trend', 'port_CPV']

    res_df = pd.DataFrame()
    fig = plt.figure(tight_layout=True)

    for port in port_list:
        hs = pd.DataFrame()
        for p in [1, 2, 3, 4, 5, '1-5']:
            pv = pd.read_csv(os.path.join('result', 'pv_'+port+'_%s' % p +'.csv'),
                             parse_dates=True, index_col=0).dropna()
            pv = pv[bt_start: bt_end]
            pv = pv / pv.iloc[0, 0]
            pv.rename(columns={pv.columns[0]: port+'_%s' % p}, inplace=True)
            if p == '1-5':
                plt.plot(pv, label=port+'_%s' % p, linestyle='--')
            else:
                plt.plot(pv, label=port+'_%s' % p)

            if hs.empty:
                hs = index[pv.index[0]: pv.index[-1]][['close']].rename(columns={'close': 'HS300'})
                hs = hs / hs.iloc[0, 0]

            res_df = res_df.append(pMatrix.p_matrix(pv, freq='D', start=pv.index[0].strftime('%Y-%m-%d'),
                                           end=pv.index[-1].strftime('%Y-%m-%d'), exchange='CN'))
        res_df = res_df.append(pMatrix.p_matrix(hs, freq='D', start=pv.index[0].strftime('%Y-%m-%d'),
                                           end=pv.index[-1].strftime('%Y-%m-%d'), exchange='CN'))
        plt.plot(hs, label='HS300')
        plt.title(port[0][:-2])
        plt.legend()
        fig.savefig('result/%s' % port)
        plt.show()

    print(res_df)
    print('done')
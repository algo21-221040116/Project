# Ruihan Liu's Branch
因为聚宽拉数据有流量限制，我们在数据获取及处理过程中尽量将需要流量的操作省略，因此需要频繁将中间过程的数据存入本地，并从本地读出，最后导致这一部分的代码分成了很多个py及ipynb文件，没有单一用一种IDE目的更多是为了同时锻炼一下PyCarm和Jupyter的使用，在此简单介绍一下运行的顺序。
## 程序简介
1. get_symbol_list.ipynb  
获取回测区间每个月index对应的标的  
2. get_symbol_info.ipynb  
获取上述所有标的的行业信息，并汇总  
3. get_minute_data.iptnb 
获取分钟数据，用于构造因子  
4. data_daily_factor_cal.py  
计算用于合成最终月频因子的日频数据  
5. data_monthly_cal_and_cs_fac.py  
计算最终所用的月频因子，以及生成CS-Factor(时间截面的所有因子信息)，用于下一步回测及因子研究

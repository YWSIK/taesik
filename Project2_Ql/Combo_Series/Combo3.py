# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 21:49:23 2022

@author: dnxor
"""

from pykrx import stock
import pandas as pd
import numpy as np
import os

# Combo3 : PER 0, PBR 0.2, EPS 20
# 백테스트 할 날짜 생성
def make_date_list(m,d):
    date_list = []
    for y in range(2003, 2022):
        day = str(y) + str(m) + str(d)
        b_day = stock.get_nearest_business_day_in_a_week(date=day)
        date_list.append(b_day)
    return date_list

# 실제 투자한 회사별 수익 구하기
def row_combo3_company(date, date2):
    codes = stock.get_market_ticker_list(date)
    corp = []
    for code in codes:
        name = stock.get_market_ticker_name(code)
        corp.append([code, name])
    df1 = pd.DataFrame(data=corp, columns = ['code', '종목명'])
    df2 = df1.set_index('code')
    
    df_c = stock.get_market_cap_by_ticker(date) #종가
    df_f = stock.get_market_fundamental_by_ticker(date) #PER, PBR, DIV, ....

    df_c2 = stock.get_market_cap_by_ticker(date2) #1년 후 종가
    df_c2 = df_c2[['종가', '상장주식수']]
    df_f2 = stock.get_market_fundamental_by_ticker(date2) #1년 후 수치들
    df_f2 = df_f2['EPS']
    
    df = pd.merge(df2, df_c, left_index=True, right_index=True)
    df = pd.merge(df, df_f, left_index=True, right_index=True)
    df = pd.merge(df, df_c2, left_index=True, right_index=True)
    df = pd.merge(df, df_f2, left_index=True, right_index=True)
    
    # BPS PER PBR EPS DIV DPS
    df = df[['종목명','종가_x', '상장주식수_x', 'EPS_x', '종가_y', '상장주식수_y', 'EPS_y', 'PBR']]
    df.columns = ['종목명','종가', '상장주식수', 'EPS', '1년후종가', '1년후상장주식수', '1년후EPS', 'PBR']
    df['상장주식수변동'] = df['1년후상장주식수'] - df['상장주식수']
    df['EPS_delta'] = (  ( (df['1년후EPS'] - df['EPS']) / df['EPS'] )* 100 )
    
    
    df = df[df['PBR'] > 0.2] 
    df = df[df['EPS_delta'] > 20]
    df['combo3_rank1'] = df['PBR'].rank() +  df['EPS_delta'].rank(ascending= False)
    df = df.sort_values(by = ['combo3_rank'])
    
    df = df.iloc[:30] #종목개수
    df['수익'] = df['1년후종가'] - df['종가']
    
    df['수익'].loc[df['상장주식수변동']<0] = df['1년후종가']*(1 + df['상장주식수변동'] / df['상장주식수']) - df['종가']    
    df['수익'].loc[df['상장주식수변동']>0] = df['1년후종가']*(1 + df['상장주식수변동'] / df['상장주식수']) - df['종가']  
    
    df['수익률'] = (df['수익'] / df['종가'] )
    df['투자년도'] = np.array([date]*len(df))
    
    return df

#연도별 수익률 구하기
def row_combo3(date, date2):
    codes = stock.get_market_ticker_list(date)
    corp = []
    for code in codes:
        name = stock.get_market_ticker_name(code)
        corp.append([code, name])
    df1 = pd.DataFrame(data=corp, columns=['code', '종목명'])
    df1 = df1.set_index(['code'])
    
    df_c = stock.get_market_cap_by_ticker(date) #종가
    df_f = stock.get_market_fundamental_by_ticker(date) #PER, PBR, DIV, ....    
    
    df_c2 = stock.get_market_cap_by_ticker(date2) #1년 후 종가
    df_c2 = df_c2[['종가', '상장주식수']]
    df_f2 = stock.get_market_fundamental_by_ticker(date2) #1년 후 수치들
    df_f2 = df_f2['EPS']
    
    df = pd.merge(df1, df_c, left_index=True, right_index=True)
    df = pd.merge(df, df_f, left_index=True, right_index=True)
    df = pd.merge(df, df_c2, left_index=True, right_index=True)
    df = pd.merge(df, df_f2, left_index=True, right_index=True)
    
    df = df[['종목명','종가_x', '상장주식수_x', 'EPS_x', '종가_y', '상장주식수_y', 'EPS_y', 'PBR', 'PER']]
    df.columns = ['종목명','종가', '상장주식수', 'EPS', '1년후종가', '1년후상장주식수', '1년후EPS', 'PBR', 'PER']
    df['상장주식수변동'] = df['1년후상장주식수'] - df['상장주식수']
    df['EPS_delta'] = ( ( (df['1년후EPS'] - df['EPS']) / df['EPS'] )*100 )
    
    df = df[df['PBR'] > 0.2] 
    df = df[df['EPS_delta'] > 20]
    df['combo3_rank1'] = df['PBR'].rank() +  df['EPS_delta'].rank(ascending= False)
    df = df.sort_values(by = ['combo3_rank'])

    
    df = df.iloc[:30] #종목개수
    df['수익'] = df['1년후종가'] - df['종가']
    
    df['수익'].loc[df['상장주식수변동']<0] = df['1년후종가']*(1 + df['상장주식수변동'] / df['상장주식수']) - df['종가']    
    df['수익'].loc[df['상장주식수변동']>0] = df['1년후종가']*(1 + df['상장주식수변동'] / df['상장주식수']) - df['종가']  
 
    df['투자년도'] = np.array([date] * len(df) )
    
    df = df.iloc[:30] #종목개수
    df['수익률'] = ( df['수익'] / df['종가'] )
    df['투자년도'] = np.array([date]*len(df))
    
    p = df['수익률'].mean()
    
    result = []
    result.append([date, date2, p])
    
    df_t = pd.DataFrame(data=result, columns = ['투자일', '1년후', '수익률'])
    return df_t

    df = df.iloc[:30] #종목개수
    df['수익'] = df['1년후종가'] - df['종가']
    
    df['수익'].loc[df['상장주식수변동']<0] = df['1년후종가']*(1 + df['상장주식수변동'] / df['상장주식수']) - df['종가']    

    df['투자년도'] = np.array([date] * len(df) )
    
    df = df.iloc[:30] #종목개수
    df['수익률'] = ( df['수익'] / df['종가'] )
    df['투자년도'] = np.array([date]*len(df))
    
    p = df['수익률'].mean()
    
    result = []
    result.append([date, date2, p])
    
    df_t = pd.DataFrame(data=result, columns = ['투자일', '1년후', '수익률'])
    return df_t

#투자 시작년도부터 마지막 년도까지 반복, date & date2 def

def invest_years(date_list):
    for n in range(len(date_list)):
        if n < len(date_list)-1:
            date = date_list[n]
            date2 = date_list[n+1]
            
            if n == 0:
                df_t = row_combo3 (date, date2)
                df = row_combo3_company (date, date2)
          
            else:
                df_t = pd.concat([df_t, row_combo3(date, date2)])
                df = pd.concat([df, row_combo3_company(date, date2)])
                
    path2 = origin_path + folder_name + '//Combo3(' + m + '월' + d + '일).xlsx'
    df.to_excel(path2)
    return df_t
    print(df_t)
    
test_days = ['28'] #매월 매수/매도일

for d in test_days:
    origin_path = 'C://USERS/dnxor/Invest/Combo_3'
    folder_name = '//Combo3_BackTest(매월' + d + '일, PBR 0이상 & PER 0이상 & EPS 성장률 20% 이상) (20개)'
    os.mkdir(origin_path + folder_name)
    
    
    #월별로 테스트를 반복하여 결과 얻기
    for m in range(12):
        if m == 0:
            m = '01'
            #연도별 날짜 List 만들기
            date_list = make_date_list(m, d)
            #백테스트 구동하기
            df_t = invest_years(date_list)
            
        else:
            m += 1
            m  = '0' + str(m)
            m = m[-2:]
            print(m)
            #연도별 날짜 List 만들기
            date_list = make_date_list(m, d)
            #백테스트 구동하기
            df_t = pd.concat([df_t, invest_years(date_list)])
    
    path = origin_path + folder_name + '//Combo3_BackTest(종합매월' + d + '일투자) 20개. xlsx'
    df_t.to_excel(path)  

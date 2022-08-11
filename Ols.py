import pandas as pd 
from scipy import stats
import matplotlib.pyplot as plt 
Lotte=pd.read_excel('C:/users/dnxor/Documents/PythonScripts/Lotte.xlsx', sheet_name = 0, header = 0) 
print(Lotte)
Lotte.corr(method='pearson')

#2)
import pandas 
from scipy import stats
import matplotlib.pyplot as plt  
Lotte=pd.read_excel('C:/users/dnxor/Documents/PythonScripts/Lotte.xlsx', sheet_name = 0, header = 0) 
t, p = stats.pearsonr(Lotte['Value'], Lotte['sales']) 
print("Pearson’s correlation coefficient: %s, p-value: %s" % (t, p))

#3)
import pandas 
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols   
Lotte=pd.read_excel('C:/users/dnxor/Documents/PythonScripts/Lotte.xlsx', sheet_name = 0, header = 0) 
model = ols("Value ~ sales + opprofit + debtratio + ROE + ROA + EPS + BPS", Lotte).fit() 
print(model.summary())
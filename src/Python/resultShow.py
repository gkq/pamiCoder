from datetime import datetime, date
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

filePath1 = 'C:\gkq\Tianchi\\test\mars_tianchi_artist_plays_predict_offline_60_stlfmaria.csv'
df_mar = pd.read_csv(filePath1, header=None, encoding='utf8')

filePath2 = 'C:\gkq\Tianchi\mars_tianchi_artist_plays_predict1.csv'
df_lr = pd.read_csv(filePath2, header=None, encoding='utf8')

#结果对比
plt.figure(1)
plt.plot(df_lr[1],color='red', label='LR')
plt.plot(df_mar[1], color='blue', label='Maria')
plt.title('the comparsion betweent LR and Maria algorithm')
plt.legend()

print("Residual sum of squares: %.2f"
      % np.mean((df_lr[1] - df_mar[1]) ** 2))

tmp = df_lr.groupby(['1'], as_index=False).average()
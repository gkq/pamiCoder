from datetime import datetime, date
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.externals import joblib
import pickle

filePath = 'C:/gkq/Tianchi/song_ds_feature.csv'
song_ds_feature = pd.read_csv(filePath, header=0, encoding='utf8')

#节假日数组构建
holidays = np.zeros(366)
# holidays[63] = 1#植树节
# holidays[66] = 1#妇女节
holidays[93:96] = np.arange(3) + 1#清明节
holidays[120:123] = np.arange(3) + 1#劳动节
holidays[170:173] = np.arange(3) + 1#端午节
holidays[268:276] = np.arange(8) + 1#中秋节+国庆节

#数据预处理
song_ds_feature['Ds'] = list(map(lambda s:datetime.strptime(s, '%Y-%m-%d').date(), song_ds_feature['Ds']))
song_ds_feature['publish_time'] = list(map(lambda s:datetime.strptime(str(s), '%Y%m%d').date(), song_ds_feature['publish_time']))

#基于已有数据构建新的特征
song_ds_feature['delta_day'] =list(map(lambda t: t.days, song_ds_feature['Ds']-song_ds_feature['publish_time']))
song_ds_feature['weekday'] = list(map(lambda d: d.weekday(),song_ds_feature['Ds']))
song_ds_feature['isholiday'] = list(map(lambda d: int(holidays[d.days]!=0), song_ds_feature['Ds']-date(2015,1,1)))
song_ds_feature['idxholiday'] = list(map(lambda d: int(holidays[d.days]), song_ds_feature['Ds']-date(2015,1,1)))

#

#特征分量归一化处理
song_ds_feature['song_init_plays'] = (song_ds_feature['song_init_plays'] - min(song_ds_feature['song_init_plays'])) / max(song_ds_feature['song_init_plays'])
song_ds_feature['delta_day'] = (song_ds_feature['delta_day'] - min(song_ds_feature['delta_day'])) / max(song_ds_feature['delta_day'])
song_ds_feature['Language'] = (song_ds_feature['Language'] - min(song_ds_feature['Language'])) / max(song_ds_feature['Language'])


test_day = date(2015,7,1) #训练数据和测试数据分割点
test_day2 = date(2015,7,1)
train_data = song_ds_feature[song_ds_feature['Ds']<test_day]
test_data = song_ds_feature[song_ds_feature['Ds']>=test_day2]

X_train = train_data[['song_init_plays','Language','Gender','downloads_mean','favorites_mean','plays_mean','downloads', 'favorites',
                      'delta_day','weekday','isholiday','idxholiday']].values #'song_id','artist_id',
y_train = train_data['plays'].values
X_test = test_data[['song_init_plays','Language','Gender', 'downloads_mean','favorites_mean','plays_mean','downloads', 'favorites',
                    'delta_day','weekday','isholiday','idxholiday']].values
y_test = test_data['plays'].values


#训练模型和预测结果
# Create linear regression object
regr = linear_model.LinearRegression()

#regr = linear_model.Ridge( alpha=10)

# regr = linear_model.Lasso( alpha=0)
regr.fit(X_train, y_train)
del song_ds_feature, X_train, y_train #释放内存
result = regr.predict(X_test)

# regr = RandomForestClassifier()
# regr.fit(X_train, y_train)
# result = regr.predict_proba(X_test)

print("Residual sum of squares: %.2f"
      % np.mean((result - y_test) ** 2))
plt.plot(y_test[500:700],color='blue')
plt.plot(result[500:700],color='green')

#结果保存
f = open('dump.txt', 'wb')
pickle.dump(regr,f)
f.close()

test_data['result'] = list(result)
test_data['plays'] = list(map(lambda p: np.int64(p), test_data['plays'].values)) #转换为np.int64，否则分组sum不了
tmp = test_data.groupby(['artist_id','Ds']).sum()
tmp.reset_index(level=[0,1],inplace=[True,True])
#预测结果展示
plt.figure(2)
plt.plot(tmp['result'],color='red', label='predict')
plt.plot(tmp['plays'], color='blue', label='groundtruth')
plt.title('the comparsion betweent predict and groundtruth')
plt.legend()

#保存预测结果
resPath = 'C:\gkq\Tianchi\mars_tianchi_artist_plays_predict.csv'
resDf = tmp[['artist_id', 'result','Ds']]
resDf.to_csv(resPath,header=None,encoding='utf8',index=False, date_format='%Y%m%d')

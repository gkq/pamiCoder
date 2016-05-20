from datetime import datetime, date
import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt

filePath = 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/song_ds_feature.csv'
song_ds_data = pd.read_csv(filePath, header=None, encoding='utf8')
feature_name = ['Ds','song_id','artist_id','publish_time','song_init_plays','Language',
                'Gender','plays']#'delta_day','weekday','holiday']
song_ds_feature = pd.DataFrame(song_ds_data.values,columns=feature_name)
#数据预处理
# song_ds_feature['song_id'] = song_ds_feature['song_id'].astype('category')
# song_ds_feature['song_id'].cat.categories = np.arange(9657)+1
# song_ds_feature['artist_id'] = song_ds_feature['artist_id'].astype('category')
# song_ds_feature['artist_id'].cat.categories = np.arange(50)+1
# print(song_ds_feature.ix[:1])
# for i in range(song_ds_feature.__len__()):
#     song_ds_feature.ix[i,'Ds'] = datetime.strptime(song_ds_feature.ix[i, 'Ds'], '%Y-%m-%d').date()
#     song_ds_feature.ix[i, 'publish_time'] = datetime.strptime(song_ds_feature.ix[i, 'publish_time'], '%Y-%m-%d').date()
song_ds_feature['Ds'] = list(map(lambda s:datetime.strptime(s, '%Y-%m-%d').date(), song_ds_feature['Ds']))
song_ds_feature['publish_time'] = list(map(lambda s:datetime.strptime(s, '%Y-%m-%d').date(), song_ds_feature['publish_time']))

#基于已有数据构建新的特征
song_ds_feature['delta_day'] =list(map(lambda t: t.days, song_ds_feature['Ds']-song_ds_feature['publish_time']))
song_ds_feature['weekday'] = list(map(lambda d: d.weekday(),song_ds_feature['Ds']))

test_day = date(2015,7,1) #训练数据和测试数据分割点
train_data = song_ds_feature[song_ds_feature['Ds']<test_day]
test_data = song_ds_feature[song_ds_feature['Ds']>=test_day]

X_train = train_data[['song_init_plays','Language','Gender','delta_day','weekday']].values #'song_id','artist_id',
y_train = train_data['plays'].values
X_test = test_data[['song_init_plays','Language','Gender','delta_day','weekday']].values
y_test = test_data['plays'].values

#训练模型和预测结果
# Create linear regression object
regr = linear_model.LinearRegression()

# Create linear regression object
# regr = linear_model.Ridge( alpha=0)

# Create linear regression object
# regr = linear_model.Lasso( alpha=0)
regr.fit(X_train, y_train)
result = regr.predict(X_test)

print("Residual sum of squares: %.2f"
      % np.mean((result - y_test) ** 2))
plt.plot(y_test[500:700],color='blue')
plt.plot(result[500:700],color='green')

#结果保存
test_data['result'] = list(result)
tmp = test_data.groupby(['artist_id','Ds']).sum()
tmp.reset_index(level=[0,1],inplace=[True,True])
resPath = 'C:\gkq\Tianchi\mars_tianchi_artist_plays_predict.csv'
resDf = tmp[['artist_id', 'result','Ds']]
resDf.to_csv(resPath,header=None,encoding='utf8',index=False, date_format='%Y%m%d')

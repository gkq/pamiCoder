import pandas as pd
import numpy as np
from sklearn import linear_model
from datetime import date, datetime
import matplotlib.pyplot as plt
from sklearn.externals import joblib
import pickle

filePath = 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/mars_tianchi_songs.csv'
song_tbl = pd.read_csv(filePath, header=None, encoding='utf8')
feature_name = ['song_id','artist_id','publish_time','song_init_plays','Language',
                'Gender']#'delta_day','weekday','holiday']
song_feature = pd.DataFrame(song_tbl.values,columns=feature_name)
start_date = date(2015,9,1)
end_date = date(2015,10,30)
Ds = pd.DataFrame(pd.date_range(start_date,end_date))
#两张表crossjoin
song_feature['key'] = 0
Ds['key'] = 0
song_ds_feature = pd.merge(song_feature, Ds, on = 'key')
song_ds_feature.drop('key',1, inplace = True)
song_ds_feature['publish_time'] = list(map(lambda s:datetime.strptime(str(s), '%Y%m%d').date(), song_ds_feature['publish_time']))
song_ds_feature.columns.values[-1] = 'Ds'

#构建特征
song_ds_feature['delta_day'] =list(map(lambda t: t.days, song_ds_feature['Ds']-song_ds_feature['publish_time']))
song_ds_feature['weekday'] = list(map(lambda d: d.weekday(),song_ds_feature['Ds']))
X_test = song_ds_feature[['song_init_plays','Language','Gender','delta_day','weekday']].values

#预测
regr = pickle.load('model')
result = regr.predict(X_test)
#结果保存
song_ds_feature['result'] = list(result)
tmp = song_ds_feature.groupby(['artist_id','Ds']).sum()
tmp.reset_index(level=[0,1],inplace=[True,True])
resPath = 'C:\gkq\Tianchi\mars_tianchi_artist_plays_predict1.csv'
resDf = tmp[['artist_id', 'result','Ds']]
resDf.to_csv(resPath,header=None,encoding='utf8',index=False, date_format='%Y%m%d')
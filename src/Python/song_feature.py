import pandas as pd
import numpy as np
from sklearn import linear_model
from datetime import date, datetime
import matplotlib.pyplot as plt

filePath = 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/mars_tianchi_songs.csv'
song_tbl = pd.read_csv(filePath, header=None, encoding='utf8')
feature_name = ['song_id','artist_id','publish_time','song_init_plays','Language',
                'Gender']
song_feature = pd.DataFrame(song_tbl.values,columns=feature_name)
song_feature.sort_values(by='song_id', ascending=True, inplace=True)

#song_action_perday表构建
song_downloads_perday_file = 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/song_downloads_perday.csv'
song_downloads_perday = pd.read_csv(song_downloads_perday_file, header=None, encoding='utf8')
song_downloads_perday.columns=['song_id', 'downloads', 'Ds']
song_downloads_perday['Ds'] = list(map(lambda s:datetime.strptime(s, '%Y-%m-%d').date(), song_downloads_perday['Ds']))

song_favorites_perday_file = 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/song_favorites_perday.csv'
song_favorites_perday = pd.read_csv(song_favorites_perday_file, header=None, encoding='utf8')
song_favorites_perday.columns=['song_id', 'favorites', 'Ds']
song_favorites_perday['Ds'] = list(map(lambda s:datetime.strptime(s, '%Y-%m-%d').date(), song_favorites_perday['Ds']))

song_plays_perday_file = 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/song_plays_perday.csv'
song_plays_perday = pd.read_csv(song_plays_perday_file, header=None, encoding='utf8')
song_plays_perday.columns=['song_id', 'plays', 'Ds']
song_plays_perday['Ds'] = list(map(lambda s:datetime.strptime(s, '%Y-%m-%d').date(), song_plays_perday['Ds']))

#处理缺失值
start_date = date(2015,3,1)
end_date = date(2015,8,30)
Ds = pd.DataFrame(pd.date_range(start_date,end_date).date, columns=['Ds'])
song = pd.DataFrame(list(set(song_feature['song_id'])), columns=['song_id'])
song.sort_values(by='song_id', inplace=True)
Ds['key'] = 0
song['key'] = 0
song_Ds = pd.merge(song, Ds, how='outer', on='key')
song_Ds.drop('key',1,inplace=True)

#下载缺失值处理
song_downloads_perday = pd.merge(song_downloads_perday, song_Ds, how='right', on=['song_id', 'Ds'])
song_downloads_perday.sort_values(by=['song_id', 'Ds'], inplace=True)
song_downloads_perday['downloads'].fillna(0, inplace=True)

#收藏缺失值处理
song_favorites_perday = pd.merge(song_favorites_perday, song_Ds, how='right', on=['song_id', 'Ds'])
song_favorites_perday.sort_values(by=['song_id', 'Ds'], inplace=True)
song_favorites_perday['favorites'].fillna(0, inplace=True)

#play缺失值处理
song_plays_perday = pd.merge(song_plays_perday, song_Ds, how='right', on=['song_id', 'Ds'])
song_plays_perday.sort_values(by=['song_id', 'Ds'], inplace=True)
song_plays_perday['plays'].fillna(0, inplace=True)


resDf = song_plays_perday[['song_id', 'Ds', 'plays']]
resDf['downloads'] = song_downloads_perday['downloads']
resDf['favorites'] = song_favorites_perday['favorites']
# #保存结果
# resPath = 'C:\gkq\Tianchi\song_action_perday.csv'
# resDf.to_csv(resPath,header=True,encoding='utf8',index=False, date_format='%Y%m%d')


#song_feature表构建
##特征构建，song本身的特征，比如
song_feature['downloads_mean'] = list(song_downloads_perday.groupby(by='song_id').mean()['downloads'])
song_feature['favorites_mean'] = list(song_favorites_perday.groupby(by='song_id').mean()['favorites'])
song_feature['plays_mean'] = list(song_plays_perday.groupby(by='song_id').mean()['plays'])

# song_featurePath = 'C:\gkq\Tianchi\song_feature.csv'
# song_feature.to_csv(song_featurePath,header=True,encoding='utf8',index=False, date_format='%Y%m%d')

#song_feature表和song_action_perday表join，之后再构建一些特征得到表song_ds_feature
song_ds_feature = pd.merge(song_feature, resDf, how='right', on='song_id')
song_ds_featurePath = 'C:\gkq\Tianchi\song_ds_feature.csv'
song_ds_feature.to_csv(song_ds_featurePath,header=True,encoding='utf8',index=False, date_format='%Y%m%d')
print(len(song_ds_feature))
print(len(song_ds_feature) == len(Ds)*len(song_feature))
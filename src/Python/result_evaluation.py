import pandas as pd
import numpy as np
from datetime import datetime, date

#groud_truth
gt_file = 'C:\gkq\Tianchi\mars_tianchi_artist_plays_gt.csv'
#predict_result
test_file = 'C:\gkq\Tianchi\mars_tianchi_artist_plays_predict.csv'
gt_df = pd.read_csv(gt_file, header=None, encoding='utf8')
test_df = pd.read_csv(test_file, header=None)

#seriesX是预测值，seriesY是真实值
def cumScore(seriesX, seriesY):
    sigma = np.sqrt(sum(pow((seriesX-seriesY)/seriesY,2))/len(seriesY))
    weight = np.sqrt(sum(seriesY))
    return sigma, weight
#数据预处理
##将歌手ID转换为整数1-50
gt_df[0] = gt_df[0].astype('category')
gt_df[0].cat.categories = np.arange(50)+1
test_df[0] = test_df[0].astype('category')
test_df[0].cat.categories = np.arange(50)+1
##将日期从字符串转化为date
gt_df[2] = list(map(lambda s:datetime.strptime(s, '%Y-%m-%d').date(), gt_df[2]))
test_df[2] = list(map(lambda s:datetime.strptime(s, '%Y-%m-%d').date(), test_df[2]))
# for i in range(gt_df.__len__()):
#     gt_df.iloc[i,2] = datetime.strptime(gt_df.iloc[i, 2], '%Y-%m-%d').date()
# for i in range(test_df.__len__()):
#     test_df.iloc[i,2] = datetime.strptime(str(test_df.iloc[i, 2]), '%Y%m%d').date()
# for i in range(50):
#     singer1 = gt_df[gt_df.iloc[:,0]==i+1]
#     singer1.iloc[:,1].plot(use_index=False)
test_df = gt_df #使用真实数据自己测试
start_date = date(2015,7,1)
end_date = date(2015,8,30)
# start_date = min(test_df[2])
# end_date = max(test_df[2])
#dates = pd.date_range(start_date,end_date,freq='D')
#gt_df = gt_df[start_date:end_date]
sigma = np.zeros(50)
weight = np.zeros(50)
for i in range(50):
    truth = gt_df[gt_df.iloc[:,0]==i+1]
    predict = test_df[test_df.iloc[:,0]==i+1]
    truthS = pd.Series(list(truth.iloc[:,1]),index=truth.iloc[:,2])
    truthS = truthS[start_date:end_date]
    #truthS.resample('D')
    #truthS.reindex(,fill_value=0)
    predictS = pd.Series(list(predict.iloc[:,1]), index=predict.iloc[:,2])
    predictS = predictS.reindex(truthS.index, fill_value=0)
    sigma[i], weight[i] = cumScore(predictS, truthS)

FScore = sum((1-sigma)*weight)
print(FScore)




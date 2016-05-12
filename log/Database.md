# 天池比赛数据库说明

## 配置

- 数据库地址：202.120.37.201:3306
- 用户名：root
- 密码：tianchi

## 数据库结构

- 数据库名称: tianchi
- 包含表格
    + 用户行为表（mars\_tianchi\_user_actions）
    + 歌曲艺人表（mars\_tianchi_songs）

### 用户行为表内容说明

- user_id：用户唯一标识 **主键** char(32) 
- song_id：歌曲唯一标识 char(32)
- gmt_create：用户播放时间（unix时间戳表示）精确到小时 int(11)
- action_type：行为类型：1，播放；2，下载，3，收藏 tinyint(3)
- Ds:记录收集日（分区）date

### 歌曲艺人表内容说明

- song_id：主键 char(32) 歌曲唯一标识
- artist_id：char(32) 歌曲所属的艺人Id
- publish_time：date 歌曲发行时间，精确到天
- song_init_plays：int(11) 歌曲的初始播放数，表明该歌曲的初始热度
- Language：smallint(11) 数字表示1,2,3…
- Gender： tinyint(8) 性别 1,2,3

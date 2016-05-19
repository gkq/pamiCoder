#数据清洗
#将publish_time>3.1且song_init_plays不为0的设置为0
select count(*) from tianchi.mars_tianchi_songs where publish_time>='2015-3-1' and song_init_plays > 0;

-- create database washed;
create table washed.mars_tianchi_songs as
select * from tianchi.mars_tianchi_songs;
update washed.mars_tianchi_songs set song_init_plays=0 where publish_time>='2015-3-1' and song_init_plays > 0;

#35W用户有8.3只出现一次，1w首歌，有500首只出现一次。需要将他们清除掉
create table washed.mars_tianchi_user_actions as select * from tianchi.mars_tianchi_user_actions;
-- delete from washed.mars_tianchi_user_actions where user_id in(
-- select user_id from 
-- (
--  select user_id, count(*) as freq from washed.mars_tianchi_user_actions group by user_id
-- )a where freq<=1
-- );
-- 
use washed;
create table user_freq as
 select user_id, count(*) as freq from mars_tianchi_user_actions group by user_id order by freq;

create table song_freq as
 select song_id, count(*) as freq from mars_tianchi_user_actions group by song_id order by freq;
 
 delete from washed.mars_tianchi_user_actions where user_id in
 (
 select user_id from user_freq where freq=1
 );
 
 delete from washed.mars_tianchi_user_actions where song_id in
 (
 select song_id from song_freq where freq=1
 );
 
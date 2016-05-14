show databases;
use tianchi;
show tables;
show index from mars_tianchi_user_actions;

select * from mars_tianchi_user_actions where user_id='7063b3d0c075a4d276c5f06f4327cf4a';

select count(*) from mars_tianchi_user_actions group by user_id, song_id order by count(*) desc limit 10;

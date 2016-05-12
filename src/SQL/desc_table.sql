show databases;
use tianchi;
show tables;
desc mars_tianchi_user_actions;
insert into mars_tianchi_user_actions
(user_id, song_id, gmt_create, action_type, Ds)
values
(7063b3d0c075a4d276c5f06f4327cf4a, effb071415be51f11e845884e67c0f8c, 20150315, 1, 20150315);

select count(*) from mars_tianchi_user_actions;
select * from mars_tianchi_user_actions where gmt_create>=0;
select * from mars_tianchi_user_actions where user_id='7063b3d0c075a4d276c5f06f4327cf4a';

select * from mars_tianchi_songs where song_id='af0e153c72bf63e21bb42702ef0d7726';

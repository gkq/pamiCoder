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

drop table if exists mars_tianchi_artist_plays_gt;

create table mars_tianchi_artist_plays_gt as
	select artist_id, count(*) as Plays, Ds from
    (
    select artist_id, song.song_id as song_id, Ds from mars_tianchi_user_actions usr 
		left outer join mars_tianchi_songs song 
        on (usr.song_id=song.song_id)
        where usr.action_type = 1 
    )a group by artist_id, Ds order by artist_id, Ds, song_id;
    

select * from washed.song_first_action 
	into outfile 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/song_first_action.csv'
    fields terminated by ','
    optionally enclosed by '"'
    lines terminated by '\n';

#导出ground_truth文件
select * from tianchi.mars_tianchi_artist_plays_gt 
	into outfile 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/ mars_tianchi_artist_plays_gt.csv'
    fields terminated by ','
    optionally enclosed by '"'
    lines terminated by '\n';
show databases;
use tianchi;
show tables;
show table status;
show index from mars_tianchi_songs;
show create table mars_tianchi_songs;

select * from mars_tianchi_songs group by artist_id limit 20;

select * from mars_tianchi_songs where publish_time>1980-0-0 order by publish_time ;

select artist_id, count(*) from mars_tianchi_songs group by artist_id;

select artist_id, count(song_id) from mars_tianchi_songs group by artist_id with rollup;

select count(*) from
	(
		select distinct artist_id from mars_tianchi_songs
	) a;

use mysql;
select * from user;

use washed;
#创建artist_plays_perday
drop table if exists artist_plays_perday;
create table artist_plays_perday as
	select artist_id, count(*) as Plays, Ds from
    (
    select artist_id, song.song_id as song_id, Ds from mars_tianchi_user_actions usr 
		left outer join mars_tianchi_songs song 
        on (usr.song_id=song.song_id)
        where usr.action_type = 1 
    )a group by artist_id, Ds order by artist_id, Ds, song_id;

select count(*) from song_plays_perday;
    
#创建artist_downloads_perday
create table artist_downloads_perday as
	select artist_id, count(*) as Downloads, Ds from
    (
    select artist_id, song.song_id as song_id, Ds from mars_tianchi_user_actions usr 
		left outer join mars_tianchi_songs song 
        on (usr.song_id=song.song_id)
        where usr.action_type = 2 
    )a group by artist_id, Ds order by artist_id, Ds, song_id;

#创建artist_favorites_perday
create table artist_favorites_perday as
	select artist_id, count(*) as Favorites, Ds from
    (
    select artist_id, song.song_id as song_id, Ds from mars_tianchi_user_actions usr 
		left outer join mars_tianchi_songs song 
        on (usr.song_id=song.song_id)
        where usr.action_type = 3
    )a group by artist_id, Ds order by artist_id, Ds, song_id;
    
#创建song_first_action
create table song_first_action as 
select * from mars_tianchi_songs song left outer join
(select song_id, min(Ds) as init_Ds from mars_tianchi_user_actions group by song_id) as
a on (song.song_id=a.song_id);

create table tmp as select song_id, min(Ds) as init_Ds from mars_tianchi_user_actions group by song_id;

create table song_first_action as 
select song.song_id,song.artist_id, song.publish_time,song.song_init_plays, Language,Gender, init_Ds
 from mars_tianchi_songs song left outer join tmp a on(song.song_id=a.song_id); 
 
select * from song_first_action limit 20;


##创建song_plays_perday
create table song_plays_perday as 
	select song_id, count(*) as plays, Ds from mars_tianchi_user_actions 
    where action_type = 1 group by song_id, Ds order by song_id, Ds;

##创建song_downloads_perday
create table song_downloads_perday as 
	select song_id, count(*) as downloads, Ds from mars_tianchi_user_actions 
    where action_type = 2 group by song_id, Ds order by song_id, Ds;
    
##创建song_favortites_perday
create table song_favorites_perday as 
	select song_id, count(*) as favorites, Ds from mars_tianchi_user_actions 
    where action_type = 3 group by song_id, Ds order by song_id, Ds;

#创建每首歌每天的信息表song_action_perday
create table song_action_perday as 
	select p.song_id,p.plays, d.downloads, f.favorites, p.Ds from song_plays_perday p  
    left outer join 
    (select d.song_id as song_id , downloads, favorites, d.Ds as Ds from song_downloads_perday d
    left outer join song_favorites_perday f
    on(d.song_id = f.song_id and d.Ds = f.Ds)
    )a on(p.song_id = a.song_id and p.Ds = a.Ds);

#创建song和Ds的直接特征表
create table song_ds_feature as
	select d.Ds as Ds, s.song_id, s.artist_id, s.publish_time, s.song_init_plays, 
    s.Language, s.Gender, d.plays from song_plays_perday d
    left outer join  mars_tianchi_songs s
    on(d.song_id=s.song_id) order by d.Ds, s.song_id;

use washed;
select * from song_ds_feature limit 2016;










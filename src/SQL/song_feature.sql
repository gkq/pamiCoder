show databases;
use tianchi;
show tables;
show table status;
show index from mars_tianchi_songs;

select * from mars_tianchi_songs group by artist_id limit 20;

select * from mars_tianchi_songs where publish_time>1980-0-0 order by publish_time ;

select artist_id, count(*) from mars_tianchi_songs group by artist_id;

select artist_id, count(song_id) from mars_tianchi_songs group by artist_id with rollup;


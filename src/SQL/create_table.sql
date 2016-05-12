  CREATE TABLE `tianchi`.`mars_tianchi_songs` (
  `song_id` CHAR(32) NOT NULL,
  `artist_id` CHAR(32) NULL,
  `publish_time` date NULL,
  `song_init_plays` INT(11) NULL,
  `Language` SMALLINT(11) NULL,
  `Gender` TINYINT(8) NULL,
   PRIMARY KEY(`song_id`));
   
CREATE TABLE `tianchi`.`mars_tianchi_user_actions` (
  #`id` INT NOT NULL AUTO_INCREMENT,
  `user_id` CHAR(32) NOT NULL,
  `song_id` CHAR(32) NULL,
  `gmt_create` int(11) NULL,
  `action_type` TINYINT(3) NULL,
  `Ds` DATE NULL);
  
  drop table mars_tianchi_user_actions;
  
  load data infile 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/mars_tianchi_user_actions.csv'
  into table mars_tianchi_user_actions
  fields terminated by ','
  optionally enclosed by '"'
  lines terminated by '\n';
  
  #SHOW VARIABLES LIKE 'secure_file_priv'
  
  load data infile 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/mars_tianchi_songs.csv'
  into table mars_tianchi_songs
  fields terminated by ','
  optionally enclosed by '"'
  lines terminated by '\n';
  

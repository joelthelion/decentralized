-- alter database prout default character set utf8;
create database prout character set utf8;
use prout;

create table if not exists kolmognus_user (
	id int primary key auto_increment,
	login varchar(30) unique,
	pass char(41) -- for md5 hash of the pass
);

create table if not exists story (
	id int primary key auto_increment,
	url text(32000),
	url_md5 char(32) unique, -- for the unique constraint, can't do on the full URL
	symbols text,
	fetch_date datetime,
	hit_count int, -- number of times a url was given in a feed
	rated_date datetime
);

create table if not exists feed (
	id int primary key auto_increment,
	url text(32000),
	url_md5 char(32) unique,
	fetch_date datetime,
	hit_count int
);

create table if not exists feed_story (
	story_id int,
	feed_id int,

	primary key (story_id,feed_id),
	foreign key (story_id)
	  references story(id),
	foreign key (feed_id)
	  references feed(id)
);

create table if not exists recommended_story (
	user_id int,
	story_id int,
	computed_rating float,
	user_rating enum('G','B','?'), -- Good, Bad or Unknown
	learned boolean,
	
	primary key (user_id,story_id),
	foreign key (user_id) 
	  references kolmognus_user(id),
	foreign key (story_id)
	  references story(id)
);

create table if not exists bayes_data ( -- this table is not needed per se, but still there for performance reasons
	user_id int,
	symbol varchar(255),
	good_count int,
	bad_count int,

	primary key (user_id,symbol)
);

-- Back-end stuff
create table if not exists service ( 
	name varchar(64) primary key,
	status varchar(512)
);
insert into service (name,status) values ('fetcher','db reset')
	on duplicate key update status='db reset';

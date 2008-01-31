create table if not exists service ( 
	name varchar(64) primary key,
	status varchar(512)
);
insert into service (name,status) values ('fetcher','db reset')
	on duplicate key update status='db reset';

create table if not exists kolmognus_user (
	login varchar(30) primary key,
	pass char(41)
);

create table if not exists cached_url (
	url_md5 char(32) primary key,
	symbols text(32000),
	fetchedi_count int(8)
);

create table if not exists incoming_url (
	url varchar(1000) primary key,
	symbols text(32000)
);

create table if not exists tag (
	name varchar(64) primary key,
	last_time_fetched date,
	fetched_count int(8)
);

create table if not exists recommended_urls (
	url varchar(1000),
	url_md5 char(32),
	login varchar(30),
	liked int(3),
	primary key (url_md5,login)
);

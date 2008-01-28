drop table users;
create table users (
	login varchar(30) primary key,
	pass char(41)
);

drop table url_cache;
create table url_cache (
	url_md5 char(32),
	url varchar(1024),
	symbols varchar(32000)
);

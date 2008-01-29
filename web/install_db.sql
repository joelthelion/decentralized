create table kolmognus_user (
	login varchar(30) primary key,
	pass char(41)
);

create table cached_url (
	url_md5 char(32) primary key,
	symbols text(32000),
	fetchedi_count int(8)
);

create table incoming_url (
	url varchar(1000) primary key,
	symbols text(32000)
);

create table tag (
	name varchar(64) primary key,
	last_time_fetched date,
	fetched_count int(8)
);

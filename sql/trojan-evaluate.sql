drop table if exists trojan;
create table trojan
(
id int,
name varchar(32),
url varchar(32),
grade int,
time varchar(10),
primary key(id)
);

alter table trojan add column type varchar(32);
update trojan set type = substr(name, 1, charindex('.', name)-1);

drop table if exists trojan_feature;
create table trojan_feature
(
id int,
name varchar(32),
url varchar(32),
type varchar(32),
grade int,
time varchar(10),
primary key(id)
);

/*
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '3' and type = 'Trojan-Clicker' order by random() limit 1;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '3' and type = 'Trojan-Downloader' order by random() limit 6;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '3' and type = 'Trojan-Dropper' order by random() limit 1;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '3' and type = 'Trojan-PSW' order by random() limit 1;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '3' and type = 'Trojan-Proxy' order by random() limit 0;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '3' and type = 'Trojan-Spy' order by random() limit 0;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '3' and type = 'Trojan' order by random() limit 1;

insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '2' and type = 'Trojan-Clicker' order by random() limit 1;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '2' and type = 'Trojan-Downloader' order by random() limit 15;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '2' and type = 'Trojan-Dropper' order by random() limit 3;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '2' and type = 'Trojan-PSW' order by random() limit 15;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '2' and type = 'Trojan-Proxy' order by random() limit 1;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '2' and type = 'Trojan-Spy' order by random() limit 2;
insert into trojan_feature select id, name, url, type, grade, time from trojan where grade = '2' and type = 'Trojan' order by random() limit 3;
*/
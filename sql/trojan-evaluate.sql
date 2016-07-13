drop table if exists trojan;
create table trojan
(
id int,
name varchar(32),
type varchar(32),
url varchar(32),
grade int,
time varchar(10),
primary key(id)
);

drop table if exists sample;
create table sample
(
id int,
name varchar(32),
type varchar(32),
url varchar(32),
grade int,
time varchar(10),
primary key(id)
);

/*
delete from sample;

insert into sample select id, name, type, url, grade, time from trojan where grade = '3' and type = 'adware' order by random()              limit 0;
insert into sample select id, name, type, url, grade, time from trojan where grade = '3' and type = 'backdoor' order by random()            limit 2;
insert into sample select id, name, type, url, grade, time from trojan where grade = '3' and type = 'exploit' order by random()             limit 1;
insert into sample select id, name, type, url, grade, time from trojan where grade = '3' and type = 'rootkit' order by random()             limit 0;
insert into sample select id, name, type, url, grade, time from trojan where grade = '3' and type = 'trojan-clicker' order by random()      limit 1;
insert into sample select id, name, type, url, grade, time from trojan where grade = '3' and type = 'trojan-downloader' order by random()   limit 3;
insert into sample select id, name, type, url, grade, time from trojan where grade = '3' and type = 'trojan-dropper' order by random()      limit 1;
insert into sample select id, name, type, url, grade, time from trojan where grade = '3' and type = 'trojan-psw' order by random()          limit 1;
insert into sample select id, name, type, url, grade, time from trojan where grade = '3' and type = 'trojan-proxy' order by random()        limit 0;
insert into sample select id, name, type, url, grade, time from trojan where grade = '3' and type = 'trojan-spy' order by random()          limit 0;
insert into sample select id, name, type, url, grade, time from trojan where grade = '3' and type = 'trojan' order by random()              limit 1;

insert into sample select id, name, type, url, grade, time from trojan where grade = '2' and type = 'adware' order by random()              limit 1;
insert into sample select id, name, type, url, grade, time from trojan where grade = '2' and type = 'backdoor' order by random()            limit 10;
insert into sample select id, name, type, url, grade, time from trojan where grade = '2' and type = 'exploit' order by random()             limit 0;
insert into sample select id, name, type, url, grade, time from trojan where grade = '2' and type = 'rootkit' order by random()             limit 1;
insert into sample select id, name, type, url, grade, time from trojan where grade = '2' and type = 'trojan-clicker' order by random()      limit 1;
insert into sample select id, name, type, url, grade, time from trojan where grade = '2' and type = 'trojan-downloader' order by random()   limit 9;
insert into sample select id, name, type, url, grade, time from trojan where grade = '2' and type = 'trojan-dropper' order by random()      limit 3;
insert into sample select id, name, type, url, grade, time from trojan where grade = '2' and type = 'trojan-psw' order by random()          limit 9;
insert into sample select id, name, type, url, grade, time from trojan where grade = '2' and type = 'trojan-proxy' order by random()        limit 1;
insert into sample select id, name, type, url, grade, time from trojan where grade = '2' and type = 'trojan-spy' order by random()          limit 2;
insert into sample select id, name, type, url, grade, time from trojan where grade = '2' and type = 'trojan' order by random()              limit 3;
*/

drop table if exists feature;
create table feature
(
name varchar(256),
lvl int,
val double,
primary key(name, lvl)
);
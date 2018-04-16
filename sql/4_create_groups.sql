use woodpecker;
drop table if exists t_groups;
create table t_groups (

　　id int auto_increment not null primary key comment '主键自增长',

    groupid varchar(20) not null comment '组号',

　　groupname varchar(20) not null comment '组名'); 
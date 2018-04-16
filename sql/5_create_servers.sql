use woodpecker;
drop table if exists t_servers;
create table t_servers (

　　id int auto_increment not null primary key comment '主键自增长',

    ip varchar(20) not null comment 'IP地址',
	
	businessname varchar(50) not null comment '业务名称',
	
	groupid varchar(20) not null comment '组编号',

    userid varchar(10) not null comment '用户编号',
	
	sysuser varchar(10) not null comment '系统用户',
	
	syspwd varchar(10) not null comment '系统密码');
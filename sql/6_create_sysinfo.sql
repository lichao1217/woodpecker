use woodpecker;
drop table if exists t_sysinfo;
create table t_sysinfo (

　　id int auto_increment not null primary key comment '主键自增长',

    serverip varchar(20) not null comment '服务器ip',
	
	cpustatus varchar(100) not null comment 'CPU状态',
	
	memstatus varchar(100) not null comment '内存状态',

    diskstatus varchar(200) not null comment '硬盘状态',
	
	recordtime datetime not null default CURRENT_TIMESTAMP comment '记录时间'); 
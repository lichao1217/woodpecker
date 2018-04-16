use woodpecker;
drop table if exists t_users;
create table t_users (

　　id int auto_increment not null primary key comment '主键自增长',

    userid varchar(10) not null comment '用户编号',
	
　　username varchar(10) not null comment '用户姓名',

　　pwd varchar(50) not null comment '用户密码',

　　regdate datetime not null default  CURRENT_TIMESTAMP comment '注册时间'); 
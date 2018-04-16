insert into t_users(userid,username,pwd) values ('1','admin','admin');
insert into t_users(userid,username,pwd) values ('2','test','test');
insert into t_users(userid,username,pwd) values ('3','test1','test1');

insert into t_groups(groupid,groupname) values ('1','第一分组');
insert into t_groups(groupid,groupname) values ('2','第二分组');

insert into t_servers(ip,businessname,groupid,userid,sysuser,syspwd) values ('192.168.42.60','业务系统1','1','2','root','Abcd1234');
insert into t_servers(ip,businessname,groupid,userid,sysuser,syspwd) values ('192.168.42.60','业务系统2','1','3','root','Abcd1234');
insert into t_servers(ip,businessname,groupid,userid,sysuser,syspwd) values ('192.168.42.60','业务系统3','1','2','root','Abcd1234');
insert into t_servers(ip,businessname,groupid,userid,sysuser,syspwd) values ('192.168.42.60','业务系统4','2','3','root','Abcd1234');
insert into t_servers(ip,businessname,groupid,userid,sysuser,syspwd) values ('192.168.42.60','业务系统5','2','2','root','Abcd1234');
insert into t_servers(ip,businessname,groupid,userid,sysuser,syspwd) values ('192.168.42.60','业务系统6','2','3','root','Abcd1234');
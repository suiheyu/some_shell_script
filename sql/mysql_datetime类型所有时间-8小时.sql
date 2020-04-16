drop PROCEDURE if EXISTS  transfer_zone;
DELIMITER $$
#创建存储过程
create PROCEDURE transfer_zone(in db_name varchar(30))
begin
## 变量
declare c_type varchar(30);
declare c_name varchar(30);
declare t_name varchar(30);
declare t_schema varchar(30);
declare flag int default 0;

DECLARE cur CURSOR FOR select column_name,column_type,table_name,table_schema from information_schema.`COLUMNS` where table_schema=db_name and column_type like 'datetime';

DECLARE CONTINUE HANDLER FOR NOT FOUND SET flag=1;

##打开游标
open cur;

	fetch cur into c_name,c_type,t_name,t_schema;
	set @update_sql_template = 'update $db.$tb set $cn=DATE_ADD($cn,interval -8 hour)';
	while flag<>1 do
		set @update_sql = replace(replace(replace(@update_sql_template,'$db',t_schema),'$tb',t_name),'$cn',c_name);
		select 'update',@update_sql;
    PREPARE stmt FROM @update_sql;  
    EXECUTE stmt;  
    deallocate prepare stmt;
		fetch cur into c_name,c_type,t_name,t_schema;
	end while;
	
##关闭游标
close cur;
end$$
DELIMITER ;

#----开启事务
start TRANSACTION;
#执行datetime类型转换存储过程
call transfer_zone('icp_vod');
COMMIT;
#-----事务结束提交

#删除存储过程
drop PROCEDURE if EXISTS  transfer_zone;
# sql_command

## 一、basic use

### 1.1 about database 

#### 1.1.1 login
本地登录：
```console
PS D:\projects\gits\pylearning_github> mysql -uroot -p
Enter password: ****
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.32 MySQL Community Server - GPL

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```
远程登录：
```console
C:\>mysql -h 192.168.0.201 -P 3306 -u root -p123
 
指定端口的P要大写，后面指定使用密码的p是小写：
mysql -h ip -P port -uroot -p

```

#### 1.1.2 show database current use
```console
mysql> select database();
+------------+
| database() |
+------------+
| NULL       |
+------------+
1 row in set (0.01 sec)

mysql> use mysql_crash;
Database changed
mysql> select database();
+-------------+
| database()  |
+-------------+
| mysql_crash |
+-------------+
1 row in set (0.00 sec)

```

#### 1.1.3 show all databases
```console
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| mysql_crash        |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.01 sec)
```

#### 1.1.4 create database
```console
mysql> create database if not exists tmp_db;
Query OK, 1 row affected (0.01 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| mysql_crash        |
| performance_schema |
| sys                |
| tmp_db             |
+--------------------+
6 rows in set (0.00 sec)
```

#### 1.1.5 drop database
```console
mysql> drop database tmp_db;
Query OK, 0 rows affected (0.02 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| mysql_crash        |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

#### 1.1.6 import sql file(source command)
```console
PS D:\projects\gits\pylearning_github> cd .\src\demo2023\mysql_db\
PS D:\projects\gits\pylearning_github\src\demo2023\mysql_db> mysql -uroot -p
Enter password: ****
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 8.0.32 MySQL Community Server - GPL

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> create database if not exists tmp_db;
Query OK, 1 row affected (0.01 sec)

mysql> use tmp_db;
Database changed
mysql> source create.sql;
Query OK, 0 rows affected (0.02 sec)
Query OK, 0 rows affected (0.01 sec)
Query OK, 0 rows affected (0.01 sec)
Query OK, 0 rows affected (0.01 sec)
Query OK, 0 rows affected (0.01 sec)
Query OK, 0 rows affected (0.00 sec)
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

#### 1.1.7 show create database
```console
mysql> show create database tmp_db;
+----------+----------------------------------------------------------------------------------------------------------------------------------+
| Database | Create Database                                                                                                                  |
+----------+----------------------------------------------------------------------------------------------------------------------------------+
| tmp_db   | CREATE DATABASE `tmp_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */ |
+----------+----------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

#### 1.1.8 export sql
```console
PS D:\projects\gits\pylearning_github\src\demo2023\mysql_db> mysqldump -uroot -p tmp_db > D:\tmp_db.sql
Enter password: ****
PS D:\projects\gits\pylearning_github\src\demo2023\mysql_db>
```

### 1.2 about tables

#### 1.2.1 show all tables in selected database
```console
mysql> show tables;
+-----------------------+
| Tables_in_mysql_crash |
+-----------------------+
| customers             |
| orderitems            |
| orders                |
| productnotes          |
| products              |
| vendors               |
+-----------------------+
6 rows in set (0.01 sec)
```

#### 1.2.2 create table
```console
mysql> create table if not exists del_table(
    ->    id int auto_increment,
    ->    name varchar(50) not null,
    ->    age int not null,
    ->    primary key(id)
    ->    );
Query OK, 0 rows affected (0.03 sec)
```

#### 1.2.3 drop table / drop tables
```console
mysql> drop table del_table;
Query OK, 0 rows affected (0.02 sec)

mysql> drop tables customers,orderitems;
ERROR 3730 (HY000): Cannot drop table 'customers' referenced by a foreign key constraint 'fk_orders_customers' on table 'orders'.

mysql> drop tables orders,customers,orderitems;
Query OK, 0 rows affected (0.02 sec)
```

#### 1.2.4 rename table
```console
mysql> show tables;
+------------------+
| Tables_in_tmp_db |
+------------------+
| customers        |
| orderitems       |
| orders           |
| productnotes     |
| products         |
| vendors          |
+------------------+
6 rows in set (0.00 sec)

mysql> rename table orders to new_orders;
Query OK, 0 rows affected (0.02 sec)

mysql> show tables;
+------------------+
| Tables_in_tmp_db |
+------------------+
| customers        |
| new_orders       |
| orderitems       |
| productnotes     |
| products         |
| vendors          |
+------------------+
6 rows in set (0.00 sec)
```

#### 1.2.5 show columns from table / desc table
desc 表示 description 也就是 对表的描述，这个命令会用一个表格描述一个数据表，而你的数据表的特征就是数据表的列名，所以用来描述的表格里面也会显示列名。
show columns from table 就是一段最简单的直译命令，就是说显示表的所有列名，
它们代表的含义是完全不同的，但是显示结果是相同的
```console
mysql> show columns from orders;
+------------+----------+------+-----+---------+----------------+
| Field      | Type     | Null | Key | Default | Extra          |
+------------+----------+------+-----+---------+----------------+
| order_num  | int      | NO   | PRI | NULL    | auto_increment |
| order_date | datetime | NO   |     | NULL    |                |
| cust_id    | int      | NO   | MUL | NULL    |                |
+------------+----------+------+-----+---------+----------------+
3 rows in set (0.01 sec)
mysql> desc orders;
+------------+----------+------+-----+---------+----------------+
| Field      | Type     | Null | Key | Default | Extra          |
+------------+----------+------+-----+---------+----------------+
| order_num  | int      | NO   | PRI | NULL    | auto_increment |
| order_date | datetime | NO   |     | NULL    |                |
| cust_id    | int      | NO   | MUL | NULL    |                |
+------------+----------+------+-----+---------+----------------+
3 rows in set (0.01 sec)
```

### 1.3 select
```console
select * from tmp_table order by name;
select * from tmp_table order by name,age;
select id,name,sex,age from tmp_table order by name desc;
select id,name,sex,age from tmp_table order by age desc limit 1;
select id,name,sex,age from tmp_table where age between 1 and 5;
select id,name,sex,age from tmp_table where name is null;
select * from tmp_table where age > 0;
select * from tmp_table where age < 18;
select * from tmp_table where age >= 12;
select * from tmp_table where id = 1;
select * from tmp_table where id > 1;
select id,name,sex,age from tmp_table where name like "%dc%";
select id,name,sex,age from tmp_table where name regexp ".000";
select id,name,sex,age from tmp_table where name regexp "dc|sen";
select Concat(name, "(", age, ")") as new_name,id from tmp_table order by name;
select prod_id,prod_price,prod_name from products order by prod_price desc,prod_name;
```

```console
mysql> select * from orders order by cust_id asc;
+-----------+---------------------+---------+
| order_num | order_date          | cust_id |
+-----------+---------------------+---------+
|     20005 | 2005-09-01 00:00:00 |   10001 |
|     20009 | 2005-10-08 00:00:00 |   10001 |
|     20006 | 2005-09-12 00:00:00 |   10003 |
|     20007 | 2005-09-30 00:00:00 |   10004 |
|     20008 | 2005-10-03 00:00:00 |   10005 |
+-----------+---------------------+---------+
5 rows in set (0.00 sec)
```

```console
获取最高或最低：order by和limit组合
//降序第一个就是最大值
select prod_id,prod_price,prod_name from products order by prod_price desc limit 1;
//升序第一个就是最小值
select prod_id,prod_price,prod_name from products order by prod_price asc limit 1;   
```

```console
select distinct cust_zip from customers;
select distinct cust_name,cust_zip from customers;
```
获取并列倒数第一：
```console
mysql> select cust_id,cust_name,cust_zip from customers where cust_zip=(select MIN(cust_zip) from customers);
+---------+-----------+----------+
| cust_id | cust_name | cust_zip |
+---------+-----------+----------+
|   10006 | wdc       | 111      |
|   10007 | tonsen    | 111      |
+---------+-----------+----------+
2 rows in set (0.00 sec)
```
获取并列第一：
```console
mysql> select cust_id,cust_name,cust_zip from customers where cust_zip=(select MAX(cust_zip) from customers);
+---------+----------------+----------+
| cust_id | cust_name      | cust_zip |
+---------+----------------+----------+
|   10004 | Yosemite Place | 88888    |
+---------+----------------+----------+
1 row in set (0.00 sec)
```

### 1.4 insert 

#### 1.4.1 Inset into 表名(字段1,字段2) values(值1,值2)
```console+
insert into customers(cust_name,cust_zip) value(“wdc”,111);
insert into customers(cust_name,cust_zip) value("tonsen",111);

mysql> select distinct cust_name,cust_zip from customers;  # 选择多个列时，去除重复仅在选择的列内容都相同时
+----------------+----------+
| cust_name      | cust_zip |
+----------------+----------+
| Coyote Inc.    | 44444    |
| Mouse House    | 43333    |
| Wascals        | 42222    |
| Yosemite Place | 88888    |
| E Fudd         | 54545    |
| wdc            | 111      |
| tonsen         | 111      |
+----------------+----------+
7 rows in set (0.00 sec)
```

### 1.5 update
```console
insert into customers(cust_name,cust_zip) value("test",111);
mysql> update customers set cust_name="test01" where cust_name="test" and cust_zip=111;
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> select distinct cust_name,cust_zip from customers;
+----------------+----------+
| cust_name      | cust_zip |
+----------------+----------+
| Coyote Inc.    | 44444    |
| Mouse House    | 43333    |
| Wascals        | 42222    |
| Yosemite Place | 88888    |
| E Fudd         | 54545    |
| wdc            | 111      |
| tonsen         | 111      |
| test01         | 111      |
+----------------+----------+
8 rows in set (0.00 sec)
```

### 1.6 delete
```console
mysql> insert into customers(cust_name,cust_zip) value("to_be_del",111);
Query OK, 1 row affected (0.01 sec)

mysql> select distinct cust_name,cust_zip from customers;
+----------------+----------+
| cust_name      | cust_zip |
+----------------+----------+
| Coyote Inc.    | 44444    |
| Mouse House    | 43333    |
| Wascals        | 42222    |
| Yosemite Place | 88888    |
| E Fudd         | 54545    |
| wdc            | 111      |
| tonsen         | 111      |
| test01         | 111      |
| to_be_del      | 111      |
+----------------+----------+
9 rows in set (0.00 sec)

mysql> delete from customers where cust_name = "to_be_del";
Query OK, 1 row affected (0.01 sec)

mysql> select distinct cust_name,cust_zip from customers;
+----------------+----------+
| cust_name      | cust_zip |
+----------------+----------+
| Coyote Inc.    | 44444    |
| Mouse House    | 43333    |
| Wascals        | 42222    |
| Yosemite Place | 88888    |
| E Fudd         | 54545    |
| wdc            | 111      |
| tonsen         | 111      |
| test01         | 111      |
+----------------+----------+
8 rows in set (0.00 sec)
```

```console
DELETE FROM syslogs WHERE status=1 ORDER BY statusid LIMIT 10000;
```

### 1.7 联结

#### 1.7.1 select [需要的列，可不同表] from [所有需要查询的表] [条件] [排序]
```console
mysql> select vend_name, prod_name, prod_price from vendors, products where vendors.vend_id = products.vend_id order by vend_name,prod_name;
+-------------+----------------+------------+
| vend_name   | prod_name      | prod_price |
+-------------+----------------+------------+
| ACME        | Bird seed      |      10.00 |
| ACME        | Carrots        |       2.50 |
| ACME        | Detonator      |      13.00 |
| ACME        | Safe           |      50.00 |
| ACME        | Sling          |       4.49 |
| ACME        | TNT (1 stick)  |       2.50 |
| ACME        | TNT (5 sticks) |      10.00 |
| Anvils R Us | .5 ton anvil   |       5.99 |
| Anvils R Us | 1 ton anvil    |       9.99 |
| Anvils R Us | 2 ton anvil    |      14.99 |
| Jet Set     | JetPack 1000   |      35.00 |
| Jet Set     | JetPack 2000   |      55.00 |
| LT Supplies | Fuses          |       3.42 |
| LT Supplies | Oil can        |       8.99 |
+-------------+----------------+------------+
14 rows in set (0.01 sec)
```

#### 1.7.2 笛卡尔积 一般是错误的返回 
```console
mysql> select vend_name,prod_name, prod_price from vendors,products order by vend_name,prod_name;
+----------------+----------------+------------+
| vend_name      | prod_name      | prod_price |
+----------------+----------------+------------+
| ACME           | .5 ton anvil   |       5.99 |
| ACME           | 1 ton anvil    |       9.99 |
| ACME           | 2 ton anvil    |      14.99 |
| ACME           | Bird seed      |      10.00 |
| ACME           | Carrots        |       2.50 |
| ACME           | Detonator      |      13.00 |
| ACME           | Fuses          |       3.42 |
| ACME           | JetPack 1000   |      35.00 |
| ACME           | JetPack 2000   |      55.00 |
| ACME           | Oil can        |       8.99 |
| ACME           | Safe           |      50.00 |
| ACME           | Sling          |       4.49 |
| ACME           | TNT (1 stick)  |       2.50 |
| ACME           | TNT (5 sticks) |      10.00 |
| Anvils R Us    | .5 ton anvil   |       5.99 |
| Anvils R Us    | 1 ton anvil    |       9.99 |
| Anvils R Us    | 2 ton anvil    |      14.99 |
| Anvils R Us    | Bird seed      |      10.00 |
| Anvils R Us    | Carrots        |       2.50 |
| Anvils R Us    | Detonator      |      13.00 |
| Anvils R Us    | Fuses          |       3.42 |
| Anvils R Us    | JetPack 1000   |      35.00 |
| Anvils R Us    | JetPack 2000   |      55.00 |
| Anvils R Us    | Oil can        |       8.99 |
| Anvils R Us    | Safe           |      50.00 |
| Anvils R Us    | Sling          |       4.49 |
| Anvils R Us    | TNT (1 stick)  |       2.50 |
| Anvils R Us    | TNT (5 sticks) |      10.00 |
| Furball Inc.   | .5 ton anvil   |       5.99 |
| Furball Inc.   | 1 ton anvil    |       9.99 |
| Furball Inc.   | 2 ton anvil    |      14.99 |
| Furball Inc.   | Bird seed      |      10.00 |
| Furball Inc.   | Carrots        |       2.50 |
| Furball Inc.   | Detonator      |      13.00 |
| Furball Inc.   | Fuses          |       3.42 |
| Furball Inc.   | JetPack 1000   |      35.00 |
| Furball Inc.   | JetPack 2000   |      55.00 |
| Furball Inc.   | Oil can        |       8.99 |
| Furball Inc.   | Safe           |      50.00 |
| Furball Inc.   | Sling          |       4.49 |
| Furball Inc.   | TNT (1 stick)  |       2.50 |
| Furball Inc.   | TNT (5 sticks) |      10.00 |
| Jet Set        | .5 ton anvil   |       5.99 |
| Jet Set        | 1 ton anvil    |       9.99 |
| Jet Set        | 2 ton anvil    |      14.99 |
| Jet Set        | Bird seed      |      10.00 |
| Jet Set        | Carrots        |       2.50 |
| Jet Set        | Detonator      |      13.00 |
| Jet Set        | Fuses          |       3.42 |
| Jet Set        | JetPack 1000   |      35.00 |
| Jet Set        | JetPack 2000   |      55.00 |
| Jet Set        | Oil can        |       8.99 |
| Jet Set        | Safe           |      50.00 |
| Jet Set        | Sling          |       4.49 |
| Jet Set        | TNT (1 stick)  |       2.50 |
| Jet Set        | TNT (5 sticks) |      10.00 |
| Jouets Et Ours | .5 ton anvil   |       5.99 |
| Jouets Et Ours | 1 ton anvil    |       9.99 |
| Jouets Et Ours | 2 ton anvil    |      14.99 |
| Jouets Et Ours | Bird seed      |      10.00 |
| Jouets Et Ours | Carrots        |       2.50 |
| Jouets Et Ours | Detonator      |      13.00 |
| Jouets Et Ours | Fuses          |       3.42 |
| Jouets Et Ours | JetPack 1000   |      35.00 |
| Jouets Et Ours | JetPack 2000   |      55.00 |
| Jouets Et Ours | Oil can        |       8.99 |
| Jouets Et Ours | Safe           |      50.00 |
| Jouets Et Ours | Sling          |       4.49 |
| Jouets Et Ours | TNT (1 stick)  |       2.50 |
| Jouets Et Ours | TNT (5 sticks) |      10.00 |
| LT Supplies    | .5 ton anvil   |       5.99 |
| LT Supplies    | 1 ton anvil    |       9.99 |
| LT Supplies    | 2 ton anvil    |      14.99 |
| LT Supplies    | Bird seed      |      10.00 |
| LT Supplies    | Carrots        |       2.50 |
| LT Supplies    | Detonator      |      13.00 |
| LT Supplies    | Fuses          |       3.42 |
| LT Supplies    | JetPack 1000   |      35.00 |
| LT Supplies    | JetPack 2000   |      55.00 |
| LT Supplies    | Oil can        |       8.99 |
| LT Supplies    | Safe           |      50.00 |
| LT Supplies    | Sling          |       4.49 |
| LT Supplies    | TNT (1 stick)  |       2.50 |
| LT Supplies    | TNT (5 sticks) |      10.00 |
+----------------+----------------+------------+
84 rows in set (0.00 sec)
```

#### 1.7.3 INNER JOIN ON  内联结
```console
mysql> select vend_name,prod_name,prod_price from vendors inner join products on vendors.vend_id=products.vend_id;
+-------------+----------------+------------+
| vend_name   | prod_name      | prod_price |
+-------------+----------------+------------+
| Anvils R Us | .5 ton anvil   |       5.99 |
| Anvils R Us | 1 ton anvil    |       9.99 |
| Anvils R Us | 2 ton anvil    |      14.99 |
| LT Supplies | Fuses          |       3.42 |
| LT Supplies | Oil can        |       8.99 |
| ACME        | Detonator      |      13.00 |
| ACME        | Bird seed      |      10.00 |
| ACME        | Carrots        |       2.50 |
| ACME        | Safe           |      50.00 |
| ACME        | Sling          |       4.49 |
| ACME        | TNT (1 stick)  |       2.50 |
| ACME        | TNT (5 sticks) |      10.00 |
| Jet Set     | JetPack 1000   |      35.00 |
| Jet Set     | JetPack 2000   |      55.00 |
+-------------+----------------+------------+
14 rows in set (0.00 sec)
```

#### 1.7.4 left join on
左边内容全列出来，右边没有对应,则为NULL
```console
mysql> select vend_name,prod_name,prod_price from vendors left join products on vendors.vend_id=products.vend_id;
+----------------+----------------+------------+
| vend_name      | prod_name      | prod_price |
+----------------+----------------+------------+
| Anvils R Us    | .5 ton anvil   |       5.99 |
| Anvils R Us    | 1 ton anvil    |       9.99 |
| Anvils R Us    | 2 ton anvil    |      14.99 |
| LT Supplies    | Fuses          |       3.42 |
| LT Supplies    | Oil can        |       8.99 |
| ACME           | Detonator      |      13.00 |
| ACME           | Bird seed      |      10.00 |
| ACME           | Carrots        |       2.50 |
| ACME           | Safe           |      50.00 |
| ACME           | Sling          |       4.49 |
| ACME           | TNT (1 stick)  |       2.50 |
| ACME           | TNT (5 sticks) |      10.00 |
| Furball Inc.   | NULL           |       NULL |
| Jet Set        | JetPack 1000   |      35.00 |
| Jet Set        | JetPack 2000   |      55.00 |
| Jouets Et Ours | NULL           |       NULL |
+----------------+----------------+------------+
16 rows in set (0.00 sec)
```

#### 1.7.5 right join on
右边内容全列出来，左边没有对应,则为NULL
```console
mysql> select vend_name,prod_name,prod_price from vendors right join products on vendors.vend_id=products.vend_id;
+-------------+----------------+------------+
| vend_name   | prod_name      | prod_price |
+-------------+----------------+------------+
| Anvils R Us | .5 ton anvil   |       5.99 |
| Anvils R Us | 1 ton anvil    |       9.99 |
| Anvils R Us | 2 ton anvil    |      14.99 |
| ACME        | Detonator      |      13.00 |
| ACME        | Bird seed      |      10.00 |
| ACME        | Carrots        |       2.50 |
| LT Supplies | Fuses          |       3.42 |
| Jet Set     | JetPack 1000   |      35.00 |
| Jet Set     | JetPack 2000   |      55.00 |
| LT Supplies | Oil can        |       8.99 |
| ACME        | Safe           |      50.00 |
| ACME        | Sling          |       4.49 |
| ACME        | TNT (1 stick)  |       2.50 |
| ACME        | TNT (5 sticks) |      10.00 |
+-------------+----------------+------------+
14 rows in set (0.00 sec)
```

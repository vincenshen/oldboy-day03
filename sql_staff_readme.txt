# Readme

## 关于作者
* Vincen Shen(Python菜鸟一枚)
* 博客地址http://www.cnblogs.com/vincenshen/

## 功能特性
* 支持SQL语句实现staff数据增删改查

## 使用方法及注意事项
### 运行环境
* 该程序使用python3版本编写,不兼容python2版本
* 该程序使用了第三方库prettytable,运行程序前需要安装该库
### 使用方法
    支持的SQL语法示例如下:
	* 查询: select staff_id,name,age from staff_table where age > 22
                select * from staff_table where enroll_date like "2017"
                select * from staff_table where name = "沈洪斌"
	* 修改: update staff_table set dept="IT" where name = "沈洪斌"
        * 新增: insert into staff_table values ("Alex",33,13812345678,"讲师",2010-01-01)
        * 删除: delete from staff_table where staff_id = 4

## 注意事项
* 无

## 更新日志
* 2017.2.6 1.0 版本
* 2017.2.8 1.1 版本
	增加prettytable库，使打印效果更美观

## License
* 本软件遵循GPL协议
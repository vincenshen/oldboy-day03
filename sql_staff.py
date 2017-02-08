import re,sys,os
from prettytable import PrettyTable

class SQL_Staff(object):

    def __init__(self, *args):
        self.staff_list = []
        self.staff_list2 = []
        self.staff_count = 0
        self.staff_id = 0
        self.syntax = self.syntax_check(args[0])   # 语法检查

    def select(self):
        staffs_info = self.__data_read(self.syntax[3])  # 获取staff数据列表
        field_names = self.syntax[1].split(",")
        for staff in staffs_info:
            self.staff_list = []
            staff_dict = self.data_process(staff)   # 获取staff数据字典
            if self.where_check(self.syntax,staff_dict):    # Where条件判断
                for field in field_names:
                    self.staff_list.append(staff_dict.get(field))
                self.staff_list2.append(self.staff_list)
                self.staff_count += 1
        self.pt_staff_data(field_names,self.staff_list2)    # 打印查询到的staff信息
        print("总共查找到%d条记录!" %self.staff_count)

    def update(self):
        staffs_info = self.__data_read(self.syntax[1])  # 获取staff数据列表
        for staff in staffs_info:
            staff_dict = self.data_process(staff)    # 获取staff数据字典
            if self.where_check(self.syntax,staff_dict):    # Where条件判断
                update_set = self.syntax[3].split("=")
                if "\"" in update_set[1]:
                    staff_dict[update_set[0]] = update_set[1][1:-1]
                else:
                    staff_dict[update_set[0]] = update_set[1]
                self.staff_count += 1
            self.staff_list.append(self.staff_info_str(staff_dict))  # 将字典转换为字符串
        self.__data_write(self.syntax[1],self.staff_list)   # 数据写回文件
        print("操作成功,总共更新%d条记录!" %self.staff_count)

    def delete(self):
        staff_info = self.__data_read(self.syntax[2])   #获取staff数据列表
        for staff in staff_info:
            self.staff_id += 1
            staff_dict = self.data_process(staff)   # 获取staff数据字典
            if self.where_check(self.syntax,staff_dict):    # 判断语法结构
                self.staff_count += 1
                self.staff_id -= 1
                continue
            else:
                staff_dict['staff_id'] = str(self.staff_id)  # 更新staff_id
                self.staff_list.append(self.staff_info_str(staff_dict))  # 将字典转换为字符串
        self.__data_write(self.syntax[2],self.staff_list)   # 数据写回文件
        print("操作成功,总共删除%d条记录!" %self.staff_count)

    def insert(self):
        staff_info = self.__data_read(self.syntax[2])   # 获取staff数据列表
        staff_values = re.split(r',',self.syntax[4])
        for i in range(len(staff_values)):  # 去掉引号
            if "\"" in staff_values[i]:
                staff_values[i] = staff_values[i].strip("\"")
        for staff in staff_info:
            staff_dict = self.data_process(staff)   # 获取staff数据字典
            if staff_values[2] in staff:
                print("Staff Phone已存在，不允许重复值!")
                return
            else:
                self.staff_list.append(self.staff_info_str(staff_dict))  # 将字典转换为字符串
        self.staff_list.append(",".join([str(len(staff_info)+1),staff_values[0],staff_values[1],staff_values[2],staff_values[3],staff_values[4]]))   # 将新增staff数据放到列表最后
        self.__data_write(self.syntax[2],self.staff_list)   # 数据写回文件
        print("成功插入1条记录!")

    def __data_read(self,file_name):  # 读取文件内容,返回列表
            staff_info = []
            with open(file_name,"r",encoding="utf-8") as f:
                for line in f.readlines():
                    staff_info.append(line.strip())
            return staff_info

    def __data_write(self,file_name,staff_info):   # 将列表转换为字符串，并写入文件
        staff_str = ""
        with open(file_name,"w",encoding="utf-8") as f:
            for line in staff_info:
                staff_str += str(line) + "\n"
            f.write(staff_str)

    def data_process(self,data):    # 将staff数据转换为字典
        student_info = data.split(',')
        staff_dict = {'staff_id': student_info[0], 'name': student_info[1], 'age': student_info[2],
                      'phone': student_info[3], 'dept': student_info[4], 'enroll_date': student_info[5]}
        return staff_dict

    def pt_staff_data(self,fields_names,staff_data):    # 格式化打印
        pt_info = PrettyTable()
        pt_info.field_names = fields_names
        for staff in staff_data:
            pt_info.add_row(staff)
        print(pt_info)

    def syntax_check(self,syntax):  # 检查语法结构,并做相应的转换
        if (syntax[2].lower() == "from" or syntax[2].lower() == "set")\
                and syntax[4].lower() == "where" and len(syntax) == 8:
            if "\"" in syntax[7]:
                syntax[7] = syntax[7][1:-1]
            if syntax[1] == "*":
                syntax[1] = "staff_id,name,age,phone,dept,enroll_date"
            return syntax
        elif syntax[1].lower() == "from" and syntax[3].lower() == "where" and len(syntax) == 7:
            if "\"" in syntax[6]:
                syntax[6] = syntax[6][1:-1]
            return syntax
        elif syntax[1].lower() == "into" and syntax[3].lower() == "values":
            syntax[4] = syntax[4][1:-1]
            return syntax
        else:
            sys.exit("语句错误,请重试!")

    def where_check(self,syntax,staff_dict):   # 判断where条件是否成立
        try:
            if len(syntax) == 8 and ((syntax[6] == "like" and ((syntax[7]) in staff_dict[syntax[5]])) or \
                    (syntax[6] == "=" and syntax[7] == staff_dict[syntax[5]]) or \
                    ((syntax[6] not in ["=", "like"]) and eval(staff_dict[syntax[5]] + syntax[6] + syntax[7]))):
                return True
            if len(syntax) == 7 and ((syntax[5] == "like" and ((syntax[6]) in staff_dict[syntax[4]])) or \
                        (syntax[5] == "=" and syntax[6] == staff_dict[syntax[4]]) or \
                        ((syntax[5] not in ["=","like"]) and eval(staff_dict[syntax[4]]+syntax[5]+syntax[6]))):
                return True
        except Exception as e:
            sys.exit("字段名错误，请重新输入!!!")

    def staff_info_str(self,staff_dict):    # 将字典转换为字符串
        staff_info= [staff_dict['staff_id'], staff_dict['name'], staff_dict['age'],staff_dict['phone'], staff_dict['dept'],staff_dict['enroll_date']]
        return ",".join(staff_info)

if os.path.isfile("staff_table") == False:
    staff_lists = [
        "1,李啸宇,22,13564081679,运维,2017-01-01",
        "2,高君,29,13911523752,IT,2014-08-02",
        "3,徐鹏,25,13811436953,运维,2015-01-01",
        "4,王耀华,77,13461044075,实习生,1937-01-21",
        "5,李家旺,69,17191195862,实习生,2017-01-21",
        "6,李西昌,27,17733786749,运维,2017-01-21",
        "7,李梦林,26,15910631989,QA,2016-10-11",
        "8,朱世阳,24,17744498194,运维,2017-01-07",
        "9,范洪涛,22,18611044558,运维,2017-01-01",
        "10,沈洪斌,29,18518740102,运维,2016-10-12",
        "11,李向阳,24,13622004447,运维,2017-01-01",
        "12,曲喆,42,18911324106,DBA,2017-01-20",
        "13,郭奇锋,26,18211144618,自动化测试,2017-01-15",
        "14,邱峰,30,18910627886,运维,2000-01-01",
        "15,贺磊,30,18500644534,开发,1998-07-01"
    ]
    staff_str = ""
    with open("staff_table", "w", encoding="utf-8") as f:
        for line in staff_lists:
            staff_str += str(line) + "\n"
        f.write(staff_str)

if __name__ == '__main__':
    sql_doc = '''
    支持的SQL语法示例如下:
        * 查询: select staff_id,name,age from staff_table where age > 22
                select * from staff_table where enroll_date like "2017"
                select * from staff_table where name = "沈洪斌"
        * 修改: update staff_table set dept="IT" where name = "沈洪斌"
        * 新增: insert into staff_table values ("Alex",33,13812345678,"讲师",2010-01-01)
        * 删除: delete from staff_table where staff_id = 4
    '''
    print(sql_doc)
    while True:
        sql_input = input("Please input SQL or Quit to exit >>>").strip()
        if len(sql_input) == 0:
            continue
        elif sql_input == "exit()":
            sys.exit("Bye!")
        try:
            sql_list = re.split(r'\s+',sql_input)
            sql_func = SQL_Staff(sql_list)
            getattr(sql_func,sql_list[0].lower())()
        except AttributeError as e:
            print("语句错误，请重新输入!!")
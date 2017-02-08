import re,sys,os

class Selected(object):

    def select(self,*args):
        syntax = self.syntax_check(args[0])   #调用syntax_check方法检查语法
        if syntax == 0:return
        staff_info = self.data_read(syntax[3])  #调用data_read方法获取staff数据列表
        self.print_column(syntax[1].split(","))   #调用print_column方法打印字段
        count = 0
        for i in staff_info:
            staff_dict = self.data_process(i)   #调用data_process方法获取staff数据字典
            if self.syntax_determine(syntax,staff_dict):    #调用syntax_determine方法判断语法结构
                if self.print_data(syntax[1].split(","), staff_dict):   #调用print_data方法打印记录
                    count +=1
                else:
                    return

        print("总共查找到%d条记录" %count)

    def update(self,*args):
        syntax = self.syntax_check(args[0])   #调用syntax_check方法检查语法
        if syntax == 0: return
        staff_info = self.data_read(syntax[1])   #调用data_read方法获取staff数据列表
        staff_info_new = []
        count = 0
        for i in staff_info:
            staff_dict = self.data_process(i)    #调用data_process方法获取staff数据字典
            if self.syntax_determine(syntax,staff_dict):    #调用syntax_determine方法判断语法结构
                update_set = syntax[3].split("=")   #将update set内容分割
                if "\"" in update_set[1]:
                    staff_dict[update_set[0]] = update_set[1][1:-1]   #去掉值的双引号
                else:
                    staff_dict[update_set[0]] = update_set[1]
                count +=1
            staff_info_new.append(self.staff_info_str(staff_dict))  #调用staff_info_str方法将字典转换为一个字符串
        self.data_write(syntax[1],staff_info_new)   #调用data_write方法写入修改后的数据
        print("总共更新%d条记录" %count)

    def delete(self,*args):
        syntax = self.syntax_check(args[0])   #调用syntax_check方法检查语法
        if syntax == 0: return
        staff_info = self.data_read(syntax[2])   #调用data_read方法获取staff数据列表
        staff_info_new = []
        count = 0
        staff_id = 0    #定义staff_id，以便在delete数据后重新生成staff_id
        for i in staff_info:
            staff_id +=1
            staff_dict = self.data_process(i)   #调用data_process方法获取staff数据字典
            if self.syntax_determine(syntax,staff_dict):    #调用syntax_determine方法判断语法结构
                count +=1
                staff_id -=1
                continue
            else:
                staff_dict['staff_id'] = str(staff_id)  #更新staff_id
                staff_info_new.append(self.staff_info_str(staff_dict))  #调用staff_info_str方法将字典转换为一个字符串
        self.data_write(syntax[2],staff_info_new)   #调用data_write方法写入修改后的数据
        print("总共删除%d条记录" %count)

    def insert(self,*args):
        syntax = self.syntax_check(args[0])   #调用syntax_check方法检查语法
        if syntax == 0:return
        staff_info = self.data_read(syntax[2])   #调用data_read方法获取staff数据列表
        staff_values = re.split(r',',syntax[4])   #将需要插入的staff数据分割为列表
        for i in range(len(staff_values)):  #去掉引号
            if "\"" in staff_values[i]:
                staff_values[i] = staff_values[i].strip("\"")
        staff_info_new = []
        for i in staff_info:
            staff_dict = self.data_process(i)   #调用data_process方法获取staff数据字典
            if staff_values[2] in i:
                print("Staff_phone已存在，不允许重复值!")
                return
            else:
                staff_info_new.append(self.staff_info_str(staff_dict))  #调用staff_info_str方法将字典转换为一个字符串
        staff_info_new.append(",".join([str(len(staff_info)+1),staff_values[0],staff_values[1],staff_values[2],staff_values[3],staff_values[4]]))   #将需要插入的staff数据放到列表最后
        self.data_write(syntax[2],staff_info_new)   #调用data_write方法写入修改后的数据

    def data_read(self,file_name):  #读取文件的内容并返回一个列表
        staff_info = []
        with open(file_name,"r",encoding="utf-8") as f:
            for line in f.readlines():
                staff_info.append(line.strip())
        return staff_info

    def data_write(self,file_name,staff_info):   #将列表转换为字符串，并写入文件中
        staff_str = ""
        with open(file_name,"w",encoding="utf-8") as f:
            for line in staff_info:
                staff_str += str(line) + "\n"
            f.write(staff_str)
            print("Success")

    def data_process(self,data):    #将staff数据转换为字典
        student_info = data.split(',')
        staff_dict = {'staff_id': student_info[0], 'name': student_info[1], 'age': student_info[2],
                      'phone': student_info[3], 'dept': student_info[4], 'enroll_date': student_info[5]}
        return staff_dict

    def print_column(self,column):  #打印字段
        for i in column:
            print(i,end='\t')
        print('\r')

    def print_data(self,data,data2):    #打印数据
        try:
            for i in data:
                print(data2[i],end='\t')
            print('\r')
            return True
        except Exception as e:
            print("要查询的字段不存在！")
            return False

    def syntax_check(self,syntax):  #检查语法结构，并做相应的转换
        try:
            if (syntax[2].lower() == "from" or syntax[2].lower() == "set") and syntax[4].lower() == "where" and len(syntax) == 8:
                if "\"" in syntax[7]:syntax[7] = syntax[7][1:-1]
                if syntax[1] == "*":syntax[1] = "staff_id,name,age,phone,dept,enroll_date"
                return syntax
            elif syntax[1].lower() == "from" and syntax[3].lower() == "where" and len(syntax) == 7:
                if "\"" in syntax[6]: syntax[6] = syntax[6][1:-1]
                return syntax
            elif syntax[1].lower() == "into" and syntax[3].lower() == "values":
                syntax[4] = syntax[4][1:-1]
                return syntax
            else:
                print("语句错误，请重新输入!")
                return 0
        except Exception as e:
            print("语句错误，请重新输入!!")
            return 0

    def syntax_determine(self,syntax,staff_dict):   #判断where条件是否成立
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
            print("语句错误，请重新输入!!")

    def staff_info_str(self,staff_dict):    #将字典转换为字符串
        staff_info= [staff_dict['staff_id'], staff_dict['name'], staff_dict['age'],staff_dict['phone'], staff_dict['dept'],staff_dict['enroll_date']]
        return ",".join(staff_info)

    def quit(self,*args):
        sys.exit()

if __name__ == '__main__':
    sql_func = Selected()
    sql_info = '''
支持的SQL语法示例如下
    * 查询: select staff_id,name,age from staff_table where age > 22
    * 修改: update staff_table set dept="IT" where name = "沈洪斌"
    * 新增: insert into staff_table values ("啊利克斯",33,13812345678,"开发",2010-01-01)
    * 删除: delete from staff_table where staff_id = 4
    '''
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
    if os.path.isfile("staff_table") == False:
        sql_func.data_write("staff_table",staff_lists)
    print(sql_info)
    while True:
        choose = input("Please input SQL or Quit to exit >>>").strip()
        if len(choose) == 0:
            continue
        choose_list = re.split(r'\s+',choose)
        try:
            getattr(sql_func,choose_list[0].lower())(choose_list)
        except AttributeError as e:
            print("语句错误，请重新输入!!")
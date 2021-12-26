import tkinter as tk
import tkinter.ttk
import getpass
import tkinter.messagebox  # 消息弹出框库
import sqlite3  # SQLite数据库
from sqlite3 import OperationalError
from tkinter import VERTICAL, Scrollbar, Y  # Scrollbar滚动条库


class StudentSystem(object):
    def __init__(self):  # 构造方法初始化变量
        self.root1 = tk.Tk()   # 窗体初始化
        self.menuTabF = tk.Frame(self.root1)   # 增删改查控件
        self.studentInputF = tk.Frame(self.root1)   # 信息输入框
        self.studentShowF = tk.Frame(self.root1)
        self.root1.title("学生成绩管理系统")   # 标题
        self.root1.geometry('700x350')   # 窗体大小
        self.root1.resizable(False, False)   # 窗体固定
        self.nameToDelete = tkinter.StringVar('')   # 删除
        self.path = "data.db"   # sqlite3连接的数据库源文件

    def menuMain(self):  # 菜单栏
        print("menu")
        menubar = tk.Menu(self.root1)  # 创建导航栏
        file_menu = tk.Menu(menubar, tearoff=False)  # 创建空菜单，菜单不独立
        file_menu.add_command(label="退出", command=self.root1.quit)  # 添加控件
        menubar.add_cascade(label="文件", menu=file_menu)  # 将”文件“菜单添加到导航栏

        do_menu = tk.Menu(menubar, tearoff=False)
        do_menu.add_command(label="添加学生", command=self.insertStudentInfo)
        do_menu.add_cascade(label='修改学生', command=self.updateStudentInfo)
        do_menu.add_command(label="删除学生", command=self.delStudentInfo)
        do_menu.add_command(label="查找学生", command=self.selStudentInfo)
        menubar.add_cascade(label="编辑", menu=do_menu)   # 将”编辑“菜单添加到导航栏

        myself_menu = tk.Menu(menubar, tearoff=False)
        myself_menu.add_command(label="帮助", command=self.showSysInfo)
        menubar.add_cascade(label="关于", menu=myself_menu)  # 将”关于“菜单添加到菜单栏

        self.root1.config(menu=menubar)

    def table(self):    # 使用Treeview组件 创建表格及表格信息
        frame = tk.Frame(self.root1)
        frame.place(x=15, y=130, width=675, height=200)  # 表格大小和位置
        self.tree = tk.ttk.Treeview(frame, columns=(
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6'), show="headings")  # 表格列数

        # 滚动条，使用Scrollbar库
        scrollBar = Scrollbar(frame, orient=VERTICAL)  # 垂直显示
        scrollBar.pack(side=tkinter.RIGHT, fill=Y)  # 滚动条位于右侧，沿y轴方向

        self.tree.config(yscrollcommand=scrollBar.set)    # Treeview组件与垂直滚动条结合
        scrollBar.config(command=self.tree.yview)

        self.tree.heading('c1', text='学号')
        self.tree.heading('c2', text='姓名')
        self.tree.heading('c3', text='性别')
        self.tree.heading('c4', text='班级')
        self.tree.heading('c5', text='学科')
        self.tree.heading('c6', text='成绩')

        self.tree.column('c1', width=110, anchor='center')
        self.tree.column('c2', width=110, anchor='center')
        self.tree.column('c3', width=110, anchor='center')
        self.tree.column('c4', width=110, anchor='center')
        self.tree.column('c5', width=110, anchor='center')
        self.tree.column('c6', width=120, anchor='center')
        self.tree.pack(side=tkinter.LEFT)
        self.tree.bind('<ButtonRelease>', self.midify_item)  # 监听事件

    def studentInput(self):   # 输入学生信息
        tk.Label(self.studentInputF, text="学号：").grid(row=0, column=0)
        self.stuNum = tk.StringVar(self.studentInputF)
        self.numberInput = tk.Entry(
            self.studentInputF, width=15, textvariable=self.stuNum)
        self.numberInput.grid(row=0, column=1)

        tk.Label(self.studentInputF, text="姓名：").grid(row=0, column=2)
        self.stuName = tk.StringVar(self.studentInputF)
        tk.Entry(self.studentInputF, width=15, textvariable=self.stuName).grid(
            row=0, column=3, sticky='w')

        tk.Label(self.studentInputF, text="性别：").grid(row=0, column=4)
        stuSex = tk.StringVar(self.studentInputF)
        self.stuSex = tk.ttk.Combobox(self.studentInputF, width=10,
                                         values=('男', '女'))
        self.stuSex.grid(row=0, column=5)

        tk.Label(self.studentInputF, text="班级：").grid(row=1, column=0)
        self.stuClass = tk.StringVar(self.studentInputF)
        tk.Entry(self.studentInputF, width=15, textvariable=self.stuClass).grid(
            row=1, column=1)

        tk.Label(self.studentInputF, text="学科：").grid(row=1, column=2)
        self.stuObj = tk.StringVar(self.studentInputF)
        tk.Entry(self.studentInputF, width=15,
                 textvariable=self.stuObj).grid(row=1, column=3)

        tk.Label(self.studentInputF, text="成绩：").grid(row=1, column=4)
        self.stuGrage = tk.StringVar(self.studentInputF)
        tk.Entry(self.studentInputF, width=15,
                 textvariable=self.stuGrage).grid(row=1, column=5)

        self.studentInputF.pack(pady=12)

    # 性别选择框清空
    def clearText(self, target):
        target.delete(0, len(target.get()))
    
    # 输入框清空
    def studentInputSetNull(self):
        self.stuNum.set("")
        self.stuName.set("")
        self.clearText(self.stuSex)
        self.stuClass.set("")
        self.stuObj.set("")
        self.stuGrage.set("")
        self.results = ''
        self.numberInput['state'] = 'normal'

    def menuTab(self):  # 增删改查
        tk.Button(self.menuTabF, text="添加", command=self.insertStudentInfo).grid(
            row=0, column=0, ipadx=10, padx=15)
        tk.Button(self.menuTabF, text="删除", command=self.delStudentInfo).grid(
            row=0, column=1, ipadx=10, padx=15)
        tk.Button(self.menuTabF, text="修改", command=self.updateStudentInfo).grid(
            row=0, column=2, ipadx=10, padx=15)
        tk.Button(self.menuTabF, text="查找", command=self.selStudentInfo).grid(
            row=0, column=3, ipadx=10, padx=15)
        tk.Button(self.menuTabF, text="清空", command=self.studentInputSetNull).grid(
            row=0, column=4, ipadx=10, padx=15)
        tk.Button(self.menuTabF, text="返回", command=self.getStudentInfo).grid(
            row=0, column=5, ipadx=10, padx=15)
        self.menuTabF.pack(pady=5)

    def studentShow(self):  # 调用功能
        self.getStudentInfo()
        pass

    def getStudentInfo(self):
        # 清空
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # 读取数据库中的所有数据
        with sqlite3.connect(self.path) as conn:  # 连接数据库
            cur = conn.cursor()
            try:  # 异常处理
                cur.execute('SELECT * FROM studentInfo2 ORDER BY id ASC')  # 搜索表
            except OperationalError as error:
                print(error)
                # 如果没有该表，创建表
                if str(error) == "no such table: studentInfo2":
                    cur.execute(
                        'CREATE TABLE "studentInfo2" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,"number" varchar,"name" varchar,"sex" varchar,"class1" varchar,"object" varchar,"grade" integer)')
                    cur.execute('SELECT * FROM studentInfo2 ORDER BY id ASC')  # 按照序号排序
            temp = cur.fetchall()  # 过滤特殊字符
        # 把数据插入列表
        for i, item in enumerate(temp):
            print(i, item)
            self.tree.insert(parent='', index=i, iid=i,
                                text='', values=(item[1:]))

    def buttonAddClick(self):  # 检查输入——输入成功
        # 检查姓名
        name = self.stuName.get().strip()
        if name == '':
            tkinter.messagebox.showerror(title='ERROR!!', message='必须输入姓名')
            return

        # 获取选择的性别
        sex = self.stuSex.get()
        if sex not in ('男', '女'):
            tkinter.messagebox.showerror(title='ERROR!!', message='性别不可为空')
            return

        # 检查学号
        number = self.stuNum.get().strip()
        # 学号不能重复
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute(
                'SELECT COUNT(id) from studentInfo2 where number="' + number + '"')
            c = cur.fetchone()[0]

        if c != 0:
            tkinter.messagebox.showerror(title='ERROR!!', message='学号重复')
            return

        class1 = self.stuClass.get().strip()
        if class1 == '':
            tkinter.messagebox.showerror(title='ERROR!!', message='必须输入班级')
            return

        # 检查学科
        object = self.stuObj.get().strip()
        if object == '':
            tkinter.messagebox.showerror(title='ERROR!!', message='必须输入学科')
            return

        # 检查成绩
        grade = self.stuGrage.get().strip()
        if grade == '' or (not grade.isdigit()):
            tkinter.messagebox.showerror(title='ERROR!!', message='必须输入成绩')
            return

        # 插入数据库
        # 对要存入的数据进行匹配检查
        sql = 'INSERT INTO studentInfo2(number,name,sex,class1,object,grade) VALUES("' \
                 + number + '","' + name + '","' + sex + '","' + class1 + '","' + object + '","' \
                 + grade + '")'
        self.connectDb(sql)  # 连接
        self.studentInputSetNull()  # 清空输入框
        self.bindData()
        tkinter.messagebox.showinfo(title='SUCCESS!!', message='学生信息添加成功')
        pass

    def bindData(self):
        self.getStudentInfo()
        pass

    def get_select(self):
        selected = self.tree.focus()
        if selected:
            self.nameToDelete.set(self.tree.item(selected, 'values')[0])
            return self.tree.item(selected, 'values')

    def midify_item(self, event):  # 按顺序添加修改数据
        item = self.get_select()
        if item is None:  # 空的不管
            item = self.get_select()
        self.stuNum.set(item[0])
        self.stuName.set(item[1])
        self.clearText(self.stuSex)
        self.stuSex.insert(0, item[2])
        self.stuClass.set(item[3])
        self.stuObj.set(item[4])
        self.stuGrage.set(item[5])
        self.numberInput['state'] = 'readonly'


    # 调用添加学生的功能
    def insertStudentInfo(self):
        self.buttonAddClick()
        pass

    # 删除学生
    def delStudentInfo(self):
        number = self.stuNum.get()
        if number == '':
            tk.messagebox.showinfo('提示', "请先输入信息再进行对应功能操作")
            return
            # 如果已经选择了一条通信录，执行SQL语句将其删除
        sql = 'DELETE FROM studentInfo2 WHERE number="' + number + '"'
        self.connectDb(sql)
        self.studentInputSetNull()
        self.getStudentInfo()
        tkinter.messagebox.showinfo('SUCCESS!!', '删除成功')

    def selStudentInfo(self):  # 查询
        for row in self.tree.get_children():
            self.tree.delete(row)

        name = self.stuName.get().strip()
        class1 = self.stuClass.get().strip()
        number = self.stuNum.get().strip()
        object = self.stuObj.get().strip()

        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            if (number != ''):
                cur.execute('select * from studentInfo2 where number = "' + number + '"')
            if (name != ''):
                cur.execute('select * from studentInfo2 where name = "' + name + '" order by number')
            if (class1 != ''):
                cur.execute('select * from studentInfo2 where class1 = "' + class1 + '" order by number')
            if (object != ''):
                cur.execute('select * from studentInfo2 where object = "' + object + '" order by number')
            if (class1 != '' and object != ''):
                cur.execute('select * from studentInfo2 where class1 = "' + class1 + '" and object = "' + object + '" order by number')
            temp = cur.fetchall()
        for i, item in enumerate(temp):
            print(i, item)
            self.tree.insert(parent='', index=i, iid=i,
                             text='', values=(item[1:]))
        conn.close()
        self.studentInputSetNull()

# 检查修改——修改成功
    def buttonModifyClick(self):
        # 从数据库读取数据
        # 检查姓名
        name = self.stuName.get().strip()
        if name == '':
            tkinter.messagebox.showerror(title='ERROR!!', message='必须输入姓名')
            return

        # 获取选择的性别
        sex = self.stuSex.get()
        if sex not in ('男', '女'):
            tkinter.messagebox.showerror(title='ERROR!!', message='性别不可为空')
            return

        # 检查学号
        number = self.stuNum.get().strip()

        # 检查班级
        class1 = self.stuClass.get().strip()
        if class1 == '':
            tkinter.messagebox.showerror(title='ERROR!!', message='必须输入班级')
            return

        # 检查学科
        object = self.stuObj.get().strip()
        if object == '':
            tkinter.messagebox.showerror(title='ERROR!!', message='必须输入学科')
            return

        # 检查成绩
        grade = self.stuGrage.get().strip()
        if grade == '' or (not grade.isdigit()):
            tkinter.messagebox.showerror(title='ERROR!!', message='必须输入成绩')
            return

        # 插入数据库
        sql = 'UPDATE studentInfo2 SET name = "' + name + '",sex = "' + sex + '",number = "' + number + \
                 '",class1 = "' + class1 + '",object = "' + object + '",grade = "' + \
                 grade + '" WHERE number=' + number
        self.connectDb(sql)
        self.studentInputSetNull()
        self.numberInput['state'] = 'normal'
        tkinter.messagebox.showinfo(title='SUCCESS!!', message='修改成功')
        self.bindData()
        pass

    # 调用修改学生信息的功能
    def updateStudentInfo(self):
        self.buttonModifyClick()

    def connectDb(self, do):  # 用来执行sql语句
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute(do)
            conn.commit()
        pass

    def showSysInfo(self):   # 导航栏“关于”菜单中的“帮助”
        tk.messagebox.showinfo(
            '操作提示', "单击表格内条目进行修改操作，修改后即可完成添加和删除。\n除性别和成绩外的单个输入框中进行输入即可查找对应全部信息。\n"
                    "注：用户进行多项查找时只能同时输入班级和学科的信息。")

    def conclude(self):  # ui的优化
        self.menuMain()
        self.studentInput()
        self.menuTab()
        self.table()
        self.studentShow()


class LoginPage(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("登录")
        self.root.geometry('260x170')
        self.root.resizable(False, False)
        self.menuTabF = tk.Frame(self.root)
        self.loginInputF1 = tk.Frame(self.root)
        self.loginInputF2 = tk.Frame(self.root)
        self.root.resizable(False, False)

    def createPage(self):
        tk.Label(self.loginInputF1, text="用户：").grid(row=0, column=0)
        self.Name = tk.StringVar(self.loginInputF1)
        self.nameInput = tk.Entry(self.loginInputF1, width=18, textvariable=self.Name)
        self.nameInput.grid(row=0, column=1)

        tk.Label(self.loginInputF2, text="密码：").grid(row=1, column=0)
        self.Passwd = tk.StringVar(self.loginInputF2)
        tk.Entry(self.loginInputF2, width=18, textvariable=self.Passwd).grid(row=1, column=1, sticky='w')

        self.loginInputF1.pack(pady=10)
        self.loginInputF2.pack(pady=10)

        tk.Button(self.menuTabF, text="登录", command=self.loginCheck).grid(
                row=0, column=0, ipadx=10, padx=15)
        tk.Button(self.menuTabF, text="退出", command=self.Quit).grid(
                row=0, column=1, ipadx=10, padx=15)

        self.menuTabF.pack(pady=25)

    def loginCheck(self):
        name = self.Name.get().strip()
        passwd = self.Passwd.get().strip()
        if (name == 'root' and passwd == '123456') or (name == 'root1' and passwd == '000000'):
            self.root.destroy()
        else:
            tkinter.messagebox.showinfo('ERROR!!', message='账号或密码错误')

    def Quit(self):
        quit()


def login():
    lt = LoginPage()
    lt.createPage()
    tk.mainloop()


def main():
    xt = StudentSystem()
    xt.conclude()
    tk.mainloop()


if __name__ == "__main__":
    login()
    main()

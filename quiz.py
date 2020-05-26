import pickle
import os
import re
import random
import uuid

filename = 'all_quizes.dat'


class Quiz(object):
    def __init__(self, title='', choices=[], answer_id=0):
        self.uuid = str(uuid.uuid1())  # 唯一标识题目
        self.title = title
        self.choices = choices
        self.answer_id = answer_id

    def set_title(self, s):
        self.title = s

    def set_choices(self, lst):
        self.choices = lst

    def set_answer(self, i):
        self.answer_id = i

    def __str__(self):
        s = '=' * 60 + '?\n'
        s += self.title + '?\n'
        s += '-' * 60 + '?\n'
        for i in range(4):
            s += f'{i + 1} ' + self.choices[i] + '\n'
        s += '\n'
        return s

    def __repr__(self):
        return self.__str__()


all_quizes = []
rand_quizes = []
user_answers = {}  # uuid->answerid


def interactive_add_quiz():
    '''交互式录入
    注意此处每个input都应该加输入验证
    '''
    title = input('输入题目标题:\n')
    # 示例输入验证1
    # if len(title) < 5:
    #     print('标题至少5个字符！')
    #     return

    # 示例输入验证2
    # while len(title) < 5:
    #     print('标题至少5个字符！')
    #     title = input('输入题目标题:\n')
    lst = []
    for i in range(4):
        lst.append(input(f'输入第{i + 1}个选项的内容:\n'))
    answer_id = int(input(f'输入正确答案的序号(1234中的一个):\n'))
    global all_quizes
    all_quizes.append(Quiz(title, lst, answer_id))
    print(f'成功录入题目，现在总数{len(all_quizes)}')


def save_all_quizes():
    with open(filename, 'wb') as f:
        global all_quizes
        pickle.dump(all_quizes, f)
        print(f'已将所有试题保存到{filename}.')


def load_all_quizes():
    '''如果文件存在则读入所有已经保存的题'''
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            global all_quizes
            all_quizes = pickle.load(f)
            print(f'已将从{filename}读取{len(all_quizes)}道试题.')
            print(all_quizes)


def randomly_choose_quizes():
    global all_quizes
    length = len(all_quizes)
    input_str = input(f"请输入要抽取的题目数1<=N<={length}")
    while not re.match(r'^\d+$', input_str):
        print('输入的不是整数，请重新输入')
        input_str = input(f"请输入要抽取的题目数1<=N<={length}")
    n = int(input_str)
    N = n
    # 如果输入的n不在合理范围，就取极值
    # 也可以用while循环要求不断修改输入，但稍麻烦一点
    if n < 1:
        N = 1
    elif n > length:
        N = length
    global rand_quizes
    print(f'从{length}题目中抽取了{N}道题目')
    rand_quizes = random.sample(all_quizes, k=N)
    print(rand_quizes)


def answer_quizes():
    global rand_quizes
    global user_answers
    length = len(rand_quizes)
    if length <= 0:
        print('必须先抽题再答题')
        return
    for i in range(length):
        print(f'共{length}题，第{i + 1}题')
        q = rand_quizes[i]
        print(q)
        user_input = input('你的答案是(1234中任意一个数字):')
        user_answers[q.uuid] = user_input.strip()
    print('答题结束！')


def judge_answers():
    global all_quizes
    global user_answers
    length = len(user_answers)
    if length <= 0:
        print('必须先答题再评卷')
        return
    print('开始评卷!')
    right = 0

    for (uuid, answer) in user_answers.items():
        q = next(qz for qz in all_quizes if qz.uuid == uuid)
        print(q)
        if str(q.answer_id) == answer:
            print('恭喜答对')
            right += 1
        else:
            print(f'遗憾答错,正确答案是{q.answer_id}，你的答案是{answer}')
    print(f'共{length}题，答对{right}题，共{100 * right / length}分')


def add_sample_quizes():
    global all_quizes

    q1 = Quiz()
    q1.set_title('苹果是什么')
    q1.set_choices(['公司', '手机', '电脑', '水果'])
    q1.set_answer(4)

    q2 = Quiz()
    q2.set_title('你的学校是')
    q2.set_choices(['清华', '北大', '北理', '上交'])
    q2.set_answer(3)

    q3 = Quiz()
    q3.set_title('今天多少号')
    q3.set_choices(['24', '25', '26', '27'])
    q3.set_answer(3)

    all_quizes.append(q1)
    all_quizes.append(q2)
    all_quizes.append(q3)
    # print(all_quizes)#测试显示所有试题


def interactive_input_menu():
    global property_list
    # add_sample_quizes()  # 添加示例数据，也可以注释掉
    user_input = ''
    while user_input.lower() != 'q':
        user_input = input('''*** 单项选择题标准化考试系统 ***
a - 保存试题
b - 录入试题
c - 试题抽取
d - 答题
e - 自动判卷
q - 退出\r\n请输入:\n''')
        # print(user_input)
        if user_input.lower() == 'a':
            save_all_quizes()
        elif user_input.lower() == 'b':
            interactive_add_quiz()
        elif user_input.lower() == 'c':
            randomly_choose_quizes()
        elif user_input.lower() == 'd':
            answer_quizes()
        elif user_input.lower() == 'e':
            judge_answers()
        else:
            print('非法输入，请重试！')


def test():
    '''自动化测试，
    避免交互输入，
    更快测试程序
    '''
    add_sample_quizes()
    save_all_quizes()
    load_all_quizes()


if __name__ == "__main__":
    load_all_quizes()
    add_sample_quizes()
    interactive_input_menu()

import pickle

filename = 'all_quizes.dat'


class quiz(object):
    def __init__(self):
        self.title = ''
        self.choices = []
        self.answer_index = 0

    def set_title(self, s):
        self.title = s

    def set_choices(self, lst):
        self.choices = lst

    def set_answer(self, i):
        self.answer_index = i

    def __str__(self):
        s = '=' * 60 + '?\n'
        s += self.title + '?\n'
        s += '-' * 60 + '?\n'
        for i in range(4):
            s += f'{i} ' + self.choices[i] + '\n'
        s += '\n'
        return s

    def __repr__(self):
        return self.__str__()


all_quizes = []


def add_quiz():
    pass


def save_all_quizes():
    with open(filename, 'wb') as f:
        global all_quizes
        pickle.dump(all_quizes, f)
        print(f'已将所有试题保存到{filename}.')


def load_all_quizes():
    with open(filename, 'rb') as f:
        global all_quizes
        all_quizes = pickle.load(f)
        print(f'已将从{filename}读取{len(all_quizes)}道试题.')


def add_sample_quizes():
    global all_quizes

    q1 = quiz()
    q1.set_title('苹果是什么')
    q1.set_choices(['公司', '手机', '电脑', '水果'])
    q1.set_answer(3)

    q2 = quiz()
    q2.set_title('你的学校是')
    q2.set_choices(['清华', '北大', '北理', '上交'])
    q2.set_answer(2)

    all_quizes.append(q1)
    all_quizes.append(q2)
    print(all_quizes)


if __name__ == "__main__":
    add_sample_quizes()
    save_all_quizes()
    load_all_quizes()
    print('end of main.')

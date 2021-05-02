import os
import random
import re
import jieba
from tqdm import trange


class Markov():
    def __init__(self, n: int = 1, path: str = '', text_type='English'):
        """
        构建马尔科夫链
        :param n: 阶数, 前缀单词的个数
        :param path: 文本路径
        :param text_type: 文本语言
        """
        self.path = path
        self.type = text_type
        self.n = n
        self.txt = self.get_path()
        self.words = self.text_procession()
        self.words_dict = self.analyze()

    def get_path(self):
        path = os.path.join(os.getcwd(), self.path+'.txt')
        if os.path.exists(path):
            with open(path) as txt:
                return txt.read()
        else:
            return ''

    def text_procession(self) -> list:
        path = os.path.join(os.getcwd(), self.path+'_segmentation.txt')
        if os.path.exists(path):
            with open(path) as file_obj:
                text = file_obj.read()
                words = text.split(' ')
            return words
        else:
            text = self.txt.replace('\n', ' ').replace('[', ' ').replace(']', ' ')
            r = '[-*#\"\'\\()%“‘’”、（）|=\d]+'
            text = re.sub(r, '', text)
            if self.type == 'English':
                for symbol in [',', '.', ':', ';', '?', '!']:
                    text = re.sub('[{}]+'.format(symbol), ' '+symbol+' ', text)
                    # text = text.replace(symbol, ' '+symbol+' ', text)
                words = text.split(' ')
                words = [word.lower() for word in words if word != '']
            else:
                # for symbol in ['，', '。', '：', '；', '？', '！']:
                #     text = text.replace(symbol, ' '+symbol+' ')
                print('start segmentation')
                words = [word for word in jieba.cut(text)]
            return words

    def save_segmentation(self):
        path = os.path.join(os.getcwd(), self.path+'_segmentation.txt')
        with open(path, 'w') as file_obj:
            for word in self.words:
                file_obj.write(word+' ')

    def analyze(self) -> dict:
        words_dict = {}
        count = len(self.words)//self.n if self.n != 1 else len(self.words)//self.n-1

        print('Start analyzing')
        for i in trange(count):
            n_words = tuple([self.words[i+j] for j in range(self.n)])
            if n_words not in words_dict:
                words_dict[n_words] = {}

                words_dict[n_words][self.words[i+self.n]] = words_dict[n_words].get(self.words[i+self.n], 0)+1
        return words_dict

    def word_frequency_sum(self, fre_dict: dict) -> int:
        sum = 0
        for word, value in fre_dict.items():
            sum += value
        return sum

    def fetch_suffix(self, fre_dict: dict) -> str:
        rand_int = random.randint(1, self.word_frequency_sum(fre_dict))
        for word, value in fre_dict.items():
            rand_int -= value
            if rand_int <= 0:
                return word

    def generate(self, length: int = 100, cur_word: str = ''):
        chain = ''
        if not cur_word:
            cur_word = random.choice(list(self.words_dict.keys()))
        else:
            for words_tuple in self.words_dict.keys():
                if cur_word == words_tuple[0]:
                    cur_word = words_tuple
            if not isinstance(cur_word, tuple):  # 若指定单词不存在, 还是在文本中随机寻取
                cur_word = random.choice(list(self.words_dict.keys()))

        print('Start generating')
        for i in trange(length):
            for word in cur_word:
                chain += word
                if self.type == 'English':
                    chain += ' '
            cur_word = self.fetch_suffix(self.words_dict[cur_word])

            key = []
            for words_tuple in self.words_dict.keys():
                if cur_word == words_tuple[0]:
                    key.append(words_tuple)
            cur_word = random.choice(key)

        return chain


# eng_mar = Markov(2, r'experiment3\data\The Old Man and the Sea.txt')
# eng_mar.generate(200)
chi_mar = Markov(3, r'experiment3\data\dirty_words', text_type='Chinese')
# chi_mar.save_segmentation()
print(chi_mar.generate(length=10))
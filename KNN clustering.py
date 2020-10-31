# coding:utf-8
import nltk
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import pandas as pd

doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle."
doc_complete = [doc1, doc2, doc3, doc4, doc5]


def excel_one_line_to_list(path, col):
    df = pd.read_excel(path, usecols=[col], names=None)  # 读取项目名称列,不要列名
    df_li = df.values.tolist()
    result = []
    for s_li in df_li:
        result.append(s_li[0])
        # print(s_li[0])
    return result


def participles(text):  # 分词函数
    pattern = r"""(?x)               # set flag to allow verbose regexps 
              (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A. 
              |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages 
              |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe 
              |\.\.\.                # ellipsis 
              |(?:[.,;"'?():-_`])    # special characters with meanings 
            """
    t = nltk.regexp_tokenize(text, pattern)
    length = len(t)
    for i in range(length):
        t[i] = t[i].lower()
    return t


def readstop(path):  # 读取txt文件，并返回list，这里用来读取停用词文件
    f = open(path, encoding='utf-8')
    data = []
    for line in f.readlines():
        data.append(line)
    return data


def getridofsw(lis, swlist):  # 去除文章中的停用词
    afterswlis = []
    for i in lis:
        if str(i) in swlist:
            continue
        else:
            afterswlis.append(str(i).lower())
    return afterswlis


def getstopword(path):  # 获取停用词表
    swlis = []
    for i in readstop(path):
        outsw = str(i).replace('\n', '').lower()
        swlis.append(outsw)
    return swlis


def corpus_1(filelist, swlist):  # 建立语料库
    alllist = []
    for i in filelist:
        afterswlis = getridofsw(participles(str(i)), swlist)
        for j in afterswlis:
            alllist.append(j)
    return alllist


if __name__ == "__main__":

    swpath = r'/Users/pineleaf/PycharmProjects/English_word_segmentation/English_stop_words.txt'  # 停用词表路径
    swlist = getstopword(swpath)  # 获取停用词表列表
    # print(swlist)
    #     filelist = excel_one_line_to_list(r"/Users/pineleaf/Desktop/OLED简化 3.xls",)
    labels = corpus_1(doc_complete, swlist)  # 这里放着每个单词
    #     print(labels)

    str_1 = ''
    corpus = []
    for i in doc_complete:
        afterswlis = getridofsw(participles(str(i)), swlist)  # 去除停用词表后的每个语料
        #         print(afterswlis)
        for j in afterswlis:
            str_1 = str_1 + j + ' '
        corpus.append(str_1)  # 列表中放有每个语句去除停用词并分词后的结果
        str_1 = ''
    #     print(corpus)

    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print("-------这里输出第", i, u"类文本的词语tf-idf权重------")
        for j in range(len(word)):
            print(word[j], weight[i][j])
    weight = tfidf.toarray()
    print(weight)  # 将TF-IDF矩阵抽取出来
    clusters = 2  # 集群的个数（K-means聚类的个数）
    mykms = KMeans(n_clusters=clusters)
    y = mykms.fit_predict(weight)
    for i in range(0, clusters):
        label_i = []
        for j in range(0, len(y)):
            if y[j] == i:
                label_i.append(labels[j])
        print('label_' + str(i + 1) + ':' + str(label_i))

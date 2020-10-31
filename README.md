# English-analysis-and-KNN-clustering
英文分词+KNN聚类 可以实现读取excel文件

# 主要实现了英文的分词和KNN的聚类
### 代码中含有英文停用词表，可以选择使用自带的停用词表，也可以选择该表，表中我添加了标点符号，我认为标点符号对于词频分析没用，如果有其他需要可以自行删除
### 代码可以实现读取excel文件，使用了pandas库，语料我使用的是几个语句，方便进行调试和查看，也可以使用已经封装好的excel_one_line_to_list函数读取Excel表格中的一列直接进行处理，其中得到的结果应该和列表doc_complete相同才可以进行处理
### 如果需要读取txt文件，可以修改函数来实现

# 参考的博客
https://blog.csdn.net/u013250071/article/details/81911434 实现了写入数据的功能
https://blog.csdn.net/whyoceansea/article/details/79808854 实现了主要功能，大部分代码来源
在这里进行致谢

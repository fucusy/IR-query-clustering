# IR-query-clustering


Description
======
this project is about query clustering. in a search engine, there is always a related search 
section to provide similar search query to user. those similar search query can be mined by
query clustering.


Method
=======
this project implement the query clustering algorithm from log of paper *Beeferman, Doug, and Adam Berger. "Agglomerative clustering of a search engine query log." Proceedings of the sixth ACM SIGKDD international conference on Knowledge discovery and data mining. ACM, 2000.*

Before jump into the code
=======
you should know some basic knowledge of set, and union-find data structure.


Test data
=======
search log from [data lab of sogou.com](http://www.sogou.com/labs/dl/q-e.html).
extract query url pair from completed data. got 863k pairs data. and sorted by url, take first 10k pairs
as test data. because it costs too much time when adopt all of query and url pairs. 


run environment
=======

1. windows or *nix system, tested on *nix system   
1. python version 2.7 or higher, tested at 2.7


How to run test
=======

    ./query_clustering.py

Result
======
after finishing program, a new file named query_clustering.log will appear, which content looks like below.
the number after '[INFO]' is the cluster id, the strings after the number split by ',' is the content of this cluster.

    2016-01-07 20:24:10[INFO] 4355: 新黑暗圣经,黑暗圣经
    2016-01-07 20:24:10[INFO] 4359: 哲学研究生就业,汽油机+气门重叠+废气,母女同欢小说,SM女战士
    2016-01-07 20:24:10[INFO] 4366: 家居墙壁生虫,211.144.66.100
    2016-01-07 20:24:10[INFO] 4373: SM-3BLOCK2,成龙年轻时的照片,猫眼匹萨团结湖,内邱扁鹊庙
    2016-01-07 20:24:10[INFO] 4386: 徐士泰,永安邱天,putting+in+a+window+will,银行贷款业务的核算要求,文学层次分析法
    2016-01-07 20:24:10[INFO] 4413: 邓昌宁,同济大学汽车学院鉴定证书
    2016-01-07 20:24:10[INFO] 4453: 张钰公布第三部录像,东莞佳登宝电子科技有限公司
    2016-01-07 20:24:10[INFO] 4476: FAプロ]部屋系列,,吉崎直绪+中出
    2016-01-07 20:24:10[INFO] 4488: 警花+巨大的阳物,枫ひみつ
    2016-01-07 20:24:10[INFO] 4493: 东北大炕全集,东北大炕续
    2016-01-07 20:24:10[INFO] 4507: 洋女欧美,天海丽BT+图
    2016-01-07 20:24:10[INFO] 4511: 东热名模,水朝美树+南波杏
    2016-01-07 20:24:10[INFO] 4514: h-nancy-ho-v04c,泰国+natalia+图
    2016-01-07 20:24:10[INFO] 4550: 陈春雨+刘洁,218.189.234.244+AV
    2016-01-07 20:24:10[INFO] 4614: 校园育婷,校园育婷+佳雨+雅茹
    2016-01-07 20:24:10[INFO] 4634: silvia+saint全集,世钦+暴露
    2016-01-07 20:24:10[INFO] 4641: filetype:all+国际贸易法,建筑抗震设计规范理解与应用pdf
    2016-01-07 20:24:10[INFO] total running time: 21.00 second
    2016-01-07 20:24:10[INFO] end program---------------------

Performance
=======

it cost 21s to process 10k pairs query and url.
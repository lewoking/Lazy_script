#导入relationship库中的Relationship类 
from relationship import Relationship 
 
#自定义节点词典（小说中人物角色） 
dictpath = r'角色名单.txt' 
#小说路径，只能是编码方式为utf-8的txt文件 
datapath = r'人民的名义.txt' 
#程序运行生成的角色关系图保存地址 
pic = r'人物关系图.png' 
Re = Relationship(dictpath, datapath) 
relation = Re.relationship() 
graph = Re.network_digraph(relation, pic) 
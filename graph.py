#cmd /k cd "$(FULL_CURRENT_PATH)" &  python "$(FULL_CURRENT_PATH)" & ECHO. & PAUSE & EXIT；
#关系可视化
from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.globals import ThemeType
 
import webbrowser
import pandas as pd

 
#---------------------------------------
 
#主要设置
#InitOpts：初始化配置项（在图形创建开始时即可设置)
init_opts=opts.InitOpts(width="100%",   #图宽
                        height="900px", #图高
                        renderer="canvas", #渲染模式 svg 或 canvas，即 RenderType.CANVAS 或 RenderType.SVG
                        page_title="Pyecharts Graph关系图",    #网页标题
                        theme=ThemeType.DARK,  #主题风格可选：WHITE,LIGHT,DARK,CHALK,ESSOS,INFOGRAPHIC,MACARONS,PURPLE_PASSION,ROMA,ROMANTIC,SHINE,VINTAGE,WALDEN,WESTEROS,WONDERLAND
                        #bg_color="#333333",    #背景颜色
                        js_host=""  #js主服务位置 留空则默认官方远程主服务
                        )
                        
#label_opts:节点显示文字样式设置
#formatter结合rich可以设置丰富的文本样式 类似CSS
label_opts=opts.LabelOpts(color="#008080",
                          distance=0,
                          font_size=14,
                          #font_weight="bold",
                          formatter="{a}\n{x| {b} }\n{t| {c} }",    #{a}, {b}，{c}...，分别表示系列名，数据名，数据值等
                          rich={"x":{"color":"pink","backgroundColor":"#008080","borderRadius":8,"fontSize":14},"t":{"color":"yellow"}},    #像CSS类似设置
                          ) 
label_opts_name=opts.LabelOpts(color="#008080",
                          distance=0,
                          font_size=14,
                          #font_weight="bold",
                          formatter="{x| {b} }",    #{a}, {b}，{c}...，分别表示系列名，数据名，数据值等
                          rich={"x":{"color":"pink","backgroundColor":"rgba(0,0,0,0.1)","borderRadius":8,"fontSize":14}},    #像CSS类似设置
                          )                             
label_opts_value=opts.LabelOpts(color="#008080",
                          distance=0,
                          font_size=14,
                          #font_weight="bold",
                          formatter="{x| {c} }",    #{a}, {b}，{c}...，分别表示系列名，数据名，数据值等
                          rich={"x":{"color":"pink","backgroundColor":"rgba(0,0,0,0.1)","borderRadius":8,"fontSize":14}},    #像CSS类似设置
                          ) 
#ToolboxOpts：工具栏配置（可实现图片保存等功能）
toolbox_opts=opts.ToolboxOpts(is_show=True, #是否显示工具栏
                              orient="vertical",  #工具栏工具摆放方向
                              pos_left="right")   #工具栏左边位置
                              
#TooltipOpts：提示文字显示设置
tooltip_opts=opts.TooltipOpts(formatter="{a}<br/>{b}<br/>{c}",
                              background_color="rgba(255,255,255,0.3)",
                              border_color="yellow",
                              border_width=2,
                              )
                            
 
#★★★★★       
#通过opts.ItemStyleOpts，设置node节点样式（颜色、大小、透明度)     
itemstyle_opts=opts.ItemStyleOpts(color="orange", #节点颜色
                                  border_color="red", #节点边线颜色
                                  border_width=1,    #节点边线宽度
                                  opacity=0.9,    #节点透明度
                                  )
                                  
#节点间连接线样式设置
linestyle_opts=opts.LineStyleOpts(is_show=True,
                                  width=1,
                                  opacity=0.6,
                                  curve=0.3,
                                  type_="solid", 
                                  color="#008080", 
                                 )
linestyle_opts_repeated=opts.LineStyleOpts(is_show=True,
                                  width=1,
                                  opacity=0.6,
                                  curve=0.3,
                                  type_="solid", 
                                  color="red", 
                                 )
#---------------------------------------
 
#导入excel数据
excel_file=input("请输入EXCEL表的绝对地址：")
if excel_file.strip()=="":
    excel_file="test.xlsx"
print(excel_file)
   
data=pd.read_excel(excel_file,sheet_name='Sheet1')
#EXCEL表列名
column_names=data.columns.values
 
#---------------------------------------
 
#节点样式类别
categories=[
    {"symbol":"circle"},
    {"symbol":"roundRect"},
    {"symbol":"triangle"},
    {"symbol":"diamond"},
    {"symbol":"pin"},
    {"symbol":"rect"},
    {"symbol":"roundRect"},
    {"symbol":"triangle"},
    {"symbol":"diamond"},
    {"symbol":"pin"},  
]
 
#节点样式类别补足
if len(categories)<data.shape[1]:
    for i in range(data.shape[1]-len(categories)):
        categories.append({"symbol":"circle"})
        
#---------------------------------------
#生成大量节点和连接线
node_names=[]
nodes=[]
links=[]
 
for i in range(data.shape[0]):
    #索引节点
    index_node_name=" "+str(i)
    node_names.append(index_node_name)
    index_node=opts.GraphNode(name=index_node_name,   #节点名称 ★ 不能有重名！
                                value=str(i), #节点值
                                symbol_size=30,   #节点大小
                                symbol="circle",  #节点样式
                                label_opts=label_opts_name,
                                category=0,
                                )
    nodes.append(index_node)
    
    #节点展开
    for j in range(data.shape[1]):
        #列名节点
        column_node_name=" "+column_names[j]+"_"+str(i)+"_"+str(j)
        column_node_value=column_names[j]
        column_node=opts.GraphNode(name=column_node_name,   #节点名称 ★ 不能有重名！
                                    value=column_node_value, #节点值
                                    symbol_size=15,   #节点大小
                                    #symbol="circle",  #节点样式
                                    label_opts=label_opts_value,
                                    category=0,
                                    )
        nodes.append(column_node)
        links.append({"source":index_node_name,"target":column_node_name,"lineStyle":linestyle_opts,"symbol":["","arrow"]})
        #单元格节点
        #----------------------
        cell_node_name=" "+str(data.iloc[i,j])
        if cell_node_name not in node_names:
            cell_node=opts.GraphNode(name=cell_node_name,   #节点名称 ★ 不能有重名！
                                value=str(i)+"-"+str(j), #节点值
                                symbol_size=12,   #节点大小
                                #symbol="circle",  #节点样式
                                label_opts=label_opts_name,
                                category=j,
                                )
            nodes.append(cell_node)
            node_names.append(cell_node_name)
            links.append({"source":column_node_name,"target":cell_node_name,"lineStyle":linestyle_opts,"symbol":["","arrow"]})
        else:
            links.append({"source":column_node_name,"target":cell_node_name,"lineStyle":linestyle_opts_repeated,"symbol":["","arrow"]})
         
#生成图像并渲染输出
g=(
    Graph(init_opts)
    .add("", nodes, links, repulsion=8000,itemstyle_opts=itemstyle_opts,is_draggable=True,categories=categories)
    .set_global_opts(title_opts=opts.TitleOpts(title=""),toolbox_opts=toolbox_opts,tooltip_opts=tooltip_opts)
    .render("graph.html")
)
 
#---------------------------------------
 
 
 
 
 
 
 
 
 
 
 
#网络服务程序
#---------------------------------------
 
from flask import Flask,g,request,render_template,Response,stream_with_context
import threading
import time
 
 
#---------------------------------------
app=Flask(__name__,static_url_path='',template_folder='',static_folder='')
 
@app.route('/')
def index():
    return render_template("graph.html")
    
#---------------------------------------
 
def run_app():
    print("应用启动")
    if __name__ == '__main__':
        app.run("0.0.0.0")
 
def open_browser():
    time.sleep(1)
    print("打开浏览器")
    webbrowser.open("http://localhost:5000")
    
def main():
    #主要程序
    # 创建线程
    thread1 = threading.Thread(target=open_browser)
    thread2 = threading.Thread(target=run_app)
    # 启动线程
    thread1.start()
    thread2.start()
 
if __name__ == '__main__':
    main()
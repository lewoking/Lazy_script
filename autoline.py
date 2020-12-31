import ipaddress
import pandas as pd
import pymysql

## 加上字符集参数，防止中文乱码
dbconn=pymysql.connect(
  host="127.0.0.1",
  database="jmjkxx",
  user="root",
  password="usbw",
  port=3306,
  charset='utf8'
 )

#sql语句
sqlcmd="SELECT PrimaryKey, ForeignKey, DevIndex, DevType, IfDescr, IfEnca, IfFatherDev, IfFatherIf, IfFatherMAC, IfIP, IfIndex, IfMAC, IfMask, IfSegIndex FROM o2000.devinfo"

#利用pandas 模块导入mysql数据
df=pd.read_sql(sqlcmd,dbconn)
# df=df.head()


#转化为网络地址
def cal_ip(ip_net):
    try:
        
        net = ipaddress.ip_network(ip_net, strict=False)
        # print('网络号： ' + str(net.network_address))
    except ValueError:
        print('您输入格式有误，请检查！')
    return net.network_address

 
def exchange_mask(mask):
    
    # 计算二进制字符串中 '1' 的个数
    count_bit = lambda bin_str: len([i for i in bin_str if i=='1'])
 
    # 分割字符串格式的子网掩码为四段列表
    mask_splited = mask.split('.')
 
    # 转换各段子网掩码为二进制, 计算十进制
    mask_count = [count_bit(bin(int(i))) for i in mask_splited]
    
    return sum(mask_count)


def auto(df):
    for index,row in df.iterrows():
        ip_net=row['ip_net']
#        print(index,ip_net)
        df.loc[index,'ipnet']= cal_ip(ip_net)
    return df

def mask(df):
    for index,row in df.iterrows():
        mask=row['IfMask']
#        print(index,mask)
        df.loc[index,'MASK_COUNT']= exchange_mask(mask)
    return df

def match(df):
    for index,row in df.iterrows():
        ma_ipnet1=row['ipnet']
        tmp1=df.loc[index,:]
        tmp1=tmp1.tolist()
        print(index)
        ma_df =df.drop([index])
        ma_df.columns=['PrimaryKey0', 'ForeignKey0', 'DevIndex0', 'DevType0', 'IfDescr0', 'IfEnca0', 'IfFatherDev0', 'IfFatherIf0', 'IfFatherMAC0', 'IfIP0', 'IfIndex0', 'IfMAC0', 'IfMask0', 'IfSegIndex0','MASK_COUNT0','ip_net0','ipnet0']   #修改匹配表列名

        for index,row in ma_df.iterrows():

            ma_ipnet2=row['ipnet0']
            if ma_ipnet1 == ma_ipnet2:
                tmp2=ma_df.loc[index,:]
                tmp2=tmp2.tolist()
                
                # print(tmp2)
                ma_net= tmp1 + tmp2 # 匹配完成表
                print(ma_net)
    # return ma_net

        




if __name__ == '__main__':
#    ip_net = '192.168.1.140/30'
#    print(cal_ip(ip_net))
#    print(exchange_mask('255.255.254.0'))
    mask(df)
    df['MASK_COUNT']=df['MASK_COUNT'].astype("int")      #取整
    df['ip_net']= df["IfIP"]+"/"+df["MASK_COUNT"].map(str)  #auto处理前格式化数据
    auto(df)
    # print(df)
    match(df)


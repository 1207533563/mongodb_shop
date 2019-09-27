import pymongo,sys,os

conn = pymongo.MongoClient("mongodb://localhost:27017/")
db = conn["commodity_db"]   #创建数据库
stus = db["commodity_sales"]  #创建集合
# s = {"商品ID":1001,"商品名称":"百事可乐","商品进价":"2.5","购入单位":"百事"}  commodity_info 信息表/进货表
# s = {"商品ID":1001,"商品库存":100}   commodity_inventory 库存表
# s = {"商品ID":1001,"出售量":0,"售价":3,"实收":0,"盈利":0}  commodity_sales 售货表
# stus.insert_one(s)


def add_info(ids,name,price,unit):
    '''
    函数功能：增加商品信息
    函数参数："商品ID":ids,"商品名称":name,"商品进价":price,"购入单位":unit
    '''
    info = db["commodity_info"]
    s = {"商品ID":ids,"商品名称":name,"商品进价":price,"购入单位":unit}
    info.insert(s)
    # print("增加成功:",s)


def add_nums(ids,num=0):
    '''
    函数功能：进货，增加商品库存信息
    函数参数："商品ID":ids,"商品库存":num 默认为0
    '''
    inve = db["commodity_inventory"]
    s = {"商品ID":ids,"商品库存":num}
    inve.insert(s)
    # print("增加成功:",s)
    

def add_sale(ids,sale_price,sale_num=0,income=0,profit=0):
    '''
    函数功能：增加商品销售信息
    函数参数："商品ID":ids,"售价":sale_price,"出售量":sale_num 默认为0,"实收":income 默认为0,"盈利":profit 默认为0
    '''
    sale = db["commodity_sales"]
    s = {"商品ID":ids,"出售量":sale_num,"售价":sale_price,"实收":income,"盈利":profit}
    sale.insert(s)
    # print("增加成功:",s)



def del_info(ids):
    '''
    函数功能：删除商品信息
    函数参数：商品ID
    返回值：删除成功返回0，删除失败返回1
    '''
    info = db["commodity_info"]
    r = info.delete_one({"商品ID":ids})
    if r.deleted_count == 1:
        return 0
    else:
        return 1

    

def del_nums(ids):
    '''
    函数功能：删除商品库存
    函数参数：商品ID
    返回值：删除成功返回0，删除失败返回1
    '''
    inve = db["commodity_inventory"]
    r = inve.delete_one({"商品ID":ids})
    if r.deleted_count == 1:
        return 0
    else:
        return 1

def del_sale(ids):
    '''
    函数功能：删除商品销售信息
    函数参数：商品ID
    返回值：删除成功返回0，删除失败返回1
    '''
    sale = db["commodity_sales"]
    r = sale.delete_one({"商品ID":ids})
    if r.deleted_count == 1:
        return 0
    else:
        return 1



def update_info(old,new):
    '''
    函数功能：更改商品信息
    函数参数：old:必须为字典，如{"商品ID":1001},new:必须为字典，如{"商品ID":1002}
    描述：将old改成new
    '''
    info = db["commodity_info"]
    info.update_one(old, {"$set":new})
    info.upda
    

def update_nums(old,new):
    '''
    函数功能：更改商品库存
    函数参数：old:必须为字典，如{"商品ID":1001},new:必须为字典，如{"商品ID":1002}
    描述：将old改成new
    '''
    inve = db["commodity_inventory"]
    inve.update_one(old, {"$set":new})
    


def update_sale(old,new):
    '''
    函数功能：更改商品销售信息
    函数参数：old:必须为字典，如{"商品ID":1001},new:必须为字典，如{"商品ID":1002}
    描述：将old改成new
    '''
    sale = db["commodity_sales"]
    sale.update_one(old, {"$set":new})
    



def find_info(ids):
    '''
    函数功能：查找某ID商品的库存
    函数参数：商品ID
    返回值：商品所有信息的字典
    '''
    info = db["commodity_info"]
    f = info.find_one({"商品ID":int(ids)})
    return f


def find_nums(ids):
    '''
    函数功能：查找某ID商品的库存
    函数参数：商品ID
    返回值：商品ID和数量的字典
    '''
    inve = db["commodity_inventory"]
    f = inve.find_one({"商品ID":int(ids)})
    return f


def find_sale(ids):
    '''
    函数功能：查找某ID商品的库存
    函数参数：商品ID
    返回值：商品所有出售信息的字典
    '''
    sale = db["commodity_sales"]
    f = sale.find_one({"商品ID":int(ids)})
    return f



def main():
    while True:
        print("1.新商品入库")
        print("2.进货")
        print("3.删货")
        print("4.售货")
        print("5.查询")
        print("6.退出")
        r = input("请选择功能：")
        if r == "1":
            os.system("cls")
            ids = int(input("新商品ID:"))
            name = input("新商品名字:")
            price = input("进价:")
            unit = input("进货单位:")
            sale_price = input("售价:")
            add_info(ids,name,price,unit)
            add_nums(ids)
            add_sale(ids,sale_price)
            os.system("cls")
            print("入库成功！")
        elif r == "2":
            os.system("cls")
            ids = int(input("商品ID："))
            nums = int(input("请输入本次新进商品数量"))
            old_nums = find_nums(ids)["商品库存"]
            update_nums({"商品ID":ids},{"商品库存":old_nums + nums})
            os.system("cls")
            print("进货成功！")

        elif r == "3":
            os.system("cls")
            ids = int(input("商品ID:"))
            del_info(ids)
            del_nums(ids)
            del_sale(ids)
            os.system("cls")
            print("删除成功！")

        elif r == "4":
            os.system("cls")
            ids = int(input("商品ID:"))
            nums = int(input("本次出售数量:"))
            old_nums = find_nums(ids)["商品库存"]
            sale_info = find_sale(ids)
            if old_nums < nums:
                print("存货不足!")
            else:
                update_nums({"商品ID":ids},{"商品库存":old_nums - nums})
                update_sale({"商品ID":ids},{"出售量":sale_info["出售量"] + nums})
                update_sale({"商品ID":ids},{"实收":sale_info["实收"] + nums*eval(sale_info["售价"])})
                update_sale({"商品ID":ids},{"盈利":sale_info["盈利"] + nums*(eval(sale_info["售价"])-eval(find_info(ids)["商品进价"]))})
                os.system("cls")
                print("售货成功！")

        elif r == "5":
            os.system("cls")
            print("1.查询商品信息")
            print("2.查询商品库存信息")
            print("3.查询商品出售信息")
            c = input("请选择功能：")
            if c == "1":
                os.system("cls")
                print("1.查询所有商品信息")
                print("2.查询单个商品信息")
                n = input("请选择功能：")
                if n == "1":
                    os.system("cls")
                    info = db["commodity_info"]
                    all = info.find()
                    for x in all:
                        print(x)
                if n == "2":
                    os.system("cls")
                    ids = int(input("请输入商品ID："))
                    print(find_info(ids))

            elif c == "2":
                os.system("cls")
                print("1.查询所有商品库存信息")
                print("2.查询单个商品库存信息")
                n = input("请选择功能：")
                if n == "1":
                    os.system("cls")
                    inve = db["commodity_inventory"]
                    all = inve.find()
                    for x in all:
                        print(x)
                if n == "2":
                    os.system("cls")
                    ids = int(input("请输入商品ID："))
                    print(find_nums(ids))
    
            elif c == "3":
                os.system("cls")
                print("1.查询所有商品出售信息")
                print("2.查询单个商品出售信息")
                n = input("请选择功能：")
                if n == "1":
                    os.system("cls")
                    sale = db["commodity_sales"]
                    all = sale.find()
                    for x in all:
                        print(x)
                if n == "2":
                    os.system("cls")
                    ids = int(input("请输入商品ID："))
                    print(find_sale(ids))


        elif r == "6":
            sys.exit()

if __name__ == "__main__":
    main()


    
    
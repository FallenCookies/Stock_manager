import matplotlib.pyplot as plt
import timeit
class product: #Класс продукта
    def __init__(self,name_=None, category_= None, volume_= None, date_= None,):
        self.category = category_
        self.volume = int(volume_)
        self.date = date_
        self.name=name_
        self.index=int(self.date)/int(self.volume)
        #конструктор класса_
    def __gt__(self, other):
        return self.index>other.index

    def __str__(self):#перегруженный метод для печати
      print("Имя продукта: " +self.name)
      print("Категория: "+self.category)
      print("Обьем: "+str(self.volume))
      print("Срок годности: "+self.date+" дн.")
      return ""
class rack:# класс стеллажа
    def __init__(self,max_size_=None,category_=None,current_size_ = 0):
        #конструктор класса
        self.max_size = max_size_
        self.current_size = current_size_
        self.products=[]
        self.category=category_
    def Add(self,product):
        #метод добавления продукта на стеллаж

        if self.current_size+product.volume<=self.max_size:
            self.products.append(product)
            self.current_size+=product.volume
            return True
        else:
            return False
    def __str__(self):
      #перегруженный метод для печати
      print("Стеллаж с: "+self.category)
      print("Занятый объем: "+str(self.current_size)+" из "+str(self.max_size))
      out=''
      for x in self.products:
          out+=x.name+","
      print("Список размещенных продуктов: "+out)
      return ""



stock_index={}# склад магазина
stock_greed={}# склад магазина
stock_backtrack={}# склад магазина
temp={}
#создание стеллажей
Rack_index1 = rack(20, "Vegetables")
Rack_index2 = rack(30, "Sweets")
Rack_index3 = rack(40, "Fruits")
Rack_greed1 = rack(20, "Vegetables")
Rack_greed2 = rack(30, "Sweets")
Rack_greed3 = rack(40, "Fruits")
Rack_backtrack1 = rack(20, "Vegetables")
Rack_backtrack2 = rack(30, "Sweets")
Rack_backtrack3 = rack(40, "Fruits")
def stock_from_file(stock_name):
    with open("Input.txt") as file:  # чтение файла
        array = [row.strip() for row in file]
    #Заполнение склада из фала
    while array:
        p = product(array.pop(0), array.pop(0), array.pop(0),array.pop(0))
        if len(array)>0:
            array.pop(0)
        if p.category in stock_name:
            stock_name[p.category].append(p)
        else:
            stock_name[p.category]=[]
            stock_name[p.category].append(p)

def Stack_print(stock):     #Вывод продуктов на складе
    for category in stock:
        out=category+":"
        for product in stock[category]:
             out+=str(product.index)+", "
        print(out)
#алгоритм заполнения стеллажей на индексах
def rack_from_stock_index():
    stock_from_file(stock_index)
    for x in stock_index:
        stock_index[x].sort(key=lambda j: j.index, reverse=False)
    for category in stock_index:
        for pr in stock_index[category]:
            if ''.join(pr.category).strip()=="Vegetables":
                Rack_index1.Add(pr)
            elif pr.category == "Sweets":
                Rack_index2.Add(pr)
            elif pr.category == "Fruits":
                Rack_index3.Add(pr)

def rack_from_stock_greed(): #алгоритм заполнения стеллажей жадным алгоритмом
    stock_from_file(stock_greed)
    for x in stock_greed:
        stock_greed[x].sort(key=lambda j: j.date, reverse=False)
    for category in stock_greed:
        for pr in stock_greed[category]:
            if ''.join(pr.category).strip()=="Vegetables":
                Rack_greed1.Add(pr)
            elif pr.category == "Sweets":
                Rack_greed2.Add(pr)
            elif pr.category == "Fruits":
                Rack_greed3.Add(pr)
result=[]
def backtrack_fill(curr_stock,temp_list,curr_size):
    if len(curr_stock)>2 and curr_size+curr_stock[2].volume<Rack_backtrack1.max_size:
        product=curr_stock.pop(2)
        temp_list.append(product)
        curr_size+=product.volume
        backtrack_fill(curr_stock,temp_list,curr_size)
    if len(curr_stock)>1 and curr_size+curr_stock[1].volume<Rack_backtrack1.max_size:
        product=curr_stock.pop(1)
        temp_list.append(product)
        curr_size+=product.volume
        backtrack_fill(curr_stock, temp_list, curr_size)

    if len(curr_stock)>0 and curr_size+curr_stock[0].volume<Rack_backtrack1.max_size:
        product=curr_stock.pop(0)
        temp_list.append(product)
        curr_size+=product.volume
        backtrack_fill(curr_stock, temp_list, curr_size)
    else:
        result.append(temp_list)
        return
def rack_from_stock_backtrack(): # бэктрэкинг
    stock_from_file(stock_backtrack)
    count=1
    for x in stock_backtrack:
        stock_backtrack[x].sort(key=lambda j: j.index, reverse=False)

        backtrack_fill(stock_backtrack[x],[],0)
        min = 1000
        best_of_three=[]
        for x in result:
            sum=0
            for product in x:
                sum += product.index
            if sum<min:
                min=sum
                best_of_three=x
        if count==1:
            for x in best_of_three:
                Rack_backtrack1.Add(x)
            count+=1
        if count==2:
            for x in best_of_three:
                Rack_backtrack2.Add(x)
            count+=1
        if count==3:
            for x in best_of_three:
                Rack_backtrack3.Add(x)

        result.clear()



def bench(f):
    return timeit.timeit(f, number=1)
def Remove_products(stock,racks): #синхронизация склада
    for rack in racks:
        for x in rack.products:
            if stock[rack.category].count(x)>0:
                stock[rack.category].remove(x)
def Stock_pr_print(stock): #печать продуктов на складе
    for x in stock:
        out=x+":"
        for j in stock[x]:
            out+=str(j.index)+", "
        print(out)
def Stock_result(stock): #подсчет остатков склада
    capacity=0
    date_sum=0
    for x in stock:
        for j in stock[x]:
            capacity+=j.volume
            date_sum+=int(j.date)
    return capacity,date_sum
def Evaluate_result(stock,racks):
    Remove_products(stock, racks)
    Stock_pr_print(stock)
    return Stock_result(stock)
#вывод ифнормации  по стеллажам после заполнения


values = [bench(lambda: rack_from_stock_backtrack()),
          bench(lambda: rack_from_stock_index()),
          bench(lambda: rack_from_stock_greed())]
capacity_values=[]
date_values=[]


#бэктрэкинг

racks_for_backtrack=[Rack_backtrack1,Rack_backtrack2,Rack_backtrack3]
print(len(temp))
pair=Evaluate_result(stock_backtrack,racks_for_backtrack)
capacity_values.append(pair[0])
date_values.append(pair[1])


#индексы
racks_for_index=[Rack_index1,Rack_index2,Rack_index3]
pair=Evaluate_result(stock_index,racks_for_index)
capacity_values.append(pair[0])
date_values.append(pair[1])
print(Rack_index1)
print(Rack_index2)
print(Rack_index3)

#жадная эвристика
racks_for_greed=[Rack_greed1,Rack_greed2,Rack_greed3]
pair=Evaluate_result(stock_greed,racks_for_greed)
capacity_values.append(pair[0])
date_values.append(pair[1])


#отрисовка данных на графиках
fig1=plt.figure(1,figsize=(10,5))
time=fig1.add_subplot(121)
capacity=fig1.add_subplot(122)
time.bar(['Backtrack(time)', 'Index(time)','Greed(time)'], values)
capacity.bar(['Backtrack(capacity)', 'Index(capacity)','Greed(capacity)'], capacity_values)
fig1.show()
plt.bar(['Backtrack(date)', 'Index(date)','Greed(date)'], date_values)
plt.show()
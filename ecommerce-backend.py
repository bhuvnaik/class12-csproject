import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Bhuvan123",
  database="enterprise"
)
mycursor=mydb.cursor()
def createadmin():
    x=input("Enter new admin ID: ")
    y=input("Enter new admin name: ")
    z=input("Enter new admin password: ")
    mycursor.execute("insert into admin values(%s,%s,%s)",(x,y,z))
    mydb.commit()
def createcustomer():
    s=input("Enter your name: ")
    a=input("Enter your address: ")
    c=input("Enter your Contact No: ")
    p=input("Create your password: ")
    mycursor.execute("select count(ID) from customer")
    l=mycursor.fetchone();
    mycursor.execute('''insert into customer values(%s,%s,%s,%s,%s,%s)'''
                     ,(l[0]+1,s,a,c,p,0.0))
    print("Your ID is ", l[0]+1)
    mydb.commit()
    print("Account created")
def createvendor():
    s=input("Enter your name: ")
    p=input("Create your password: ")
    mycursor.execute("select count(ID) from vendor")
    l=mycursor.fetchone();
    mycursor.execute("insert into vendor values(%s,%s,%s,0)",(l[0]+1,s,p))
    print("Your ID is ",l[0]+1,": ")
    mydb.commit();
    print("Account created")
def menu():
    print("Hello! Welcome")
    x= int(input('''Press 1. for customer 2. for vendor 3. for admin 4. for new customer 5. for new vendor: '''))
    if x==3:
        s=input("Enter admin ID: ")
        passwd=input("Enter admin password: ")
        mycursor.execute('''select ID,password from admin where ID=%s and 
                         password=%s''',(s,passwd))
        l=mycursor.fetchall()
        k=0
        try:
            k=len(l)
        except:
            pass
        if k!=0:
            while True:
                y=int(input("1.Add balance 2.Add admin 3.Extract balance: "))
                if y==1:
                    addbalance()
                elif y==2:
                    createadmin()
                elif y==3:
                    extractbalance()
                else:
                    print("Error!Try again")
                ans=input("EXIT? y/n: ")
                if ans=='y':
                    break
        else:
            print("Authorisation failed")
    elif x==1:
        s=input("Enter customer ID: ")
        passwd=input("Enter password: ")
        mycursor.execute('''select ID,password,balance from customer where 
                         ID=%s and password=%s''',(s,passwd))
        l=mycursor.fetchone()
        k=0
        try:
            k=len(l)
        except:
            pass
        if k!=0:
            if l[2]>0:
                while True:
                    y=int(input('''Do you wish to 1.Review orders 2.Place orders 3.Review balance 4.Exit: '''))
                    if y==1:
                        displayorders_Cust(s)
                        continue
                    elif y==3:
                        mycursor.execute('''select balance from customer 
                                         where ID=%s''',(s,))
                        l=mycursor.fetchone()
                        print("Your current balance is ",l[0],": ")
                        continue
                    elif y==4:
                        break
                    else:
                        pass
                    p=int(input('''Do you want to search or place order directly? 1/2: '''))
                    if p==2 or (p==1 and search()):
                        placeorder(s)
                        mycursor.execute('''select balance from customer where
                                         ID=%s''',(s,))
                        l=mycursor.fetchone()
                        print("Your current balance is ",l[0],": ")
            else:
                print("Insufficient balance")
        else:
            print("Authorisation failed")
    elif x==2:
        s=input("Enter vendor ID: ")
        passwd=input("Enter password: ")
        mycursor.execute('''select ID,password from vendor where ID=%s and 
                         password=%s''',(s,passwd))
        l=mycursor.fetchall()
        k=0
        try:
            k=len(l)
        except:
            pass
        if k!=0:
            while True:
                k=int(input('''1. Deliver order 2. Add product 3. Display orders 4. Review Balance 5. Delete product 6. Display products 7. Exit : '''))
                if k==2:
                    addproduct(s)
                elif k==1:
                    deliverorder(s)
                elif k==3:
                    displayorders(s)
                elif k==4:
                    mycursor.execute('''select balance from vendor where 
                                     ID=%s''',(s,))
                    l=mycursor.fetchone()
                    print("Your current balance is ",l[0],": ")
                elif k==5:
                    deleteproduct(s)
                elif k==6:
                    displayproduct(s)
                else:
                    break
        else:
            print("Authorisation failed")
    elif x==4:
        createcustomer()
    elif x==5:
        createvendor()
    else:
        print("Error! Try again")
def placeorder(m):
    x=input("Please enter your product with ID: ")
    n=input("Enter the quantity: ")
    try:
        mycursor.execute("select order_ID from orders order by order_ID")
        t=mycursor.fetchall()
        ans=mingap(t)
        mycursor.execute('''select price,vend_ID,delay from product where 
                         ID=%s''',(x,))
        k=mycursor.fetchone()
        mycursor.execute('''update customer set balance=balance-%s where ID 
                         =%s''',(k[0]*int(n),m))
        mycursor.execute('''update vendor set balance=balance+%s where 
                         ID =%s''',(k[0]*int(n),k[1]))
        mycursor.execute('''insert into orders values(%s,%s,%s,%s,%s,
                         CURDATE()+%s)''',(ans,m,x,n,k[1],k[2]))
        mydb.commit()
        print("Order placed")
    except:
        mydb.rollback()
        print("Error. Please Try again")
def deliverorder(l):
    s=input("Enter Order ID: ")
    m=input("Enter customer password: ")
    try:
        mycursor.execute('''Select * from customer inner join orders on 
                         orders.cust_ID=customer.ID where customer.password=%s 
                         and orders.order_ID=%s and 
                         orders.vend_ID=%s''',(m,s,l))
        p=mycursor.fetchall()
        k=0
        try:
            k=len(p)
        except:
            pass
        if k!=0:
            mycursor.execute('''delete from orders where order_ID=%s and 
                             vend_ID=%s''',(s,l))
            mydb.commit()
            print("Order delivered")
        else:
            print("Error. Please Try again")
    except Exception as e:
        mydb.rollback()
        print("Error. Please Try again")
        print(e)
def mingap(l):
    prev=1
    for i in l:
        if prev==i[0]:
            prev+=1
        else:
            break
    return prev
def addproduct(x):
    y=input("Enter your products name: ")
    z=input("Enter the price: ")
    d=input("Enter the delivery time in days: ")
    try:
        mycursor.execute("select ID from product order by ID")
        t=mycursor.fetchall()
        ans=mingap(t)
        mycursor.execute('''insert into product values(%s,%s,
                         %s,%s,%s)''',(ans,y,z,x,d))
        mydb.commit()
        print("Product added")
    except:
        mydb.rollback()
        print("Error. Please Try again")
def deleteproduct(x):
    try:
        y=input("Enter product_ID: ")
        mycursor.execute('''delete from product where ID=%s and 
                         vend_ID=%s''',(y,x))
        print("Successful update")
    except:
        mydb.rollback()
        print("Error. Please Try again")
def addbalance():
    x=input("Enter customer ID: ")
    b=input("Enter balance increment: ")
    try:
        mycursor.execute('''update customer set balance=balance+%s where 
                         ID=%s''',(b,x))
        mydb.commit()
        mycursor.execute("select count(ID) from customer where ID=%s",(x,))
        l=mycursor.fetchone()
        if l[0]!=0:
            print("Successful update")
        else:
            print("Record not found")
    except:
        mydb.rollback()
        print("Error. Please Try again")
def extractbalance():
    x=input("Enter vendor ID: ")
    b=input("Enter balance extraction: ")
    try:
        mycursor.execute('''update vendor set balance=balance-%s where 
                         ID=%s''',(b,x))
        mydb.commit()
        mycursor.execute("select count(ID) from vendor where ID=%s",(x,))
        l=mycursor.fetchone()
        if l[0]!=0:
            print("Successful update")
        else:
            print("Record not found")
    except:
        mydb.rollback()
        print("Error. Please Try again")
def displayorders(k):
    print("Your orders are:")
    print('''Order_ID\t\tCust_ID\t\tProduct_ID\t\tquantity\t\taddress\t\tcontact_num''')
    mycursor.execute('''Select orders.Order_ID,orders.cust_ID,orders.
                     product_ID,orders.quantity,customer.address,customer.
                     contact_num from orders inner join customer on orders.
                     cust_ID=customer.ID where vend_ID=%s order by 
                     orders.delivery,orders.order_ID''',(k,))
    t=mycursor.fetchall();
    for i in t:
        for j in i:
            print(j,end="\t\t\t\t")
        print()
def displayorders_Cust(k):
    print("Your orders are:")
    print(''''Order_ID\t\tVendor\t\tProduct ID\t\tQuantity\t\tPrice 
          per unit\t\tDelivery Date''')
    mycursor.execute('''Select orders.Order_ID,orders.vend_ID,orders.
                     product_ID,orders.quantity,product.price, orders.delivery 
                     from ((orders inner join customer on orders.cust_ID=
                            customer.ID) inner join product on product.ID=
                           orders.product_ID) where customer.ID=%s order by 
                     orders.delivery,orders.order_ID'''
                     ,(k,))
    t=mycursor.fetchall();
    for i in t:
        for j in i:
            print(j,end="\t\t\t\t")
        print()
def displayproduct(k):
    print("Your products are:")
    print("ProductID\t\tName\t\t\t    Price\t\t\tDelivery Time")
    mycursor.execute('''select ID,name,price,delay from product where 
                     vend_ID=%s''',(k,))
    t=mycursor.fetchall();
    for i in t:
        for j in i:
            print(j,end="\t\t\t\t")
        print()
def search():
    x=input("Please enter the keyword to search for: ")
    y=int(input("Include how many search results?"))
    mycursor.execute("select ID,name,price from product")
    l=mycursor.fetchall()
    k=[]
    for i in l:
        ans=LD(i[1],x)
        k.append((ans,i[0],i[1],i[2]))
    y = min(len(k),y)
    k.sort(key =compare)
    try:
        print("Product name\tProduct ID\tPrice")
        for i in range(0,y):
            m=k[i]
            print()
            print(m[2],"\t\t\t",m[1],"\t\t\t",m[3])
        return True
    except:
        print("Error! Please try again")
        return False
def LD(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
    res = min([LD(s[:-1], t)+1,
               LD(s, t[:-1])+1, 
               LD(s[:-1], t[:-1]) + cost])
    return res
def compare(x):
    return x[0]
while True:
    menu()
    y=input("Exit marketplace? y/n: ")
    if y=='y':
        break
mydb.close()
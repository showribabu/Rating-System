from flask import Flask,render_template,request,redirect
#from pymongo import MongoClient
import mysql.connector as mysql

#obj..
app=Flask(__name__)
mydb=mysql.connect(
    host='localhost',
    user='root',
    password='Ksb6419*',
    database='showri'
)
cursor=mydb.cursor()

amount=0
name=''
password=''
adhar=''
otcount=0
c=0



#handlers..
@app.route('/')
def func1():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def signin():
    return render_template('login.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/signe')
def signe():
    return render_template('signupe.html')
@app.route('/signs')
def signs():
    return render_template('signups.html')


@app.route('/lerror')
def lerror():
    return render_template('loginerror.html')

@app.route('/lsuccess')
def lsucess():
    return render_template('loginsuccess.html',n=name,a=adhar)

@app.route('/balance')
def balance():
    return redirect('/lbsuccess')
@app.route('/lbsuccess')
def lbsucess():
    global amount,otcount,adhar
    #amount get from table..
    s='select * from transaction'
    cursor.execute(s)
    d=cursor.fetchall()
    for i in d:
        if(i[0]==adhar):
            amount=int(i[1])
            otcount=int(i[2])
    
    return render_template('loginsuccess.html',n=name,a=adhar,b=amount,t='Amount is:')

@app.route('/status') 
def status():
    return redirect('/checks')  

@app.route('/trans')
def trans():
    return render_template('transaction.html') 

@app.route('/high')
def high():
    return render_template('high.html')
@app.route('/low')
def low():
    return render_template('low.html')

@app.route('/medium')
def medium():
    return render_template('medium.html')

@app.route('/ad')
def admin():
    return render_template('admin.html')



#actions..

#for signup
@app.route('/dt',methods=['post'])
def sdata():
    global amount,otcount
    amount=0
    otcount=0
    name=request.form['name'].strip()
    phone=request.form['phone'].strip()
    Domain=request.form['Domain'].strip()
    adhar=request.form['adhar'].strip()
    pin=request.form['pin'].strip()
    password=request.form['pass'].strip()
    sql='select * from customers'
    cursor.execute(sql)
    d=cursor.fetchall()
    for i in d:
        if i[3]==adhar:
            return redirect('/signe')
    #k={'name':name,'phone':phone,'password':password,'Domain':Domain,'adhar':adhar,'pin':pin}
    #sql='create table customers(name varchar(50),phone varchar(10) ,Domain varchar(50) ,adhar varchar(12) not null,pin varchar(10),password varchar(20)'
    #cursor.execute(sql)
    s2='insert into customers(name,phone,Domain,adhar,pin,password) values(%s,%s,%s,%s,%s,%s)'
    val=(name,phone,Domain,adhar,pin,password)
    cursor.execute(s2,val)
    mydb.commit()
    s3='insert into transaction(adhar,amount,otcount)values(%s,%s,%s)'
    v=(adhar,str(amount),str(otcount))
    cursor.execute(s3,v)
    mydb.commit()
    return redirect('/signs')

#for login


@app.route('/ld',methods=['post'])
def ldata():
    global adhar,password,name
    adhar=request.form['adhar'].strip()
    password=request.form['pass'].strip()
    name=request.form['name'].strip()
    #check login..based on adhar and pass
    sql='select * from customers'
    cursor.execute(sql)
    d=cursor.fetchall()
    for i in d:
        if(i[3]==adhar and i[5]==password):
            return redirect('/lsuccess')
    return redirect('/lerror')




#for check status
@app.route('/checks')
def checks():
    global amount,otcount,adhar
    #based on user tranctions status will update
    #if amount>..and otcount>..itcount>...
    #else if....
    s='select * from transaction'
    cursor.execute(s)
    d=cursor.fetchall()
    for i in d:
        if(i[0]==adhar):
            amount=int(i[1])
            otcount=int(i[2])
    
    if(amount>=10000 or otcount>=20):
        return render_template('high.html')
    if((amount>6000 and amount<10000) or (otcount>13 and otcount<20 )):
        return render_template('medium.html')
    if(amount<=6000 or otcount<=10):
        return render_template('low.html')
    

#for transaction data..

@app.route('/tdata',methods=['post'])
def tdata():
    global amount,otcount,adhar,c
    c=c+1
    tamt=request.form['amt']
    tamt=int(tamt)
    s='select * from transaction'
    cursor.execute(s)
    d=cursor.fetchall()
    for i in d:
        if(i[0]==adhar):
            amount=int(i[1])
            otcount=int(i[2])
    if(tamt>amount):
        #transaction error html page...
        return render_template('tfailure.html') 
    else:
        
        otcount=otcount+1
        amount=amount-tamt
        if(c>30):
            otcount=0
            
        s1='update transaction set amount=%s,otcount=%s where adhar=%s'
        v=(str(amount),str(otcount),str(adhar))
        cursor.execute(s1,v)
        mydb.commit()
        
        #transaction successhtml page...
        return render_template('tsuccess.html')

#add amount to account..
@app.route('/addb')
def addb():
    global amount,adhar,c,otcount
    c=c+1
    s='select * from transaction'
    cursor.execute(s)
    d=cursor.fetchall()
    for i in d:
        if(i[0]==adhar):
            amount=int(i[1])
    amount=amount+200
    s1='update transaction set amount=%s,otcount=%s where adhar=%s'
    v=(str(amount),str(otcount),str(adhar))
    cursor.execute(s1,v)
    mydb.commit()
    if(c>30):
        otcount=0
    return redirect('/lbsuccess')

    
    
@app.route('/adata',methods=['post'])
def adata():
    name=request.form['name']
    password=request.form['pass']
    s='select * from admin'
    cursor.execute(s)
    d=cursor.fetchall()
    for i in d:
        if(i[0]==name and i[1]==password):
            return render_template('admins.html')
    return render_template('admine.html')
    
@app.route('/access',methods=['post'])
def access():
    global amount,otcount,adhar
    f=0
    adhar=request.form['adhar']
    sql='select * from customers'
    cursor.execute(sql)
    d=cursor.fetchall()
    for i in d:
        if(i[3]==adhar):
            name=i[0]
            adhar=i[3]
            f=1
    if f==0:
        return render_template('admins.html',de='USER Details are Not Found')
    
    s='select * from transaction'
    cursor.execute(s)
    d=cursor.fetchall()
    for i in d:
        if(i[0]==adhar):
            amount=int(i[1])
            otcount=int(i[2])
    if(amount>=10000 or otcount>=20):
        
        return render_template('ahigh.html',n=name,a=adhar,t1='Name is',t2='Adhar number is',t3='Amount is',t4='Transactions count:',amt=amount,tc=otcount)
    if((amount>6000 and amount<10000) or (otcount>13 and otcount<20 )):
        
        return render_template('amedium.html',n=name,a=adhar,t1='Name is',t2='Adhar number is',t3='Amount is',t4='Transactions count:',amt=amount,tc=otcount)
    
    if(amount<=6000 or otcount<=10):
        
        return render_template('alow.html',n=name,a=adhar,t1='Name is',t2='Adhar number is',t3='Amount is',t4='Transactions count:',amt=amount,tc=otcount)
    
    
    
        
    

    
    



#server ..

if __name__=='__main__':
    app.run(debug=True)



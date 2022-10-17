"""
Routes and views for the flask application.
"""

import os
from datetime import datetime
from lib2to3.pgen2.token import NAME
from flask import render_template
from XueXi import app
from XueXi.DateEncoder import DateEncoder

from flask import Response, request,make_response
from XueXi.accessdb import accessdb

import glob
import  time
from decimal import *



@app.route('/everyday/<day>')
def everyday(day):
    """Renders the home page."""
    
    steps=accessdb.get_data("学习任务")
    dir =app.config.get("IMG_ROOT") 
    dir=os.path.join(dir,day)

    date=datetime.strptime(day,'%Y%m%d');
    riqi=str(date.month)+"月"+str(date.day)+"日"
    week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
    xingqi=week_list[date.weekday()]
    
    for item in steps:
        root=os.path.join(dir,str(item["ID"])+"-*.*")
        imgs = glob.glob(root)
        item["图片"]=[]
        miao2=0
        for filename in imgs:
            print(filename)            
            fileShort=os.path.basename(filename);
            print(fileShort) 
            miao1=os.path.getctime(filename)
            yongshi = (miao1-miao2)/(60)
            yongshi2=Decimal(yongshi).quantize(Decimal("0"))
            ctime =time.localtime(miao1);

            strtime=time.strftime("%H:%M",ctime)
            data={}
            data["name"]=fileShort;
            data["ctime"]=strtime;

            
            color = getColor(yongshi2)
            data["color"]=color;
            if yongshi2/60>10:
                data["yongshi"]=""
            else:
                data["yongshi"]=str(yongshi2)+"分";
            item["图片"].append(data)
            miao2=miao1;
    
    return render_template(
        'index.html',
        selectDay=day,
        steps=steps,
        title = riqi+"，"+xingqi

    )
    print(day)

def getColor(yongshi):
    if(yongshi/60)>10:
        return ""
    if(yongshi/60)>1:
        return "red"
    if(yongshi/60)>0.5:
        return "yellow"
    return "green"
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    # 默认当天
    day = datetime.now().strftime('%Y%m%d')
    #day="20220929"
    return everyday(day)
    
    steps=accessdb.get_data("学习任务")
    dir =app.config.get("IMG_ROOT") 
    
    for item in steps:
        root=dir+str(item["ID"])+"-*.*"
        imgs = glob.glob(root)
        item["图片"]=[]
        for filename in imgs:
            print(filename)
            fileShort=filename.replace(dir,"")
            print(fileShort)
            item["图片"].append(fileShort)

    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        steps=steps

    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

#定义接口地址为imageprocess
@app.route('/imageprocess', methods=['POST'])
def image_preprocess():
	#获取到post请求传来的file里的image文件
    image = request.files.get("fileVal")
    #获取到post请求里传来的form表单中的文件名字段
    data = request.form.get("filename")
    
    name=request.form["name"];
    type=request.form["type"];
    size=request.form["size"];
    stepid=request.form["stepid"];
    position=request.form["position"];
    selectDay=request.form["selectDay"];

    lastModifiedDate=request.form["lastModifiedDate"];    
    
    dir =app.config.get("IMG_ROOT") 
    root=os.path.join(dir,selectDay,stepid+"-*.*")
    imgs = glob.glob(root)  
    ext=os.path.splitext(name)[-1]#扩展名是上传文件名的扩展名

    shortName = stepid+"-"+str(len(imgs)+int(position)).zfill(2)+ext

    print(data)
    print(image)
    if image is None:
        return "nothing found"
    #获取到的文件名，将文件存放到对应的位置
    #image.save("./photo/"+name+".png")
    dir = create_folder("每日打卡",selectDay)
    file_full =os.path.join(dir,shortName)
    image.save(file_full)

    sqlInsert = r"""

    INSERT INTO
    图片上传(学习任务ID,目录日期,文件名)
VALUES
    (?,?,?)
    """
    data = accessdb.sql_nodata(sqlInsert,stepid,selectDay,shortName)

    return {"status":"图片上传成功"}

# _*_coding:utf-8_*_

def create_folder(path,day = datetime.now().strftime('%Y%m%d')):
    # 年-月-日 时：分：秒
    #now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ## 年
    #year =datetime.now().strftime('%Y')
    ## 年-月
    #month = datetime.now().strftime('%Y-%m')
    ## 年-月-日
    ##day = datetime.now().strftime('%Y-%m-%d')
    #day = datetime.now().strftime('%Y%m%d')
    # 时：分：秒
    #hour = datetime.now().strftime("%H:%M:%S")
    #print(now_time + "\n"+day + "\n" + hour)
 
    #foldername = path+"\\"+year+"\\"+month+"\\"+day
    foldername = path+"\\"+day
    # print(pwd)
    # 文件路径
    word_name = os.path.exists(foldername)
    # 判断文件是否存在：不存在创建
    if not word_name:
        os.makedirs(foldername)
    return foldername


 
@app.route('/display/img/<riqimulu>/<string:filename>', methods=['GET'])
def display_img(riqimulu,filename):
    request_begin_time = datetime.today()
    print("request_begin_time", request_begin_time)
    
    dir =app.config.get("IMG_ROOT") 
    IMG_PATH=os.path.join(dir,riqimulu)
    fileName =os.path.join(IMG_PATH, filename)
    #fileName=IMG_PATH
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(fileName, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpg'
            return response
    else:
        pass

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from web import models
import hashlib
import datetime
import time
import random
def index(request):

	query = models.Produce.objects.order_by("-結束日期").all()
	context = []
	for index in query:

		context.append({})
		context[len(context)-1]["ID"] = index.id
		context[len(context)-1]["名稱"] = index.名稱
		context[len(context)-1]["分類"] = index.分類
		if (index.狀態 == "ed"):
			context[len(context)-1]["狀態"] = "已收成"
			context[len(context)-1]["狀態顏色"] = "red"
			
		elif(index.狀態 == "ing"):
			context[len(context)-1]["狀態"] = "等待結果"
			context[len(context)-1]["狀態顏色"] = "green"
		else:
			context[len(context)-1]["狀態"] = "還是種子"
			context[len(context)-1]["狀態顏色"] = "brown"
		#context[len(context)-1]["金額"] = index.金額
		
		#context[len(context)-1]["開始日期"] = index.開始日期
		#context[len(context)-1]["結束日期"] = index.結束日期
		if (models.Produce_meta.objects.all().filter(Produce_id = index.id).filter(項目 = "excerpts")):
			temp =  models.Produce_meta.objects.all().filter(Produce_id = index.id).filter(項目 = "excerpts")[0]
			context[len(context)-1]["內容"] = temp.內容
		if (models.Produce_meta.objects.all().filter(Produce_id = index.id).filter(項目 = "FeaturedImage")):
			temp =  models.Produce_meta.objects.all().filter(Produce_id = index.id).filter(項目 = "FeaturedImage")[0]
			context[len(context)-1]["特色圖片"] = temp.內容
	return render(request,"index.html",{"context":context})

def farmer_Account(request):
	if 'Account_token' in request.session:
		userid = models.Member_Farmer_token.objects.get(token = request.session['Account_token']).Farmer.id
		user = models.Member_Farmer.objects.get(id = userid)
		context = {}
		context["姓名"] = user.姓名
		context["帳號"] = user.帳號
		context["生日"] = user.生日
		context["農資"] = user.農資日期
		context["所在地"] = user.所在地
		context["信箱"] = user.信箱
		context["註冊日期"] = user.註冊日期
		context["簡介"] = user.簡介
		print(context)
	
		return render(request,'farmer_info.html',{'context':context})
	if request.method == 'GET':
		return render(request,'Account.html')
	elif request.method =='POST':
		account = request.POST["inputAccount"]
		password = request.POST["inputPassword"]
		if (account and password):
			try:
				t = models.Member_Farmer.objects.get(帳號=account)
			except Exception as  e:
				return render(request,'Account.html',{'error_message':"資料錯誤!"})
			
			print(t.密碼)
			print(password)
			if t.密碼 == password:
				h = hashlib.new('md5')
				print(t.帳號)
				h.update(bytes(t.帳號,'utf-8'))
				h.update(bytes(str(time.time()),'utf-8'))
				hash_token = h.hexdigest()
				insert_token = models.Member_Farmer_token(Farmer=t,token=hash_token,IP = request.META.get('REMOTE_ADDR'),有效時間=datetime.datetime.now()+datetime.timedelta(hours=6),更新時間=datetime.datetime.now())
				insert_token.save()
				request.session['Account_token'] = hash_token
				return render(request,'Account.html')
			else:
				return render(request,'Account.html',{'error_message':"資料錯誤!"})
		return render(request,'Account.html',{'error_message':"資料未輸入!"})
	return render(request,'Account.html')
def logout(request):
	if request.method == "POST":
		if 'Account_token' in request.session:
			request.session.pop("Account_token")
	return redirect('/login')
def ALL_Farmer(request):
	query = models.Member_Farmer.objects.all()
	context = []
	for item in query:
		context.append({})
		context[len(context)-1]["ID"] = item.id
		context[len(context)-1]["姓名"] = item.姓名
		context[len(context)-1]["簡介"] = item.簡介
		if (models.Member_Farmer_meta.objects.all().filter(Farmer_id = item.id).filter(項目 = "FeaturedImage")):
			temp =  models.Member_Farmer_meta.objects.all().filter(Farmer_id = item.id).filter(項目 = "FeaturedImage")[:1]
			for i in temp:
				context[len(context)-1]["特色圖片"] = i.內容

	return render(request,'農夫大集合.html',{"context":context})

def farmer_introduction(request,userId):
	return render(request,"farmer_introduction.html")

def product_introduction(request,productId):
	query = models.Produce.objects.get(id = productId)
	query2 = models.Produce_meta.objects.all().filter(Produce_id = productId)
	query3 = models.Member_Farmer_meta.objects.all().filter(Farmer_id = query.Farmer.id)
	context = {}
	context["ID"] = query.Farmer.id
	context["農夫"] = query.Farmer.姓名
	context["產地"] = query.Farmer.所在地
	context["名稱"] = query.名稱
	context["分類"] = query.分類
	if (query.狀態 == "ed"):
		context["狀態"] = "已收成"
		context["狀態按鈕"] = "我要買"
		
	elif(query.狀態 == "ing"):
		context["狀態"] = "等待結果"
		context["狀態按鈕"] = "我要預購"
	else:
		context["狀態"] = "還是種子"
		context["狀態按鈕"] = "我想要"
	context["金額"] = query.金額
	context["內容"] = query.內容
	context["農夫照片"] = [item.內容 for item in query3 if item.項目 == "FeaturedImage"][0]
	context["圖片集"] = []
	for item in query2:
		try:
			if item.項目 == "FeaturedImage":
				context["特色圖片"] = item.內容
			elif item.項目 == "images" and len(context["圖片集"])<3:
				context["圖片集"].append(item.內容)
		except Exception as e:
			print(e)
	query = models.Produce.objects.all()
	count = len(query)
	now_c = 0
	st = 0
	produce_list = []
	contain=[]
	while now_c < 3 and st <100:
		t = query[random.randint(0,len(query)-1)]
		if t.id != int(productId) and t.id not in contain:
			now_c+=1
			st +=1
			contain.append(t.id)
			produce_list.append({})
			produce_list[len(produce_list)-1]["ID"] = t.id
			produce_list[len(produce_list)-1]["名稱"] = t.名稱
			produce_list[len(produce_list)-1]["分類"] = t.分類
			if (models.Produce_meta.objects.all().filter(Produce_id = t.id).filter(項目 = "excerpts")):
				temp =  models.Produce_meta.objects.all().filter(Produce_id = t.id).filter(項目 = "excerpts")[0]
				produce_list[len(produce_list)-1]["內容"] = temp.內容
			if (models.Produce_meta.objects.all().filter(Produce_id = t.id).filter(項目 = "FeaturedImage")):
				temp =  models.Produce_meta.objects.all().filter(Produce_id = t.id).filter(項目 = "FeaturedImage")[0]
				produce_list[len(produce_list)-1]["特色圖片"] = temp.內容
	

	return render(request,"Produce_introduction.html",{"context":context,"produce_list":produce_list})


def about(request,userId):
	query = models.Member_Farmer.objects.get(id = userId)
	context = {}
	context["姓名"] = query.姓名
	context["生日"] = query.生日

	return render(request,"personal-about.html")
def story(request,userId):
	return render(request,"personal-story.html")


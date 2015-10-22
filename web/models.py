from django.db import models

# Create your models here.
class Member_Farmer(models.Model):
	姓名 = models.CharField(max_length=50)
	生日 = models.DateTimeField()
	農資日期 = models.DateField()
	所在地 = models.CharField(max_length=255)
	信箱 = models.EmailField(unique=True)
	註冊日期 = models.DateTimeField(auto_now=True)
	帳號 = models.CharField(max_length=255,unique=True)
	密碼 = models.CharField(max_length=255)
	簡介 = models.TextField(default="")
	def __str__(self):
		return "%s %s " % (self.帳號,self.姓名)

class Member_Farmer_meta(models.Model):
	Farmer = models.ForeignKey(Member_Farmer)
	項目 = models.CharField(max_length=255)
	內容 = models.CharField(max_length=255)
	def __str__(self):
		return "%s %s " % (self.Farmer.帳號,self.項目)


class Member_Seed(models.Model):
	姓名 = models.CharField(max_length=50)
	生日 = models.DateTimeField()
	信箱 = models.EmailField(unique=True)
	註冊日期 = models.DateTimeField(auto_now=True)
	帳號 = models.CharField(max_length=255,unique=True)
	密碼 = models.CharField(max_length=255)
	簡介 = models.TextField(default="")
	def __str__(self):
		return "%s %s " % (self.帳號,self.姓名)

class Member_Seed_meta(models.Model):
	Seed = models.ForeignKey(Member_Seed)
	項目 = models.CharField(max_length=255)
	內容 = models.CharField(max_length=255)
	def __str__(self):
		return "%s %s " % (self.Seed.帳號,self.項目)
		
class Produce(models.Model):
	Farmer = models.ForeignKey(Member_Farmer)
	名稱 = models.CharField(max_length=255)
	分類 = models.CharField(max_length=50)
	狀態 = models.CharField(max_length=50)
	金額 = models.FloatField()
	內容 = models.TextField()
	開始日期 = models.DateTimeField()
	結束日期 = models.DateTimeField()
	def __str__(self):
		return self.名稱

class Produce_meta(models.Model):
	Produce = models.ForeignKey(Produce)
	項目 = models.CharField(max_length=255)
	內容 = models.CharField(max_length=255)
	def __str__(self):
		return "%s %s " % (self.Produce.名稱,self.項目)

class shopping_cart(models.Model):
	Seed = models.OneToOneField(Member_Seed)
	加入日期 = models.DateTimeField(auto_now=True)
	Produces = models.ManyToManyField(Produce)
	def __str__(self):
		return self.Seed.姓名

class Member_Farmer_token(models.Model):
	Farmer = models.ForeignKey(Member_Farmer)
	token = models.CharField(max_length=255)
	IP = models.CharField(max_length=50)
	有效時間 = models.DateTimeField()
	建立時間 = models.DateTimeField(auto_now=True)
	更新時間 = models.DateTimeField()
	def __str__(self):
		return self.Farmer.帳號

class Member_Seed_token(models.Model):
	Seed = models.ForeignKey(Member_Seed)
	token = models.CharField(max_length=255)
	IP = models.CharField(max_length=50)
	有效時間 = models.DateTimeField()
	建立時間 = models.DateTimeField(auto_now=True)
	更新時間 = models.DateTimeField()
	def __str__(self):
		return self.Seed.帳號
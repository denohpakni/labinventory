from django.db import models
from django import forms
from .backend import Factory
import datetime

class Category(models.Model):
	'''Category whre all items are included'''
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField(max_length=400)

	def __str__(self):
		return self.name

class Product(models.Model):
	''' Item class'''	
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	name = models.CharField(max_length=50, unique=True)
	brand = models.CharField(max_length=50)
	Catalog_No = models.CharField(max_length=100, blank=True)
	description = models.TextField(max_length=400)
	pkey = models.PositiveSmallIntegerField(unique=True, blank=True, help_text="Unique Product Key or Catalogue number. Current P.Key is unique")
	quantity = models.PositiveSmallIntegerField(help_text="Initial quantity value. Do no try to create a produt that already exists.")
	price = models.DecimalField(max_digits=8, decimal_places=2, help_text= " ex: $ 127.99 * Just type numbers")
	
	
	def __str__(self):
		return (f"{self.name} -  {self.category}  -")

	

class HistConf(models.Model):
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	actual= models.PositiveSmallIntegerField()
	transition = models.IntegerField()
	total = models.PositiveSmallIntegerField()
	user = models.CharField(max_length=50)
	time = models.DateTimeField()

	@classmethod
	def create(cls, actual, transition, pid, user=''):
		hist = cls(actual=actual, transition=transition, total=actual+transition, user=user, time=datetime.datetime.now(), item=pid)
		return hist

	def __str__(self):
		return f"Before: {self.actual} Change: {self.transition} After: {self.total} by user: {self.user} at {self.time}"


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['name', 'brand', 'category','Catalog_No', 'description', 'pkey', 'quantity', 'price']
		localized_fields=('price',)
		widgets = {
			'name' : forms.TextInput(attrs={'class' : 'fname', 'placeholder': 'Required', 'required': True, 'title':'name'}),
			'brand': forms.TextInput(attrs={'class' : 'fname', 'placeholder': 'Empty', 'required': False, 'title':'brand'}),
			'category': forms.Select(attrs={'class': 'fname', 'required': True}),
			'description': forms.Textarea(attrs={'class': 'fname desc', 'placeholder': 'Add a description','title': 'description', 'rows': 3}),
			'pkey': forms.NumberInput(attrs={'class': 'fname', 'decimal_places':'0', 'required': True}),
			'Catalog_No':forms.TextInput(attrs={'class':'fname','placeholder': 'Required','required': False,'title':'Catalogue Number'}),
			'quantity': forms.NumberInput(attrs={'class': 'fname', 'decimal_places': '0' , 'required': True}),
			'price': forms.NumberInput(attrs={'class': 'fname', 'max_digits': '8', 'decimal_places': '2', 'required': True, 'placeholder': "$ 127.99"}),
			}

		




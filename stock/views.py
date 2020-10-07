from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
#importng/exporting data
from tablib import Dataset
from .resources import ProductResource

# Create your views here.
from .models import Product, ProductForm, HistConf
from .backend import Factory


def index(request):
	all_products = Product.objects.all()
	context = Factory.get_product_context(Product)
	
	# context = {'products': all_products,
	# 			'total_products': len(all_products),
	# 			'total_value': Factory.value_calculate(all_products),
	# 			'total_items': Factory.total_items(all_products)}
	return render(request, 'stock/stock_home.html', context)


@login_required(login_url='/login/')
def manage(request):
	form = ProductForm()
	sucess= None
	if request.method == 'POST':
		form  = ProductForm(request.POST)
		print(request.POST)
		if form.is_valid():
			form.save()
			sucess= f"{form.cleaned_data['name']} created in database with Pkey: {form.cleaned_data['pkey']}"
			form = ProductForm()
		else:
			form.errors

	rand_pkey = Factory.get_pkey_unique(Product)
	form.fields['pkey'].widget.attrs.update({'placeholder':rand_pkey})
	form.fields['pkey'].initial=rand_pkey
	context = {'form': form,	
			 	'sucess': sucess,
			 	'all_products': Product.objects.all(),
			 	}
	return render(request, 'stock/stock_manage.html', context)


@login_required(login_url='/login/')
def deleted(request, pkey):
	form = ProductForm()
	sucess= None
	rand_pkey = Factory.get_pkey_unique(Product)
	form.fields['pkey'].widget.attrs.update({'placeholder':rand_pkey})
	form.fields['pkey'].initial=rand_pkey
	context = {'form': form,
			 	'all_products': Product.objects.all(),
			 	}
	context['pkey']= pkey
	Product.objects.filter(pkey=pkey)[0].delete()

	return render(request, 'stock/stock_manage.html', context)


@login_required(login_url='/login/')
def detail(request, pk):
	item = Product.objects.filter(pk=pk)[0]
	sucess= None
	remove= None
	
	if request.method=="POST":
		qnt = int(item.quantity)
		get = int(request.POST.get('quantity'))
		if qnt+get<0:
			print('error')
		else:
			HistConf.create(qnt, get, item, request.user).save()
			item.quantity = qnt+get			
			item.save()

			if get>0:
				sucess = f"{get} items Added to product - {item.name} -"
			else:
				remove = f"{-get} items Removed to product - {item.name} -"


	context ={
			"pk": pk,
			"item": item,
			"value": item.quantity * item.price,
			'sucess': sucess,
			'remove': remove,
			'history': HistConf.objects.filter(item=pk)[::-1],
		
			}
	return render(request, 'stock/stock_detail.html', context)


def history(request):
	context ={'history':HistConf.objects.all()[::-1]}
	return render(request, 'stock/stock_history.html', context)

def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = ProductResource()
        dataset = Dataset()
        new_employees = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(new_employees.read().decode('utf-8'),format='csv')
            result = employee_resource.import_data(dataset, dry_run=True)                                                                 
        elif file_format == 'JSON':
            imported_data = dataset.load(new_employees.read().decode('utf-8'),format='json')
            # Testing data import
            result = employee_resource.import_data(dataset, dry_run=True) 

        if not result.has_errors():
            # Import now
            employee_resource.import_data(dataset, dry_run=False)

    return render(request, 'import.html')    
 

def export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        employee_resource = ProductResource()
        dataset = employee_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response   

    return render(request, 'export.html')



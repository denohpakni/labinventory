from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from .models import Product, ProductForm, HistConf
from .backend import Factory


@login_required(login_url='/login/')
def index(request):
	all_products = Product.objects.all()
	context = Factory.get_product_context(Product)
	
	# context = {'products': all_products,
	# 			'total_products': len(all_products),
	# 			'total_value': Factory.value_calculate(all_products),
	# 			'total_items': Factory.total_items(all_products)}
	return render(request, 'stock_home.html', context)


@user_passes_test(lambda user: user.is_superuser, login_url='/login/')
def manage(request):
	form = ProductForm()
	sucess= None
	if request.method == 'POST':
		form  = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			sucess= f"{form.cleaned_data['name']} created in database with Pkey: {form.cleaned_data['pkey']}"
			form = ProductForm()

	rand_pkey = Factory.get_pkey_unique(Product)
	form.fields['pkey'].widget.attrs.update({'placeholder':rand_pkey})
	form.fields['pkey'].initial=rand_pkey
	context = {'form': form,	
			 	'sucess': sucess,
			 	'all_products': Product.objects.all(),
			 	}
	return render(request, 'stock_manage.html', context)


@user_passes_test(lambda user: user.is_superuser, login_url='/login/')
def deleted(request, pkey):
	if request.method != 'POST':
		return redirect('manage')
	product = get_object_or_404(Product, pkey=pkey)
	name = product.name
	product.delete()
	messages.success(request, f'{name} was deleted.')
	return redirect('manage')


@login_required(login_url='/login/')
def detail(request, pk):
	item = get_object_or_404(Product, pk=pk)
	sucess= None
	remove= None
	
	if request.method == "POST":
		try:
			change = int(request.POST.get('quantity', ''))
		except (TypeError, ValueError):
			messages.error(request, 'Enter a whole number for the stock change.')
			return redirect('detail', pk=item.pk)
		if change == 0:
			messages.error(request, 'Enter a non-zero stock change.')
			return redirect('detail', pk=item.pk)
		with transaction.atomic():
			item = Product.objects.select_for_update().get(pk=item.pk)
			updated = item.quantity + change
			if updated < 0 or updated > 32767:
				messages.error(request, 'Stock must stay between 0 and 32,767 units.')
				return redirect('detail', pk=item.pk)
			HistConf.objects.create(actual=item.quantity, transition=change, total=updated, user=request.user.get_username(), time=timezone.now(), item=item)
			Product.objects.filter(pk=item.pk).update(quantity=F('quantity') + change)
		if change > 0:
			messages.success(request, f'{change} items added to {item.name}.')
		else:
			messages.success(request, f'{-change} items removed from {item.name}.')
		return redirect('detail', pk=item.pk)


	context ={
			"pk": pk,
			"item": item,
			"value": item.quantity * item.price,
			'sucess': sucess,
			'remove': remove,
			'history': HistConf.objects.filter(item=item).order_by('-time', '-pk'),
		
			}
	return render(request, 'stock_detail.html', context)


@login_required(login_url='/login/')
def history(request):
	context ={'history':HistConf.objects.select_related('item', 'item__category').order_by('-time', '-pk')}
	return render(request, 'stock_history.html', context)



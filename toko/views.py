from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import Produk
from .models import Customer
from .models import Itempesan
from .models import IDpesan
from .models import Pesan

#Apabil from .... import * (Semua) pada simbol bintang akan membuat akses pencarian menjadi berat pada Django

def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		pesan, created = Pesan.objects.get_or_create(customer=customer, complete=False)
		#filter digunakan untuk mengambil query lebih dari 1
		items = pesan.itempesan_set.all()
		cartItems = pesan.get_cart_items 
	else:
		items =[]
		pesan ={'get_cart_total':0, 'get_cart_items':0}
		cartItems = pesan ['get_cart_items']

	produks = Produk.objects.all()
	context = {'Produks':produks, 'cartItems':cartItems, 'pengiriman':False}
	return render(request, 'toko1/store.html', context)

def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		pesan, created = Pesan.objects.get_or_create(customer=customer, complete=False)
		items=pesan.itempesan_set.all()
		cartItems = pesan.get_cart_items 
	else:
		items =[]
		pesan ={'get_cart_total':0, 'get_cart_items':0}
		cartItems = pesan ['get_cart_items']

	context = {'items':items, 'pesan':pesan, 'cartItems':cartItems, 'pengiriman':False}
	return render(request, 'toko1/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		pesan, created = Pesan.objects.get_or_create(customer=customer, complete=False)
		items=pesan.itempesan_set.all()
		cartItems = pesan.get_cart_items 
	else:
		#Create empty cart for now non-logged in user
		items =[]
		pesan ={'get_cart_total':0, 'get_cart_items':0}
		cartItems = pesan ['get_cart_items']

	context = {'items':items, 'pesan':pesan, 'cartItems':cartItems, 'pengiriman':False}
	return render(request, 'toko1/checkout.html', context)

#advanechURL
def updateItem(request):
	data = json.loads(request.body)
	produkId = data['produkId']
	action = data['action']

	print('action:', action)
	print('produkId:', produkId)

	customer = request.user.customer
	produk = Produk.objects.get(id=produkId)
	pesan, created = Pesan.objects.get_or_create(customer=customer, complete=False)

	itemPesan, created = Itempesan.objects.get_or_create(pesan=pesan, produk=produk)
	if action == 'add':
		itemPesan.jumlah = (itemPesan.jumlah + 1)
	elif action == 'remove':
		itemPesan.jumlah = (itemPesan.jumlah - 1)

	itemPesan.save()

	if itemPesan.jumlah <= 0:
		itemPesan.delete()

	return JsonResponse('Item telah ditambahkan', safe=False)

def prosesPesan(request):
	transaksi_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		pesan, created = Pesan.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		pesan.transaksi_id = transaksi_id

		if total == pesan.get_cart_total:
			pesan.complete = True
		pesan.save()

		if pesan.pengiriman == True:
			IDpesan.objects.create(
			customer=customer,
			pesan=pesan,
			idgame=data['pengiriman']['idgame'],
			servergame=data['pengiriman']['servergame'],
			)
	else:
			print("User is'n logged in..")
	return JsonResponse('Pembayaran Selesai!',safe=False)
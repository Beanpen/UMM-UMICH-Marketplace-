# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .forms import uploadImgForm, postForm, OrderForm, confirmationForm, updateForm
from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.conf import settings


import os
import json
from pathlib import Path
import google.generativeai as genai
import PIL.Image

def details(request, pk):

    user = request.user
    context = {}
    details = {}

    with connection.cursor() as cursor:
        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid,
        p_quantity, p_description, p_date, price, category
        FROM Product where p_id = %s;'''%pk)
        row = cursor.fetchall()[0]

    details['name'] = row[1]
    details['order_url'] = '/products/order/%s'%pk
    details['pic_link'] = row[2]
    seller = row[3]
    user_url = '/homepage/user/%s'%seller
    details['user_url'] = user_url
    details['seller'] = seller
    details['quantity'] = row[4]
    details['description'] = row[5]
    details['date']= row[6]
    details['price'] = row[7]
    details['category'] = row[8]

    if seller == user.username:
        context['denied'] = 1

    context['detail'] = details

    template = 'details.html'
    return render(request, template, context)



@login_required
def post(request):
    user = request.user
    template = 'post.html'
    success = {'success': 1}

    if request.method == 'POST':
        upload_form = uploadImgForm(request.POST, request.FILES)
        if upload_form.is_valid():
            myfile = request.FILES['Upload_your_item_picture']
            # print("myfile", myfile)
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            file_path_within_storage = fs.url(filename)
            
            local_absolute_path = str(settings.MEDIA_ROOT + "/" +myfile.name)
            # print( "MEDIA_ROOT", settings.MEDIA_ROOT)
            # print("local_absolute_path", local_absolute_path)
            # gemini API to get other product info in a json format
            nextFormJson = apicallFuc(local_absolute_path)
            # print(nextFormJson)

            context = {
                'product_name': nextFormJson.get('product_name'),
                'description': nextFormJson.get('short_description'),
                'quantity': int(nextFormJson.get('quantity')),
                'price': nextFormJson.get('price_suggestion'),
                'category': nextFormJson.get('category'),
            }

            post_form = postForm(context)
            return render(request, template, {'upload_form': upload_form, 'post_form': post_form, 'file_path_within_storage': file_path_within_storage})

        post_form = postForm(request.POST)
        if post_form.is_valid():
            productname = post_form.cleaned_data.get('product_name')
            discription = post_form.cleaned_data.get('description')
            quantity = int(post_form.cleaned_data.get('quantity'))
            price = post_form.cleaned_data.get('price')
            category = post_form.cleaned_data.get('category') #note here should be changed in future
            file_path_within_storage = request.POST.get('file_path_within_storage', '')

            now = datetime.now().replace(microsecond=0)
            # print("file_path_within_storage", file_path_within_storage)
            with connection.cursor() as cursor:
                cursor.execute('''SELECT p_id FROM Product ORDER BY p_id DESC LIMIT 1;''')
                row = cursor.fetchall()

                if row == ():
                    cursor.execute('''INSERT INTO Product (p_id, sellerid,
                    p_name, p_quantity, p_description, p_date, product_pic_link, category, price) values
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s);''', (0, user,
                    productname, quantity, discription, now, file_path_within_storage, category, price))

                else:
                    pid = int(row[0][0]) + 1
                    cursor.execute('''INSERT INTO Product (p_id, sellerid,
                    p_name, p_quantity, p_description, p_date, product_pic_link, category, price) values
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s);''', (pid, user,
                    productname, quantity, discription, now, file_path_within_storage, category, price))
            return render(request, 'post.html', success)
        
    else:
        upload_form = uploadImgForm()
        post_form = postForm()

    return render(request, template, {'upload_form': upload_form, 'post_form': post_form})



@login_required
def update(request, pk):

        template = 'update.html'
        success = {'success': 1}
        details = {}

        with connection.cursor() as cursor:
            cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid,
            p_quantity, p_description, p_date, price
            FROM Product where p_id = %s;'''%pk)
            row = cursor.fetchall()[0]

        pid = row[0]
        details['name'] = row[1]
        details['order_url'] = '/products/order/%s'%pk
        details['pic_link'] = row[2]
        seller = row[3]
        user_url = '/homepage/user/%s'%seller
        details['user_url'] = user_url
        details['seller'] = seller
        details['quantity'] = row[4]
        details['description'] = row[5]
        details['date']= row[6]
        details['price'] = row[7]

        if request.method == 'POST':
            form = updateForm(request.POST)
            if form.is_valid():

                discription = form.cleaned_data.get('new_description')
                quantity = int(form.cleaned_data.get('new_quantity'))
                price = form.cleaned_data.get('new_price')

                with connection.cursor() as cursor:
                        cursor.execute('''UPDATE  Product
                        set p_quantity = %s, p_description = %s, price = %s
                        where p_id = %s;''',
                        (quantity, discription, price, pk))
                return render(request, 'update.html', success)

        else:
            form = updateForm()

        context = {'detail': details, 'form': form}
        return render(request, template, context)



@login_required
def order(request, pk):
    user = request.user
    details = {}
    with connection.cursor() as cursor:
        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid,
        p_quantity, p_description, p_date, price
        FROM Product where p_id = %s;'''%pk)
        row = cursor.fetchall()[0]

    pid = row[0]
    details['name'] = row[1]
    details['order_url'] = '/products/order/%s'%pk
    details['pic_link'] = row[2]
    seller = row[3]
    user_url = '/homepage/user/%s'%seller
    details['user_url'] = user_url
    details['seller'] = seller
    details['quantity'] = row[4]
    details['description'] = row[5]
    details['date']= row[6]
    details['price'] = row[7]
    template = 'order.html'

    success = {'success': 1}
    denied = {'denied': 1}
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            quantity = int(form.cleaned_data.get('quantity'))
            now = datetime.now().replace(microsecond=0)

            if quantity > int(details['quantity']):
                return render(request, 'order.html', denied)
            else:

                with connection.cursor() as cursor:

                    cursor.execute('''SELECT o_id FROM OrderRecord ORDER BY o_id DESC LIMIT 1;''')

                    row = cursor.fetchall()
                    if row == ():
                        cursor.execute('''INSERT INTO OrderRecord (o_id, productid, productseller,
                        o_quantity, buyerid, o_date, tradeinfo, trade_result) values
                        (%s, %s, %s, %s, %s, %s, %s, %s);''', (0, pid, seller,
                        quantity, user, now, message, 0))

                    else:

                        oid = int(row[0][0]) + 1
                        cursor.execute('''INSERT INTO OrderRecord (o_id, productid, productseller,
                        o_quantity, buyerid, o_date, tradeinfo, trade_result) values
                        (%s, %s, %s, %s, %s, %s, %s, %s);''', (oid, pid, seller,
                        quantity, user, now, message, 0))

            return render(request, 'order.html', success)

    else:
        form = OrderForm()
    context = {'detail': details, 'form': form}
    return render(request, template, context)


@login_required
def confirmation(request, pk):

    details = {}

    with connection.cursor() as cursor:

        cursor.execute('''SELECT o_id, productid, o_quantity, buyerid, tradeinfo
                    FROM OrderRecord WHERE o_id = %s'''%pk)
        sell_record = dictfetchall(cursor)[0]
        pid = sell_record['productid']

        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid,
        p_quantity, p_description, p_date, price
        FROM Product where p_id = %s;'''%pid)
        row = cursor.fetchall()[0]

    product_id = row[0]
    details['name'] = row[1]
    details['pic_link'] = row[2]
    details['quantity_left'] = row[4]
    details['quantity_acquired'] = sell_record['o_quantity']
    buyer_url = '/homepage/user/%s'%sell_record['buyerid']
    details['buyer_url'] = buyer_url
    details['buyer'] = sell_record['buyerid']
    details['tradeinfo'] = sell_record['tradeinfo']
    template = 'confirmation.html'
    success = {'success': 1}

    if request.method == 'POST':
        form = confirmationForm(request.POST)
        if form.is_valid():
            result = form.cleaned_data.get('Options')
            with connection.cursor() as cursor:

                cursor.execute('''UPDATE OrderRecord SET trade_result = %s where
                o_id = %s''',(result, pk))
                # if success, cut product quantity by one
                if int(result) == 1:
                    cursor.execute('''UPDATE Product SET p_quantity = p_quantity - %s where
                    p_id = %s''',(sell_record['o_quantity'], product_id))
                    # if no stock, decline all order records
                    # cursor.execute('''SELECT p_quantity
                    # FROM Product where p_id = %s;'''%product_id)
                    # res = dictfetchall(cursor)[0]
                    # quantity_left = res['p_quantity']
                    # if quantity_left == 0:
                    #     cursor.execute('''UPDATE OrderRecord SET trade_result = %s where
                    #     productid = %s and o_id <> %s''',(2, product_id, pk))

                    ## replaced by lingyun's terliger

            return render(request, template, success)
    else:
        form = confirmationForm()

    context = {'detail': details, 'form': form}

    return render(request, template, context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]



# from google.colab import userdata
genai.configure(api_key=settings.GOOGLE_API_KEY)


def apicallFuc(imgUrl):
    prompt = """You are a super exprienced second hand market agent, and you received the image your client. Please provide your client with the product name, quantity, price suggestion (just a number), category (electronic_device, health_beauty, fashion, sports, groceries, food, book, stationary, others) and short description for the product. Output in json format (don't show the word json)"""
    model = genai.GenerativeModel('gemini-pro-vision')
    image = PIL.Image.open(imgUrl)
    response = model.generate_content([prompt, image])
    # print(response.text)
    result = json.loads(response.text)
    return result





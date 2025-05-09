# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.shortcuts import render
from django.db import connection
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from difflib import SequenceMatcher
from collections import Counter
from django.http import JsonResponse

# Debug for timezone difference.
# from django.conf import settings
# Print out the TIME_ZONE setting
# print("Client Timezone:", settings.TIME_ZONE)

def home(request):
    user = request.user
    user_products = []
    all_products = []
    if user.is_authenticated:
        # Fetch user's search history
        with connection.cursor() as cursor:
            cursor.execute('''SELECT content FROM Search_Record where user = %s''', [user])
            user_products = [row['content'] for row in dictfetchall(cursor)]

    # Fetch all products
    with connection.cursor() as cursor:
        cursor.execute("SELECT p_id, p_name FROM Product WHERE p_quantity > 0")
        all_products = [(row['p_id'], row['p_name']) for row in dictfetchall(cursor)]

    # Recommend products based on user's search history
    combined_recommend, recommend1, recommend1_url = recommend_products(user_products, all_products)

    # Fetch popular sellers
    with connection.cursor() as cursor:
        cursor.execute("SELECT username FROM auth_user")
        popular_seller = dictfetchall(cursor)
    for user in popular_seller:
        user['get_absolute_url'] = reverse('user-view', args=[str(user['username'])])

    # Fetch all categories
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT category FROM Product")
        all_categories = [row[0] for row in cursor.fetchall()]

    # Fetch products for current page with pagination
    offset = int(request.GET.get('offset', 0))
    products = fetch_products(offset)

    context = {
        "popular_seller": popular_seller,
        "products": products,
        'combined_recommend': combined_recommend,
        'recommend1': recommend1,
        'recommend1_url': recommend1_url,
        "all_categories": all_categories,
        "num_total_products": len(all_products),
        "num_displayed_products": len(products),
    }
    return render(request, 'home.html', context)


def get_total_products(request):
    # Fetch total number of products
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM Product WHERE p_quantity > 0")
        total_products = cursor.fetchone()[0]
    
    # Return total number of products as JSON response
    return JsonResponse({'totalProducts': total_products})

    

def recommend_products(user_products, all_products):
    list_of_similarity = [[] for _ in range(len(user_products))]
    recommended_products = []
    recommend_urls = []
    product_ids = []
    
    # If the user has search history
    if user_products:
        # Compute similarities between user products and all available products
        for k, target_product in enumerate(user_products):
            for product_id, product_name in all_products:
                similarity_score = similar(product_name, target_product)
                list_of_similarity[k].append((product_id, similarity_score))
        
        # Select the top similar products
        for similarities in list_of_similarity:
            top_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)[:2]
            product_ids.extend([product_id for product_id, _ in top_similarities])
        
        # Fetch additional information for recommended products from the database
        # print(f'product_ids: {product_ids}')
        product_ids = first_n(product_ids, 4)
        # print(f'product_ids: {product_ids}')

        # First display the similar products
        with connection.cursor() as cursor:
            for product_id in product_ids:
                cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid
                                    FROM Product WHERE p_id = %s''', [product_id])
                recommended_product = dictfetchall(cursor)
                recommended_products.extend(recommended_product)
                recommend_urls.append('/products/details/%s' % recommended_product[0]['p_id'])

    # If not enough (<4), then display the most recent products
    existing_count = len(recommended_products)
    missing_count = 4 - existing_count
    if existing_count < 4:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid
                                FROM Product WHERE p_quantity > 0 ORDER BY p_id DESC LIMIT %s''', missing_count)
            recommended_products.extend(dictfetchall(cursor))
            for i in range(existing_count, 4):
                if (len(recommended_products) < i+1):
                    break
                # print('recommended_products: ', recommended_products)
                recommend_urls.append('/products/details/%s' % recommended_products[i]['p_id'])

    # Recommend1 is the first product in the list, and reccomend_* includes the rest three
    # I did this because the html template is designed to display the first product separately
    recommend_urls = ['/products/details/%s' % product['p_id'] for product in recommended_products]
    recommend1 = recommended_products[0] if recommended_products else {}
    recommend1_url = '/products/details/%s' % recommend1.get('p_id', '') if recommend1 else ''
    recommended_products = recommended_products[1:]
    recommend_urls = recommend_urls[1:]
    
    combined_recommend = list(zip(recommended_products, recommend_urls))
    return combined_recommend, recommend1, recommend1_url


def fetch_products(offset):
    # print(f'offset: {offset}')
    with connection.cursor() as cursor:
        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid, price
                          FROM Product WHERE p_quantity > 0 ORDER BY p_id DESC LIMIT 5 OFFSET %s''', [offset])
        products = dictfetchall(cursor)

    for product in products:
        product['url'] = '/products/details/%s' % product['p_id']

    return products


def fetch_products_with_pagination(request):
    offset = request.GET.get('offset', 0)  # Get the offset parameter from the request
    offset = int(offset)  # Convert offset to an integer if necessary

    products = []
    with connection.cursor() as cursor:
        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid, price
                          FROM Product WHERE p_quantity > 0 ORDER BY p_id DESC LIMIT 5 OFFSET %s''', [offset])
        products = dictfetchall(cursor)

    for product in products:
        product['url'] = '/products/details/%s' % product['p_id']

    return JsonResponse(products, safe=False)


def search(request):

    content = request.GET.get('content')
    sellername = request.GET.get('sellername')
    category = request.GET.get('category')
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    price_max = request.GET.get('price_max')
    price_min = request.GET.get('price_min')
    
    query_sentence = "SELECT * FROM Product WHERE (p_name REGEXP %s OR p_description REGEXP %s) "
    query_list = [content, content]
    if sellername != "":
        query_sentence += "AND sellerid REGEXP %s "
        query_list += [sellername]
    if category != "":
        query_sentence += "AND category = %s "
        query_list += [category]
    if startdate != "" and enddate != "":
        query_sentence += "and p_date Between %s AND %s"
        query_list += [startdate + " 00:00:00", enddate + " 23:59:59"]

    with connection.cursor() as cursor:
        cursor.execute(query_sentence, query_list)
        product_list = dictfetchall(cursor)
        cursor.execute("SELECT DISTINCT category FROM Product")
        all_categories = [category[0] for category in cursor.fetchall()]
        if request.user.is_authenticated:
            cursor.execute("INSERT INTO Search_Record VALUES (%s, %s, %s)",
                           [request.user, content, '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())])
    categories = set()
    for product in product_list:
        product['detail'] = '/products/details/%s' %product['p_id']
        categories.add(product['category'])
    categories = list(categories)

    return render(request, 'results.html', {'post_list': product_list,
                                            'categories': categories,
                                            'all_categories': all_categories})


@login_required
def user_view(request, pk):
    if request.method == 'POST':
        rate = request.POST.get("rate", "")
        rating_user = request.POST.get("rating_user", "")
        feedback_user = request.POST.get("feedback_user", "")
        product = request.POST.get("product", "")
        Feedback_id = request.POST.get("Feedback_id", "")
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Rating ORDER BY r_id DESC LIMIT 1")
            last_record = dictfetchall(cursor)
            if not last_record:
                last_id = 0
            else:
                last_id = last_record[0]["r_id"]

            cursor.execute("INSERT INTO Rating VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           [last_id + 1, rate, datetime.datetime.now().date(), rating_user, feedback_user, product, Feedback_id])
    template = 'profile_other.html'
    with connection.cursor() as cursor:
        cursor.execute("SELECT p_name, p_id, product_pic_link, p_quantity FROM Product WHERE sellerid = %s", [pk])
        products = dictfetchall(cursor)
        cursor.execute("SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY','')); ")
        cursor.execute("SELECT F.f_id, p_id, p_name, F.f_date, F.f_content, F.FeedbackUser, score FROM("
                        "SELECT p_id, p_name, Feedback.f_id, Feedback.f_date, Feedback.FeedbackUser, Feedback.f_content, AVG(Rating.r_score) AS score FROM Feedback, auth_user, Product, Rating "
                        "WHERE Feedback.f_id = Rating.Feedback_id "
                        "AND seller = %s "
                        "GROUP BY Feedback.f_id "
                        "ORDER BY score DESC) AS F ",
                       [pk])
        comment_list = dictfetchall(cursor)
        cursor.execute("SELECT FeedbackUser, f_content, f_date, f_id, p_name, p_id "
                       "FROM Feedback, Product "
                       "WHERE Seller = %s "
                       "AND Feedback.Product = Product.p_id",
                       [pk])
        comment_list2 = dictfetchall(cursor)
        comment_ids = set()
        for comment in comment_list:
            comment_ids.add(comment['f_id'])
        for comment in comment_list2:
            if comment['f_id'] not in comment_ids:
                comment['score'] = 'None'
                comment_list += [comment]
        for comment in comment_list:
            comment['date_ago'] = (datetime.datetime.now().date() - comment['f_date']).days

        for comment in comment_list:
            cursor.execute("SELECT * FROM Rating WHERE Feedback_id = %s AND RatingUser = %s;", [int(comment['f_id']), request.user])
            rating_value = dictfetchall(cursor)
            if not rating_value:
                comment['current_rating'] = 0
            else:
                comment['current_rating'] = rating_value[0]['r_score']
        for comment in comment_list:
            cursor.execute("SELECT profile_pic FROM auth_user WHERE username = %s ", [comment['FeedbackUser']])
            comment['profile_pic'] = cursor.fetchall()[0][0]

        for product in products:
            product['detail'] = '/products/details/%s' %product['p_id']
    seller = {'seller': '''this is %s's public profile page'''%pk}
    context = {'product_list': products,
               'comment_list': comment_list,
               'seller': seller}
    return render(request, template, context)


def stats(request):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT * FROM Product
            Where p_id IN
            (SELECT productid FROM (
            SELECT productid, count(o_id) FROM OrderRecord
            WHERE trade_result = 0
            GROUP BY productid
            ORDER BY count(o_id) DESC
            LIMIT 5)AS COUNT);''')
        pop_product = dictfetchall(cursor)

        cursor.execute('''SELECT productseller FROM (
            SELECT count(o_id), productseller FROM OrderRecord
            GROUP BY productseller
            ORDER BY count(o_id) DESC
            LIMIT 5) AS COUNT;''')

        pop_seller = dictfetchall(cursor)
    for i in range(len(pop_product)):
        # print(f'pop_product[i]: {pop_product[i]}')
        url = '/products/details/%s'%pop_product[i]['p_id']
        pop_product[i]['url'] = url

    for user in pop_seller:
        user['get_absolute_url'] = '/homepage/user/%s'%user['productseller']

    template = 'stats.html'
    context = {}
    context['pop_product'] = pop_product
    context['pop_seller'] = pop_seller
    return render(request, template, context)


def first_n(productid, num):
    # Count the occurrences of each product ID
    counts = Counter(productid)
    
    # Select the most common product IDs
    most_common = counts.most_common(num)
    
    # Extract the product IDs from the most_common list
    selected_product_ids = [pid for pid, _ in most_common]
    
    return selected_product_ids

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def chat(request = None):
    return render(request, "chat.html", {})

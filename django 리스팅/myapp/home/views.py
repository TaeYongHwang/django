from django.shortcuts import render, redirect
from myapp.item.models import Product
from myapp.item.models import Ingredient
from .forms import ProductQueryForm
from .forms import ProductDetailForm

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def show_ingredient(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredients.html', {'ingredients': ingredients})


# 상품 목록 조회하기
def product_list(request):
    form = ProductQueryForm()

    if request.GET.get('skin_type') is not None:
        skin_type = request.GET.get('skin_type')
        # category = request.GET.get('category')
        page = request.GET.get('page')
        # exclude_in = request.GET.get('exclude_ingredient')
        # include_in = request.GET.get('include_ingredient')
        products, fitness = products_print(skin_type, 50, None, page, None, None)
        return render(request, 'product_list.html', {'form': form, 'products': products, 'fitness': fitness})

    return render(request, 'product_list.html', {'form': form})


# 상품 상세 정보 조회하기
def product_detail(request, id):
    form = ProductDetailForm()

    product = Product.objects.get(id=id)
    base_url = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/"
    image_dir = "image/"
    thumbnail_dir = "thumbnail/"
    image_url = base_url + image_dir
    thumbnail_url = base_url + thumbnail_dir
    # 추천 상품 3개 보여주는 경우
    if request.GET.get('skin_type') is not None:
        skin_type = request.GET.get('skin_type')
        recommended, _ = products_print(skin_type, 3)
        return render(request, 'product_detail.html', {'product': product, 'image_url': image_url,
                                                       'thumbnail_url': thumbnail_url, 'recommended': recommended})

    return render(request, 'product_detail.html', {'form': form, 'product': product, 'image_url': image_url,
                                                   'thumbnail_url': thumbnail_url})


# -------------inner function in product_list---------------
# 보여질 50개의 제품
def products_print(skin_type, num_of_product=50, category=None, page=None, exclude_str=None, include_str=None):
    if page is None:
        page = 1
    else:
        page = int(page)

    products = set_products(category, exclude_str, include_str)
    id_score = {}  # 제품 id에 현재 피부타임 점수를 key-value로 저장

    for product in products:
        score = 0
        ingredients = product.ingredients.split(',')
        for ingredient in ingredients:
            cur_ingre = Ingredient.objects.get(name=ingredient)
            if Ingredient.get_effect(cur_ingre, skin_type) == 'O':
                score += 1
            elif Ingredient.get_effect(cur_ingre, skin_type) == 'X':
                score -= 1
        id_score[product.id] = score


    # id_score을 score를 기준으로 정렬 후, 페이지에 맞는 요소들을 꺼내옴
    sorted_id_score = sorted(id_score.items(), reverse=True, key=lambda id_score:id_score[1])

    id_list = []
    ans_list = []
    for i in range(num_of_product*(page-1), num_of_product*page):
        if i < len(sorted_id_score):
            id_list.append(sorted_id_score[i][0])
            ans_list.append(Product.objects.filter(id=sorted_id_score[i][0]))

    return Product.objects.filter(id__in=id_list), ans_list


# 상품 카테고리가 정해진 경우 해당 상품만 list로 반환
def set_products(category, exclude_str, include_str):
    products = []
    if category is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=category)
    if exclude_str is not None:
        products = exclude_ingredient(products, exclude_str)
    if include_str is not None:
        products = include_ingredient(products, include_str)
    return products


# 제외할 성분을 하나라도 갖는 경우 리스트에서 제외시킴
def exclude_ingredient(products, exclude_str):
    delete_list =[]
    exclude_list = exclude_str.split(',')
    for product in products:
        is_delete = False
        ingredients = product.ingredients.split(',')
        for ingredient in ingredients:
            if isdelete is True:
                break
            for exclude in exclude_lst:
                if ingredient == exclude:
                    is_delete = True
                if isdelete is True:
                    break
        if is_delete is True:
            delete_list.append(product.id)

    products = products.exclude(id__in=delete_list)

    return products


# 포함할 성분을 하나라도 포함하지 않은 경우 리스트에서 제외시킴
def include_ingredient(products, include_str):
    delete_list = []
    include_list = include_str.split(',')
    for product in products:
        is_delete = False
        ingredients = product.ingredients.split(',')
        for ingredient in ingredients:
            is_include = False
            for include in include_list:
                if include == ingredient:
                    is_include = True
                if is_include is True:
                    break

            if is_include is False:
                is_delete = True
        if is_delete is True:
            delete_list.append(product.id)

    products = products.exclude(id__in=delete_list)
    return products


# 재료명과 피부타입이 주어지면, 점수를 반환해줌
# ingredient : Ingredient class
# type : oily dry sensitive
def ingredient_effect(ingredient, skin_type):
    if ingredient.get_effect(skin_type) == 'O':
        return 1
    elif ingredient.get_effect(skin_type) == 'X':
        return -1
    else:
        return 0



        





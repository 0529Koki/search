from django.shortcuts import render, get_object_or_404, redirect
from search_app.models import Product, Category
from search_app.forms import ProductForm, SearchForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from .utils import search_amazon_products

# Amazon 商品検索ビュー
def amazon_product_search_view(request):
    query = request.GET.get('q', '')
    if query:
        # Amazon API を使って商品を検索
        response_data = search_amazon_products(query)
        return JsonResponse({'data': response_data}, safe=False)
    else:
        return JsonResponse({'error': '検索クエリが指定されていません。'}, status=400)

# 商品作成ビュー
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'meal_planner.html', {'form': form})  # テンプレートを変更

# 商品詳細ビュー
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

# 商品編集ビュー
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'meal_planner.html', {'form': form, 'product': product})  # テンプレートを変更

# 商品削除ビュー
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

# 商品一覧ビュー
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store_search.html', {'products': products})

# 検索ビュー（meal_search.html に対応）
def search_view(request):
    form = SearchForm(request.GET or None)
    results = Product.objects.all()  # クエリセットの初期化

    # 検索クエリの処理
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = results.filter(name__icontains=query)

    # カテゴリフィルタリング
    category_name = request.GET.get('category')
    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            results = results.filter(category_id=category.id)
        except Category.DoesNotExist:
            results = results.none()  # 存在しないカテゴリの場合、結果を空にする

    # 価格のフィルタリング（最低価格・最高価格）
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        results = results.filter(price__gte=min_price)
    if max_price:
        results = results.filter(price__lte=max_price)

    # 並び替え処理
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        results = results.order_by('price')
    elif sort_by == 'price_desc':
        results = results.order_by('-price')

    # ページネーション処理
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'meal_search.html', {'form': form, 'page_obj': page_obj, 'results': results})

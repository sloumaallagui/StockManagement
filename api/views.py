from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from .models import Group,Product,Primary,Base
from django.views.decorators.csrf import csrf_exempt

# import packages for excel export
import xlwt



# Create your views here.

# ***************************** Group apis ***************************
# add a new group

import xlwt

def export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="groups.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Groups')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Group', 'Product', 'Base']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    groups = Group.objects.all()
    for group in groups:
        row_num += 1
        ws.write(row_num, 0, group.name, font_style)
        products = Product.objects.filter(group=group.id)
        for product in products:
            row_num += 1
            ws.write(row_num, 1, "Nom:", font_style)
            ws.write(row_num, 2, product.name, font_style)
            ws.write(row_num, 3, "Ref:", font_style)
            ws.write(row_num, 4, product.ref, font_style)
            ws.write(row_num, 5, "Quantité:", font_style)
            ws.write(row_num, 6, product.quantity, font_style)
            ws.write(row_num, 7, "Matière première:", font_style)
            primaries = Primary.objects.filter(product=product.id)
            for primary in primaries:
                row_num += 1
                ws.write(row_num, 7, "Nom:", font_style)
                ws.write(row_num, 8, primary.name, font_style)
                ws.write(row_num, 9, "Stock1:", font_style)
                ws.write(row_num, 10, primary.stock1, font_style)
                ws.write(row_num, 11, "Stock2:", font_style)
                ws.write(row_num, 12, primary.stock2, font_style)
                ws.write(row_num, 13, "Stock3:", font_style)
                ws.write(row_num, 14, primary.stock3, font_style)
        ws.write(row_num, 15, "Bases:", font_style)
        bases = Base.objects.filter(group=group.id)
        for base in bases:
            row_num += 1
            ws.write(row_num, 15, "Base Nom:", font_style)
            ws.write(row_num, 16, base.name, font_style)
    
    wb.save(response)
    return response


 

@csrf_exempt
def group_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        group = Group.objects.create(name = name)
        data = {'id': group.id, 'name': group.name}
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# delete a group
@csrf_exempt
def group_delete(request, group_id):
    if request.method == 'DELETE':
        group = get_object_or_404(Group, pk=group_id)
        group.delete()
        return JsonResponse({'message': 'Group  deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# update a group
@csrf_exempt
@api_view(['PUT'])
def group_update(request, group_id):
    if request.method == 'PUT':
        group = get_object_or_404(Group, pk=group_id)
        group.name = request.data.get('name') if request.data.get('name') else group.name
        group.save()
        data = {'id': group.id, 'name': group.name}
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


   
# get all groups paginated by page begin and page size empty for all
def group_list(request):
    group_name = request.GET.get('group_name')
    page_begin = int(request.GET.get('page_begin', 0))
    page_size = int(request.GET.get('page_size', 5))
    
    if request.method == 'GET':
        groups = Group.objects.all()

        if group_name:
            groups = groups.filter(name__icontains=group_name)

        total_pages = groups.count() if page_size > 0 else 1

        if page_size > 0:
            groups = groups[page_begin:page_begin + page_size]

        data = {'items': [{'id': group.id, 'name': group.name} for group in groups], 'total_pages': total_pages}

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

#get all group
def group_list_all(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        data = [{'id': group.id, 'name': group.name} for group in groups]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



# get group detail by id
def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    data = {'id': group.id, 'name': group.name}
    return JsonResponse(data)


#get all primarys by group
def group_primary_list(request, group_id):
    products = Product.objects.filter(group=group_id)
    primarys = Primary.objects.filter(product__in=products)
    data = [{'id': primary.id, 'name': primary.name, 'ref': primary.ref, 'product': primary.product.id, 'product_name':primary.product.name} for primary in primarys]
    return JsonResponse(data, safe=False)

#get all products by group
def group_product_list(request, group_id):
    products = Product.objects.filter(group=group_id)
    data = [{'id': product.id, 'name': product.name, 'ref': product.ref, 'group': product.group.id, 'group_name':product.group.name} for product in products]
    return JsonResponse(data, safe=False)

# get all bases by group
def base_list_by_group(request, group_id):
    bases = Base.objects.filter(group=group_id)
    data = [{'id': base.id, 'name': base.name, 'group': base.group.id, 'group': base.group.name} for base in bases]
    return JsonResponse(data, safe=False)


# ***************************** Product apis ***************************
# add a new product
@csrf_exempt
def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        ref = request.POST.get('ref')
        quentity = request.POST.get('quantity')
        group_id = request.POST.get('group_id')
        group = get_object_or_404(Group, pk=group_id)
        product = Product.objects.create(name = name, ref = ref, group = group)
        data = {'id': product.id, 'name': product.name, 'ref': product.ref, 'group': product.group.id}
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# delete a product
@csrf_exempt
def product_delete(request, product_id):
    if request.method == 'DELETE':
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return JsonResponse({'message': 'Product  deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# update a product
@csrf_exempt
@api_view(['PUT'])
def product_update(request, product_id):
    if request.method == 'PUT':
        product = get_object_or_404(Product, pk=product_id)
        product.name = request.data.get('name') if request.data.get('name') else product.name
        product.ref = request.data.get('ref') if request.data.get('ref') else product.ref
        product.quantity = request.data.get('quantity') if request.data.get('quantity') else product.quantity
        product.group = get_object_or_404(Group, pk=request.data.get('group_id')) if request.data.get('group_id') else product.group
        product.save()
        data = {'id': product.id, 'name': product.name, 'ref': product.ref,'quantity': product.quantity, 'group_id': product.group.id}
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# get all products
def product_list(request):
    product_name = request.GET.get('product_name')
    page_begin = int(request.GET.get('page_begin', 0))
    page_size = int(request.GET.get('page_size', 5))
    
    if request.method == 'GET':
        products = Product.objects.all()

        if product_name:
            products = products.filter(name__icontains=product_name) 

        total_pages = products.count() if page_size > 0 else 1

        if page_size > 0:
            products = products[page_begin:page_begin + page_size]

        data = {'items': [{'id': product.id, 'name': product.name,'ref':product.ref, "quantity": product.quantity, "group_name": product.group.name , "group_id": product.group.id} for product in products], 'total_pages': total_pages}

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)








# get product detail by id
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    data = {'id': product.id, 'name': product.name, 'ref': product.ref, 'group_id': product.group.id, 'group_name': product.group.name}
    return JsonResponse(data)

# search product by name
def product_search(request, product_name):
    products = Product.objects.filter(name__icontains=product_name)
    data = [{'id': product.id, 'name': product.name, 'ref': product.ref, 'group_id': product.group.id, 'group_name': product.group.name} for product in products]
    return JsonResponse(data, safe=False)
# get all product
def product_list_all(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = [{'id': product.id, 'name': product.name} for product in products]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# get all primarys by product
def product_primary_list(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    primarys = Primary.objects.filter(product=product)
    data = [{'id': primary.id, 'name': primary.name, 'stock1': primary.stock1, 'stock2': primary.stock2, 'stock3': primary.stock3, 'product': primary.product.id} for primary in primarys]
    return JsonResponse(data, safe=False)



# ***************************** Primary apis ***************************
# add a new primary
@csrf_exempt
def primary_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        stock1 = request.POST.get('stock1')
        stock2 = request.POST.get('stock2')
        stock3 = request.POST.get('stock3')
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        primary = Primary.objects.create(name = name, stock1 = stock1, stock2 = stock2, stock3 = stock3, product = product)
        data = {'id': primary.id, 'name': primary.name, 'stock1': primary.stock1, 'stock2': primary.stock2, 'stock3': primary.stock3, 'product_id': primary.product.id, "product_name":primary.product.name }
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# delete a primary
@csrf_exempt
def primary_delete(request, primary_id):
    if request.method == 'DELETE':
        primary = get_object_or_404(Primary, pk=primary_id)
        primary.delete()
        return JsonResponse({'message': 'Primary  deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# update a primary
@csrf_exempt
@api_view(['PUT'])
def primary_update(request, primary_id):
    if request.method == 'PUT':
        primary = get_object_or_404(Primary, pk=primary_id)
        primary.name = request.data.get('name') if  request.data.get('name') else primary.name
        primary.stock1 = request.data.get('stock1') if request.data.get('stock1') else primary.stock1
        primary.stock2 = request.data.get('stock2') if request.data.get('stock2') else primary.stock2
        primary.stock3 = request.data.get('stock3') if request.data.get('stock3') else primary.stock3
        product_id = request.data.get('product_id') if request.data.get('product_id') else primary.product.id
        product = get_object_or_404(Product, pk=product_id)
        primary.product = product
        primary.save()
        data = {'id': primary.id, 'name': primary.name, 'stock1': primary.stock1, 'stock2': primary.stock2, 'stock3': primary.stock3, 'product': primary.product.id}
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# get all primarys
def primary_list(request):
    primary_name = request.GET.get('primary_name')
    page_begin = int(request.GET.get('page_begin', 0))
    page_size = int(request.GET.get('page_size', 5))
    
    if request.method == 'GET':
        primarys = Primary.objects.all()

        if primary_name:
            primarys = primarys.filter(name__icontains=primary_name) 

        total_pages = primarys.count() if page_size > 0 else 1

        if page_size > 0:
            primarys = primarys[page_begin:page_begin + page_size]

        data = {'items': [{'id': primary.id, 'name': primary.name,'stock1':primary.stock1, "stock2": primary.stock2,"stock3": primary.stock3, "product_name": primary.product.name , "product_id": primary.product.id} for primary in primarys], 'total_pages': total_pages}

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)





# get primary detail by id
def primary_detail(request, primary_id):
    primary = get_object_or_404(Primary, pk=primary_id)
    group = get_object_or_404(Group, pk=primary.group.id)
    data = {'id': primary.id, 'name': primary.name, 'stock1': primary.stock1, 'stock2': primary.stock2, 'stock3': primary.stock3, 'product_id': primary.product.id, 'product_name': primary.product.name, 'group': group.id, 'group_name': group.name}
    return JsonResponse(data)

# search primary by name
def primary_search(request, primary_name):
    primarys = Primary.objects.filter(name__icontains=primary_name)
    data = [{'id': primary.id, 'name': primary.name, 'stock1': primary.stock1, 'stock2': primary.stock2, 'stock3': primary.stock3, 'product': primary.product.id,'product_name': primary.product.name, 'group': group.id, 'group_name': group.name} for primary in primarys]
    return JsonResponse(data, safe=False)


# ***************************** Base apis ***************************
# add a new base
@csrf_exempt
def base_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        group_id = request.POST.get('group_id')
        group = get_object_or_404(Group, pk=group_id)
        base = Base.objects.create(name = name, group = group)
        data = {'id': base.id, 'name': base.name, 'group_id': base.group.id}
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# delete a base
@csrf_exempt
def base_delete(request, base_id):
    if request.method == 'DELETE':
        base = get_object_or_404(Base, pk=base_id)
        base.delete()
        return JsonResponse({'message': 'Base  deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# update a base
@csrf_exempt
@api_view(['PUT'])
def base_update(request, base_id):
    if request.method == 'PUT':
        base = get_object_or_404(Base, pk=base_id)
        base.name = request.data.get('name') if  request.data.get('name') else base.name
        group_id = request.data.get('group_id') if request.data.get('group_id') else base.group.id
        group = get_object_or_404(Group, pk=group_id) 
        base.group = group
        base.save()
        data = {'id': base.id, 'name': base.name, 'group': base.group.id}
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# get all bases
def base_list(request):
    base_name = request.GET.get('base_name')
    page_begin = int(request.GET.get('page_begin', 0))
    page_size = int(request.GET.get('page_size', 5))
    
    if request.method == 'GET':
        bases = Base.objects.all()

        if base_name:
            products = bases.filter(name__icontains=base_name) 

        total_pages = bases.count() if page_size > 0 else 1

        if page_size > 0:
            bases = bases[page_begin:page_begin + page_size]

        data = {'items': [{'id': base.id, 'name': base.name,"group_name": base.group.name , "group_id": base.group.id} for base in bases], 'total_pages': total_pages}

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



# get base detail by id
def base_detail(request, base_id):
    base = get_object_or_404(Base, pk=base_id)
    data = {'id': base.id, 'name': base.name, 'group': base.group.id, 'group_name': base.group.name}
    return JsonResponse(data)

# search base by name
def base_search(request, base_name):
    bases = Base.objects.filter(name__icontains=base_name)
    data = [{'id': base.id, 'name': base.name, 'group': base.group.id} for base in bases]
    return JsonResponse(data, safe=False)





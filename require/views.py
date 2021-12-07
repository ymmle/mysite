from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Require, RequireType,ReadNum
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import Commentform


# Create your views here.
def get_require_common_data(requires_all_list,request):
    paginator = Paginator(requires_all_list, settings.EACH_PAGE_REQUIRE_NUMBERS)  # 每10篇进行分页
    page_num = request.GET.get('page', 1)  # 获取页码参数（GET请求）
    page_of_requires = paginator.get_page(page_num)
    current_page_num = page_of_requires.number  # 获取当前页码

    # 获取当前页前后各两页的页码范围
    page_range = list(range(max(1, current_page_num - 2), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    require_dates = Require.objects.dates('created_time', 'month', order='DESC')
    require_dates_dict = {}
    for require_date in require_dates:
        require_count = Require.objects.filter(created_time__year = require_date.year, created_time__month=require_date.month).count()
        require_dates_dict[require_date] = require_count

    context = {}
    context['requires'] = page_of_requires.object_list
    context['page_of_requires'] = page_of_requires
    context['require_types'] = RequireType.objects.annotate(require_count = Count('require'))
    context['page_range'] = page_range
    context['require_dates'] = require_dates_dict
    return context


def require_list(request):
    requires_all_list = Require.objects.all()
    context = get_require_common_data(requires_all_list,request)
    return render(request, 'require/require_list.html', context)


def require_detail(request, require_pk):
    require = get_object_or_404(Require, pk=require_pk)
    if not request.COOKIES.get('require_%s_readed' % require_pk):
        if ReadNum.objects.filter(require=require).count():
            readnum = ReadNum.objects.get(require=require)
        else:
            readnum = ReadNum(require=require)
        readnum.read_num += 1
        readnum.save()
    require_content_type = ContentType.objects.get_for_model(require)
    comments = Comment.objects.filter(content_type=require_content_type,object_id=require.pk, parent = None)

    context = {}
    context['previous_require'] = Require.objects.filter(created_time__gt=require.created_time).last()
    context['next_require'] = Require.objects.filter(created_time__lt=require.created_time).first()
    context['require'] = require
    context['comments'] = comments.order_by('-comment_time')
    context['comment_form'] = Commentform(initial={'content_type':require_content_type.model,'object_id':require_pk, 'reply_comment_id':'0'})
    response = render(request, 'require/require_detail.html', context)
    response.set_cookie('require_%s_readed' % require_pk,'true')
    return response


def requires_with_type(request, require_type_pk):
    require_type = get_object_or_404(RequireType, pk=require_type_pk)
    requires_all_list = Require.objects.filter(require_type=require_type)
    context = get_require_common_data(requires_all_list,request)
    context['require_type'] = require_type
    return render(request, 'require/require_with_type.html', context)


def requires_with_date(request,year,month):
    requires_all_list = Require.objects.filter(created_time__year=year,created_time__month=month)
    context = get_require_common_data(requires_all_list,request)
    context['requires_with_date'] = '%s-%s' %(year,month)
    return render(request, 'require/require_with_date.html', context)
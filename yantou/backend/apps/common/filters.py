"""
通用过滤器
提供通用过滤器基类和常用过滤方法
"""
import django_filters
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseFilterSet(django_filters.FilterSet):
    """
    通用过滤器基类
    提供日期范围过滤、多字段搜索等通用功能
    """
    # 通用搜索字段
    search = django_filters.CharFilter(method='filter_search', help_text=_('多字段搜索'))
    
    # 通用日期范围过滤
    created_at_start = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte', help_text=_('创建时间开始'))
    created_at_end = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte', help_text=_('创建时间结束'))
    updated_at_start = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte', help_text=_('更新时间开始'))
    updated_at_end = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte', help_text=_('更新时间结束'))
    
    # 通用排序
    ordering = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('id', 'id'),
        ),
        label=_('排序字段')
    )
    
    class Meta:
        abstract = True
    
    def filter_search(self, queryset, name, value):
        """
        多字段搜索（默认实现）
        子类可以重写此方法以实现自定义搜索逻辑
        
        Args:
            queryset: 查询集
            name: 字段名
            value: 搜索值
            
        Returns:
            QuerySet: 过滤后的查询集
        """
        if not value:
            return queryset
        
        # 默认搜索字段（子类可以重写 get_search_fields 方法）
        search_fields = self.get_search_fields()
        if not search_fields:
            return queryset
        
        # 构建 Q 对象
        q_objects = models.Q()
        for field in search_fields:
            q_objects |= models.Q(**{f'{field}__icontains': value})
        
        return queryset.filter(q_objects).distinct()
    
    def get_search_fields(self):
        """
        获取搜索字段列表
        子类可以重写此方法以指定要搜索的字段
        
        Returns:
            list: 搜索字段列表
        """
        return []


class DateRangeFilterMixin:
    """
    日期范围过滤混入类
    提供通用的日期范围过滤方法
    """
    
    @staticmethod
    def add_date_range_filter(field_name, filter_class=None):
        """
        添加日期范围过滤字段
        
        Args:
            field_name: 字段名
            filter_class: 过滤器类（默认为 DateFilter）
            
        Returns:
            tuple: (start_filter, end_filter)
        """
        if filter_class is None:
            filter_class = django_filters.DateFilter
        
        start_filter = filter_class(
            field_name=field_name,
            lookup_expr='gte',
            help_text=_('{field_name} 开始时间').format(field_name=field_name)
        )
        end_filter = filter_class(
            field_name=field_name,
            lookup_expr='lte',
            help_text=_('{field_name} 结束时间').format(field_name=field_name)
        )
        
        return start_filter, end_filter


class MultiFieldSearchMixin:
    """
    多字段搜索混入类
    提供通用的多字段搜索方法
    """
    
    def filter_multi_field_search(self, queryset, name, value, fields):
        """
        多字段搜索方法
        
        Args:
            queryset: 查询集
            name: 字段名
            value: 搜索值
            fields: 要搜索的字段列表
            
        Returns:
            QuerySet: 过滤后的查询集
        """
        if not value or not fields:
            return queryset
        
        # 构建 Q 对象
        q_objects = models.Q()
        for field in fields:
            q_objects |= models.Q(**{f'{field}__icontains': value})
        
        return queryset.filter(q_objects).distinct()
    
    def filter_related_search(self, queryset, name, value, related_fields):
        """
        关联字段搜索方法
        
        Args:
            queryset: 查询集
            name: 字段名
            value: 搜索值
            related_fields: 关联字段列表，格式：[('related_model__field', 'field_name'), ...]
            
        Returns:
            QuerySet: 过滤后的查询集
        """
        if not value or not related_fields:
            return queryset
        
        # 构建 Q 对象
        q_objects = models.Q()
        for related_field, _ in related_fields:
            q_objects |= models.Q(**{f'{related_field}__icontains': value})
        
        return queryset.filter(q_objects).distinct()


class NumberRangeFilterMixin:
    """
    数字范围过滤混入类
    提供通用的数字范围过滤方法
    """
    
    @staticmethod
    def add_number_range_filter(field_name, filter_class=None):
        """
        添加数字范围过滤字段
        
        Args:
            field_name: 字段名
            filter_class: 过滤器类（默认为 NumberFilter）
            
        Returns:
            tuple: (min_filter, max_filter)
        """
        if filter_class is None:
            filter_class = django_filters.NumberFilter
        
        min_filter = filter_class(
            field_name=field_name,
            lookup_expr='gte',
            help_text=_('{field_name} 最小值').format(field_name=field_name)
        )
        max_filter = filter_class(
            field_name=field_name,
            lookup_expr='lte',
            help_text=_('{field_name} 最大值').format(field_name=field_name)
        )
        
        return min_filter, max_filter


# 常用过滤器字段定义
class CommonFilters:
    """
    常用过滤器字段定义
    提供常用的过滤器字段，方便复用
    """
    
    # 状态过滤
    is_active = django_filters.BooleanFilter(help_text=_('是否激活'))
    is_deleted = django_filters.BooleanFilter(help_text=_('是否删除'))
    
    # ID 过滤
    id = django_filters.NumberFilter(help_text=_('ID'))
    id__in = django_filters.BaseInFilter(field_name='id', lookup_expr='in', help_text=_('ID 列表'))
    id__not_in = django_filters.BaseInFilter(field_name='id', lookup_expr='exclude', help_text=_('排除的 ID 列表'))
    
    # 创建时间范围
    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte', help_text=_('创建时间 >='))
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte', help_text=_('创建时间 <='))
    created_at__gt = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gt', help_text=_('创建时间 >'))
    created_at__lt = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lt', help_text=_('创建时间 <'))
    
    # 更新时间范围
    updated_at__gte = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte', help_text=_('更新时间 >='))
    updated_at__lte = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte', help_text=_('更新时间 <='))
    updated_at__gt = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gt', help_text=_('更新时间 >'))
    updated_at__lt = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lt', help_text=_('更新时间 <'))


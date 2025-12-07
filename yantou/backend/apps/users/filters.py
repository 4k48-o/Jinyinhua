"""
用户过滤和搜索
"""
import django_filters
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, Department


class UserFilter(django_filters.FilterSet):
    """
    用户过滤器
    支持用户名、邮箱、手机号搜索
    支持部门、状态、角色过滤
    支持创建时间、更新时间排序
    """
    # 搜索字段
    search = django_filters.CharFilter(method='filter_search', help_text=_('搜索用户名、邮箱、手机号'))
    
    # 过滤字段
    department = django_filters.NumberFilter(field_name='profile__department', lookup_expr='exact')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    is_staff = django_filters.BooleanFilter(field_name='is_staff')
    
    # 日期范围过滤
    date_joined_start = django_filters.DateFilter(field_name='date_joined', lookup_expr='gte')
    date_joined_end = django_filters.DateFilter(field_name='date_joined', lookup_expr='lte')
    created_at_start = django_filters.DateTimeFilter(field_name='date_joined', lookup_expr='gte')
    created_at_end = django_filters.DateTimeFilter(field_name='date_joined', lookup_expr='lte')
    
    # 排序
    ordering = django_filters.OrderingFilter(
        fields=(
            ('date_joined', 'date_joined'),
            ('last_login', 'last_login'),
            ('username', 'username'),
        ),
        label='排序字段'
    )

    class Meta:
        model = User
        fields = ['search', 'department', 'is_active', 'is_staff', 'date_joined_start', 'date_joined_end']

    def filter_search(self, queryset, name, value):
        """
        多字段搜索
        搜索用户名、邮箱、手机号
        """
        if not value:
            return queryset
        
        return queryset.filter(
            models.Q(username__icontains=value) |
            models.Q(email__icontains=value) |
            models.Q(profile__phone__icontains=value) |
            models.Q(first_name__icontains=value) |
            models.Q(last_name__icontains=value) |
            models.Q(profile__employee_no__icontains=value)
        ).distinct()


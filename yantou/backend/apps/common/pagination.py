"""
自定义分页类
提供页码分页和游标分页两种方式
"""
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _


class CustomPageNumberPagination(PageNumberPagination):
    """
    自定义分页类
    提供统一的分页响应格式
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        返回分页响应
        格式：
        {
            "success": true,
            "code": 200,
            "message": "操作成功",
            "data": {
                "results": [...],
                "pagination": {
                    "count": 100,
                    "page": 1,
                    "page_size": 20,
                    "pages": 5,
                    "has_next": true,
                    "has_previous": false
                }
            }
        }
        """
        return Response({
            'success': True,
            'code': 200,
            'message': _('操作成功'),
            'data': {
                'results': data,
                'pagination': {
                    'count': self.page.paginator.count,
                    'page': self.page.number,
                    'page_size': self.get_page_size(self.request),
                    'pages': self.page.paginator.num_pages,
                    'has_next': self.page.has_next(),
                    'has_previous': self.page.has_previous(),
                }
            },
            'request_id': getattr(self.request, 'request_id', None),
            'timestamp': self._get_timestamp()
        })

    def _get_timestamp(self):
        """获取时间戳"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'


class CustomCursorPagination(CursorPagination):
    """
    自定义游标分页类
    适用于大数据量场景，提供基于游标的分页
    游标分页不会暴露总记录数，性能更好
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = '-created_at'  # 默认按创建时间倒序
    cursor_query_param = 'cursor'  # 游标参数名
    
    def get_paginated_response(self, data):
        """
        返回分页响应
        格式：
        {
            "success": true,
            "code": 200,
            "message": "操作成功",
            "data": {
                "results": [...],
                "pagination": {
                    "page_size": 20,
                    "has_next": true,
                    "has_previous": false,
                    "next": "cursor_string",
                    "previous": "cursor_string"
                }
            }
        }
        """
        return Response({
            'success': True,
            'code': 200,
            'message': _('操作成功'),
            'data': {
                'results': data,
                'pagination': {
                    'page_size': self.get_page_size(self.request),
                    'has_next': self.has_next,
                    'has_previous': self.has_previous,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                }
            },
            'request_id': getattr(self.request, 'request_id', None),
            'timestamp': self._get_timestamp()
        })
    
    def _get_timestamp(self):
        """获取时间戳"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'


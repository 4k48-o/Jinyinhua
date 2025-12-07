"""
通用 Mixin 类
提供切面功能，统一收集和保存日志
"""
import time
from rest_framework import viewsets
from rest_framework.response import Response
from .audit import log_audit


class AuditLogMixin:
    """
    操作日志 Mixin
    自动记录 ViewSet 的 CRUD 操作日志
    
    使用方式：
        class MyViewSet(AuditLogMixin, viewsets.ModelViewSet):
            ...
    
    功能：
    - 自动记录 create, update, destroy, retrieve 操作
    - 自动获取资源类型、资源ID、资源名称
    - 自动记录执行时间、操作状态、错误信息
    - 支持自定义资源类型名称
    """
    
    # 资源类型名称（如果不设置，会从 queryset.model 自动获取）
    resource_type_name = None
    
    # 是否记录 retrieve（查看详情）操作，默认 False
    log_retrieve = False
    
    # 是否记录 list（列表查询）操作，默认 False
    log_list = False
    
    def get_resource_type(self):
        """
        获取资源类型名称
        
        Returns:
            str: 资源类型名称
        """
        if self.resource_type_name:
            return self.resource_type_name
        
        # 从 queryset.model 获取
        if hasattr(self, 'queryset') and self.queryset is not None:
            model = self.queryset.model
            # 获取模型名称（小写）
            return model.__name__.lower()
        
        # 从 ViewSet 名称推断
        viewset_name = self.__class__.__name__
        if viewset_name.endswith('ViewSet'):
            return viewset_name[:-7].lower()  # 移除 'ViewSet' 后缀
        
        return 'unknown'
    
    def get_resource_name(self, instance):
        """
        获取资源名称
        
        Args:
            instance: 模型实例
            
        Returns:
            str: 资源名称
        """
        if instance is None:
            return None
        
        # 尝试获取 name 字段
        if hasattr(instance, 'name'):
            return str(instance.name)
        
        # 尝试获取 username 字段
        if hasattr(instance, 'username'):
            return str(instance.username)
        
        # 尝试获取 title 字段
        if hasattr(instance, 'title'):
            return str(instance.title)
        
        # 使用 __str__ 方法
        return str(instance)
    
    def _log_action(self, action, instance=None, status=1, error_message=None, execution_time=None):
        """
        记录操作日志
        
        Args:
            action: 操作类型（create, update, delete, view, list）
            instance: 模型实例（可选）
            status: 操作状态（1:成功, 0:失败）
            error_message: 错误信息（失败时）
            execution_time: 执行时间（毫秒）
        """
        try:
            resource_type = self.get_resource_type()
            resource_id = instance.id if instance and hasattr(instance, 'id') else None
            resource_name = self.get_resource_name(instance) if instance else None
            
            # 生成操作描述
            action_display = {
                'create': '创建',
                'update': '更新',
                'partial_update': '更新',
                'destroy': '删除',
                'retrieve': '查看',
                'list': '列表查询',
            }.get(action, action)
            
            description = f"{action_display}{resource_type}"
            if resource_name:
                description += f": {resource_name}"
            
            log_audit(
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                resource_name=resource_name,
                description=description,
                request=self.request,
                status=status,
                error_message=error_message,
                execution_time=execution_time,
            )
        except Exception as e:
            # 日志记录失败不应该影响主业务
            import logging
            logger = logging.getLogger('django.audit')
            logger.warning(f"Failed to log audit in {self.__class__.__name__}: {str(e)}")
    
    def create(self, request, *args, **kwargs):
        """创建资源"""
        start_time = time.time()
        status_code = 1
        error_message = None
        instance = None
        
        try:
            response = super().create(request, *args, **kwargs)
            
            # 从响应中获取创建的实例
            if hasattr(response, 'data') and isinstance(response.data, dict):
                instance_id = response.data.get('id')
                if instance_id and hasattr(self, 'queryset'):
                    try:
                        instance = self.queryset.model.objects.get(pk=instance_id)
                    except:
                        pass
            
            return response
        except Exception as e:
            status_code = 0
            error_message = str(e)
            raise
        finally:
            execution_time = int((time.time() - start_time) * 1000)
            self._log_action('create', instance, status_code, error_message, execution_time)
    
    def update(self, request, *args, **kwargs):
        """更新资源（完整更新）"""
        start_time = time.time()
        status_code = 1
        error_message = None
        instance = None
        
        try:
            instance = self.get_object()
            response = super().update(request, *args, **kwargs)
            return response
        except Exception as e:
            status_code = 0
            error_message = str(e)
            raise
        finally:
            execution_time = int((time.time() - start_time) * 1000)
            self._log_action('update', instance, status_code, error_message, execution_time)
    
    def partial_update(self, request, *args, **kwargs):
        """更新资源（部分更新）"""
        start_time = time.time()
        status_code = 1
        error_message = None
        instance = None
        
        try:
            instance = self.get_object()
            response = super().partial_update(request, *args, **kwargs)
            return response
        except Exception as e:
            status_code = 0
            error_message = str(e)
            raise
        finally:
            execution_time = int((time.time() - start_time) * 1000)
            self._log_action('update', instance, status_code, error_message, execution_time)
    
    def destroy(self, request, *args, **kwargs):
        """删除资源"""
        start_time = time.time()
        status_code = 1
        error_message = None
        instance = None
        
        try:
            instance = self.get_object()
            response = super().destroy(request, *args, **kwargs)
            return response
        except Exception as e:
            status_code = 0
            error_message = str(e)
            raise
        finally:
            execution_time = int((time.time() - start_time) * 1000)
            self._log_action('delete', instance, status_code, error_message, execution_time)
    
    def retrieve(self, request, *args, **kwargs):
        """查看资源详情"""
        if not self.log_retrieve:
            return super().retrieve(request, *args, **kwargs)
        
        start_time = time.time()
        status_code = 1
        error_message = None
        instance = None
        
        try:
            instance = self.get_object()
            response = super().retrieve(request, *args, **kwargs)
            return response
        except Exception as e:
            status_code = 0
            error_message = str(e)
            raise
        finally:
            execution_time = int((time.time() - start_time) * 1000)
            self._log_action('view', instance, status_code, error_message, execution_time)
    
    def list(self, request, *args, **kwargs):
        """列表查询"""
        if not self.log_list:
            return super().list(request, *args, **kwargs)
        
        start_time = time.time()
        status_code = 1
        error_message = None
        
        try:
            response = super().list(request, *args, **kwargs)
            return response
        except Exception as e:
            status_code = 0
            error_message = str(e)
            raise
        finally:
            execution_time = int((time.time() - start_time) * 1000)
            self._log_action('view', None, status_code, error_message, execution_time)


"""
操作日志记录工具
提供便捷的操作日志记录函数和装饰器
"""
import time
import json
from functools import wraps
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import AuditLog, LoginLog

User = get_user_model()


def get_client_ip(request):
    """
    获取客户端 IP 地址
    
    Args:
        request: Django request 对象
        
    Returns:
        str: IP 地址
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    return ip


def log_audit(
    action,
    resource_type,
    resource_id=None,
    resource_name=None,
    description=None,
    request=None,
    user=None,
    status=1,
    error_message=None,
    execution_time=None,
    **kwargs
):
    """
    记录操作日志
    
    Args:
        action: 操作类型（create, update, delete, view, etc.）
        resource_type: 资源类型（user, role, etc.）
        resource_id: 资源 ID
        resource_name: 资源名称
        description: 操作描述
        request: Django request 对象（可选）
        user: 用户对象（可选，如果提供 request 会自动获取）
        status: 操作状态（1:成功, 0:失败）
        error_message: 错误信息（失败时）
        execution_time: 执行时间（毫秒）
        **kwargs: 其他字段
    """
    # 从 request 获取信息
    if request:
        if user is None:
            user = getattr(request, 'user', None)
        
        request_method = request.method
        request_path = request.path
        request_params = {}
        
        # 获取请求参数
        if request.method in ['GET', 'DELETE']:
            request_params = dict(request.GET)
        elif request.method in ['POST', 'PUT', 'PATCH']:
            # 只记录非敏感参数
            request_params = {}
            if hasattr(request, 'data'):
                request_params = dict(request.data)
            elif hasattr(request, 'POST'):
                request_params = dict(request.POST)
            
            # 过滤敏感字段
            sensitive_fields = ['password', 'old_password', 'new_password', 'token', 'secret']
            request_params = {
                k: '***' if k.lower() in sensitive_fields else v
                for k, v in request_params.items()
            }
        
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
    else:
        request_method = None
        request_path = None
        request_params = {}
        ip_address = None
        user_agent = None
    
    # 获取用户信息
    user_id = None
    username = None
    if user and hasattr(user, 'id'):
        user_id = user.id
        username = getattr(user, 'username', None) or str(user)
    
    # 创建日志记录
    audit_log = AuditLog(
        user_id=user_id,
        username=username,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        resource_name=resource_name,
        description=description,
        request_method=request_method,
        request_path=request_path,
        ip_address=ip_address,
        user_agent=user_agent,
        status=status,
        error_message=error_message,
        execution_time=execution_time,
        **kwargs
    )
    
    # 设置请求参数
    if request_params:
        audit_log.set_request_params(request_params)
    
    # 保存日志
    try:
        audit_log.save()
    except Exception as e:
        # 日志记录失败不应该影响主业务
        import logging
        logger = logging.getLogger('django.audit')
        logger.error(f"Failed to save audit log: {str(e)}")
    
    return audit_log


def audit_log(action, resource_type, description=None):
    """
    操作日志装饰器
    
    Usage:
        @audit_log(action='create', resource_type='user', description='创建用户')
        def create_user(request, ...):
            ...
    
    Args:
        action: 操作类型
        resource_type: 资源类型
        description: 操作描述（可选，可以从函数名自动生成）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取 request 对象（通常是第一个参数）
            request = None
            for arg in args:
                if hasattr(arg, 'method') and hasattr(arg, 'path'):
                    request = arg
                    break
            
            # 如果没有找到 request，尝试从 kwargs 获取
            if request is None:
                request = kwargs.get('request')
            
            # 获取用户
            user = None
            if request:
                user = getattr(request, 'user', None)
            
            # 自动生成描述
            if description is None:
                desc = f"{func.__name__}"
            else:
                desc = description
            
            # 记录开始时间
            start_time = time.time()
            status = 1
            error_message = None
            resource_id = None
            resource_name = None
            
            try:
                # 执行函数
                result = func(*args, **kwargs)
                
                # 尝试从结果中获取资源信息
                if hasattr(result, 'data') and isinstance(result.data, dict):
                    data = result.data
                    if 'id' in data:
                        resource_id = data['id']
                    if 'name' in data:
                        resource_name = data['name']
                    elif 'username' in data:
                        resource_name = data['username']
                
                return result
            except Exception as e:
                status = 0
                error_message = str(e)
                raise
            finally:
                # 计算执行时间
                execution_time = int((time.time() - start_time) * 1000)
                
                # 记录日志
                log_audit(
                    action=action,
                    resource_type=resource_type,
                    resource_id=resource_id,
                    resource_name=resource_name,
                    description=desc,
                    request=request,
                    user=user,
                    status=status,
                    error_message=error_message,
                    execution_time=execution_time,
                )
        
        return wrapper
    return decorator


def log_login(
    user=None,
    username=None,
    login_type='password',
    request=None,
    status=1,
    failure_reason=None,
    device_info=None,
):
    """
    记录登录日志（审计日志，保存到数据库）
    
    Args:
        user: 用户对象（可选）
        username: 用户名（可选，如果提供 user 会自动获取）
        login_type: 登录类型（password, token, sso, other）
        request: Django request 对象（可选，用于获取 IP、User-Agent 等）
        status: 登录状态（1:成功, 0:失败）
        failure_reason: 失败原因（失败时）
        device_info: 设备信息字典（可选，包含 device, browser, os, location 等）
    """
    # 从 request 获取信息
    ip_address = None
    user_agent = None
    if request:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # 获取用户信息
    user_id = None
    if user and hasattr(user, 'id'):
        user_id = user.id
        if username is None:
            username = getattr(user, 'username', None) or str(user)
    elif username:
        # 如果只有用户名，尝试查找用户 ID
        try:
            user_obj = User.objects.get(username=username)
            user_id = user_obj.id
        except User.DoesNotExist:
            pass
    
    # 从 device_info 获取设备信息
    device = None
    browser = None
    os_info = None
    location = None
    if device_info:
        device = device_info.get('device')
        browser = device_info.get('browser')
        os_info = device_info.get('os')
        location = device_info.get('location')
    
    # 创建登录日志记录
    login_log = LoginLog(
        user_id=user_id,
        username=username,
        login_type=login_type,
        ip_address=ip_address,
        user_agent=user_agent,
        location=location,
        device=device,
        browser=browser,
        os=os_info,
        status=status,
        failure_reason=failure_reason,
    )
    
    # 保存日志
    try:
        login_log.save()
    except Exception as e:
        # 日志记录失败不应该影响主业务
        import logging
        logger = logging.getLogger('django.audit')
        logger.error(f"Failed to save login log: {str(e)}")
    
    return login_log


def log_logout(
    user=None,
    username=None,
    request=None,
    status=1,
    failure_reason=None,
):
    """
    记录退出日志（审计日志，保存到数据库）
    
    Args:
        user: 用户对象（可选）
        username: 用户名（可选，如果提供 user 会自动获取）
        request: Django request 对象（可选，用于获取 IP、User-Agent 等）
        status: 退出状态（1:成功, 0:失败）
        failure_reason: 失败原因（失败时）
    """
    # 从 request 获取信息
    ip_address = None
    user_agent = None
    if request:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # 获取用户信息
    user_id = None
    if user and hasattr(user, 'id'):
        user_id = user.id
        if username is None:
            username = getattr(user, 'username', None) or str(user)
    
    # 记录到操作日志（AuditLog）
    log_audit(
        action='logout',
        resource_type='auth',
        resource_name=username,
        description=f'用户退出登录',
        request=request,
        user=user,
        status=status,
        error_message=failure_reason,
    )


"""
用户工具函数
"""
import os
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from io import BytesIO
import sys


def validate_image_file(file):
    """
    验证图片文件
    
    Args:
        file: 上传的文件对象
        
    Raises:
        ValidationError: 如果文件不符合要求
    """
    # 检查文件大小（最大 5MB）
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError(_('图片大小不能超过 5MB'))
    
    # 检查文件类型
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if file.content_type not in allowed_types:
        raise ValidationError(_('只支持 JPEG、PNG、GIF、WebP 格式的图片'))
    
    # 检查文件扩展名
    ext = os.path.splitext(file.name)[1].lower()
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if ext not in allowed_extensions:
        raise ValidationError(_('只支持 .jpg、.jpeg、.png、.gif、.webp 格式的图片'))


def compress_image(image_file, max_size=(800, 800), quality=85):
    """
    压缩图片
    
    Args:
        image_file: 图片文件对象
        max_size: 最大尺寸 (width, height)
        quality: JPEG 质量 (1-100)
        
    Returns:
        BytesIO: 压缩后的图片数据
    """
    try:
        # 打开图片
        img = Image.open(image_file)
        
        # 转换为 RGB（如果是 RGBA）
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # 调整尺寸
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 保存到内存
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return output
    except Exception as e:
        raise ValidationError(_('图片处理失败: {}').format(str(e)))


def generate_thumbnail(image_file, size=(200, 200), quality=75):
    """
    生成缩略图
    
    Args:
        image_file: 图片文件对象
        size: 缩略图尺寸 (width, height)
        quality: JPEG 质量 (1-100)
        
    Returns:
        BytesIO: 缩略图数据
    """
    try:
        img = Image.open(image_file)
        
        # 转换为 RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # 生成缩略图（保持宽高比）
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # 保存到内存
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return output
    except Exception as e:
        raise ValidationError(_('缩略图生成失败: {}').format(str(e)))


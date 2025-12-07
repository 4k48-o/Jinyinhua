"""
为角色添加权限的管理命令
用于快速为角色添加特定权限
"""
from django.core.management.base import BaseCommand
from apps.permissions.models import Role, Permission, RolePermission
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = '为角色添加权限'

    def add_arguments(self, parser):
        parser.add_argument(
            '--role-code',
            type=str,
            required=True,
            help='角色代码，如：admin'
        )
        parser.add_argument(
            '--permission-codes',
            type=str,
            nargs='+',
            required=True,
            help='权限代码列表，如：role:update role:read'
        )
        parser.add_argument(
            '--granted-by',
            type=int,
            help='授权人用户ID（可选）'
        )

    def handle(self, *args, **options):
        role_code = options['role_code']
        permission_codes = options['permission_codes']
        granted_by_id = options.get('granted_by')

        # 获取角色
        try:
            role = Role.objects.get(code=role_code)
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'角色 {role_code} 不存在'))
            return

        # 获取授权人
        granted_by = None
        if granted_by_id:
            try:
                granted_by = User.objects.get(pk=granted_by_id)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'用户 {granted_by_id} 不存在，将不设置授权人'))

        # 获取权限
        permissions = Permission.objects.filter(code__in=permission_codes, is_active=True)
        found_codes = set(permissions.values_list('code', flat=True))
        missing_codes = set(permission_codes) - found_codes

        if missing_codes:
            self.stdout.write(self.style.WARNING(f'以下权限不存在或未激活: {", ".join(missing_codes)}'))

        if not permissions.exists():
            self.stdout.write(self.style.ERROR('没有找到任何有效的权限'))
            return

        # 添加权限
        added_count = 0
        skipped_count = 0
        for permission in permissions:
            role_permission, created = RolePermission.objects.get_or_create(
                role=role,
                permission=permission,
                defaults={'granted_by': granted_by}
            )
            if created:
                added_count += 1
                self.stdout.write(f'  ✓ 添加权限: {permission.name} ({permission.code})')
            else:
                skipped_count += 1
                self.stdout.write(f'  - 权限已存在: {permission.name} ({permission.code})')

        self.stdout.write(self.style.SUCCESS(
            f'\n完成！为角色 {role.name} ({role.code}) 添加了 {added_count} 个权限，跳过 {skipped_count} 个已存在的权限'
        ))


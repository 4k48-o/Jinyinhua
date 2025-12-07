"""
初始化权限数据
创建默认角色和权限
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.permissions.models import Role, Permission, RolePermission, UserRole


class Command(BaseCommand):
    help = '初始化权限数据，创建默认角色和权限'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化权限数据...')
        
        # 创建默认权限
        permissions = self.create_default_permissions()
        self.stdout.write(self.style.SUCCESS(f'✓ 创建了 {len(permissions)} 个默认权限'))
        
        # 创建默认角色
        roles = self.create_default_roles(permissions)
        self.stdout.write(self.style.SUCCESS(f'✓ 创建了 {len(roles)} 个默认角色'))
        
        # 为超级管理员分配角色
        self.assign_superuser_role(roles)
        self.stdout.write(self.style.SUCCESS('✓ 为超级管理员分配了角色'))
        
        self.stdout.write(self.style.SUCCESS('\n权限数据初始化完成！'))

    def create_default_permissions(self):
        """创建默认权限（层级结构）"""
        # 定义权限层级结构
        # 格式: {'parent': {...}, 'children': [{...}, ...]}
        permissions_structure = [
            {
                'parent': {
                    'name': '用户管理',
                    'code': 'user:manage',
                    'content_type': 'user',
                    'action': 'manage',
                    'description': '用户管理权限组',
                    'sort_order': 10,
                },
                'children': [
                    {'name': '用户创建', 'code': 'user:create', 'content_type': 'user', 'action': 'create', 'description': '创建用户', 'sort_order': 1},
                    {'name': '用户查询', 'code': 'user:read', 'content_type': 'user', 'action': 'read', 'description': '查询用户', 'sort_order': 2},
                    {'name': '用户更新', 'code': 'user:update', 'content_type': 'user', 'action': 'update', 'description': '更新用户', 'sort_order': 3},
                    {'name': '用户删除', 'code': 'user:delete', 'content_type': 'user', 'action': 'delete', 'description': '删除用户', 'sort_order': 4},
                    {'name': '用户导入', 'code': 'user:import', 'content_type': 'user', 'action': 'import', 'description': '导入用户', 'sort_order': 5},
                    {'name': '用户导出', 'code': 'user:export', 'content_type': 'user', 'action': 'export', 'description': '导出用户', 'sort_order': 6},
                ]
            },
            {
                'parent': {
                    'name': '角色管理',
                    'code': 'role:manage',
                    'content_type': 'role',
                    'action': 'manage',
                    'description': '角色管理权限组',
                    'sort_order': 20,
                },
                'children': [
                    {'name': '角色创建', 'code': 'role:create', 'content_type': 'role', 'action': 'create', 'description': '创建角色', 'sort_order': 1},
                    {'name': '角色查询', 'code': 'role:read', 'content_type': 'role', 'action': 'read', 'description': '查询角色', 'sort_order': 2},
                    {'name': '角色更新', 'code': 'role:update', 'content_type': 'role', 'action': 'update', 'description': '更新角色', 'sort_order': 3},
                    {'name': '角色删除', 'code': 'role:delete', 'content_type': 'role', 'action': 'delete', 'description': '删除角色', 'sort_order': 4},
                ]
            },
            {
                'parent': {
                    'name': '权限管理',
                    'code': 'permission:manage',
                    'content_type': 'permission',
                    'action': 'manage',
                    'description': '权限管理权限组',
                    'sort_order': 30,
                },
                'children': [
                    {'name': '权限创建', 'code': 'permission:create', 'content_type': 'permission', 'action': 'create', 'description': '创建权限', 'sort_order': 1},
                    {'name': '权限查询', 'code': 'permission:read', 'content_type': 'permission', 'action': 'read', 'description': '查询权限', 'sort_order': 2},
                    {'name': '权限更新', 'code': 'permission:update', 'content_type': 'permission', 'action': 'update', 'description': '更新权限', 'sort_order': 3},
                    {'name': '权限删除', 'code': 'permission:delete', 'content_type': 'permission', 'action': 'delete', 'description': '删除权限', 'sort_order': 4},
                ]
            },
            {
                'parent': {
                    'name': '部门管理',
                    'code': 'department:manage',
                    'content_type': 'department',
                    'action': 'manage',
                    'description': '部门管理权限组',
                    'sort_order': 40,
                },
                'children': [
                    {'name': '部门创建', 'code': 'department:create', 'content_type': 'department', 'action': 'create', 'description': '创建部门', 'sort_order': 1},
                    {'name': '部门查询', 'code': 'department:read', 'content_type': 'department', 'action': 'read', 'description': '查询部门', 'sort_order': 2},
                    {'name': '部门更新', 'code': 'department:update', 'content_type': 'department', 'action': 'update', 'description': '更新部门', 'sort_order': 3},
                    {'name': '部门删除', 'code': 'department:delete', 'content_type': 'department', 'action': 'delete', 'description': '删除部门', 'sort_order': 4},
                ]
            },
        ]
        
        all_permissions = []
        
        # 创建权限层级结构
        for group in permissions_structure:
            # 创建父权限
            parent_data = group['parent']
            parent, created = Permission.objects.get_or_create(
                code=parent_data['code'],
                defaults={
                    'name': parent_data['name'],
                    'content_type': parent_data['content_type'],
                    'action': parent_data['action'],
                    'description': parent_data['description'],
                    'sort_order': parent_data['sort_order'],
                    'is_active': True,
                    'is_system': True,
                    'parent': None,  # 父权限没有父级
                }
            )
            all_permissions.append(parent)
            if created:
                self.stdout.write(f'  - 创建父权限: {parent.name} ({parent.code})')
            else:
                # 更新现有父权限的属性
                parent.name = parent_data['name']
                parent.description = parent_data['description']
                parent.sort_order = parent_data['sort_order']
                parent.save()
            
            # 创建子权限
            for child_data in group['children']:
                child, created = Permission.objects.get_or_create(
                    code=child_data['code'],
                    defaults={
                        'name': child_data['name'],
                        'content_type': child_data['content_type'],
                        'action': child_data['action'],
                        'description': child_data['description'],
                        'sort_order': child_data['sort_order'],
                        'is_active': True,
                        'is_system': True,
                        'parent': parent,  # 设置父权限
                    }
                )
                all_permissions.append(child)
                if created:
                    self.stdout.write(f'    └─ 创建子权限: {child.name} ({child.code})')
                else:
                    # 更新现有子权限的属性
                    child.name = child_data['name']
                    child.description = child_data['description']
                    child.sort_order = child_data['sort_order']
                    child.parent = parent  # 确保父权限关系正确
                    child.save()
        
        return all_permissions

    def create_default_roles(self, permissions):
        """创建默认角色"""
        roles_data = [
            {
                'name': '超级管理员',
                'code': 'super_admin',
                'description': '超级管理员，拥有所有权限',
                'is_system': True,
                'permission_codes': [p.code for p in permissions],  # 所有权限
            },
            {
                'name': '管理员',
                'code': 'admin',
                'description': '管理员，拥有大部分管理权限',
                'is_system': True,
                'permission_codes': [
                    # 用户管理权限（包含所有子权限）
                    'user:create', 'user:read', 'user:update', 'user:delete', 'user:import', 'user:export',
                    # 角色管理权限
                    'role:create', 'role:read', 'role:update', 'role:delete',
                    # 权限管理权限
                    'permission:create', 'permission:read', 'permission:update', 'permission:delete',
                    # 部门管理权限
                    'department:create', 'department:read', 'department:update', 'department:delete',
                ],
            },
            {
                'name': '普通用户',
                'code': 'user',
                'description': '普通用户，拥有基本查看权限',
                'is_system': True,
                'permission_codes': [
                    'user:read',
                    'department:read',
                ],
            },
            {
                'name': '访客',
                'code': 'guest',
                'description': '访客，仅拥有查看权限',
                'is_system': True,
                'permission_codes': [
                    'user:read',
                ],
            },
        ]
        
        roles = []
        for data in roles_data:
            role, created = Role.objects.get_or_create(
                code=data['code'],
                defaults={
                    'name': data['name'],
                    'description': data['description'],
                    'is_active': True,
                    'is_system': data['is_system'],
                }
            )
            roles.append(role)
            
            if created:
                self.stdout.write(f'  - 创建角色: {role.name} ({role.code})')
                
                # 分配权限
                permission_codes = data.get('permission_codes', [])
                for permission_code in permission_codes:
                    try:
                        permission = Permission.objects.get(code=permission_code)
                        RolePermission.objects.get_or_create(
                            role=role,
                            permission=permission
                        )
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'    警告: 权限 {permission_code} 不存在'))
            else:
                # 更新现有角色的权限
                permission_codes = data.get('permission_codes', [])
                existing_permission_codes = set(
                    role.permissions.values_list('code', flat=True)
                )
                
                # 添加新权限
                for permission_code in permission_codes:
                    if permission_code not in existing_permission_codes:
                        try:
                            permission = Permission.objects.get(code=permission_code)
                            RolePermission.objects.get_or_create(
                                role=role,
                                permission=permission
                            )
                        except Permission.DoesNotExist:
                            pass
        
        return roles

    def assign_superuser_role(self, roles):
        """为超级管理员分配角色"""
        super_admin_role = next((r for r in roles if r.code == 'super_admin'), None)
        if not super_admin_role:
            return
        
        superusers = User.objects.filter(is_superuser=True)
        for user in superusers:
            UserRole.objects.get_or_create(
                user=user,
                role=super_admin_role,
                defaults={'is_active': True}
            )


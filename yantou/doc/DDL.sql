-- =====================================================
-- 企业级应用系统数据库 DDL
-- 版本: v1.0.0
-- 说明: 所有基础表以 sys_ 前缀开头
-- 设计原则: 不使用外键约束，数据一致性由应用层维护
-- 支持数据库: MySQL 5.7+, PostgreSQL 10+
-- =====================================================

-- =====================================================
-- 1. 用户相关表
-- =====================================================

-- 1.1 sys_user - 用户基础表
CREATE TABLE IF NOT EXISTS `sys_user` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `username` VARCHAR(150) NOT NULL COMMENT '用户名（唯一）',
    `email` VARCHAR(254) DEFAULT NULL COMMENT '邮箱地址',
    `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号',
    `password` VARCHAR(128) NOT NULL COMMENT '密码（加密）',
    `first_name` VARCHAR(150) DEFAULT '' COMMENT '名',
    `last_name` VARCHAR(150) DEFAULT '' COMMENT '姓',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否激活',
    `is_staff` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否员工',
    `is_superuser` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否超级管理员',
    `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否删除（软删除）',
    `last_login` DATETIME DEFAULT NULL COMMENT '最后登录时间',
    `date_joined` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`),
    UNIQUE KEY `uk_phone` (`phone`),
    KEY `idx_email` (`email`),
    KEY `idx_is_active` (`is_active`),
    KEY `idx_is_deleted` (`is_deleted`),
    KEY `idx_date_joined` (`date_joined`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户基础表';

-- 1.2 sys_user_profile - 用户扩展信息表
CREATE TABLE IF NOT EXISTS `sys_user_profile` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `user_id` BIGINT NOT NULL COMMENT '用户 ID（关联 sys_user.id）',
    `avatar` VARCHAR(500) DEFAULT NULL COMMENT '头像 URL',
    `gender` TINYINT DEFAULT NULL COMMENT '性别（0:未知, 1:男, 2:女）',
    `birthday` DATE DEFAULT NULL COMMENT '生日',
    `address` VARCHAR(500) DEFAULT NULL COMMENT '地址',
    `bio` TEXT COMMENT '个人简介',
    `department_id` BIGINT DEFAULT NULL COMMENT '部门 ID（关联 sys_department.id）',
    `position` VARCHAR(100) DEFAULT NULL COMMENT '职位',
    `employee_no` VARCHAR(50) DEFAULT NULL COMMENT '工号',
    `join_date` DATE DEFAULT NULL COMMENT '入职日期',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_id` (`user_id`),
    UNIQUE KEY `uk_employee_no` (`employee_no`),
    KEY `idx_department_id` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户扩展信息表';

-- 1.3 sys_department - 部门表
CREATE TABLE IF NOT EXISTS `sys_department` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `name` VARCHAR(100) NOT NULL COMMENT '部门名称',
    `code` VARCHAR(50) DEFAULT NULL COMMENT '部门代码（唯一）',
    `parent_id` BIGINT DEFAULT NULL COMMENT '父部门 ID（关联 sys_department.id）',
    `level` INT NOT NULL DEFAULT 1 COMMENT '部门层级',
    `path` VARCHAR(500) DEFAULT NULL COMMENT '部门路径（如：1/2/3）',
    `manager_id` BIGINT DEFAULT NULL COMMENT '部门负责人 ID（关联 sys_user.id）',
    `description` TEXT COMMENT '部门描述',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序顺序',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否激活',
    `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否删除',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_code` (`code`),
    KEY `idx_name` (`name`),
    KEY `idx_parent_id` (`parent_id`),
    KEY `idx_level` (`level`),
    KEY `idx_manager_id` (`manager_id`),
    KEY `idx_is_active` (`is_active`),
    KEY `idx_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='部门表';

-- =====================================================
-- 2. 权限相关表
-- =====================================================

-- 2.1 sys_role - 角色表
CREATE TABLE IF NOT EXISTS `sys_role` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `name` VARCHAR(50) NOT NULL COMMENT '角色名称',
    `code` VARCHAR(50) NOT NULL COMMENT '角色代码（唯一，如：admin）',
    `description` TEXT COMMENT '角色描述',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序顺序',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否激活',
    `is_system` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否系统角色（不可删除）',
    `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否删除',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间',
    `created_by` BIGINT DEFAULT NULL COMMENT '创建人 ID（关联 sys_user.id）',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_name` (`name`),
    UNIQUE KEY `uk_code` (`code`),
    KEY `idx_is_active` (`is_active`),
    KEY `idx_is_deleted` (`is_deleted`),
    KEY `idx_created_by` (`created_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

-- 2.2 sys_permission - 权限表
CREATE TABLE IF NOT EXISTS `sys_permission` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `name` VARCHAR(100) NOT NULL COMMENT '权限名称',
    `code` VARCHAR(100) NOT NULL COMMENT '权限代码（唯一，如：user:create）',
    `content_type` VARCHAR(100) DEFAULT NULL COMMENT '资源类型（如：user, role）',
    `action` VARCHAR(50) DEFAULT NULL COMMENT '操作类型（如：create, read, update, delete）',
    `description` TEXT COMMENT '权限描述',
    `parent_id` BIGINT DEFAULT NULL COMMENT '父权限 ID（关联 sys_permission.id）',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序顺序',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否激活',
    `is_system` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否系统权限',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_code` (`code`),
    KEY `idx_content_type` (`content_type`),
    KEY `idx_parent_id` (`parent_id`),
    KEY `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';

-- 2.3 sys_user_role - 用户角色关联表
CREATE TABLE IF NOT EXISTS `sys_user_role` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `user_id` BIGINT NOT NULL COMMENT '用户 ID（关联 sys_user.id）',
    `role_id` BIGINT NOT NULL COMMENT '角色 ID（关联 sys_role.id）',
    `assigned_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '分配时间',
    `assigned_by` BIGINT DEFAULT NULL COMMENT '分配人 ID（关联 sys_user.id）',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否激活',
    `expires_at` DATETIME DEFAULT NULL COMMENT '过期时间（NULL 表示永久）',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_role` (`user_id`, `role_id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_role_id` (`role_id`),
    KEY `idx_assigned_by` (`assigned_by`),
    KEY `idx_expires_at` (`expires_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';

-- 2.4 sys_role_permission - 角色权限关联表
CREATE TABLE IF NOT EXISTS `sys_role_permission` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `role_id` BIGINT NOT NULL COMMENT '角色 ID（关联 sys_role.id）',
    `permission_id` BIGINT NOT NULL COMMENT '权限 ID（关联 sys_permission.id）',
    `granted_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '授权时间',
    `granted_by` BIGINT DEFAULT NULL COMMENT '授权人 ID（关联 sys_user.id）',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_role_permission` (`role_id`, `permission_id`),
    KEY `idx_role_id` (`role_id`),
    KEY `idx_permission_id` (`permission_id`),
    KEY `idx_granted_by` (`granted_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- =====================================================
-- 3. 菜单相关表
-- =====================================================

-- 3.1 sys_menu - 菜单表
CREATE TABLE IF NOT EXISTS `sys_menu` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `name` VARCHAR(50) NOT NULL COMMENT '菜单名称',
    `title` VARCHAR(100) NOT NULL COMMENT '菜单标题（显示名称）',
    `path` VARCHAR(200) DEFAULT NULL COMMENT '路由路径',
    `component` VARCHAR(200) DEFAULT NULL COMMENT '组件路径',
    `icon` VARCHAR(100) DEFAULT NULL COMMENT '图标名称',
    `parent_id` BIGINT DEFAULT NULL COMMENT '父菜单 ID（关联 sys_menu.id）',
    `level` INT NOT NULL DEFAULT 1 COMMENT '菜单层级',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序顺序',
    `is_visible` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否显示',
    `is_cache` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否缓存',
    `is_external` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否外部链接',
    `external_url` VARCHAR(500) DEFAULT NULL COMMENT '外部链接地址',
    `permission_code` VARCHAR(100) DEFAULT NULL COMMENT '所需权限代码',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否激活',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_path` (`path`),
    KEY `idx_parent_id` (`parent_id`),
    KEY `idx_level` (`level`),
    KEY `idx_is_visible` (`is_visible`),
    KEY `idx_permission_code` (`permission_code`),
    KEY `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='菜单表';

-- 3.2 sys_menu_permission - 菜单权限关联表
CREATE TABLE IF NOT EXISTS `sys_menu_permission` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `menu_id` BIGINT NOT NULL COMMENT '菜单 ID（关联 sys_menu.id）',
    `permission_id` BIGINT NOT NULL COMMENT '权限 ID（关联 sys_permission.id）',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_menu_permission` (`menu_id`, `permission_id`),
    KEY `idx_menu_id` (`menu_id`),
    KEY `idx_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='菜单权限关联表';

-- =====================================================
-- 4. 日志相关表
-- =====================================================

-- 4.1 sys_audit_log - 操作日志表
CREATE TABLE IF NOT EXISTS `sys_audit_log` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `user_id` BIGINT DEFAULT NULL COMMENT '用户 ID（关联 sys_user.id）',
    `username` VARCHAR(150) DEFAULT NULL COMMENT '用户名（冗余字段）',
    `action` VARCHAR(50) NOT NULL COMMENT '操作类型（create, update, delete, view）',
    `resource_type` VARCHAR(100) NOT NULL COMMENT '资源类型（user, role, etc.）',
    `resource_id` BIGINT DEFAULT NULL COMMENT '资源 ID',
    `resource_name` VARCHAR(200) DEFAULT NULL COMMENT '资源名称',
    `description` TEXT COMMENT '操作描述',
    `request_method` VARCHAR(10) DEFAULT NULL COMMENT 'HTTP 方法（GET, POST, etc.）',
    `request_path` VARCHAR(500) DEFAULT NULL COMMENT '请求路径',
    `request_params` TEXT COMMENT '请求参数（JSON）',
    `ip_address` VARCHAR(50) DEFAULT NULL COMMENT 'IP 地址',
    `user_agent` VARCHAR(500) DEFAULT NULL COMMENT '用户代理',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '操作状态（1:成功, 0:失败）',
    `error_message` TEXT COMMENT '错误信息',
    `execution_time` INT DEFAULT NULL COMMENT '执行时间（毫秒）',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_username` (`username`),
    KEY `idx_action` (`action`),
    KEY `idx_resource_type` (`resource_type`),
    KEY `idx_resource_id` (`resource_id`),
    KEY `idx_ip_address` (`ip_address`),
    KEY `idx_status` (`status`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';

-- 4.2 sys_login_log - 登录日志表
CREATE TABLE IF NOT EXISTS `sys_login_log` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `user_id` BIGINT DEFAULT NULL COMMENT '用户 ID（关联 sys_user.id）',
    `username` VARCHAR(150) DEFAULT NULL COMMENT '用户名',
    `login_type` VARCHAR(20) NOT NULL COMMENT '登录类型（password, token, etc.）',
    `ip_address` VARCHAR(50) DEFAULT NULL COMMENT 'IP 地址',
    `user_agent` VARCHAR(500) DEFAULT NULL COMMENT '用户代理',
    `location` VARCHAR(200) DEFAULT NULL COMMENT '登录地点',
    `device` VARCHAR(100) DEFAULT NULL COMMENT '设备信息',
    `browser` VARCHAR(100) DEFAULT NULL COMMENT '浏览器信息',
    `os` VARCHAR(100) DEFAULT NULL COMMENT '操作系统',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '登录状态（1:成功, 0:失败）',
    `failure_reason` VARCHAR(200) DEFAULT NULL COMMENT '失败原因',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登录时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_username` (`username`),
    KEY `idx_ip_address` (`ip_address`),
    KEY `idx_status` (`status`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='登录日志表';

-- =====================================================
-- 5. 系统配置表
-- =====================================================

-- 5.1 sys_system_config - 系统配置表
CREATE TABLE IF NOT EXISTS `sys_system_config` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `config_key` VARCHAR(100) NOT NULL COMMENT '配置键（唯一）',
    `config_value` TEXT COMMENT '配置值',
    `config_type` VARCHAR(50) NOT NULL DEFAULT 'string' COMMENT '配置类型（string, number, boolean, json）',
    `category` VARCHAR(50) DEFAULT NULL COMMENT '配置分类',
    `description` TEXT COMMENT '配置描述',
    `is_encrypted` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否加密存储',
    `is_system` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否系统配置（不可删除）',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `updated_by` BIGINT DEFAULT NULL COMMENT '更新人 ID（关联 sys_user.id）',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_config_key` (`config_key`),
    KEY `idx_config_type` (`config_type`),
    KEY `idx_category` (`category`),
    KEY `idx_updated_by` (`updated_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- =====================================================
-- 6. 文件相关表
-- =====================================================

-- 6.1 sys_file - 文件表
CREATE TABLE IF NOT EXISTS `sys_file` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `file_name` VARCHAR(255) NOT NULL COMMENT '原始文件名',
    `file_path` VARCHAR(500) NOT NULL COMMENT '文件存储路径',
    `file_url` VARCHAR(500) DEFAULT NULL COMMENT '文件访问 URL',
    `file_type` VARCHAR(50) DEFAULT NULL COMMENT '文件类型（MIME）',
    `file_size` BIGINT NOT NULL DEFAULT 0 COMMENT '文件大小（字节）',
    `file_ext` VARCHAR(20) DEFAULT NULL COMMENT '文件扩展名',
    `storage_type` VARCHAR(20) NOT NULL DEFAULT 'local' COMMENT '存储类型（local, oss, s3）',
    `bucket_name` VARCHAR(100) DEFAULT NULL COMMENT '存储桶名称（OSS/S3）',
    `md5_hash` VARCHAR(32) DEFAULT NULL COMMENT '文件 MD5 值',
    `uploader_id` BIGINT DEFAULT NULL COMMENT '上传人 ID（关联 sys_user.id）',
    `related_type` VARCHAR(100) DEFAULT NULL COMMENT '关联类型（user, article, etc.）',
    `related_id` BIGINT DEFAULT NULL COMMENT '关联 ID',
    `is_public` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否公开',
    `download_count` INT NOT NULL DEFAULT 0 COMMENT '下载次数',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_file_path` (`file_path`),
    KEY `idx_file_type` (`file_type`),
    KEY `idx_file_ext` (`file_ext`),
    KEY `idx_md5_hash` (`md5_hash`),
    KEY `idx_uploader_id` (`uploader_id`),
    KEY `idx_related_type` (`related_type`),
    KEY `idx_related_id` (`related_id`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文件表';

-- =====================================================
-- 7. 初始化数据
-- =====================================================

-- 7.1 默认角色
INSERT INTO `sys_role` (`name`, `code`, `description`, `is_system`, `is_active`, `sort_order`) VALUES
('超级管理员', 'super_admin', '拥有所有权限', TRUE, TRUE, 1),
('管理员', 'admin', '系统管理员', TRUE, TRUE, 2),
('普通用户', 'user', '普通用户', TRUE, TRUE, 3),
('访客', 'guest', '访客用户', TRUE, TRUE, 4)
ON DUPLICATE KEY UPDATE `name`=VALUES(`name`);

-- 7.2 默认权限
-- 用户管理权限
INSERT INTO `sys_permission` (`name`, `code`, `content_type`, `action`, `description`, `is_system`, `sort_order`) VALUES
('用户创建', 'user:create', 'user', 'create', '创建用户', TRUE, 1),
('用户查看', 'user:read', 'user', 'read', '查看用户', TRUE, 2),
('用户更新', 'user:update', 'user', 'update', '更新用户', TRUE, 3),
('用户删除', 'user:delete', 'user', 'delete', '删除用户', TRUE, 4),
('用户导出', 'user:export', 'user', 'export', '导出用户', TRUE, 5),
('用户导入', 'user:import', 'user', 'import', '导入用户', TRUE, 6)
ON DUPLICATE KEY UPDATE `name`=VALUES(`name`);

-- 角色管理权限
INSERT INTO `sys_permission` (`name`, `code`, `content_type`, `action`, `description`, `is_system`, `sort_order`) VALUES
('角色创建', 'role:create', 'role', 'create', '创建角色', TRUE, 10),
('角色查看', 'role:read', 'role', 'read', '查看角色', TRUE, 11),
('角色更新', 'role:update', 'role', 'update', '更新角色', TRUE, 12),
('角色删除', 'role:delete', 'role', 'delete', '删除角色', TRUE, 13)
ON DUPLICATE KEY UPDATE `name`=VALUES(`name`);

-- 权限管理权限
INSERT INTO `sys_permission` (`name`, `code`, `content_type`, `action`, `description`, `is_system`, `sort_order`) VALUES
('权限创建', 'permission:create', 'permission', 'create', '创建权限', TRUE, 20),
('权限查看', 'permission:read', 'permission', 'read', '查看权限', TRUE, 21),
('权限更新', 'permission:update', 'permission', 'update', '更新权限', TRUE, 22),
('权限删除', 'permission:delete', 'permission', 'delete', '删除权限', TRUE, 23)
ON DUPLICATE KEY UPDATE `name`=VALUES(`name`);

-- 菜单管理权限
INSERT INTO `sys_permission` (`name`, `code`, `content_type`, `action`, `description`, `is_system`, `sort_order`) VALUES
('菜单创建', 'menu:create', 'menu', 'create', '创建菜单', TRUE, 30),
('菜单查看', 'menu:read', 'menu', 'read', '查看菜单', TRUE, 31),
('菜单更新', 'menu:update', 'menu', 'update', '更新菜单', TRUE, 32),
('菜单删除', 'menu:delete', 'menu', 'delete', '删除菜单', TRUE, 33)
ON DUPLICATE KEY UPDATE `name`=VALUES(`name`);

-- 部门管理权限
INSERT INTO `sys_permission` (`name`, `code`, `content_type`, `action`, `description`, `is_system`, `sort_order`) VALUES
('部门创建', 'department:create', 'department', 'create', '创建部门', TRUE, 40),
('部门查看', 'department:read', 'department', 'read', '查看部门', TRUE, 41),
('部门更新', 'department:update', 'department', 'update', '更新部门', TRUE, 42),
('部门删除', 'department:delete', 'department', 'delete', '删除部门', TRUE, 43)
ON DUPLICATE KEY UPDATE `name`=VALUES(`name`);

-- 7.3 默认菜单
INSERT INTO `sys_menu` (`name`, `title`, `path`, `icon`, `sort_order`, `level`, `is_active`, `is_visible`) VALUES
('dashboard', '仪表盘', '/dashboard', 'DashboardOutlined', 1, 1, TRUE, TRUE),
('system', '系统管理', '/system', 'SettingOutlined', 2, 1, TRUE, TRUE),
('user', '用户管理', '/system/users', 'UserOutlined', 3, 2, TRUE, TRUE),
('role', '角色管理', '/system/roles', 'TeamOutlined', 4, 2, TRUE, TRUE),
('permission', '权限管理', '/system/permissions', 'SafetyOutlined', 5, 2, TRUE, TRUE),
('menu', '菜单管理', '/system/menus', 'MenuOutlined', 6, 2, TRUE, TRUE),
('department', '部门管理', '/system/departments', 'ApartmentOutlined', 7, 2, TRUE, TRUE)
ON DUPLICATE KEY UPDATE `title`=VALUES(`title`);

-- 更新菜单的 parent_id（系统管理子菜单）
UPDATE `sys_menu` SET `parent_id` = (SELECT `id` FROM (SELECT `id` FROM `sys_menu` WHERE `name` = 'system' LIMIT 1) AS t) 
WHERE `name` IN ('user', 'role', 'permission', 'menu', 'department') AND `parent_id` IS NULL;

-- 7.4 为超级管理员角色分配所有权限
INSERT INTO `sys_role_permission` (`role_id`, `permission_id`, `granted_at`)
SELECT 
    (SELECT `id` FROM `sys_role` WHERE `code` = 'super_admin' LIMIT 1) AS role_id,
    `id` AS permission_id,
    NOW() AS granted_at
FROM `sys_permission`
WHERE NOT EXISTS (
    SELECT 1 FROM `sys_role_permission` 
    WHERE `role_id` = (SELECT `id` FROM `sys_role` WHERE `code` = 'super_admin' LIMIT 1)
    AND `permission_id` = `sys_permission`.`id`
);

-- =====================================================
-- 8. 说明
-- =====================================================
-- 1. 本 DDL 脚本使用 MySQL 语法，如需 PostgreSQL 版本，请调整：
--    - AUTO_INCREMENT -> SERIAL 或 BIGSERIAL
--    - BOOLEAN -> BOOLEAN (相同)
--    - DATETIME -> TIMESTAMP
--    - ON UPDATE CURRENT_TIMESTAMP -> 使用触发器
--    - ENGINE=InnoDB -> 移除
--    - DEFAULT CHARSET -> 移除
--    - COMMENT -> 使用 COMMENT ON
--
-- 2. 所有表不使用外键约束，数据一致性由应用层维护
--
-- 3. 建议在生产环境执行前：
--    - 备份现有数据
--    - 在测试环境验证
--    - 根据实际需求调整字段类型和长度
--
-- 4. 初始化数据使用 ON DUPLICATE KEY UPDATE 防止重复插入
--    PostgreSQL 使用 ON CONFLICT DO UPDATE
--
-- =====================================================


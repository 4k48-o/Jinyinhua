# 数据库备份策略

## 概述

本文档描述了数据库备份和恢复的策略及操作方法。

## 备份策略

### 自动备份

建议使用 cron 定时任务进行自动备份：

```bash
# 编辑 crontab
crontab -e

# 添加每天凌晨 2 点备份
0 2 * * * cd /path/to/backend && ./scripts/backup_db.sh
```

### 手动备份

```bash
cd backend
./scripts/backup_db.sh
```

备份文件将保存在 `backups/` 目录下，格式为：`yantou_db_YYYYMMDD_HHMMSS.sql.gz`

### 备份保留策略

- 自动删除 7 天前的备份文件
- 建议定期将重要备份文件归档到其他存储位置

## 恢复数据库

### 恢复步骤

1. 停止应用服务（如果正在运行）
2. 执行恢复脚本：

```bash
cd backend
./scripts/restore_db.sh backups/yantou_db_20240101_120000.sql.gz
```

3. 确认恢复成功后，重启应用服务

### 注意事项

- 恢复操作会覆盖当前数据库，请谨慎操作
- 恢复前建议先备份当前数据库
- 确保备份文件完整且未损坏

## 数据库维护

### 查看数据库大小

```bash
docker exec yantou-postgres psql -U postgres -c "
SELECT pg_size_pretty(pg_database_size('yantou_db'));
"
```

### 查看表大小

```bash
docker exec yantou-postgres psql -U postgres -d yantou_db -c "
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

### 清理日志表

定期清理过期的日志数据，避免数据库过大：

```sql
-- 删除 90 天前的操作日志
DELETE FROM sys_audit_log WHERE created_at < NOW() - INTERVAL '90 days';

-- 删除 90 天前的登录日志
DELETE FROM sys_login_log WHERE created_at < NOW() - INTERVAL '90 days';
```

## 监控

建议监控以下指标：

- 数据库大小
- 备份文件数量
- 备份文件大小
- 备份执行时间
- 数据库连接数


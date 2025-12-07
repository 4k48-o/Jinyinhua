#!/bin/bash
# 数据库恢复脚本

if [ -z "$1" ]; then
    echo "使用方法: $0 <备份文件路径>"
    echo "示例: $0 backups/yantou_db_20240101_120000.sql.gz"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "错误: 备份文件不存在: $BACKUP_FILE"
    exit 1
fi

echo "警告: 此操作将覆盖当前数据库！"
read -p "确认继续? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "操作已取消"
    exit 0
fi

echo "开始恢复数据库..."

# 如果是压缩文件，先解压
if [[ "$BACKUP_FILE" == *.gz ]]; then
    TEMP_FILE=$(mktemp)
    gunzip -c "$BACKUP_FILE" > "$TEMP_FILE"
    docker exec -i yantou-postgres psql -U postgres yantou_db < "$TEMP_FILE"
    rm "$TEMP_FILE"
else
    docker exec -i yantou-postgres psql -U postgres yantou_db < "$BACKUP_FILE"
fi

if [ $? -eq 0 ]; then
    echo "✓ 数据库恢复成功"
else
    echo "✗ 数据库恢复失败"
    exit 1
fi


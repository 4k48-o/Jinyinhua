#!/bin/bash
# 数据库备份脚本

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/yantou_db_${TIMESTAMP}.sql"

# 创建备份目录
mkdir -p ${BACKUP_DIR}

echo "开始备份数据库..."
docker exec yantou-postgres pg_dump -U postgres yantou_db > ${BACKUP_FILE}

if [ $? -eq 0 ]; then
    # 压缩备份文件
    gzip ${BACKUP_FILE}
    echo "✓ 数据库备份成功: ${BACKUP_FILE}.gz"
    
    # 删除 7 天前的备份
    find ${BACKUP_DIR} -name "yantou_db_*.sql.gz" -mtime +7 -delete
    echo "✓ 已清理 7 天前的备份文件"
else
    echo "✗ 数据库备份失败"
    exit 1
fi


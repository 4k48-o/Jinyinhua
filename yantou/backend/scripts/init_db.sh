#!/bin/bash
# 数据库初始化脚本

echo "检查 PostgreSQL 容器状态..."
if ! docker ps | grep -q yantou-postgres; then
    echo "启动 PostgreSQL 容器..."
    docker-compose up -d postgres
    echo "等待 PostgreSQL 启动..."
    sleep 5
fi

echo "检查数据库连接..."
docker exec yantou-postgres psql -U postgres -c "SELECT 1;" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ PostgreSQL 连接正常"
else
    echo "✗ PostgreSQL 连接失败"
    exit 1
fi

echo "数据库初始化完成！"


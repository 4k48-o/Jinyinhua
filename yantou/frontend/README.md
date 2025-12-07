# 企业级应用前端项目

基于 React + TypeScript + Ant Design 的企业级应用前端项目。

## 技术栈

- **框架**: React 18.x
- **语言**: TypeScript
- **构建工具**: Vite
- **UI 组件库**: Ant Design 5.x
- **路由**: React Router v6
- **状态管理**: Redux Toolkit
- **HTTP 客户端**: Axios
- **工具库**: dayjs, lodash-es

## 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API 接口
│   ├── components/        # 组件
│   │   ├── Layout/        # 布局组件
│   │   ├── Form/          # 表单组件
│   │   ├── Table/         # 表格组件
│   │   └── common/        # 通用组件
│   ├── pages/             # 页面
│   ├── store/             # 状态管理
│   ├── hooks/             # 自定义 Hooks
│   ├── utils/             # 工具函数
│   ├── router/            # 路由配置
│   ├── types/             # TypeScript 类型
│   └── assets/            # 静态资源
│       ├── images/        # 图片
│       ├── styles/        # 样式
│       └── fonts/         # 字体
├── .env.development       # 开发环境配置
├── .env.production        # 生产环境配置
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发环境运行

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

## 环境变量

### 开发环境 (.env.development)

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=企业级应用管理系统
VITE_APP_VERSION=1.0.0
```

### 生产环境 (.env.production)

```
VITE_API_BASE_URL=https://api.example.com/api/v1
VITE_APP_TITLE=企业级应用管理系统
VITE_APP_VERSION=1.0.0
```

## 开发规范

- 使用 TypeScript 严格模式
- 遵循 React Hooks 最佳实践
- 组件命名使用 PascalCase
- 函数命名使用 camelCase
- 使用 ESLint 和 Prettier 进行代码格式化

## 相关文档

- [前端开发计划](../doc/frontend-development-plan.md)
- [后端 API 文档](../backend/docs/API_DOCUMENTATION.md)


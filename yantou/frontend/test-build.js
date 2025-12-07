// 简单的语法检查
const fs = require('fs');
const files = [
  'src/App.tsx',
  'src/main.tsx',
  'src/router/index.tsx',
  'src/api/index.ts',
  'src/store/index.ts',
];

console.log('🔍 检查关键文件是否存在...');
files.forEach(file => {
  if (fs.existsSync(file)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} 不存在`);
  }
});

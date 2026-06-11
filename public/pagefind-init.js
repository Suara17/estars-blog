// pagefind-init.js — 独立入口，避开 Vite 打包器处理
// 放在 public/ 目录下，Astro 会原样复制到构建输出

(async () => {
    if (window.pagefind) return; // 防止重复初始化

    const PAGE_URL = '/pagefind/pagefind.js';

    try {
        // 1. 先验证文件存在
        const headResp = await fetch(PAGE_URL, { method: 'HEAD' });
        if (!headResp.ok) {
            throw new Error(`Pagefind script not found (${headResp.status})`);
        }

        // 2. 动态导入 pagefind 模块
        const mod = await import(PAGE_URL);

        // 3. 初始化选项（这也会触发索引加载）
        await mod.options({ excerptLength: 20 });

        // 4. 暴露到全局
        window.pagefind = mod;

        // 5. 通知所有监听者
        document.dispatchEvent(new CustomEvent('pagefindready'));

        console.log('[Pagefind-init] loaded successfully');
    } catch (err) {
        console.error('[Pagefind-init] failed:', err);
        document.dispatchEvent(new CustomEvent('pagefindloaderror'));
    }
})();

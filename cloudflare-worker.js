// ポータル管理プロキシ — Cloudflare Worker
//
// 【初回セットアップ】
// 1. https://dash.cloudflare.com → Workers & Pages → 「Create」→ Worker を作成
// 2. このファイルの内容をコードエディタに貼り付けて「Deploy」
// 3. Worker の Settings → Variables & Secrets → 以下の2つのシークレットを追加:
//      GH_TOKEN   : GitHubのPersonal Access Token（repoスコープ必要）
//      ADMIN_PASS : 管理ページのパスワード（例: 3535）
// 4. Worker の URL（例: https://portal-proxy.xxx.workers.dev）をコピー
// 5. admin.html 冒頭の WORKER_URL をそのURLに書き換えてコミット・プッシュ
//
// 【パスワード変更時】
// 管理ページの「設定 → パスワード変更」で保存後、
// CloudflareダッシュボードのADMIN_PASSシークレットも同じ値に更新してください。

const OWNER = 'sakadosoutan-boop';
const REPO  = 'portal';

const CORS = {
  'Access-Control-Allow-Origin':  '*',
  'Access-Control-Allow-Methods': 'GET, PUT, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-Admin-Pass',
};

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }

    const pass = request.headers.get('X-Admin-Pass') || '';
    if (!pass || pass !== env.ADMIN_PASS) {
      return resp({ error: 'Unauthorized' }, 401);
    }

    const BASE = `https://api.github.com/repos/${OWNER}/${REPO}`;
    const GH = {
      'Authorization':  `token ${env.GH_TOKEN}`,
      'Accept':         'application/vnd.github+json',
      'User-Agent':     'portal-proxy',
      'Content-Type':   'application/json',
    };

    const url  = new URL(request.url);
    const path = url.pathname.replace(/\/$/, '');

    // 接続確認
    if (path === '/api/check' && request.method === 'GET') {
      const r = await fetch(BASE, { headers: GH });
      return resp({ ok: r.ok }, r.ok ? 200 : 502);
    }

    // GitHub Actions workflow dispatch（AI チラシ読み取りトリガー）
    if (path === '/api/dispatch' && request.method === 'POST') {
      const r = await fetch(
        `${BASE}/actions/workflows/update-seminars.yml/dispatches`,
        { method: 'POST', headers: GH, body: JSON.stringify({ ref: 'main' }) }
      );
      return new Response(null, { status: r.status, headers: CORS });
    }

    // ファイル GET/PUT（SHA取得・保存・バイナリアップロード共通）
    if (path === '/api/file') {
      const filePath = url.searchParams.get('path');
      if (!filePath) return resp({ error: 'path required' }, 400);

      if (request.method === 'GET') {
        const r = await fetch(`${BASE}/contents/${filePath}`, { headers: GH });
        return resp(await r.json(), r.status);
      }

      if (request.method === 'PUT') {
        const body = await request.text();
        const r = await fetch(`${BASE}/contents/${filePath}`, {
          method: 'PUT', headers: GH, body,
        });
        return resp(await r.json(), r.status);
      }
    }

    return resp({ error: 'Not found' }, 404);
  }
};

function resp(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

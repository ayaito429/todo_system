# ============================================================
# フロントエンド用 Dockerfile（Next.js）
# ============================================================
# バックエンドとは別イメージなので、Dockerfile も別ファイル。
# Node が動く軽いイメージをベースにする。

FROM node:20-alpine
# ↑ Node.js 20 が入った軽量イメージ（Python の backend とは別なので別 Dockerfile）

WORKDIR /app
# ↑ コンテナ内の作業ディレクトリを /app に

COPY package.json package-lock.json* ./
# ↑ 依存情報だけ先にコピー（レイヤーキャッシュのため）

RUN npm install
# ↑ 依存をインストール（node_modules ができる）

COPY . .
# ↑ ソース一式をコンテナにコピー

EXPOSE 3000
# ↑ 「3000番で待ち受ける」という宣言（実際に開くのは Next.js）

CMD ["npm", "run", "dev"]
# ↑ コンテナ起動時に実行するコマンド（next dev で開発サーバー起動）

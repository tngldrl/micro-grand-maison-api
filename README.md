# Micro Grand Maison API - Core Backend API

Micro Grand Maison (MGM) のプロジェクトデータ管理、キューイング、およびエージェント連携を制御するバックエンド API サーバー。

## 🌟 主な機能

* **自律的コード探索 (Agentic Code Retrieval) 連携**:
  * チャットリクエストを受信すると、Gemini に対するファイルコンテキストの自動収集が走ります。
  * **Hop 0 (初期化)**: 最初に対象サービスの `key_files`（コード内に登録された中心的なファイル群）の内容を取得してプロンプトにインジェクションします。
  * **Hop 1〜6 (自律拡張)**: Gemini に「現在のコンテキストで足りない情報」を問合せ、必要なインポートファイルなどを GitHub API 経由で段階的にフェッチ・拡張します。最大 36 枚（6ホップ × ホップあたり最大6枚）まで辿り、最大 **100KB (102,400文字)** までの豊富なコード情報をメモリ空間（プロンプト）に保持してチャットに引き渡すことで、高精度な回答を実現します。
* **GitHub Webhook 連携と再解析処理**:
  * GitHub App と統合され、登録されたリポジトリへの git push をリアルタイムに捕捉。
  * 対象プロジェクトの `has_update` フラグを true に変更し、フロントエンドに「更新あり」のマークとプッシュ通知を即時送出します。
* **バックグラウンド・タスクワーカー (`queue_worker_loop`)**:
  * 登録されたリポジトリの新規解析、手動アップデート、webhook push 起因の再解析要求をキューで管理します。
  * スレッドがプロジェクトの `status` を `pending` / `analyzing` に切り替え、順番に MCP 解析サーバーへ `/analyze` リクエストを非同期で送信します。
  * タイムアウト誤判定を防ぐため、プロジェクトの `updated_at`（最終変更日時）を基準にした 15 分タイムアウト監視ロジックを実装。

---

## 📂 主要ディレクトリ・コード構造

```
micro-grand-maison-api/
├── main.py            # API ルート定義、チャットエンドポイント、コード探索ロジック、バックグラウンドキューワーカー
├── models.py          # SQLAlchemy を用いたデータベースモデル定義 (Project, Microservice, WebhookDelivery など)
├── database.py        # データベースセッション接続設定（PostgreSQL / SQLite 自動マイグレーション対応）
├── auth.py            # Firebase JSON Web Token (JWT) デコードおよび認証ミドルウェア
├── github_app.py      # GitHub App 認証、インストール用アクセストークン取得、リポジトリ探索用ヘルパー
└── requirements.txt   # Python 依存関係一覧
```

---
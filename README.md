# adk-poc

## セットアップ

1. 仮想環境を作成します:
   ```bash
   python -m venv _
   ```

2. 仮想環境を有効にします:
   - Windowsの場合:
     ```bash
     _\Scripts\activate
     ```
   - macOS/Linuxの場合:
     ```bash
     source _/bin/activate
     ```

3. 必要なライブラリをインストールします:
   ```bash
   pip install -r requirements.txt
   ```

4. `my_agent` ディレクトリに `.env` ファイルを作成し、以下の内容を記述します:
   ```
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=______________APIKEY__________________
   ```
   環境変数は外部LLMサービスによって異なります(https://google.github.io/adk-docs/get-started/quickstart/#set-up-the-model)

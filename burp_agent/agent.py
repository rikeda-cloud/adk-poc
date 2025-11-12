from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams


burp_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="burp_agent",
    instruction="""BurpSuiteを利用可能にするためのエージェント""",
    tools=[
        MCPToolset(connection_params=SseConnectionParams(url="http://127.0.0.1:9876/sse", headers={})),
    ],
)


root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    description="BurpSuiteの機能を利用可能なエージェント",
    instruction="""
    BurpSuiteを利用可能にするためのエージェント
    BurpのMCPは下記の機能が存在します。それらの機能を駆使して目的を達成してください。
    Tools:
        - base64_decode
            Base64でエンコードされた文字列をデコードします。
        
        - base64_encode
            文字列をBase64形式でエンコードします。
        
        - create_repeater_tab
            指定されたHTTPリクエストで新しいRepeaterタブを作成します。
        
        - generate_random_string
            指定された長さと文字セットでランダムな文字列を生成します。
        
        - get_active_editor_contents
            アクティブなメッセージエディタの内容を取得します。
        
        - get_proxy_http_history
            プロキシのHTTP履歴からアイテムを取得します。
        
        - get_proxy_http_history_regex
            プロキシのHTTP履歴から指定された正規表現に一致するアイテムを取得します。
        
        - get_proxy_websocket_history
            プロキシのWebSocket履歴からアイテムを取得します。
        
        - get_proxy_websocket_history_regex
            プロキシのWebSocket履歴から指定された正規表現に一致するアイテムを取得します。
        
        - output_project_options
            現在のプロジェクトレベルの設定をJSON形式で出力します。
        
        - output_user_options
            現在のユーザーレベルの設定をJSON形式で出力します。
        
        - send_http1_request
            HTTP/1.1リクエストを送信し、レスポンスを返します。
        
        - send_http2_request
            HTTP/2リクエストを送信し、レスポンスを返します。
        
        - send_to_intruder
            指定されたHTTPリクエストをIntruderに送信します。
        
        - set_active_editor_contents
            アクティブなメッセージエディタの内容を設定します。
        
        - set_project_options
            プロジェクトレベルの設定をJSON形式で設定します。
        
        - set_proxy_intercept_state
            Burp Proxyのインターセプト状態を有効または無効にします。
        
        - set_task_execution_engine_state
            Burpのタスク実行エンジンの状態（一時停止または一時停止解除）を設定します。
        
        - set_user_options
            ユーザーレベルの設定をJSON形式で設定します。
        
        - url_decode
            URLエンコードされた文字列をデコードします。
        
        - url_encode
            文字列をURLエンコードします。
    """,
    tools=[AgentTool(burp_agent),],
)

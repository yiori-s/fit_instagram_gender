# fit_instagram_gender

## 環境変数の設定
InstagramAPIキーをINSTAGRAM_ACCESS_TOKEN、AlchemyAPIキーをALCHEMYAPI_KEYとして環境変数を設定してください。
setting.pyでそれらの環境変数を読み込みます。
*setting.py
    import os
    instgram_access_token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
    alchemyapi_key = os.environ.get("ALCHEMYAPI_KEY")

## IPアドレスおよびポートの設定
([@main.py}(https://github.com/yiori-s/fit_instagram_gender/blob/master/main.py#L47-51))で、アプリケーションを起動するIPアドレスとポート番号を設定しています。
任意のIPアドレス、ポート番号に変更ができます。
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(debug=True, port=port, host='0.0.0.0')

## アプリケーションの実行
以下のコマンドでアプリケーションを実行してください。
    python main.py
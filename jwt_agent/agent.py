from google.adk.agents import LlmAgent
import jwt


def generate_jwt(header: dict, payload: dict, key: str, algorithm: str) -> dict:
    """
    PyJWTライブラリを用いて、指定したheaderとpayloadからJWTを生成する。
    JWTへの追加のheaderが必要ない場合は{}を指定してください。
    payloadが特にない場合は{}を指定してください。
    署名を必要としない場合、algorithm="none"を指定してください。
    """
    if algorithm == "none":
        token = jwt.encode(payload, key="", algorithm="none", headers=header)
    else:
        token = jwt.encode(payload, key, algorithm=algorithm, headers=header)
    return {"jwt": token}


def decode_jwt(token: str, algorithms: str) -> dict:
    """
    JWTをデコードしてheader, payload, signatureを返す。
    署名はいかなる時も検証されない。
    algorithmsを指定しない場合は空文字列を指定する。
    """
    # decodeはheaderを返さないので、get_unverified_headerを利用
    header = jwt.get_unverified_header(token)
    payload = jwt.decode(
        token,
        "",
        algorithms if algorithms != "" else None,
        options={"verify_signature": False},
    )

    # signature部分を手動で抽出
    parts = token.split(".")
    signature = parts[2] if len(parts) == 3 else ""
    return {"header": header, "payload": payload, "signature": signature}


root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="jwt_attack_agent",
    description="JWTの作成、閲覧、書き換えを行うことが可能なエージェント",
    instruction="""
    JWTの作成、JWTのheader, bodyの表示、JWTの書き換えを行うことが可能です。

    JWTの作成：
        generate_jwtツール関数を用いて、生成。

    JWTの閲覧：
        decode_jwtツール関数を用いて、デコード後、表示。

    JWTの書き換え：
        decode_jwtツール関数を用いて、書き換え前JWTのheader・payloadを確認し、
        generate_jwtツール関数を用いて、書き換え後のheader・payloadを指定して新たなJWTを作成。


    generate_jwtとdecode_jwt内ではPyJWTを用いています。下記はPyJWTのAPIリファレンスです。

    jwt.encode(payload, key, algorithm='HS256', headers=None, json_encoder=None)
        Encode the payload as JSON Web Token.

        Parameters:
            payload (dict) – JWT claims, e.g. dict(iss=..., aud=..., sub=...)
            key (str or bytes or jwt.PyJWK) –
                a key suitable for the chosen algorithm:
                    for asymmetric algorithms: PEM-formatted private key, a multiline string
                    for symmetric algorithms: plain string, sufficiently long for security
            algorithm (str) – algorithm to sign the token with, e.g. "ES256". If headers includes alg, it will be preferred to this parameter. If key is a jwt.PyJWK object, by default the key algorithm will be used.
            headers (dict) – additional JWT header fields, e.g. dict(kid="my-key-id").
            json_encoder (json.JSONEncoder) – custom JSON encoder for payload and headers
        Return type:
            str
        Returns:
            a JSON Web Token

    jwt.decode(jwt, key='', algorithms=None, options=None, audience=None, issuer=None, leeway=0)
        Verify the jwt token signature and return the token claims.

        Parameters:
            jwt (str) – the token to be decoded
            key (str or bytes or jwt.PyJWK) – the key suitable for the allowed algorithm
            algorithms (list) –
                allowed algorithms, e.g. ["ES256"] If key is a jwt.PyJWK object, allowed algorithms will default to the key algorithm.
                Warning: Do not compute the algorithms parameter based on the alg from the token itself, or on any other data that an attacker may be able to influence, as that might expose you to various vulnerabilities (see RFC 8725 §2.1). Instead, either hard-code a fixed value for algorithms, or configure it in the same place you configure the key. Make sure not to mix symmetric and asymmetric algorithms that interpret the key in different ways (e.g. HS* and RS*).
            options (dict) –
                extended decoding and validation options
                verify_signature=True verify the JWT cryptographic signature
                require=[] list of claims that must be present. Example: require=["exp", "iat", "nbf"]. Only verifies that the claims exists. Does not verify that the claims are valid.
                verify_aud=verify_signature check that aud (audience) claim matches audience
                verify_iss=verify_signature check that iss (issuer) claim matches issuer
                verify_exp=verify_signature check that exp (expiration) claim value is in the future
                verify_iat=verify_signature check that iat (issued at) claim value is an integer
                verify_nbf=verify_signature check that nbf (not before) claim value is in the past
                strict_aud=False check that the aud claim is a single value (not a list), and matches audience exactly
                Warning: exp, iat and nbf will only be verified if present. Please pass respective value to require if you want to make sure that they are always present (and therefore always verified if verify_exp, verify_iat, and verify_nbf respectively is set to True).
            audience (Union[str, Iterable]) – optional, the value for verify_aud check
            issuer (str) – optional, the value for verify_iss check
            leeway (float) – a time margin in seconds for the expiration check
        Return type:
            dict
        Returns:
            the JWT claims
    """,
    tools=[generate_jwt, decode_jwt],
)

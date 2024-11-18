import requests
import time
import hashlib
import hmac
import base64
from urllib.parse import quote

# 必要な認証情報
AWS_ACCESS_KEY = 'YOUR_AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'YOUR_AWS_SECRET_KEY'
ASSOCIATE_TAG = 'YOUR_AMAZON_ASSOCIATE_TAG'
REGION = 'us-east-1'  # 適切なリージョンを選択
ENDPOINT = 'webservices.amazon.com'
REQUEST_URI = '/onca/xml'

def get_amazon_signed_url(params):
    """Amazon Product Advertising API に送信するための署名付き URL を生成"""
    params['Service'] = 'AWSECommerceService'
    params['AWSAccessKeyId'] = AWS_ACCESS_KEY
    params['AssociateTag'] = ASSOCIATE_TAG
    params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    params['SignatureMethod'] = 'HmacSHA256'
    params['SignatureVersion'] = '2'

    # パラメータをアルファベット順にソート
    sorted_params = sorted(params.items())
    
    # 署名のベース文字列を作成
    canonical_query_string = '&'.join([f"{quote(str(k))}={quote(str(v))}" for k, v in sorted_params])
    string_to_sign = f"GET\n{ENDPOINT}\n{REQUEST_URI}\n{canonical_query_string}"
    
    # 署名を作成
    digest = hmac.new(AWS_SECRET_KEY.encode('utf-8'),
                       string_to_sign.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode('utf-8')

    # 最終的な URL を作成
    signed_url = f"https://{ENDPOINT}{REQUEST_URI}?{canonical_query_string}&Signature={quote(signature)}"
    return signed_url

def search_amazon_products(query):
    """Amazon Product Advertising API を使用して商品を検索"""
    params = {
        'Operation': 'ItemSearch',
        'SearchIndex': 'All',  # または特定のカテゴリを指定
        'Keywords': query,
        'ResponseGroup': 'Images,ItemAttributes,Offers',
    }

    # 署名付き URL を取得
    signed_url = get_amazon_signed_url(params)
    
    # API リクエストを送信
    response = requests.get(signed_url)
    if response.status_code == 200:
        return response.text  # XML 形式で返されるため、必要に応じてパースする
    else:
        return None

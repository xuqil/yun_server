import base64
import hmac
import hashlib
import base64


class Token:
    """
    生成token
    解析token
    """
    def __init__(self, expire=7200):
        self.expire = expire

    def generate_token(self, key, timestamp):
        """
           生成token
           :param key: 生成token的code
           :param timestamp: 用于生成token的时间戳
           :return: key
           """
        ts_str = str(float(timestamp) + self.expire)[:10]
        # print(ts_str)
        ts_byte = ts_str.encode("utf-8")
        sha1_result = hmac.new(str(key).encode("utf-8"), ts_byte, 'sha1').hexdigest()
        token = ts_str + ':' + sha1_result
        # print(token)
        b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
        return b64_token.decode("utf-8")

    def certify_token(self, key, token, timestamp):
        """
        验证token
        :param key: 生成token的code
        :param token: token
        :param timestamp: 验证token的有效性
        :return: 是否正确和过期
        """
        token_str = base64.urlsafe_b64decode(str(token)).decode('utf-8')
        token_list = token_str.split(':')
        # print("时间戳", token_list[0][:10])
        if len(token_list) != 2:
            return False
        ts_str = token_list[0][:10]
        if float(ts_str) < float(timestamp):
            # print("超时")
            return False
        known_sha1_result = token_list[1]
        sha1 = hmac.new(str(key).encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
        calc_sha1_result = sha1.hexdigest()
        if calc_sha1_result != known_sha1_result:
            return False
        return True

    def valid_time(self, token):
        """
        :param token: token
        :return: 返回有效时间戳
        """
        token_str = base64.urlsafe_b64decode(token).decode('utf-8')
        token_list = token_str.split(':')
        return token_list[0][:10]


def md5(arg):
    """
    md5加密
    :param arg: 加密前的数据
    :return: 加密后的数据
    """
    m = hashlib.md5()
    m.update(arg.encode("utf8"))
    return m.hexdigest()


def base64_encryption(str_encrypt):
    """
    base64加密
    :param str_encrypt: 被加密的字符串
    :return:
    """
    return base64.b64encode(str_encrypt.encode('utf-8')).decode("ascii")


def base64_decode(str_encrypt):
    """
    base64解密
    :param str_encrypt: base64加密后的字符串
    :return:
    """
    return base64.b64decode(str_encrypt).decode()

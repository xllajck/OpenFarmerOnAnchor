# windows下导包
from Cryptodome.Cipher import AES


from binascii import b2a_hex, a2b_hex


class prpcrypt():
    def __init__(self, key):
        self.key = self.handle_length(key)
        self.mode = AES.MODE_CBC

    def handle_length(self, text):
        length = 16
        count = len(text)
        if (count % length != 0):
            add = length - (count % length)
        else:
            add = 0
        text = text + ('\0' * add)
        return text.encode()

    def encrypt(self, text):
        text = self.handle_length(text)
        cryptor = AES.new(self.key, self.mode, self.key)
        ciphertext = cryptor.encrypt(text)
        return b2a_hex(ciphertext).decode()

    # 解密函数
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode().rstrip('\0')



def encrypt_key():
    print("这里加密你的私钥，输入账号和私钥，例如：openfarmercn aksdfhk328923bk32h4kl23h4l32j4hklj")
    a, b = (input("请输入账号和私钥(空格隔开)：").split())
    pc = prpcrypt(a)
    encrypt_text = pc.encrypt(b)
    print("您的加密字符串是：", encrypt_text)
    print("将加密串复制到user.yml的private_key字段")


if __name__ == '__main__':
    encrypt_key()

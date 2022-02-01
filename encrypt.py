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
        try:
            text = self.handle_length(text)
            cryptor = AES.new(self.key, self.mode, self.key)
            ciphertext = cryptor.encrypt(text)
            return b2a_hex(ciphertext).decode()
        except ValueError as e:
            return False


    # 解密函数
    def decrypt(self, text):
        try:
            cryptor = AES.new(self.key, self.mode, self.key)
            plain_text = cryptor.decrypt(a2b_hex(text))
            return plain_text.decode().rstrip('\0')
        except UnicodeDecodeError as e:
            return False

def save_to_file(file_name, contents):
    with open(file_name, 'w') as f:
        f.write(contents)


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
        return content

def encrypt_key():
    encrypttext = read_file('encrypttext')
    if not encrypttext:
        private_key = input('请输入私钥：')
        key_pwd = input('请输入密码：')
        pc = prpcrypt(key_pwd)
        encrypt_key = pc.encrypt(private_key)
        save_to_file('encrypttext', encrypt_key)
    else:
        key_pwd = input('请输入密码：')
        pc = prpcrypt(key_pwd)
        decrypt_key = pc.decrypt(encrypttext)
        print(decrypt_key)

if __name__ == '__main__':
    encrypt_key()

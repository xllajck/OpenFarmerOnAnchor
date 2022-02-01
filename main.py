#!/usr/bin/python3
import getpass

from encrypt import prpcrypt, read_file, save_to_file
from farmer import Farmer
import logger
from logger import log
import yaml
import sys
import utils
from settings import load_user_param, user_param, cfg


def run(config_file: str):
    with open(config_file, "r", encoding="utf8") as file:
        user: dict = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
    load_user_param(user)

    encrypttext = read_file('encrypttext')
    if not encrypttext:
        private_key = getpass.getpass('请输入私钥：')
        key_pwd = getpass.getpass("请输入密码:")
        pc = prpcrypt(key_pwd)
        encrypt_key = pc.encrypt(private_key)
        if not encrypt_key:
            print('私钥格式有误，请重新输入')
            exit()
        save_to_file('encrypttext', encrypt_key)
    else:
        cfg.key_pwd = getpass.getpass("请输入密码:")

    logger.init_loger(user_param.wax_account)
    log.info("项目开源地址：https://github.com/lintan/OpenFarmerOnAnchor")
    log.info("WAX账号: {0}".format(user_param.wax_account))
    farmer = Farmer()
    farmer.wax_account = user_param.wax_account
    if user_param.use_proxy:
        farmer.proxy = user_param.proxy
        log.info("use proxy: {0}".format(user_param.proxy))
    farmer.init()
    farmer.start()
    log.info("=====开始自动化=====")
    return farmer.run_forever()




def main():

    try:
        user_yml = "user.yml"
        if len(sys.argv) == 2:
            if sys.argv[1] == 'clear':
                save_to_file('encrypttext', '')
                print('密钥已删除，请重新输入')
                exit()
            else:
                user_yml = sys.argv[1]
        run(user_yml)
    except Exception:
        log.exception("start error")
    input()


if __name__ == '__main__':
    main()

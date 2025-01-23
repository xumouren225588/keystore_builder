import subprocess
import argparse
import os

def generate_password():
    """使用openssl生成随机密码"""
    try:
        result = subprocess.run(
            ["openssl", "rand", "-base64", "16"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"生成密码失败: {e}")
        exit(1)

def generate_keystore(keystore_path, password, alias, validity, dname):
    """使用keytool生成keystore文件"""
    try:
        # 构造keytool命令
        command = [
            "keytool",
            "-genkey",
            "-keystore", keystore_path,
            "-storepass", password,
            "-keypass", password,
            "-alias", alias,
            "-dname", dname,
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", str(validity),
        ]
        subprocess.run(command, check=True)
        print(f"Keystore文件已生成: {keystore_path}")
    except subprocess.CalledProcessError as e:
        print(f"生成keystore失败: {e}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description="生成keystore文件")
    parser.add_argument("-o", "--output", required=True, help="输出keystore文件路径")
    parser.add_argument("-v", "--validity", type=int, required=True, help="证书有效期（天数）")
    parser.add_argument("-cn", "--common-name", required=True, help="通用名称 (CN)")
    parser.add_argument("-o", "--organization", required=True, help="组织名称 (O)")
    parser.add_argument("-l", "--locality", required=True, help="城市或地区名称 (L)")
    parser.add_argument("-st", "--state", required=True, help="州或省份名称 (ST)")
    parser.add_argument("-c", "--country", required=True, help="国家代码 (C)")
    args = parser.parse_args()

    # 生成随机密码
    password = generate_password()

    # 提取别名（默认为"mykey"）
    alias = "mykey"

    # 构造-dname参数
    dname = f"CN={args.common_name},O={args.organization},L={args.locality},ST={args.state},C={args.country}"

    # 生成keystore
    generate_keystore(
        keystore_path=args.output,
        password=password,
        alias=alias,
        validity=args.validity,
        dname=dname,
    )

if __name__ == "__main__":
    main()

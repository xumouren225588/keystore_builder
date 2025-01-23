import subprocess
import argparse
import os

def generate_random_string(length=16):
    """使用openssl生成随机Base64字符串"""
    try:
        result = subprocess.run(
            ["openssl", "rand", "-base64", str(length)],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"生成随机字符串失败: {e}")
        exit(1)

def generate_keystore(password, alias, validity, dname):
    """使用keytool生成keystore文件"""
    import os
    os.mkdir('output')
    try:
        # 构造keytool命令
        command = [
            "keytool",
            "-genkey",
            "-keystore", 'output/keystore.jks',
            "-storepass", password,
            "-keypass", password,
            "-alias", alias,
            "-dname", dname,
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", str(validity),
        ]
        subprocess.run(command, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"生成keystore失败: {e}")
        exit(1)

def save_credentials(output_dir, keystore_path, password, alias):
    """将keystore路径、密码和别名保存到文本文档"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    credentials_file = os.path.join(output_dir, "credentials.txt")
    with open(credentials_file, "w") as f:
        f.write(f"Password: {password}\n")
        f.write(f"Alias: {alias}\n")
    

def main():
    parser = argparse.ArgumentParser(description="生成keystore文件")
    
    parser.add_argument("-v", "--validity", type=int, required=True, help="证书有效期（天数）")
    parser.add_argument("-cn", "--common-name", required=True, help="通用名称 (CN)")
    parser.add_argument("-org", "--organization", required=True, help="组织名称 (O)")
    parser.add_argument("-l", "--locality", required=True, help="城市或地区名称 (L)")
    parser.add_argument("-st", "--state", required=True, help="州或省份名称 (ST)")
    parser.add_argument("-c", "--country", required=True, help="国家代码 (C)")
    args = parser.parse_args()

    # 指定保存目录
    output_dir = "output"  # 硬编码保存目录路径

    # 生成随机密码和别名
    password = generate_random_string(16)
    alias = generate_random_string(16)

    # 构造dname参数
    dname = (
        f"CN={args.common_name},"
        f"O={args.organization},"
        f"L={args.locality},"
        f"ST={args.state},"
        f"C={args.country}"
    )

    # 生成keystore
    generate_keystore(
        password=password,
        alias=alias,
        validity=args.validity,
        dname=dname,
    )

    # 保存凭证到指定目录
    save_credentials(
        output_dir=output_dir
        password=password,
        alias=alias,
    )

if __name__ == "__main__":
    main()

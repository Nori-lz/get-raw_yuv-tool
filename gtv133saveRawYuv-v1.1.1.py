import requests  
import os
import subprocess 
import paramiko 
import json
import time  
import sys
import cv2
import numpy as np


# 私钥字符串
key_str = '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAxqt7zuejJLyP0cVa8O7kJ5rRkyulCjQpdZGf0IFYYKyMKy0+
ZcLFnRkUEK7ELV23Sly+fACqDk3MNyVSHaYBqRIGSTTGPfxx5wU7ym6XCoh3IJ/n
H2HIYsNOcB6523wfqxoM0/YKDwMi8k6mKX1ERkhg0JBCor4yUx38wEun9Rv2ctFG
uTL+PA6RS1lZg0HzRHXFzvlgmdkZWMnm51gOIPsvBSofgytFI0a6cLZy8XFwGiHY
XkfakO+E6Z0fOVc3eUd2tMyq1fmI8F4C8CpzGbZXfI0dhWxCHXK8c+GqNt8ryn7X
649YX21upaiQqfugmMhUP7/+2szo/RIYd30CEwIDAQABAoIBAEQ+Q5kfGHtWClEU
adi5NsYj+DmFlHucz2EDVNJam/EZVEzAjd6GuTrtkmbooZqzxnJUyVnvIHspXizT
NRHaJFffSSl8Z1yDitzAf3lZ46hKmCEszEeLXzoNvLPm2hD64iX0HNPygCIIAcka
GxnFXd6GnjsGUt10V/UVJ+0mD9ux1CrBz4PU00jwtiCa/Pqr0djjH8vbqu04TwlJ
Zoo5nGi1YjFsnTKAHv0JGkLkxALuURfUll1rcrQwTr5ixAW4tFFZk0/dyoIOn10J
Ldzsou051tPDxbz2U2bQIKubEXcs1MTlqVzgmrea87sWiLxca7+Q9uch2tuR7E9B
zS9bygECgYEA7GeWYxzSsWO1oyj9Ydsi2sSaMA/ht6HEKC/s3qibkQ72x+92QlTq
pkwrHr9KrH6JjjuCroPrEOmGy39ScmJZhNC6ALxSTldieSHnO4C13Ca9qpQjy2Vv
AsDoyg0AP1YZpFKGgl51Nb2Absm5s2ZMxMBKCp+jOEzOC1Ax27IkqbECgYEA1yMt
2qGacUKPKUCMwbxmRteui5GoOydZ8VLMHPIifFDzW4tvpj4cwojHSJavkCQYmTPj
9csO6a5J8RsgnjAAIYgwnViInf9OFa2dxhejK3zsnuzW7VFXfUGSDKacT4914eB4
oHwRUMD5bMbkcyf36M9AWhcwOKo76R/jXva7lQMCgYBIgEBT5ywKsRysjE6hKzaW
R0NOSCCeU6M3+/K2GpmTNDak/KCVGTvZgnSa+mmpWylOkJu0b8qwph3r3QFpCRaR
L/5LaXYIhq4xnh8vVXrwqIT0gngz0cjo3EbIaJJR2lME3TZZVyS1NYfk8kLcbRxQ
HvTWKz1Ab/Wk7JRN32V1EQKBgDrV6R1oorckz8glWhlFr+bh519OF2cODP/9d8rW
wW2kKdm4WXFqfS0KgQ2uABd4d622TjqTLOHlg11H4PTCBdclyr3NT5d+EdnF4Gcj
YcFr6b5Q4TqHy1h7DTkee5Malc+PNw4UwBuImu4PurxvitIFlADPZKWqkLXhvanj
6ksHAoGBALFCQ8vlCKOIEFRhhsgHjBryqCBUTAspJ3fzrDhgTPH+8utqK0E1jBPA
MhTf9N2MDi3mG9jawFH30VyWdeEBf6uA5+XQwMZXsMa0MvQ5vvsKWiSox545Wth1
6pavFFTGuQfBRPix9MSO2zARTX6+eReG1lYt0BKnhl6XvVq/3I/4
-----END RSA PRIVATE KEY-----'''

def exec_command_and_wait(ssh, command):  
    stdin, stdout, stderr = ssh.exec_command(command)  
    while not stdout.channel.recv_ready() and not stderr.channel.recv_stderr_ready() and not stdout.channel.exit_status_ready():  
        time.sleep(0.1)  
    return stdout.read().decode(), stderr.read().decode()

def httpGoto(hostname):
    session = requests.Session()
    url = f'http://{hostname}:8858'  
    headers = {  
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': f'{hostname}:8858',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    }  
    session.headers.update(headers)
    response = session.get(url)
    # response1 = session.get(f'http://{hostname}:8858/ApicalControl.xsl')
    # response2 = session.get(f'http://{hostname}:8858/css/main.min.css')
    # response3 = session.get(f'http://{hostname}:8858/js/main.min.js')
    # response4 = session.get(f'http://{hostname}:8858/fonts/foundation-icons.woff')
    # response5 = session.get(f'http://{hostname}:8858/command.json')
    # response6 = session.get(f'http://{hostname}:8858/img/ct32.png')
    # response7 = session.get(f'http://{hostname}:8858/version')
    response8 = session.post(f'http://{hostname}:8858/am','"boff":264;"size":1024;"init":t')
    # while response8.status_code != 200:
    #     response8 = session.post(f'http://{hostname}:8858/am','"boff":264;"size":1024;"init":t')
    # print(response.text)
    # print('**************************************************************')
    # print(response1.text)
    # print('**************************************************************')
    # print(response2.text)
    # print('**************************************************************')
    # print(response3.text)
    # print('**************************************************************')
    # print(response4.text)
    # print('**************************************************************')
    # print(response5.text)
    # print('**************************************************************')
    # print(response6.text)
    # print('**************************************************************')
    session.close()

def httpGet(hostname,data):
    url = f'http://{hostname}:8858/fw/get'  
    headers = {  
        'Host': f'${hostname}:8858',  
        'Connection': 'keep-alive',  
        'Content-Length': '26',  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'Content-Type': 'text/plain;charset=UTF-8',  
        'Accept': '*/*',  
        'Origin': f'http://${hostname}:8858',  
        'Referer': f'http://${hostname}:8858/',  
        'Accept-Encoding': 'gzip, deflate',  
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'  
    }  
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        httpGoto(hostname)
        response = requests.post(url, headers=headers, data=data)
    print(response.text)
    jstr = json.loads(response.text)
    return jstr['val']

def httpSet(hostname,data):
    url = f'http://{hostname}:8858/fw/set'  
    headers = {  
        'Host': f'${hostname}:8858',  
        'Connection': 'keep-alive',  
        'Content-Length': '26',  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',  
        'Content-Type': 'text/plain;charset=UTF-8',  
        'Accept': '*/*',  
        'Origin': f'http://${hostname}:8858',  
        'Referer': f'http://${hostname}:8858/',  
        'Accept-Encoding': 'gzip, deflate',  
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'  
    }  
    response = requests.post(url, headers=headers, data=data)
    print(response.text)

def nv12_to_rgb_bt709(nv12, width, height, isfull=True): 
    nv12 = nv12.astype(np.float32) 
    y_size = width * height  
    uv_size = width * height // 2  
    y = nv12[:y_size].reshape((height, width))  
    uv = nv12[y_size:y_size + uv_size].reshape((height // 2, width // 2, 2))  
    u = np.repeat(uv[:, :, 0], 2, axis=0)  
    u = np.repeat(u, 2, axis=1)  
    v = np.repeat(uv[:, :, 1], 2, axis=0)  
    v = np.repeat(v, 2, axis=1)  
    if isfull == False:  
        y = (y - 16)*255/219  
        u = (u - 16)*255/224  
        v = (v - 16)*255/224  
    y = y  
    u = u - 128  
    v = v - 128 
    # BT.709 full range  
    r = y + 1.5748 * v  
    g = y - 0.1873 * u - 0.4681 * v  
    b = y + 1.8556 * u  
    r = np.clip(r, 0, 255).astype(np.uint8)  
    g = np.clip(g, 0, 255).astype(np.uint8)  
    b = np.clip(b, 0, 255).astype(np.uint8)  
    rgb = np.stack((b, g, r), axis=2)  
    return rgb  
#print('...\n')

def httpRead(hostname,data):
    url = f'http://{hostname}:8858/hw/read'  
    headers = {  
        'Host': f'${hostname}:8858',  
        'Connection': 'keep-alive',  
        'Content-Length': '26',  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'Content-Type': 'text/plain;charset=UTF-8',  
        'Accept': '*/*',  
        'Origin': f'http://${hostname}:8858',  
        'Referer': f'http://${hostname}:8858/',  
        'Accept-Encoding': 'gzip, deflate',  
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'  
    }  
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        httpGoto(hostname)
        response = requests.post(url, headers=headers, data=data)
    # print(response.text)
    jstr = json.loads(response.text)
    return jstr['bytes']
    
def get_raw_yuv(hostname,savepath,capture_count):
    # 创建一个SSH客户端实例
    ssh = paramiko.SSHClient()
    # 设置SSH客户端在遇到未知主机密钥时自动添加到本地known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 将私钥字符串写入临时文件
    with open(f'{sys.argv[0]}.key', 'w') as file:
        file.write(key_str)
    # 使用临时私钥文件建立 SSH 连接，并禁用指定的公钥算法
    ssh.connect(hostname, 22, 'root', key_filename=f'{sys.argv[0]}.key',disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})
    # 删除临时私钥文件，确保私钥不会在本地磁盘上长期存储
    os.remove(f'{sys.argv[0]}.key')
    # 打开 SFTP 会话，用于文件传输
    sftp = ssh.open_sftp()

    SYSTEM_INTEGRATION_TIME = httpGet(hostname,'"sec":3;"cmd":36' )
    print(SYSTEM_INTEGRATION_TIME)
    SYSTEM_SENSOR_ANALOG_GAIN = httpGet(hostname,'"sec":3;"cmd":40' )
    print(SYSTEM_SENSOR_ANALOG_GAIN)
    SYSTEM_AWB_RED_GAIN = httpGet(hostname,'"sec":3;"cmd":46' )
    SYSTEM_AWB_BLUE_GAIN = httpGet(hostname,'"sec":3;"cmd":47' )
    print(SYSTEM_AWB_RED_GAIN,SYSTEM_AWB_BLUE_GAIN)
    stdout, stderr = exec_command_and_wait(ssh,'cd /nextvpu/example/media/vi_venc_rtsp;rm -rf data;sync')
    

    for i in range(capture_count):
        # 触发新帧生成（原触发命令前移）
        httpSet(hostname,'"sec":6;"cmd":112;"page":1')
        httpSet(hostname,'"sec":6;"cmd":113;"page":1')
        time.sleep(1)  # 增加等待确保文件生成

        # 获取带序号的文件名
        stdoutraw, _ = exec_command_and_wait(ssh,'ls /nextvpu/example/media/vi_venc_rtsp/data/raw')
        raw = stdoutraw.rstrip('\r\n ').split()[-1]  # 获取最新文件
        stdoutyuv, _ = exec_command_and_wait(ssh,'ls /nextvpu/example/media/vi_venc_rtsp/data/yuv')
        yuv = stdoutyuv.rstrip('\r\n ').split()[-1]

        # 添加序号标识
        sequence = f'-0{i+1}'
        if raw:
            rawnew = raw.rstrip('.raw')
            rawsavepath = f'{savepath}/{rawnew}_exp{SYSTEM_INTEGRATION_TIME}_gain{SYSTEM_SENSOR_ANALOG_GAIN}_r{SYSTEM_AWB_RED_GAIN}_b{SYSTEM_AWB_BLUE_GAIN}{spectrum}{sequence}.raw'
            sftp.get(f'/nextvpu/example/media/vi_venc_rtsp/data/raw/{raw}', rawsavepath)
        else:
            print("no raw file!!!!!!!!!!!!!!!!!!!!!!!!!")
        if yuv:
            yuvnew = yuv.rstrip('.yuv')
            yuvsavepath = f'{savepath}/{yuvnew}_exp{SYSTEM_INTEGRATION_TIME}_gain{SYSTEM_SENSOR_ANALOG_GAIN}_r{SYSTEM_AWB_RED_GAIN}_b{SYSTEM_AWB_BLUE_GAIN}{spectrum}{sequence}.yuv'
            sftp.get(f'/nextvpu/example/media/vi_venc_rtsp/data/yuv/{yuv}', yuvsavepath)
            frame_height = httpRead(hostname,'"type":"r";"offset":154;"size":2')
            frame_width  = httpRead(hostname,'"type":"r";"offset":152;"size":2')
            frame_height = int.from_bytes(frame_height, byteorder='little')
            frame_width  = int.from_bytes(frame_width, byteorder='little')
            file=open(yuvsavepath,'rb')
            yuvfile = file.read()
            file.close()
            yuvfile=np.frombuffer(yuvfile, dtype = np.uint8, count=frame_width*frame_height*3//2)
            bgr = nv12_to_rgb_bt709(yuvfile,frame_width,frame_height)
            # yuvfile=yuvfile.reshape(frame_height*3//2,frame_width,order='c')
            # bgr=cv2.cvtColor(yuvfile,cv2.COLOR_YUV2BGR_NV12)
            bgrsavepath = f'{savepath}/{yuvnew}_exp{SYSTEM_INTEGRATION_TIME}_gain{SYSTEM_SENSOR_ANALOG_GAIN}_r{SYSTEM_AWB_RED_GAIN}_b{SYSTEM_AWB_BLUE_GAIN}{spectrum}{sequence}.png'
            cv2.imwrite(bgrsavepath, bgr)
            print(bgrsavepath)
        else:
            print("no yuv file!!!!!!!!!!!!!!!!!!!!!!!!!")

    # 关闭 SFTP 会话，释放系统资源
    sftp.close()
    
if __name__ == "__main__":
    hostname = '192.168.70.224'  # 板端IP地址
    savepath = r'D:\PycharmFile\get raw_yuv tool\000'  # 图片存放位置
    capture_count = 2  # 设置抓取次数（2或3次）

    """
    # 初始化 spectrum 变量为空字符串
    spectrum = ''
    # 检查命令行参数数量是否大于 1
    if len(sys.argv) > 1:
        # 如果有额外参数，将第二个参数添加到 spectrum 变量中，并在前面加上 - 符号
        spectrum = '-'+sys.argv[1]

    代码精简：
    spectrum = f'-{sys.argv[1]}' if len(sys.argv) > 1 else ''
    """
    # 处理命令行参数
    spectrum = f'-{sys.argv[1]}' if len(sys.argv) > 1 else ''

    get_raw_yuv(hostname,savepath,capture_count)

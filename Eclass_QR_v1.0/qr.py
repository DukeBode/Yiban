# 生成带logo的二维码图片
import qrcode
from PIL import Image
import os


def make_logo_qr(str='博德校园', logo='RMC', save='博德校园'):
    # 参数配置
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=1
    )
    # 添加转换内容
    qr.add_data(str)
    #
    qr.make(fit=True)
    # 生成二维码
    img = qr.make_image()
    #
    img = img.convert("RGBA")
 
    # 添加logo
    if logo and os.path.exists(logo):
        icon = Image.open(logo)
        # 获取二维码图片的大小
        img_w, img_h = img.size
 
        factor = 2.5
        size_w = int(img_w/factor)
        size_h = int(img_h/factor)
 
        # logo图片的大小不能超过二维码图片的1/4
        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
        # 详见：http://pillow.readthedocs.org/handbook/tutorial.html
 
        # 计算logo在二维码图中的位置
        w = int((img_w-icon_w)/2)
        h = int((img_h-icon_h)/2)
        icon = icon.convert("RGBA")
        img.paste(icon, (w, h), icon)
        # 详见：http://pillow.readthedocs.org/reference/Image.html#PIL.Image.Image.paste
 
    # 保存处理后图片
    img.save('code/'+save)


if __name__ == '__main__':
    filename = input('请输入文档名及链接：')
    files = open(filename, 'r')
    for eachLine in files:
        name = eachLine.split('\t')[0] + '.png'
        logo = 'LOGO.png'
        url = eachLine.split('\t')[1]
        make_logo_qr(url, logo, name)

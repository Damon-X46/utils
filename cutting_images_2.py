"""
    author:nrzheng
    function:cutting pic
    edition:final_3.0
    date:2022.5.16

    说明: 只在三通道的图上调通了, 单通道的图以及索引图都需要改改, 很容易
    所以参数设置中的channels和if_cmap就暂时没有用了
"""
import os
import argparse
import glob
from PIL import Image
import numpy as np
import math
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = None

label_mapping = {0:[0,0,255], 1:[139,0,0], 2:[83,134,139], 
                3:[255,0,0], 4:[205,173,0], 5:[0,255,0], 
                6:[0,139,0], 7:[189,183,107], 8:[178,34,34]}
n_labels = len(label_mapping)

def parse_args():
    """
        参数设置
    """
    parser = argparse.ArgumentParser(description='cutting pic')
    parser.add_argument('--path', help='the path of big images', default=r'D:\code_python\try\aaa')
    parser.add_argument('--save_path', help='the path of small images', default=r'D:\code_python\try\bbb')
    parser.add_argument('--ext', help='the extension of the images', default='.png')
    parser.add_argument('--channels', help='the number of channels', default=3)
    parser.add_argument('--if_cmap', help='if using the color map or not', default=False)
    parser.add_argument('--size', help='the cutting size', default=512)
    parser.add_argument('--strides', help='the moving strides', default=256)
    parser.add_argument('--if_pad', help='if padding the images(using 0 padding)', default=True)

    args = parser.parse_args()
    return args

def get_cmap():
    labels = np.ndarray((n_labels, 3), dtype='uint8')
    for i, (k, v) in enumerate(label_mapping.items()):
        labels[i] = v
    cmap = np.zeros([768], dtype='uint8')
    index = 0
    for i in range(0, n_labels):
        for j in range(0, 3):
            cmap[index] = labels[i][j]
            index += 1
    print('cmap define finished')
    return cmap

def gen_pad_img(raw_img_shape, args):
    """
        生成需要padding后的图像, 都是0, 出去该函数再赋值
    """
    small_img_size = args.size
    strides = args.strides
    h, w, c = raw_img_shape

    row = math.floor((h - small_img_size) / strides) + 1
    col = math.floor((w - small_img_size) / strides) + 1

    if args.if_pad:
        row = row + 1
        col = col + 1
    pad_img = np.zeros(((row - 1) * strides + small_img_size, (col - 1) * strides + small_img_size, c))
    return row, col, pad_img

def pic_cutting(args, images):
    """
        切图代码
    """
    save_path = args.save_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for ii, image in enumerate(images):
        image_names = os.path.split(image)[1]                   # 每张大图的名字, 带扩展
        image_name, ext = os.path.splitext(image_names)
        img = Image.open(image)
        img = np.asarray(img)
        img_shape = img.shape                                   # 大图的尺寸

        row, col, pad_img = gen_pad_img(img_shape, args)   # 计算行, 列, 并返回padding后的图像

        pad_shape = pad_img.shape
        if pad_shape > img_shape:
            pad_img[:img_shape[0], :img_shape[1], :] = img
        else:
            pad_img[:,:,:] = img[:pad_shape[0], :pad_shape[1], :]

        del img
        stride = args.strides

        id_hang = 1
        for i in tqdm(range(row), total=row):
            row_start = i * stride
            row_end = i * stride + args.size
            id_lie = 1
            for j in range(col):
                col_start = j * stride
                col_end = j * stride + args.size
                if args.channels == 3:
                    small_pic = pad_img[row_start:row_end, col_start:col_end, :]
                elif args.channels == 1:
                    small_pic = pad_img[row_start:row_end, col_start:col_end]
                small_name = 'image' + str(ii + 1).rjust(3, '0') + '_' + str(id_hang).rjust(3, '0') + 'row_' + str(id_lie).rjust(3, '0') + 'col' + ext
                small_pic = Image.fromarray(np.uint8(small_pic))
                if args.if_cmap:
                    small_pic.putpalette(args.cmap)
                small_pic.save(os.path.join(save_path, small_name))
                id_lie += 1
            id_hang += 1

def main():
    """
        主函数
    """
    args = parse_args()
    args.cmap = get_cmap()
    images = glob.glob(os.path.join(args.path, '*{}'.format(args.ext)))
    pic_cutting(args, images)
    pass

if __name__ == '__main__':
    main()


# """
#     author:nrzheng
#     function:cutting pic
#     edition:final_2.0
#     date:2021.12.26
# """
# import os
# import argparse
# import glob
# from PIL import Image
# import numpy as np
# import math
# from tqdm import tqdm

# Image.MAX_IMAGE_PIXELS = None

# label_mapping = {0:[0,0,255], 1:[139,0,0], 2:[83,134,139], 
#                 3:[255,0,0], 4:[205,173,0], 5:[0,255,0], 
#                 6:[0,139,0], 7:[189,183,107], 8:[178,34,34]}
# n_labels = len(label_mapping)

# def parse_args():
#     """
#         参数设置
#     """
#     parser = argparse.ArgumentParser(description='cutting pic')
#     parser.add_argument('--path', help='the path of big images', default=r'F:\znr_GF3\lab_test')
#     parser.add_argument('--save_path', help='the path of small images', default=r'F:\znr_GF3\dataset\lab_test_256')
#     parser.add_argument('--ext', help='the extension of the images', default='.png')
#     parser.add_argument('--channels', help='the number of channels', default=1)
#     parser.add_argument('--if_cmap', help='if using the color map or not', default=True)
#     parser.add_argument('--size', help='the cutting size', default=256)
#     parser.add_argument('--strides', help='the moving strides', default=256)

#     args = parser.parse_args()
#     return args

# def get_cmap():
#     labels = np.ndarray((n_labels, 3), dtype='uint8')
#     for i, (k, v) in enumerate(label_mapping.items()):
#         labels[i] = v
#     cmap = np.zeros([768], dtype='uint8')
#     index = 0
#     for i in range(0, n_labels):
#         for j in range(0, 3):
#             cmap[index] = labels[i][j]
#             index += 1
#     print('cmap define finished')
#     return cmap

# def pic_cutting(args, images):
#     """
#         切图代码
#     """
#     save_path = args.save_path
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     for ii, image in enumerate(images):
#         image_names = os.path.split(image)[1]
#         image_name, ext = os.path.splitext(image_names)
#         img = Image.open(image)
#         img = np.asarray(img)
#         img_shape = img.shape
#         h = img_shape[0]
#         w = img_shape[1]
#         stride = args.strides
#         height = args.size
#         width = args.size

#         # 计算切图的行数和列数
#         row = math.floor((h - height) / stride)
#         column = math.floor((w - width) / stride)

#         id_hang = 1
#         for i in tqdm(range(row), total=row):
#             row_start = i * stride
#             row_end = i * stride + height
#             id_lie = 1
#             for j in range(column):
#                 col_start = j * stride
#                 col_end = j * stride + width
#                 if args.channels == 3:
#                     small_pic = img[row_start:row_end, col_start:col_end, :]
#                 elif args.channels == 1:
#                     small_pic = img[row_start:row_end, col_start:col_end]
#                 small_name = 'image' + str(ii + 1).rjust(3, '0') + '_' + str(id_hang).rjust(3, '0') + 'row_' + str(id_lie).rjust(3, '0') + 'col' + ext
#                 small_pic = Image.fromarray(np.uint8(small_pic))
#                 if args.if_cmap:
#                     small_pic.putpalette(args.cmap)
#                 small_pic.save(os.path.join(save_path, small_name))
#                 id_lie += 1
#             id_hang += 1

# def main():
#     """
#         主函数
#     """
#     args = parse_args()
#     args.cmap = get_cmap()
#     images = glob.glob(os.path.join(args.path, '*{}'.format(args.ext)))
#     pic_cutting(args, images)
#     pass

# if __name__ == '__main__':
#     main()

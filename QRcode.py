from openpyxl import load_workbook
from PIL import Image
import qrcode, sys, os

class QRCode:
    def __init__(this,filename):
        wb = load_workbook(filename = filename)
        pass

    def make
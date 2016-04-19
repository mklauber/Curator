from __future__ import division

import wx

def scale_bitmap(bitmap, width, height, quality=wx.IMAGE_QUALITY_NORMAL):
    image = wx.ImageFromBitmap(bitmap)
    hRatio = height / image.Height
    wRatio = width / image.Width 
    ratio = min(hRatio, wRatio)
    image = image.Scale(image.Width * ratio, image.Height * ratio, quality)
    result = wx.BitmapFromImage(image)
    return result
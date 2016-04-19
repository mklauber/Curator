from __future__ import division

import wx

def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    hRatio = height / image.Height
    wRatio = width / image.Width 
    ratio = min(hRatio, wRatio)
    image = image.Scale(image.Width * ratio, image.Height * ratio, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result
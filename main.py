import qrcode 

website= "https://www.buzzfeed.com/in"

filename="site.png"

img=qrcode.make(website)
img.save(filename)


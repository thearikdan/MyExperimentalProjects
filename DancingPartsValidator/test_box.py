from components.primitives import box


b = box.Box()
print b.getName()
print b.getVolume()
print b.getSignature()


b = box.Box(1,2,3)
print b.getName()
print b.getVolume()
print b.getSignature()




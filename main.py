from ObfuscatedImage import ObfuscatedImage

img = ObfuscatedImage.fromImagePath("images/flower.jpg")
img.obfuscate()
key = ObfuscatedImage.keyFromPattern(img.pattern)
print(key)
#img.decode(ObfuscatedImage.patternFromKey(key))

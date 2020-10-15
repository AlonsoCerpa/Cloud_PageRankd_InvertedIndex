import os 

dir = "txts_prueba"
for filename in os.listdir(dir): 
    src = dir + "/" + filename
    dst = src.replace(" ", "")
        
    os.rename(src, dst) 

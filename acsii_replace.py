fw=open('bl\\synopsis_manager1.py',"w")
fr = open("bl\synopsis_manager.py","r")
fw.write(fr.read().replace('\xc2',"").replace("\xa0",""))

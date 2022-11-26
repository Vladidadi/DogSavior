import requests as reqs
from io import BytesIO as byte
from bs4 import BeautifulSoup as bs
from PIL import Image
import re
import http.server
import socketserver
import unicodedata
from time import sleep
import os
from tqdm import tqdm
import webbrowser
import subprocess
import json
class DOGSAVIOR():
    def __init__(self):
        super().__init__()
        self.count = 0
        self.briefcase = {}
        def writeout(self, props):
            f=open('output.html','w')
            f.write(props)
            f.close()

    def fetchmany(self, url):
        rec = reqs.get(url)

    def fetchone(self, url):
        rec = reqs.get(url)
        return rec
    def parseimg(self, props):
        soup = byte(props.content)
        i = Image.open(soup)
        i.show()
        return i

    def saveimg(self, img,imgname,id):
        img.save(f'{id}.jpeg','jpeg')

    def savetext(self, text,textname,id):
        outfile = open(f'{id}.txt','w')
        outfile.write(str(text))
        outfile.close()
        
    

    def parsetext(self, props):
        soup = bs(props.content,'html.parser')
        text = soup.select_one('td.DetailDesc')
        return text

    def parsedogid(self,props):
    # m = re.search(r'\b#\.\.\.\.\.\.\.\.',props)
    #print(props)
        dogid = re.search(r'(?<=#)\w+',str(props))

        return dogid.group(0)

    def newgetimg(self,dogid):
        img = reqs.get(f'https://petharbor.com/get_image.asp?RES=Detail&ID={dogid}&LOCATION=PKPK')
        i = Image.open(byte(img.content))
        return i    

    def dothething(self, props, searchurl):
        
        # props2 = props[0]
        # print(f'props is {props}\n\n\nprops2 is {props2}\n\n\nthe first element of props2 is {props2[0]}')
        # print(props,type(props[0]))
        for thing in props:
           
            
            print(f'querrying {self.count}th dog')
            if os.path.isfile(f'{thing}.txt') == 0:
                try:
                    print('searching the url:', f'{searchurl}{thing}')
                    fullhtmlpage = self.fetchone(f'{searchurl}{thing}')
                    print('got full html')



                    text = self.parsetext(fullhtmlpage)
                    print('got the discription')
                    dogid = self.parsedogid(text)
                    print('got the dog id, it is :',dogid)
                    pic = self.newgetimg(dogid)
                    print('got the dog pic')
                    self.savetext(text,self.count,dogid)
                    self.saveimg(pic,self.count,dogid)
                    print('dog saved to disk')
                    self.briefcase[f'img + {dogid}'] = pic
                    self.briefcase[f'text + {dogid}'] = text
                    print('dog saved to briefcase')
                    self.count += 1
                    print(f'dog {self.count} complete')
                except:
                    print(f'dog get failed on dog number {self.count}')
                finally:
                    print('finished gathering dogs')
            else: print('dog already exists on disk')
            self.count+=1


    def scanall(self, url):
    #exclude = ('Spayed'  'Neutered')
    #we need to put the url of the search querry in the doglist,
    #we should also make a doglist.old file is a valid file exists
        if (os.path.isfile('doglist.json')):
            print('found the dog list')
            oldlist = open('doglist.json','r')
            oldlistlocal = oldlist.read()
            oldlist.close()
            jsonifieddoglist = json.loads(oldlistlocal)
            print(type(jsonifieddoglist),jsonifieddoglist,'jsonifieddoglist^^^')
            return jsonifieddoglist
        print('no dog list found\nscanning all nearby dogs')
        basehtml = self.fetchone(url)
        print(basehtml.headers,'\n\n')
        soup = bs(basehtml.content,'html.parser')
        ids=[]
        temp = soup.select('div.gridText')
        #print(temp)
        find =  re.findall(r'(?<=\()\w+',str(temp))
        print(find)
        print(type(find))
        filtered = [i for i in find if i != 'Spayed' and i != 'Neutered']
        print(filtered)

        with open('doglist.json','w',encoding='utf-8') as doglist:
            json.dump(filtered, doglist, ensure_ascii=False, indent=4)
    
        return filtered




    def constructhtmlpage(self,doglist,imglink):
        count = 0
        numberofdogs=47
        #get this thru lsdir
        for i in tqdm(range(100)):    

            webserver = open('index.html','w')
            webserver.write('<!DOCTYPE html><head>dogs</head><body>')
            for dog in doglist:
                if os.path.isfile(f'{dog}.txt'):
                    infile= open(f'{dog}.txt','r')
                    
              
                    webserver.write(f'<a href={imglink}{dog}><img src= {dog}.jpeg></a>')

                    text = infile.readlines()
                    for word in text:
                        unicodedata.normalize('NFC' ,word)
                    for line in text:
                        
                        print(line)
                        webserver.write(str(line))
                    infile.close()
              
                count += 1
            webserver.write('</body>')
            webserver.close()


    def startserver(self):
        port = 9476
        Handler = http.server.SimpleHTTPRequestHandler
        htp = socketserver.TCPServer(("",port),Handler)
        print(f'serving on port {port}')
       # subprocess.Popen(['python','-m','SimpleHTTPServer','9476'])
        webbrowser.open('http://127.0.0.1:9476', new=2) 
        htp.serve_forever()    

    def userinput(self):
        inpt = input('would you like to querry a new website url?(Y/n)')
        if inpt != 'n' and inpt != 'N':
            newfetchallurl = input('paste the url from a search results page')
            return newfetchallurl
        return 0

    # def checkifdogsexist(self,doglist):
    #     for dog in doglist:
    #         if os.path.isfile(f'{dog}.txt'):
    #             return 0
def main():
    for i in tqdm(range(1,1000)):
          singleurl='https://petharbor.com/pet.asp?uaid=PKPK.'
          listallurl='https://petharbor.com/results.asp?searchtype=LOST&start=4&grid=1&friends=1&samaritans=1&nosuccess=0&orderby=Brought%20to%20the%20Shelter&rows=960&imght=120&imgres=Detail&tWidth=200&view=sysadm.v_pkpk_stray&nobreedreq=1&nocustom=1&bgcolor=ffffff&text=000000&link=d8723c&alink=d8723c&vlink=d8723c&fontface=Noto%20Sans,%20Open%20Sans,%20Helvetica%20Neue,%20Helvetica,Arial,%20sans-serif&fontsize=10&miles=20&shelterlist=%27pkpk%27&atype=&where=type_DOG&PAGE=1'
          imgurl1='https://petharbor.com/get_image.asp?RES=Detail&ID='
          imgurl2='&LOCATION=PKPK'
          dogsaver1 = DOGSAVIOR()
          #dogsaver1.dothething('https://petharbor.com/pet.asp?uaid=PKPK.A1615612')
          #  print(dogsaver1.count)
          # print(dogsaver1.briefcase)
          userurl = dogsaver1.userinput()
          if userurl:
            idlist = dogsaver1.scanall(userurl)
            print('using user defined url search')
          else :
            idlist = dogsaver1.scanall('https://petharbor.com/results.asp?searchtype=LOST&start=4&grid=1&friends=1&samaritans=1&nosuccess=0&orderby=Brought%20to%20the%20Shelter&rows=960&imght=120&imgres=Detail&tWidth=200&view=sysadm.v_pkpk_stray&nobreedreq=1&nocustom=1&bgcolor=ffffff&text=000000&link=d8723c&alink=d8723c&vlink=d8723c&fontface=Noto%20Sans,%20Open%20Sans,%20Helvetica%20Neue,%20Helvetica,Arial,%20sans-serif&fontsize=10&miles=20&shelterlist=%27pkpk%27&atype=&where=type_DOG&PAGE=1')
            print('using default url search')
          dogsaver1.dothething(idlist,singleurl)
          dogsaver1.constructhtmlpage(idlist,singleurl)
          dogsaver1.startserver()
          
if __name__ == '__main__':
    main()


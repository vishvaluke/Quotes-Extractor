import requests,bs4,re,webbrowser,time,pyperclip,os,sys
import numpy as np
import cv2,textwrap,os,shutil
def link():
    book=input('Enter Book Name: ')
    print("Book Title: ",book.title())
    print("Searching Book Link:")
    books="+".join(book.split(" "))
    ftitle="_".join(book.split(' '))
    ftitle=ftitle.title()
    ftitle=ftitle+'.txt'
    link='http://www.google.com/search?q=site%3Agoodreads.com+{0}+quotes&rlz=1C1CHBF_enIN848US848&oq=si&aqs=chrome.0.69i59l3j69i60l3.1691j0j7&sourceid=chrome&ie=UTF-8'.format(books)
    rem=requests.get(link)
    rem.raise_for_status()
    soup=bs4.BeautifulSoup(rem.text,'html.parser')
    href=soup.find_all(href=True)
    com=re.compile(r'https://www.goodreads.com/work/quotes/.*')
    found=com.findall(str(href))
    try:
        x=found[0]
        final=x.split('&')
        final=final[0]
        webbrowser.open(final)
        print("Search Done, Book Link Found!!")
        scrape(final,ftitle)
    except:
        print("Search Failed, Can't Find  Book Link")
        print("Sorry!!")
        return 0

def scrape(seed,ftitle):
    text=seed
    #title=ftitle
    lion=[]
    nopage=int(input('Number of Pages to Scrape: '))
    print("Scraping Quotes Link:")
    for j in range(nopage):
        print("(",j+1," / ",nopage,")")
        req=requests.get('{0}?page={1}'.format(text,str(j)))
        #webbrowser.open('{0}?page={1}'.format(text,str(j)))
        xi=bs4.BeautifulSoup(req.text,'html.parser')
        y=xi.select('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.leftContainer')
        xi=re.compile(r' “.*”\n    ―')
        di=xi.findall(y[0].text)
        for i in range(len(di)):
            di[i]=di[i].replace('    ―','')
            #print(di[i])
            #time.sleep(0.3)
        print("Found Quotes: ",len(di))
        lion.extend(di)
    unique(lion,ftitle)
def unique(lion,ftitle): 
    unique=[]
    os.chdir(r'C:\Users\VISHVA\Desktop\Projects\Quotes\found')
    jtitle=ftitle.replace('.txt','')
    try:
        os.mkdir(jtitle)
    except:
        pass
    os.chdir(r'C:\Users\VISHVA\Desktop\Projects\Quotes\found\{}'.format(jtitle))
    f1=open(ftitle,'w',encoding='utf-8')
    for i in lion:
        if i not in unique: 
            unique.append(i)
            f1.write(i)
    f1.close()
    print("Found:",len(unique),"quotes")
    webbrowser.open(ftitle)
    pic(ftitle)
def pic(ftitle):
    jtitle=ftitle.replace('.txt','')
    f1=open(ftitle,'r',encoding='utf-8')
    j=10
    for x in f1:
        if(len(x)<=80):
            print(x)
            x=x.replace('“','"')
            x=x.replace('”','"')
            x=x.replace("’","'")
            x=x[:1]+x[1].upper()+x[2:]  
            os.chdir(r'C:\Users\VISHVA\Desktop\Projects\Quotes\found')
            img = cv2.imread('1.jpg')
            #print(img.shape)
            height, width, channel = img.shape
            text_img = np.ones((height, width))
            #print(text_img.shape)
            font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
            text = x
            wrapped_text = textwrap.wrap(text, width=35)
            x, y = 10, 40
            font_size = 1.5
            font_thickness = 2
            i = 0
            
            for line in wrapped_text:
                textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
                gap = textsize[1] + 10
                y = int((img.shape[0] + textsize[1]) / 2) + i * gap
                x = int((img.shape[1] - textsize[0]) / 2)
                cv2.putText(img, line, (x, y), font,
                            font_size, 
                            (255,255,255), 
                            font_thickness, 
                            lineType = cv2.LINE_AA)
                i +=1
            st=str(j)+'.jpg'
            os.chdir(r'C:\Users\VISHVA\Desktop\Projects\Quotes\found\{}'.format(jtitle))
            #cv2.imshow("Result Image", img)
            
            cv2.imwrite(st, img)
            #webbrowser.open(st)
            time.sleep(1)
            j+=1 
            cv2.waitKey(0)
            cv2.destroyAllWindows()
link()
input('Press ENTER to exit')

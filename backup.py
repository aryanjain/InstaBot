from selenium import webdriver
from time import sleep
import math
import random
import threading
from sqlConn import create_connection,create,create_table,insertData
import sqlConn
from utilities import createList,CreateDbFileStr
import sys
from enums import URL,EMAIL,PASSWORD,LIKE_PERCENTAGE_MAX,LIKE_COUNT,FOLLOW_PERCENTAGE_MAX,FOLLOW_COUNT,COMMENT_COUNT,AVG_SLEEP,SMALL_SLEEP
from enums import commonDiv,commonDiv2,verifiedBadge1,verifiedBadge2,verifiedBadge3
from enums import SCROLL,MIN_LIKES_IN_POST
from hashtags import countEachHashtag
from utilities import pickCommentFromList


class TinderBot():
    def __init__(self):
        self.driver=webdriver.Firefox()
        self.driver.get(URL)
        
        
        self.randomList,self.randomListSmallNumber= createList()
        self.follow_count=0
        self.like_count=0
        self.comment_count=0
        filename=CreateDbFileStr()
        print(filename)
        fileDir="E:\webscrapper\\tinderbot\src\db\{}".format(filename)
        print(fileDir)
        conn=create_connection(fileDir)
        if conn is not None:
            
            create(conn)
            print("table created")     
            sleep(3)         
            self.conn=conn  



    def signIn(self):
        try:
            emailId=self.driver.find_element_by_xpath('{}div[2]/div/label/input'.format(commonDiv))
            emailId.send_keys(EMAIL)
            password=self.driver.find_element_by_xpath('{}div[3]/div/label/input'.format(commonDiv))
            password.send_keys(PASSWORD)

            login_btn=self.driver.find_element_by_xpath('{}div[4]/button'.format(commonDiv))

            login_btn.click()
            
            sleep(AVG_SLEEP)
        
        except Exception as e :
            print("email or pass div not loaded")
            print(e)
            signIn()
        try:
            save_passBtn=self.driver.find_element_by_xpath('{}div/div/div/button'.format(commonDiv2))
            save_passBtn.click()
        except Exception as e :
            print("save pass btn not there")
            print(e)
        
        

    def random_number(self):
        num2=random.choice(self.randomList)
        print("random no is {} for sleep".format(num2))
        return num2

    def small_random_number(self):
        num2=random.choice(self.randomListSmallNumber)
        print("random no is {} for sleep".format(num2))
        return num2


    def discover_posts(self):
        try: 
            explore_btn=self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[3]/a')
            explore_btn.click()

        #pics=self.driver.find_element_by_xpath('//*[@id="react-root"]')
        
            #sleep(self.random_number())
            sleep(AVG_SLEEP)
            pics=self.driver.find_element_by_xpath('{}div[2]'.format(commonDiv2))
            #scrolling
            links=self.scrollList(pics)
            while math.floor(random.random()*10) > SCROLL : #continue scrolling  
                print("More scroll") 
                links=self.scrollList(pics)
            print("len of list of links: {}".format(len(links)))
            print(links)

            num_pics=math.floor(random.random()*len(links))
            print(num_pics)
            pics_href=links[num_pics].get_attribute('href')
            print(pics_href)
            print(type(pics_href))
            sleep(SMALL_SLEEP)

            #go to the post:
            self.driver.get(pics_href)
            sleep(self.random_number())

            # to inseert in Db
            flag=0 

            like_percentage=math.floor(random.random()*10)
            follow_percentage=math.floor(random.random()*10)
            print("like perc is {} and follow perc is {} for post".format(like_percentage,follow_percentage))
            
            #count Hashtags
            #hashTagCount=countEachHashtag(self.driver)

            #check for verified profile
            verified=self.isVerifiedPost()
            print(verified)
            if verified :
                flag=1
                self.like()
                self.like_count=self.like_count+1
                self.follow_from_post()
                self.follow_count=self.follow_count+1
                if self.comment_count <= COMMENT_COUNT:
                    self.comment_on_post()
                    self.comment_count=self.comment_count+1
                
            else:
                likeCountSpan=self.driver.find_element_by_css_selector('button._8A5w5 > span:nth-child(1)').text
                print("likeCount={}".format(likeCountSpan))
                
                if like_percentage >= LIKE_PERCENTAGE_MAX and self.like_count <=LIKE_COUNT :
                    self.like()
                    self.like_count=self.like_count+1
                    flag=1
                if follow_percentage >=FOLLOW_PERCENTAGE_MAX and self.follow_count <=FOLLOW_COUNT:
                    self.follow_from_post()
                    self.follow_count=self.follow_count+1
                    """
                    if flag == 1 :
                        if self.comment_count<= COMMENT_COUNT:
                            self.comment_on_post()
                            self.comment_count=self.comment_count+1
                    """
                    flag=1
                    followFlag=1  
                print("like count is {} and follow count is {} for post".format(self.like_count,self.follow_count))
                if flag ==1 or followFlag ==1:
                    if self.comment_count<= COMMENT_COUNT:
                        self.comment_on_post()
                        self.comment_count=self.comment_count+1

            if flag == 1:
                with self.conn:
                    print("inserting in db")
                    task1=(self.like_count,self.follow_count,pics_href)
                    insertDb=insertData(self.conn,task1)
                    print(insertDb)
            sleep(AVG_SLEEP)
            
        except Exception as e:
            print("Out of range::discover_posts")
            print(e)
            self.rollback()
    
        #return -1

    def scrollList(self,pics):
        links=pics.find_elements_by_tag_name('a')
        
        if math.floor(random.random()*10) > 2 :
            print("scrolling") 
            for list in links :
                self.driver.execute_script("arguments[0].scrollIntoView();", list )
                sleep(SMALL_SLEEP)
                links=pics.find_elements_by_tag_name('a')
        print("scroll ends")
        return links

    def rollback(self):
        print("in rollback")
        try:
            close_btn=self.driver.find_element_by_xpath('/html/body/div[1]/section/div/div/section/div[2]/button[3]/div')
            close_btn.click()
            self.discover_posts()
        except Exception as e:
            print(e)
            
            self.close_pic()
            self.discover_posts()

    def isVerifiedPost(self):
        isVerified=False
        try:
            verifiedPost=self.driver.find_element_by_xpath(verifiedBadge2)
            isVerified=True
        except Exception as e:
            print(e)
            try:
                
                verifiedPost=self.driver.find_element_by_xpath(verifiedBadge1)
                isVerified=True
            except Exception as e:
                print(e)
                isVerified=False
                try:
                    verifiedPost=self.driver.find_element_by_xpath(verifiedBadge3)
                    isVerified=True
                except Exception as e:
                    print(e)
                    isVerified=False



        return isVerified

    def like(self):               
             
            like_btn=self.driver.find_element_by_xpath('{}div[1]/article/div[2]/section[1]/span[1]/button'.format(commonDiv2))
            print("before like")
            sleep(self.small_random_number())
            like_btn.click()
            print("after like")
            sleep(self.small_random_number())
            #self.discover_posts()
        

    def close_pic(self):
        print("In close pic")
        sleep(SMALL_SLEEP)
        close_btn=self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button').click()

    def follow_from_profile_page(self):
        follow_btn=self.driver.find_element_by_xpath('{}header/section/div[1]/div[1]/span/span[1]/button'.format(commonDiv2))
        sleep(SMALL_SLEEP)
        follow_btn.click()
    
    
    def follow_from_post(self):
        follow_btn=self.driver.find_element_by_xpath('{}div[1]/article/header/div[2]/div[1]/div[2]/button'.format(commonDiv2))
        print("before follow")
        sleep(self.small_random_number())
        follow_btn.click()
        print("after follow")
        sleep(self.small_random_number())
        #self.discover_posts()
    
    def comment_on_post(self):
        cBtn=self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[1]/span[2]/button')
        cBtn.click()
        textArea=self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[3]/div/form/textarea')
        comment=pickCommentFromList()
        print('comment:: {}'.format(comment))
        textArea.send_keys(comment)
        sleep(SMALL_SLEEP)
        commentBtn=self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[3]/div/form/button')
        
        commentBtn.click()
        sleep(SMALL_SLEEP)

    
    
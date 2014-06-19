# 記憶方塊
# 程式出自 Al Sweigart al@inventwithpython.com
# 來源http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
# 翻譯:陳俞臻

import random, pygame, sys, time, sys, copy
from pygame.locals import *


畫面更新率 = 30 #FPS
視窗寬 = 640 #WINDOWWIDTH 視窗寬/像素
視窗高 = 480 # WINDOWHEIGHT 視窗高/像素
動畫速度= 500 # in milliseconds
動畫延遲 = 200 # in milliseconds
按鈕大小 = 200
按鈕中間大小 = 20
時間結束 = 4 # 如果沒按按鈕的死前秒數

#                R    G    B
白        = (255, 255, 255)
黑        = (  0,   0,   0)
亮紅   = (255,   0,   0)
紅         = (155,   0,   0)
亮綠  = (  0, 255,   0)
綠        = (  0, 155,   0)
亮藍   = (  0,   0, 255)
藍         = (  0,   0, 155)
亮黃 = (255, 255,   0)
黃       = (155, 155,   0)
深灰     = ( 40,  40,  40)
背景顏色 = 黑

X邊 = int((視窗寬 - (2 * 按鈕大小) - 按鈕中間大小) / 2)
Y邊 = int((視窗高 - (2 * 按鈕大小) - 按鈕中間大小) / 2)

範圍= range 
設框大小=pygame.Rect
啟動= pygame.init
鐘類= pygame.time.Clock
設定面板大小= pygame.display.set_mode
設定面板標題= pygame.display.set_caption
字型類型=   pygame.font.Font
音樂取得=pygame.mixer.Sound
事件取得= pygame.event.get
遊戲面板更新=pygame.display.update
遊戲等待時間=pygame.time.wait
隨機選擇=random.choice
時間函式=time.time
離開遊戲=pygame.quit
系統結束=sys.exit
事件張貼= pygame.event.post
遊戲表面=pygame.Surface
塗框框顏色=pygame.draw.rect
隨機=random.randint



# 黃藍綠紅,四個方塊大小
黃方塊 = 設框大小(X邊, Y邊, 按鈕大小, 按鈕大小)
藍方塊   = 設框大小(X邊 + 按鈕大小 + 按鈕中間大小, Y邊, 按鈕大小, 按鈕大小)
紅方塊    = 設框大小(X邊, Y邊 + 按鈕大小 + 按鈕中間大小, 按鈕大小, 按鈕大小)
綠方塊  = 設框大小(X邊 + 按鈕大小 + 按鈕中間大小, Y邊 + 按鈕大小 + 按鈕中間大小, 按鈕大小, 按鈕大小)

def 主程式():
    global 畫面更新率時鐘, 面板搜尋, 基本字, 音樂1, 音樂2, 音樂3, 音樂4

    啟動()
    畫面更新率時鐘 = 鐘類()
    面板搜尋 = 設定面板大小((視窗寬, 視窗高))
    設定面板標題('記憶方塊')

    基本字 = 字型類型('freesansbold.ttf', 16)
    訊息搜尋 = 基本字.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, 深灰)
    訊息大小 = 訊息搜尋.get_rect()
    訊息大小.topleft = (10, 視窗高 - 25)

    # 載入音樂
    音樂1 = 音樂取得('beep1.ogg')
    音樂2 = 音樂取得('beep2.ogg')
    音樂3 = 音樂取得('beep3.ogg')
    音樂4 = 音樂取得('beep4.ogg')

    #初始化一些變數為一個新遊戲
    圖樣 = [] # 存儲顏色的圖案
    正確的下一步 = 0 # 玩家必須推動下一個的顏色
    最後一次按的時間 = 0 # 玩家的最後一個按按鈕的時間
    分數 = 0
    # 當False時，該模式播放。當True時，等待玩家點擊一個彩色按鈕：
    等待輸入 = False

    while True: # 主要程式迴圈
        被按的按鈕 = None # 被按的按鈕 (設置為 黃, 紅, 綠, 或 藍)
        面板搜尋.fill(背景顏色)
        按鈕塗色()

        分數搜尋 = 基本字.render('Score: ' + str(分數), 1, 白)
        分數框 = 分數搜尋.get_rect()
        分數框.topleft = (視窗寬 - 100, 10)
        面板搜尋.blit(分數搜尋, 分數框)

        面板搜尋.blit(訊息搜尋, 訊息大小)

        確認跳出()
        for 事件 in 事件取得(): # 事件處理迴圈
            if 事件.type == MOUSEBUTTONUP:
                滑鼠x, 滑鼠y = 事件.pos
                被按的按鈕 = 取得按鈕按下去(滑鼠x, 滑鼠y)
            elif 事件.type == KEYDOWN:
                if 事件.key == K_q:
                    被按的按鈕 = 黃
                elif 事件.key == K_w:
                    被按的按鈕 = 藍
                elif 事件.key == K_a:
                    被按的按鈕 = 紅
                elif 事件.key == K_s:
                    被按的按鈕 = 綠



        if not 等待輸入:
            # play the 圖樣
            遊戲面板更新()
            遊戲等待時間(1000)
            圖樣.append(隨機選擇((黃, 藍, 紅, 綠)))
            for 按鈕 in 圖樣:
                按鈕動畫(按鈕)
                遊戲等待時間(動畫延遲)
            等待輸入 = True
        else:
            # 等待玩家按按鈕
            if 被按的按鈕 and 被按的按鈕 == 圖樣[正確的下一步]:
                # 按正確的按鈕
                按鈕動畫(被按的按鈕)
                正確的下一步 += 1
                最後一次按的時間 = 時間函式()

                if 正確的下一步 == len(圖樣):
                    # 按最後一個圖樣
                    改變背景動畫()
                    分數 += 1
                    等待輸入 = False
                    正確的下一步 = 0 # 重置回第一步

            elif (被按的按鈕 and 被按的按鈕 != 圖樣[正確的下一步]) or (正確的下一步 != 0 and 時間函式() - 時間結束 > 最後一次按的時間):
                # 按到錯誤的按鈕或是沒時間了
                死亡動畫()
                # 重置新遊戲的變數
                圖樣 = []
                正確的下一步 = 0
                等待輸入 = False
                分數 = 0
                遊戲等待時間(1000)
                改變背景動畫()

        遊戲面板更新()
        畫面更新率時鐘.tick(畫面更新率)


def 終止():
    離開遊戲()
    系統結束()


def 確認跳出():
    for 事件 in 事件取得(QUIT): # 取得所有結束事件
        終止() # 如果全部事件符合則終止
    for 事件 in 事件取得(KEYUP): # 取得所有滑鼠按建的事件
        if 事件.key == K_ESCAPE:
            終止() #如果滑鼠事件是離開則終止
        事件張貼(事件) # 把其他滑鼠離開事件的對象返回


def 按鈕動畫(顏色, 動畫速度=50):
    if 顏色 == 黃:
        音樂 = 音樂1
        動畫的顏色 = 亮黃
        長方形 = 黃方塊
    elif 顏色 == 藍:
        音樂 = 音樂2
        動畫的顏色 = 亮藍
        長方形 = 藍方塊
    elif 顏色 == 紅:
        音樂 = 音樂3
        動畫的顏色 = 亮紅
        長方形 = 紅方塊
    elif 顏色 == 綠:
        音樂 = 音樂4
        動畫的顏色 = 亮綠
        長方形 = 綠方塊

    原始搜尋 = 面板搜尋.copy()
    動畫的搜尋 = 遊戲表面((按鈕大小, 按鈕大小))
    動畫的搜尋 = 動畫的搜尋.convert_alpha()
    r, g, b = 動畫的顏色
    音樂.play()
    for 開始, 結束, 步 in ((0, 255, 1), (255, 0, -1)): # 動畫迴圈
        for 阿爾法 in 範圍(開始, 結束, 動畫速度 * 步):
            確認跳出()
            面板搜尋.blit(原始搜尋, (0, 0))
            動畫的搜尋.fill((r, g, b, 阿爾法))
            面板搜尋.blit(動畫的搜尋, 長方形.topleft)
            遊戲面板更新()
            畫面更新率時鐘.tick(畫面更新率)
    面板搜尋.blit(原始搜尋, (0, 0))


def 按鈕塗色():
    塗框框顏色(面板搜尋, 黃, 黃方塊)
    塗框框顏色(面板搜尋, 藍,   藍方塊)
    塗框框顏色(面板搜尋, 紅,    紅方塊)
    塗框框顏色(面板搜尋, 綠,  綠方塊)


def 改變背景動畫(動畫速度=40):
    global 背景顏色
    新的背景色 = (隨機(0, 255), 隨機(0, 255), 隨機(0, 255))

    新背景的搜尋 = 遊戲表面((視窗寬, 視窗高))
    新背景的搜尋 = 新背景的搜尋.convert_alpha()
    r, g, b = 新的背景色
    for 阿爾法 in 範圍(0, 255, 動畫速度): # 動畫迴圈
        確認跳出()
        面板搜尋.fill(背景顏色)

        新背景的搜尋.fill((r, g, b, 阿爾法))
        面板搜尋.blit(新背景的搜尋, (0, 0))

        按鈕塗色() # 重新著按鈕顏色

        遊戲面板更新()
        畫面更新率時鐘.tick(畫面更新率)
    背景顏色 = 新的背景色


def 死亡動畫(顏色=白, 動畫速度=50):
    # 一次同時撥放所有音樂,然後閃爍螢幕
    原始搜尋 = 面板搜尋.copy()
    動畫的搜尋 = 遊戲表面(面板搜尋.get_size())
    動畫的搜尋 = 動畫的搜尋.convert_alpha()
    音樂1.play() #大致的一次撥放所有音樂.
    音樂2.play()
    音樂3.play()
    音樂4.play()
    r, g, b = 顏色
    for i in 範圍(3): # 做動畫3次
        for 開始, 結束, 步 in ((0, 255, 1), (255, 0, -1)):
            # 在這個循環的第一次迭代設置以下的for迴圈
            # 從0到255，第二個從255到0。
            for 阿爾法 in 範圍(開始, 結束, 動畫速度 * 步): # 動畫迴圈
                # 阿爾法意味著透明度. 255 是不透明, 0 是透明
                確認跳出()
                動畫的搜尋.fill((r, g, b, 阿爾法))
                面板搜尋.blit(原始搜尋, (0, 0))
                面板搜尋.blit(動畫的搜尋, (0, 0))
                按鈕塗色()
                遊戲面板更新()
                畫面更新率時鐘.tick(畫面更新率)



def 取得按鈕按下去(x, y):
    if 黃方塊.collidepoint( (x, y) ):
        return 黃
    elif 藍方塊.collidepoint( (x, y) ):
        return 藍
    elif 紅方塊.collidepoint( (x, y) ):
        return 紅
    elif 綠方塊.collidepoint( (x, y) ):
        return 綠
    return None


if __name__ == '__main__':
    主程式()

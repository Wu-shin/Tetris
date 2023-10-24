import tkinter
import random

index = 0 #管理遊戲流程
timer = 0 #管理時間
score = 0 #管理分數
tsugi = 0 #設定下個貓咪
hisc = 1000 #處存最高分數
difficulty = 0 #難易度
cursor_x, cursor_y = 0, 0 #滑鼠游標水平、垂直位置
mouse_x, mouse_y, mouse_c = 0, 0, 0 #滑鼠游標X、Y座標

def mouse_move(e): #滑鼠移動
    global mouse_x, mouse_y
    mouse_x, mouse_y = e.x, e.y

def mouse_press(e): #滑鼠點擊
    global mouse_c
    mouse_c = 1

#格子的二維陣列
neko = []
check = []
for i in range(10):
    neko.append([0, 0, 0, 0, 0, 0, 0, 0])
    check.append([0, 0, 0, 0, 0, 0, 0, 0])

def draw_neko(): #顯示貓咪
    cvs.delete("NEKO")
    for y in range(10):
        for x in range(8):
            if neko[y][x] > 0:
                cvs.create_image(x*72+60, y*72+60, image=img_neko[neko[y][x]], tag="NEKO")

def check_neko(): #判斷貓咪是否連線
    #將貓咪的值放入判斷列表
    for y in range(10): 
        for x in range(8):
            check[y][x] = neko[y][x]
    #判斷垂直連線
    for y in range(1,9):
        for x in range(8):
            if check[y][x] > 0:
                if check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:
                    neko[y-1][x], neko[y][x], neko[y+1][x] = 7, 7, 7
    #判斷水平連線
    for y in range(10):
        for x in range(1,7):
            if check[y][x] > 0:
                if check[y][x-1] == check[y][x] and check[y][x+1] == check[y][x]:
                    neko[y][x-1], neko[y][x], neko[y][x+1] = 7, 7, 7
    #判斷交叉連線
    for y in range(1,9):
        for x in range(1,7):
            if check[y][x] > 0:
                if check[y-1][x-1] == check[y][x] and check[y+1][x+1] == check[y][x]:
                    neko[y-1][x-1], neko[y][x], neko[y+1][x+1] = 7, 7, 7
                if check[y+1][x-1] == check[y][x] and check[y-1][x+1] == check[y][x]:
                    neko[y+1][x-1], neko[y][x], neko[y-1][x+1] = 7, 7, 7

def sweep_neko(): #計算消除的數量
    num = 0
    for y in range(10):
        for x in range(8):
            if neko[y][x] == 7:
                neko[y][x] = 0
                num += 1
    return num

def drop_neko(): #讓貓咪落下
    flg = False #判斷是否落下(False代表未落下)
    for y in range(8, -1, -1):
        for x in range(8):
            if neko[y][x] != 0 and neko[y+1][x] == 0:
                neko[y+1][x] = neko[y][x]
                neko[y][x] = 0
                flg = True
    return flg

def over_neko(): #判斷是否以堆疊到最上面
    for x in range(8):
        if neko[0][x] > 0:
            return True
    return False

def set_neko(): #在最上層設定貓咪
    for x in range(8):
        neko[0][x] = random.randint(0, difficulty) #依照難易度隨機設置貓咪

def draw_txt(txt, x, y, siz, col, tg): #顯示帶有陰影效果的字串
    fnt = ("Times New Roman", siz, "bold")
    cvs.create_text(x+2, y+2, text=txt, fill="black", font=fnt, tag=tg)
    cvs.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)

def game_main():
    global index, timer, score, tsugi, hisc, difficulty
    global cursor_x, cursor_y, mouse_c
    if index == 0: #標題的標誌
        draw_txt("貓咪貓咪", 312, 240, 100, "violet", "TITLE")
        #Easy
        cvs.create_rectangle(168, 384, 456, 456, fill="skyblue", width=0, tags="TITLE")
        draw_txt("Easy", 312, 420, 40, "white", "TITLE")
        #Normal
        cvs.create_rectangle(168, 528, 456, 600, fill="lightgreen", width=0, tags="TITLE")
        draw_txt("Normal", 312, 564, 40, "white", "TITLE")
        #Hard
        cvs.create_rectangle(168, 672, 456, 744, fill="orange", width=0, tags="TITLE")
        draw_txt("Hard", 312, 708, 40, "white", "TITLE")
        index = 1
        mouse_c = 0
    elif index == 1: #標題畫面 等待遊戲開始
        difficulty = 0
        if mouse_c == 1: #按下滑鼠按鍵開始
            if 168 < mouse_x and mouse_x < 456 and 384<= mouse_y and mouse_y < 456: #Easy
                difficulty = 4 
            if 168 < mouse_x and mouse_x < 456 and 528<= mouse_y and mouse_y < 600: #Normal
                difficulty = 5 
            if 168 < mouse_x and mouse_x < 456 and 672<= mouse_y and mouse_y < 744: #Hard
                difficulty = 6 
            for y in range(10):
                for x in range(8):
                    neko[y][x] = 0
            mouse_c, score, tsugi, cursor_x, cursor_y = 0, 0, 0, 0, 0 #將所有值歸零
            set_neko()  #在最上層設定貓咪
            draw_neko() #顯示貓咪
            cvs.delete("TITLE") 
            index = 2
    elif index == 2: #讓貓咪下落
        if drop_neko() == False: 
            index = 3
        draw_neko()
    elif index == 3: #是否連成一線
        check_neko()
        draw_neko()
        index = 4
    elif index == 4: #消除連成一線的貓咪
        #消除肉球，並計算分數
        sc = sweep_neko() 
        score = score + sc*difficulty*2
        if score > hisc:
            hisc = score
        if sc > 0: #假設消除了肉球
            index = 2 #讓貓咪再次落下
        else:
            if over_neko() == False: #還沒到最上層
                tsugi = random.randint(1, difficulty)
                index = 5
            else: #到最上層
                index = 6
                timer = 0
        draw_neko()
    elif index == 5: #等待玩家滑鼠輸入
        if 24 <= mouse_x and mouse_x < 24+72*8 and 24 <= mouse_y and mouse_y < 24+72*10:
            cursor_x = int((mouse_x-24)/72)
            cursor_y = int((mouse_y-24)/72)
            if mouse_c == 1:
                mouse_c = 0
                set_neko()
                neko[cursor_y][cursor_x] = tsugi #在滑鼠位置隨機配置貓咪
                tsugi = 0
                index = 2
        cvs.delete("CURSOR")
        cvs.create_image(cursor_x*72+60, cursor_y*72+60, image=cursor, tag="CURSOR")
        draw_neko()
    elif index == 6: #遊戲結束
        timer += 1
        if timer == 1:
            draw_txt("GAME OVER", 312, 348, 60, "red", "OVER")
        if timer == 50:
            cvs.delete("OVER")
            index = 0
    cvs.delete("INFO")
    draw_txt("SCORE " + str(score), 160, 60, 32, "blue", "INFO")
    draw_txt("HISC " + str(hisc), 450, 60, 32, "yellow", "INFO")
    if tsugi > 0:
        cvs.create_image(752, 128, image=img_neko[tsugi], tag="INFO")
    root.after(100,game_main)


root = tkinter.Tk()
root.title("掉落物拼圖「貓咪貓咪」")
root.resizable(False, False) #禁止更改視窗大小
root.bind("<Motion>", mouse_move) #滑鼠移動
root.bind("<ButtonPress>", mouse_press) #滑鼠點擊
cvs = tkinter.Canvas(root, width=912, height=768)#建立畫布
cvs.pack()

bg = tkinter.PhotoImage(file=r".\neko_bg.png") #背景
cursor = tkinter.PhotoImage(file=r".\neko_cursor.png") #滑鼠游標圖片
#貓咪圖片
img_neko = [
    None,
    tkinter.PhotoImage(file=r".\neko1.png"),
    tkinter.PhotoImage(file=r".\neko2.png"),
    tkinter.PhotoImage(file=r".\neko3.png"),
    tkinter.PhotoImage(file=r".\neko4.png"),
    tkinter.PhotoImage(file=r".\neko5.png"),
    tkinter.PhotoImage(file=r".\neko6.png"),
    tkinter.PhotoImage(file=r".\neko_niku.png"),
]

cvs.create_image(456, 384, image=bg)
game_main()
root.mainloop()

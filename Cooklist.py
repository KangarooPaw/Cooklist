# ウェブドライバーライブラリ
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# Chromeバイナリライブラリ
import chromedriver_binary
# GUIライブラリ
import tkinter
from tkinter import messagebox
# 画像ライブラリ
from PIL import ImageTk,Image
# リクエストライブラリ
import urllib.request as req
#　時間ライブラリ
import time
# ファイル操作ライブラリ
import os

#　メニューの配列
MenuList = ["主菜", "副菜", "汁物", "お菓子"]
# リンクタイトルの配列
title =[]
#　レシピの配列
recipe = []
# イメージの配列
image = []
#カウント変数
message_count = 0
button_count = 0
canvas_count = 0
# ボタンサイズ
ButtonWidth = 15

#　クックパッドのURL
#URL = 'https://cookpad.com/search/'
# レタスクラブのURL
#URL = "https://www.lettuceclub.net/recipe/search/"
# GoogleのURL
URL = 'https://www.google.com'

# chromedriverの設定
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options = options)

#初期化処理
def Init():
    global message_count
    global button_count
    global canvas_count
    title.clear()
    recipe.clear()
    message_count = 0
    button_count = 0
    canvas_count = 0

#検索処理
def Search():
    global driver
    #変数初期化
    Init()
    
    #　テキストボックスの内容を保存
    # 食材
    food = FileEditBox[0].get()
    #　料理名
    dish = FileEditBox[1].get()
    #　ウェブの再起動
    driver = webdriver.Chrome(options = options)
    # URLへ接続
    driver.get(URL)
    #　検索入力フィールドの取得
    query = driver.find_element(by = By.NAME,value = "q")
    
    if len(food) != 0:
        FileEditBox[0].delete(0,tkinter.END)
        query.send_keys(food+" "+Menu.get())
    
    elif len(dish) != 0:
        FileEditBox[1].delete(0,tkinter.END)
        query.send_keys(dish + " レシピ")
    else:
        messagebox.showerror("入力エラー","テキストボックスに入力がありません")
        return
    
    query.submit()     
    #　全て表示を選択
    allopen = driver.find_element(by = By.CLASS_NAME, value = "wtnimb")
    allopen.click()
    #　表示ラグを待機
    time.sleep(2)
    GetElements()

#要素獲得処理
def GetElements():
    try:
        #タイトル取得
        for title_count in driver.find_elements(by = By.CLASS_NAME, value = "hfac6d"):
            title.append(title_count.text)
            #タイトルをメッセージとして表示
            MessageAdd(title_count.text)
            if len(title) >= 10:
                break;
    
        #レシピ取得
        for recipe_count in driver.find_elements(by = By.CLASS_NAME, value = "a-no-hover-decoration"):
            recipe.append(recipe_count.get_attribute("href"))
            if len(recipe) >= 10:
                break;
            
        #イメージ取得
        for  count, img_count in enumerate(driver.find_elements(by = By.CLASS_NAME, value = "kUzFve")):
            image_url = img_count.get_attribute("src")
            #画像をダウンロード
            os.makedirs("TEXTURE/", exist_ok = True)
            req.urlretrieve(image_url, f"TEXTURE/recipe{count}.png")
            #画像を表示
            image.append(ImageAdd(count))
            if count >= 9:
                break;

        #ダウンロードした画像を消去
        for img_delete_count in range(len(title)):
            os.remove(f"TEXTURE/recipe{img_delete_count}.png")
        try:
            os.rmdir("TEXTURE/")
        except:
            print("ファイル内にアイテムが存在します。")
            pass
    except:
        import traceback
        traceback.print_exc()
    
#レシピ選択処理
def RecipeNumber(nRecipe):
    global driver
    #ウェブの再起動
    driver = webdriver.Chrome()
    #レシピへ接続
    driver.get(recipe[int(nRecipe - 1)])
    
#ボタン追加
def ButtonAdd():
    global button_count
    RecipeButton = tkinter.Button(text = button_count + 1, width = 5, command = lambda:RecipeNumber(RecipeButton["text"]))
    RecipeButton.place(x = 150, y = 55 * button_count)
    button_count += 1

#メッセージ追加
def MessageAdd(text):
    global message_count
    #ボタン追加
    ButtonAdd()
    MesText = tkinter.Message(text = text, width = 300)
    MesText.place(x = 200, y = 55 * message_count)
    message_count += 1
    
#画像追加
def ImageAdd(count):
    global canvas_count
    #　画像ファイルの読み込み
    image_op = Image.open(f"TEXTURE/recipe{count}.png")
    image_op = image_op.resize((100,50)) #リサイズ
    image_data = ImageTk.PhotoImage(image_op)
    
    # キャンバス生成
    canvas = tkinter.Canvas(bg = "black", width = 100, height = 50)
    canvas.place(x = 500, y = 55 * canvas_count)
    canvas_count += 1
    canvas.create_image(0, 0, image = image_data, anchor = tkinter.NW)
    
    # 画像データをリターン
    return image_data
    
#メイン処理
if __name__=="__main__":
    try:
        #　tkinterオブジェクト生成
        root =tkinter.Tk()
        root.title("クックリスト")# 画面タイトル
        root.geometry("800x600")# 画面サイズ
        
        #　プルダウンメニュー生成
        Menu = tkinter.StringVar(root)
        Menu.set(MenuList[0])
        Opt = tkinter.OptionMenu(root, Menu, *MenuList)
        Opt.config(width = ButtonWidth)
        Opt.grid(row = 0, column = 1)
             
        # 食材テキストボックス生成
        FileEditBox = [tkinter.Entry(width = ButtonWidth)]
        FileEditBox[0].grid(row = 1, column = 1)   
        
        # 食材ラベル生成
        Label = [tkinter.Label(text = "食材の入力")]
        Label[0].grid(row = 2, column =1)
        
        #　料理名テキストボックス生成
        FileEditBox += [tkinter.Entry(width = ButtonWidth)]
        FileEditBox[1].grid(row = 3, column = 1)

        #　料理名ラベル生成
        Label += [tkinter.Label(text = "料理名の入力")]
        Label[1].grid(row = 4, column = 1)
               
        # Searchボタン
        SearchButton = tkinter.Button(text ="検索", width = ButtonWidth, command = Search)
        SearchButton.grid(row = 5, column = 1, columnspan = 1)# ボタン位置
        
        #　描画を継続
        root.mainloop()
        
    except:# 例外処理
        import traceback
        traceback.print_exc()
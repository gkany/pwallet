import turtle as T
import random
import time

verses_list = [
"小园新种红樱树，闲绕花行便当游。",
"春雨楼头尺八箫，何时归看浙江潮？",
"芒鞋破钵无人识，踏过樱花第几桥。",
"十日樱花作意开，绕花岂惜日千回？",
"昨来风雨偏相厄，谁向人天诉此哀？",
"忍见胡沙埋艳骨，休将清泪滴深杯。",
"多情漫向他年忆，一寸春心早巳灰。",
"仙云昨夜坠庭柯，化作翩跹万玉娥。",
"映日横陈酣国色，倚风小舞荡天魔。",
"春来惆怅谁人见，醉后风怀奈汝何。",
"坐对名花应笑我，陋帮流俗似东坡。",
"嫣然欲笑媚东墙，绰约终疑胜海棠。",
"颜色不辞污脂粉，风神偏带绮罗香。",
"园林尽日开图画，丝管含情趁艳阳。",
"怪底近来浑自醉，一尊难发少年狂。",
"昨日雪如花，今日花如雪。",
"树底迷楼画里人，金钗沽酒醉余春。",
"鞭丝车影匆匆去，十里樱花十里尘。",
"万家井爨绿杨烟，樱笋春开四月天。",
"十里隅田川上路，春风细雨看花船。",
"何处哀筝随急管，樱花永巷垂杨岸。",  
"东家老女嫁不售，白日当天三月半。",  
"溧阳公主年十四，清明暖后同墙看。", 
"归来展转到五更，梁间燕子闻长叹。",   
"樱桃花下送君时，一寸春心逐折枝。",  
"别后相思最多处，千株万片绕林垂。",    
"别来几春未还家，玉窗五见樱桃花。",  
"樱花落尽阶前月，象床愁倚熏笼。",  
"昨日南园新雨后，樱桃花发旧枝柯。",  
"天明不待人同看，绕树重重履迹多。",    
"黄金捍拨紫檀槽，弦索初张调更高。",  
"尽理昨来新上曲，内官帘外送樱桃。",    
"庭前春鸟啄林声，红夹罗襦缝未成。", 
"今朝社日停针线，起向朱樱树下行。",  
"风渐暖满城春，独占幽居养病身。",  
"莫说樱桃花已发，今年不作看花人。",
"梦中繁花犹再现, 樱瓣飘飘然。",
"若问花何指，准答是樱花。",
"久居扶桑海天缈，梦里常思舞逍遥。",
"云纱山色光潋滟，花容人面魂欲烧。",
"苦蝉待夏半枝鸣，娇樱盼春三日笑。",
"旋染东风香盈满，投怀神州多一俏。",
]

# 画樱花的躯干(60,t)
def Tree(branch, t):
    time.sleep(0.0005)
    # 1. 设置画笔的颜色和粗细
    if branch > 3:
        if 8 <= branch <= 12:
            if random.randint(0, 2) == 0:
                t.color('snow')  # 白
            else:
                t.color('lightcoral')  # 淡珊瑚色 画笔颜色
            t.pensize(branch / 3) # 画笔的粗细  2.67 < size < 4
        elif branch < 8:
            if random.randint(0, 1) == 0:
                t.color('snow')
            else:
                t.color('lightcoral')  # 淡珊瑚色
            t.pensize(branch / 2) # max size 4
        else:
            t.color('sienna')  # 赭(zhě)色
            t.pensize(branch / 10)  # 6 # min size 1.2
        t.forward(branch)
        a = 1.5 * random.random() # random.random(): [0, 1) => [0, 1.5)
        t.right(20 * a)
        b = 1.5 * random.random()
        Tree(branch - 10 * b, t)
        t.left(40 * a)
        Tree(branch - 10 * b, t)
        t.right(20 * a)
        t.up()
        t.backward(branch)
        t.down()

# 掉落的花瓣
def Petal(m, t):
    for i in range(m):
        a = 200 - 400 * random.random()
        b = 10 - 20 * random.random()
        t.up()
        t.forward(b)
        t.left(90)
        t.forward(a)
        t.down()
        t.color('lightcoral')  # 淡珊瑚色
        t.circle(1)
        t.up()
        t.backward(a)
        t.right(90)
        t.backward(b)

def cherry_draw(title="春天来了(oﾟ▽ﾟ)o"):
    T.title(title)
    # 绘图区域
    t = T.Turtle()
    # 画布大小
    w = T.Screen()
    t.hideturtle()  # 隐藏画笔
    t.getscreen().tracer(5, 0)
    w.screensize(bg='wheat')  # wheat小麦 screen 背景色
    t.left(90) # 左转90度
    t.up()
    t.backward(150) # 后退150个单位
    t.down()
    t.color('sienna') # sienna: 赭黄色, 黄土

    # 画樱花的躯干
    Tree(60, t)
    # 掉落的花瓣
    Petal(250, t)
    # w.exitonclick()

def get_random_verse(verses=verses_list):
    random_index = random.randint(0, len(verses)-1)
    return verses[random_index]

def cherry_forever():
    while True: 
        title = "彩蛋 | " + get_random_verse()
        cherry_draw(title)
        time.sleep(2)
        T.clearscreen()

# cherry_forever()
import time
import smbus

BUS = smbus.SMBus(1)  # 指定使用/dev/i2c-1

def write_word(addr, data):
    global BLEN
    temp = data
    if BLEN == 1:
        temp |= 0x08   #0000 1000      打開LCD背光
    else:
        temp &= 0xF7   #1111 0111      關閉LCD背光      
    BUS.write_byte(addr ,temp)  #在addr寫入temp

def write_command(comm):    #傳指令        8位元:XXXX X(EN)(R/W)(RS)
    # 先傳指令 bit7-4 位元
    buf = comm & 0xf0   #1111 0000

    #設定暫存器 RS = 0(寫指令), R/W = 0(寫入), EN = 1(致能)
    buf |= 0x04         #0000 0100
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)

    #將EN = 0 (disable)
    buf &= 0xFB         #1111 1011   
    write_word(LCD_ADDR ,buf)

    # 再傳 bit3-0 位元
    buf = (comm & 0x0F) << 4  #0000 1111

    #設定暫存器 RS = 0(寫指令), R/W = 0(寫入), EN = 1(致能)  
    buf |= 0x04               #0000 0100  
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)

    #將EN = 0 (disable)
    buf &= 0xFB               #1111 1011     
    write_word(LCD_ADDR ,buf)

def write_data(data):       #傳資料             8位元:XXXX X(EN)(R/W)(RS)
    # 先傳資料 bit7-4 位元     
    buf = data & 0xF0      #1111 0000

    #設定暫存器 RS = 1(寫資料), R/W = 0(寫入), EN = 1(致能)
    buf |= 0x05            #0000 0101       
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)

    #將EN = 0 (disable)
    buf &= 0xFB            #1111 1011
    write_word(LCD_ADDR ,buf)

    # 再傳資料 bit3-0 位元 
    buf = (data & 0x0F) << 4

    #設定暫存器 RS = 1(寫資料), R/W = 0(寫入), EN = 1(致能)
    buf |= 0x05           #0000 0101
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)

    #將EN = 0 (disable)
    buf &= 0xFB               
    write_word(LCD_ADDR ,buf)

def init(addr, bl):   #初始化
    # global BUS
    # BUS = smbus.SMBus(1)
    global LCD_ADDR   
    global BLEN
    LCD_ADDR = addr
    BLEN = bl
    try:
        write_command(0x33) # 先初始化為8位元模式
        time.sleep(0.005)
        write_command(0x32) # 再初始化為4位元模式
        time.sleep(0.005)
        write_command(0x28) # 設定LCD為2行 5*7 點
        time.sleep(0.005)
        write_command(0x0C) # 移除LCD的游標
        time.sleep(0.005)
        write_command(0x01) # 清除LCD螢幕
        BUS.write_byte(LCD_ADDR, 0x08)
    except:
        return False
    else:
        return True

def clear():
    write_command(0x01) # 清除LCD螢幕

def openlight():  # 啟動LCD背光
    BUS.write_byte(0x27,0x08)
    BUS.close()

def write(x, y, str):
    if x < 0:
        x = 0
    if x > 15:
        x = 15
    if y < 0:
        y = 0
    if y > 1:
        y = 1

    # Move cursor
    addr = 0x80 + 0x40 * y + x
    write_command(addr)

    for chr in str:
        write_data(ord(chr))

# Write your code here :-)
import board
import busio
import time
import digitalio
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from adafruit_debouncer import Button
from lcd.lcd import CursorMode
from audiopwmio import PWMAudioOut as AudioOut
from audiomp3 import MP3Decoder
import os, mount_sd


# Talk to the LCD at I2C address 0x27.
#https://github.com/dhalbert/CircuitPython_LCD
#set up screens
i2c = busio.I2C(scl = board.GP1, sda = board.GP0)
i2c2 = busio.I2C(scl = board.GP3, sda = board.GP2)
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16)
lcd2 = LCD(I2CPCF8574Interface(i2c2, 0x26), num_rows=2, num_cols=16)
#set up buttons
button_input1 = digitalio.DigitalInOut(board.GP4) # Wired to GP15
button_input1.switch_to_input(digitalio.Pull.UP) # Note: Pull.UP for external buttons
button1 = Button(button_input1)
button_input2 = digitalio.DigitalInOut(board.GP5) # Wired to GP15
button_input2.switch_to_input(digitalio.Pull.UP) # Note: Pull.UP for external buttons
button2 = Button(button_input2)
button_input3 = digitalio.DigitalInOut(board.GP6) # Wired to GP15
button_input3.switch_to_input(digitalio.Pull.UP) # Note: Pull.UP for external buttons
button3 = Button(button_input3)
button_inputS = digitalio.DigitalInOut(board.GP7) # Wired to GP15
button_inputS.switch_to_input(digitalio.Pull.UP) # Note: Pull.UP for external buttons
buttonS = Button(button_inputS)

#set up audio
audio = AudioOut(board.GP16)
# Setup MP3 decoder
path = "/sd/game_sounds/"
#filename = "theme.mp3"
#mp3_file = open(path + filename, "rb")
filename = "theme.mp3"
mp3_file = open(path + filename, "rb")
decoder = MP3Decoder(mp3_file)


def play_mp3(filename):
    try:
        decoder.file = open(path + filename, "rb")
        audio.play(decoder)
    except OSError:
        print(f"No such file/directory: {path + filename}")
#set up questions, prompts and answers
question_1 =["What is the     capital?", "What's the      currency?", "What is the     biggest lake?", "What's the      national sport?", "What's the      oldest city?", "What's the      population?",
"Finnish word for Santa claus?", "How many cups of coffee per day?", "Who wrote       Moomins?",
"What's the National food?", " 'Thank you' in Finnish?" , "What is the highest point?", "What's holiday on May 1st?", "What color is not in the flag?", "When was Helsinki founded?"  ]
choises_1 = [ "A.Helsinki      B.Turku   C.Oulu", "A.Mark B.Euro    C.Krona" ,"A.Saimaa B.Baltic sea C.Bodensee", "A.Baseball B.Ice Hockey C.Skiing", "A.Hanko B.Turku C.Vaasa", "A.3.5mi B.12mi  C.5.5mi",
"A.Koira B.Viro  C.Joulupukki", "A. 1-2 B.3-4     C. 5+", "A.P.Skoog B. T.Jansson C. A.Kivi",
"A.Meatballs B.Potato C.Rye bread", "A.Kiitos B. Ole hyvä C. Tunti", "A.Halti B.Kemi C.Ruka", "A.Joulu B.Vappu C. Juhannus", "A.Blue B.Yellow C.White", "A.1550 B.1400 C.1200" ]
answers_1 = [1,2,1,2,2, 3,3, 2, 2, 3, 1,1, 2, 2, 1]
print(len(question_1))
#game
def game1():
    count = 0
    print("Playing")
    #play_sound("theme.wav")
    play_mp3("theme.mp3")
    while True:
        for num in range(len(question_1)):
            #play_mp3("intense.mp3")
            user_choice = 0
            lcd.clear()
            lcd2.clear()
            lcd.print(question_1[num])
            lcd2.print(choises_1[num])

            while user_choice not in [1, 2, 3]:
                button1.update()
                button2.update()
                button3.update()
                buttonS.update()
                if buttonS.pressed:
                    print("playing")
                    game1()
                if button1.pressed:
                    user_choice = 1
                elif button2.pressed:
                    user_choice = 2
                elif button3.pressed:
                    user_choice = 3
            if user_choice == answers_1[num]:
                count += 1
                lcd2.clear()
                lcd.clear()
                lcd.print("Correct! ")
                lcd2.print("  You have        "+str(count)+" points!")
                play_mp3("small_win.mp3")

                time.sleep(3)
            else:
                lcd.clear()
                lcd2.clear()
                lcd.print("Incorrect! You  lost!")
                lcd2.print("Your score is    " + str(count)+"/15")
                play_mp3("loser.mp3")
                time.sleep(5)
                count = 0
                break
                exit
        if count == len(question_1):
            play_mp3("big_win.mp3")
            lcd.clear()
            lcd2.clear()
            lcd.print("  You win! \n  Congrats!")
            break




while True:
    buttonS.update()
    if buttonS.pressed:
        print("playing")
        game1()





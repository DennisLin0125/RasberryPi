import RPi.GPIO as GPIO
import mfrc522 as MFRC522
from tkinter import *
import sys
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
import datetime

def on_closing():
    print("ctrl+c captured, ending read.")
    GPIO.cleanup()
    sys.exit(0)

class App():
    def __init__(self,window):
        #init fireStore
        cred = credentials.Certificate('firebase_key/raspbeery-a777e-firebase-adminsdk-4sfy5-aa9216d348.json')
        firebase_admin.initialize_app(cred)
        self.firestore = firestore.client()

        
        #init Rfid
        self.previousUid = []
        self.MIFAREReader = MFRC522.MFRC522()
        self.rfidStatusHandler()


    def rfidStatusHandler(self):
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        if status == self.MIFAREReader.MI_OK:
            print("status success")            
            self.cardRuning()     
            
        threading.Timer(3, self.rfidStatusHandler).start()

    def cardRuning(self):
        (status, currentUid) = self.MIFAREReader.MFRC522_Anticoll()
        if status == self.MIFAREReader.MI_OK and set(currentUid) != set(self.previousUid):
            self.previousUid = currentUid
            cardCode = ""
            for singleId in currentUid:
                cardCode += "{:x}.".format(singleId)

            print(cardCode)
            self.saveToFireStore(cardCode)

    def saveToFireStore(self,cardCode):
        doc_ref = self.firestore.collection('Doors').document()
        currentTime = time.time()
        timestamp = datetime.datetime.fromtimestamp(currentTime)
        date = timestamp.strftime("%Y-%m-%d-%H-%M-%S")
        print(date)
        doc_ref.set({
            'timestamp':timestamp,
            'cardID': cardCode,
            'date':date
        })

if __name__ == "__main__":
    GPIO.setwarnings(False);
    root = Tk()
    root.title("RFID_LCD")
    root.protocol("WM_DELETE_WINDOW",on_closing)
    app = App(root)
    root.mainloop()
import time
import siglent_driver as Siglent
import signatone_driver as Signatone
import functions as Functions
from dotenv import load_dotenv
import os 
import config

def main():
    bubbles = 0
    # load_dotenv()
    # bubbles_url = os.getenv("BUBBLE")
    # diamond_url = os.getenv("DIAMOND")
    # print(os.getenv("BUBBLE"))
    
    if bubbles == 0:
        Functions.send_slack_message(config.Bubbles,"Bubble Obstruction!")
        Functions.send_slack_message(config.Diamonds,"Diamond Obstruction!")
if __name__ == "__main__":
    main()
from time import sleep, time
import tweepy
import schedule
import markovify

import config

class Twitter():
    def __init__(self) -> None:
        CK = config.API_KEY
        CS = config.API_KEY_SECRET
        AT = config.ACCESS_TOKEN
        AS = config.ACCESS_TOKEN_SECRET
        self.auth = tweepy.OAuth1UserHandler(CK,CS,AT,AS)
        self.api = tweepy.API(self.auth)

    def tweet(self,text:str) -> None:
        try:
            self.api.update_status(text)
        except Exception as e:
            print(e)

class Markov():
    def __init__(self) -> None:
        with open('model_data.json') as f:
            self.model = markovify.NewlineText.from_json(f.read())
        
    def gen_sentence(self) -> None:
        sentence = None
        while sentence == None:
            try:
                sentence = self.model.make_short_sentence(140)
            except Exception as e:
                print(e)
        sentence = "".join(sentence.split())
        return sentence

class Task():
    def __init__(self) -> None:
        self.markov = Markov()
        self.twitter = Twitter()
    
    def cycle_task(self) -> None:
        text = self.markov.gen_sentence()
        self.twitter.tweet(text)

def main():
    task = Task()

    schedule.every().day.at("08:00").do(task.cycle_task)
    schedule.every().day.at("11:00").do(task.cycle_task)
    schedule.every().day.at("14:00").do(task.cycle_task)
    schedule.every().day.at("17:00").do(task.cycle_task)
    schedule.every().day.at("20:00").do(task.cycle_task)
    schedule.every().day.at("23:00").do(task.cycle_task)

    while True:
        schedule.run_pending()
        sleep(5)


if __name__ == '__main__':
    main()
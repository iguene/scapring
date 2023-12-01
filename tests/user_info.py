from instabot import Bot

bot = Bot()

with open("data/simulegal.txt", "r") as file:
    followers_id = file.read().split('\n')
   
followers = []
for f in followers_id:
    followers.append(bot.get_username_from_user_id(f))


print(followers)
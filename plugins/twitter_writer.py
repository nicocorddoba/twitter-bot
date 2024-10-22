import tweepy
from decouple import config


TEXT='Este es un tweet de prueba'

def post_tweet(text:str, image_path:list[str]):
   consumer_key = config('consumer_key')
   consumer_secret = config('consumer_secret')
   access_token = config('access_token')
   access_token_secret = config('access_token_secret')
   bearer_token = config('bearer_token')
   try:
      auth = tweepy.OAuth1UserHandler(
         consumer_key, consumer_secret
      )
      auth.set_access_token(access_token, access_token_secret)
      api = tweepy.API(auth)

      client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
      media_id:list[str]
      for i in range(len(image_path)):
         media_id.append(api.media_upload(image_path[i]).media_id_string)
         # print(media_id)
      media_id = api.media_upload(image_path).media_id_string
      # print(media_id)
      r = client.create_tweet(text=text, media_ids=[media_id])
      print(r)
   except Exception as e:
      print(e)

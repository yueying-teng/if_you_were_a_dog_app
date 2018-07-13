# if_you_were_a_dog_app

using the dog breeds classification model from [here](https://github.com/yueying-teng/dog_breeds_classification/blob/master/fine_tune_xception.ipynb) in Falsk to built a web app, which can be used to calssify dog breeds or to tell [what you would be if you were a dog](https://if-you-were-a-dog.herokuapp.com/)

Flask app is deployed to Heroku and the web app looks like the following

![alt text](https://github.com/yueying-teng/if_you_were_a_dog_app/blob/master/Screen%20Shot%202018-07-13%20at%2011.20.35.png)

[template](https://github.com/mtobeiyf/keras-flask-deploy-webapp) used

**deploy Keras CNN model to Heroku**

files needed:
- app.py
- requirements.txt: remember to include gunicorn
  - didn't use virtual environment and pip freeze > requirements.txt
- runtime.txt: currently using python-3.6.6
- Procfile: no suffix, and make sure there is no extra space and line in this file

heroku login

cd 'corresponding directory'

git add --all

git commit -m 'message'

git push heroku master

heroku ps:scale web=1

heroku open

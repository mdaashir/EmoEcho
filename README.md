# Instagram Sentiment Analysis

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Python](https://www.python.org/) (Django typically requires Python)
- [Django](https://www.djangoproject.com/)
- [Node.js](https://nodejs.org/)
- [npm](https://www.npmjs.com/)
- [Ionic CLI](https://ionicframework.com/docs/cli)
- [ngrok](https://ngrok.com/)
- [Facebook Developer Account](https://developers.facebook.com/) - Create an account to set up your application.
- [Instagram Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api) - Set up an app on the Facebook Developer Dashboard to obtain API credentials.
- [Instagram Account](https://instagram.com)

## Getting Started
Clone the repository:

```bash
git clone https://github.com/instaboy007/instagram-sentiment-analysis.git
cd instagram-sentiment-analysis
```

## Setting up Facebook Developer Account

Refer [https://developers.facebook.com/docs/instagram-basic-display-api/getting-started/]

## Setting up the Server
1) Navigate to backend Directory

```bash
cd backend
```
2) Create a Virtual Environment

```bash
python -m venv venv
```

3) Activate the Virtual Environment

``` bash
venv\scripts\activate
```

4) Install Packages from requirements.txt

```bash
pip install -r requirements.txt
```

5) Open another Terminal/CMD, Activate the Virtual Environment(Navigate to Root Directory which has the venv folder and Follow Step 3)
    ```bash
        python
        import nltk
        nltk.download('vader_lexicon')
    ```
    Close the Termial

7) Start the Server

```bash
cd server
python manage.py runserver
```

## Setting up Ionic App

1) From the Root Directory Navigate to frontend/app Directory

```bash
cd frontend/app
```

2) Install Node Modules

```bash
npm install
```

3) Replace Client ID and Client Secret from Instagram App created from the Facebook Developer Dashboard in the frontend/src/context/authContext.tsx

4) Run the Ionic Development Server

```bash
ionic serve
```

This will start the Developlment Server running at http://localhost:8100/

## Setting up ngrok

1) Install Ngrok extract Zip file to a Directory and Navigate to that directory 

2) Open this Directory in cmd (directory with ngrok.exe)

3) Login to [https://dashboard.ngrok.com/login] and from the Left Menu navigate to Getting Started > Your Auth Token. Copy your Auth Token

4) Run the following command to add your authtoken to the default ngrok.yml configuration file

```bash
ngrok config add-authtoken <Your-Token>
```

5) Deploy your app online

```bash
ngrok http 8100
```
Here the Port is same as the Ionic Development Server

6) Copy the `Forwarding` Link

Example: Forwarding [https://13a8-2405-201-e033-7054-e08d-ed5c-20f4-b6c9.ngrok-free.app] -> http://localhost:8100 

Deployed Link is [https://13a8-2405-201-e033-7054-e08d-ed5c-20f4-b6c9.ngrok-free.app]

Open this in Browser to View the Deployed App.

7) Open frontend/src/context/authContext.tsx replace the redirect_uri with the Deployed Link. Replace the Valid OAuth Redirect URIs, Deauthorize callback URL, Data Deletion Request URL in the Facebook Developer Portal with the Deployed Link. Open backend/server/server/settings.py replace "YOUR_DEPLOYED_LINK" with the Deployed Link for ALLOWED_HOSTS and CROSS_ORIGIN_WHITELIST.


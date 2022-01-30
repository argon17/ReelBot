# ReelBot
No more manual scrolling to watch reels, this bot filters out most viewed reels for a given profile

# Two main features

## 1. getTop

- Get recent 10 most viewed reels
```
/getTop [profileURL]
```

## 2. getAll

- Get recent over million viewed reels
```
/getAll [profileURL]
```

# Preview
<img src="docs/ReelBot.gif" width="200">


# How to use
## 1. You need two things beforehand:
Bot Token : Create a Telegram bot using [BotFather](https://telegram.me/BotFather), and get the Bot Token.

API Key (API id/hash pair) : Visit [https://my.telegram.org/apps](https://my.telegram.org/apps), Fill the details and register a new Telegram Application.

## 2. Fork this repository.
## 3. Clone your forked repository and change into this directory.
## 4. Create a virtual environment in the current directory.
Run command
```
$ virtualenv [ENV_NAME]
```
## 5. Setup your environment variables.
You can define environment variables in 
- on linux
```
$ nano [ENV_NAME]/bin/activate
```
- on windows
```
$ nano [ENV_NAME]/bin/activate.bat
```

Add all environment variables to the end of file 
- on linux 

```
export KEY=VALUE
```
- on windows

```
set KEY=VALUE
```

## 6. Run the program.
```
$ python3 main.py
``` 
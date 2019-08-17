# Twitter media downloader
This is a python script for you to download the media in a given twitter account

## Features:
* Slow: yes, this one is designed to be slow because of: 
1. avoid banning by twitter
2. do not increase the load of twitter
3. not used for batch downloading
* Easy to use. 

## Usage
` python3 TwitterDownloader.py <account_name>

## Installation

### Install python3 dependencies

`pip3 install -r requirement`

### Install Chrome & Chromedriver

Chrome is needed by Chromedriver. In mac, you can install Chromedriver by `brew`:
```
brew cask install chromedriver
```

In Linux, you can use `apt` or `yum`:
```
apt instal chromedriver
```

## Requirement
Only support python3. Let python2 gone in the wind.

## Todo
1. Bug: UrlNotExistException never thrown

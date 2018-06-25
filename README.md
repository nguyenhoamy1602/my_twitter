# Assignment 1: Creating a Twitter Clone Project

## Requirements

### 1. Functionalities

* Tweeting (POST/DELETE/PUT): Storing message to KVS
* Attaching images: Storing image files to S3
* Single Sign-On Authentication using Google OpenID Connect <https://developers.google.com/identity/protocols/OpenIDConnect>
* Following/followers
* Original feature?

### 2. UI/UX
* Front-End: React
* Back-End: Django
* Database KVS, S3 (Minio locallly)

### 3. Third party’s module selection

* Tweet
* KVS - redis, redis-py
* Minio

### 4. Database scheme
* Tweet
* User

## Steps
1. Decide detailed specification
1. Identify TODO items - Creating a GitHub issue for each item
    * Set up Django
    * Set up Redis
    * Create models & Write API for user
    * Set up Minio for attaching images
    * Create models & Write API for tweet
    * Create front-end
        * Landing Page
        * Sign Up/ Log In
        * Home Page (tweet feed, post a tweet)
        * User Page
    * New feature (Calendar?)
1. Set task priorities
1. Write unit tests for the application

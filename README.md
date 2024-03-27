---
title: PetPalAi
emoji: 👀
colorFrom: purple
colorTo: green
sdk: docker
pinned: false
license: mit
---
# Pet Pal AI Shop Assistant

Welcome to the Pet Pal AI Shop Assistant, your intelligent guide to finding the perfect products for your pets at a website. 
Powered by the cutting-edge technologies from OpenAI and Hugging Face, our assistant is designed to provide you with personalized product recommendations based on your specific queries.

### Features

* Personalized Recommendations: Get product suggestions tailored to your pet's needs, preferences, and your budget.
* Instant Responses: Our AI understands your queries and delivers recommendations in seconds.
* Wide Range of Products: Whether you're looking for pet food, toys, or health products, our assistant has you covered.
* User-Friendly Interface: Simply type your question and let our AI do the rest.

## How It Works

* Ask a Question: Type your question into the chat interface. You can ask for product recommendations based on your pet's specific needs, compare products, or inquire about product details.

* Receive Recommendations: The AI will process your question and provide you with a list of recommended products from the website. Each recommendation will include product details, price information, and a direct link to view the product on the website.

* Explore Products: Click on the product links to learn more about each recommendation and make a purchase directly on the website.

Example Questions

    "What's the best dry food for an adult Labrador with a sensitive stomach?"
    "Can you recommend a durable toy for a cat that loves to chew?"
    "I need a flea treatment that's safe for kittens under 8 weeks. What do you suggest?"

### Feedback

We're constantly looking to improve the Pet Pal AI Shop Assistant. If you have any feedback or suggestions, please don't hesitate to reach out to us.

### About Me

This app is developed by a dedicated person passionate about improving the online shopping experience for pet owners. Utilizing the latest in AI technology from OpenAI and Hugging Face, we strive to offer a convenient, personalized shopping assistant that helps you find exactly what you need for your beloved pets.

## How to run in local
In your IDE use module chainlit

## How to build
docker build -t pet-pal-ai .

## How to run in local
docker run --env-file .env -p 7860:7860 pet-pal-ai

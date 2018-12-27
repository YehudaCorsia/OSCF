**Create a Web Page Content Filter API
Use the Watson Natural Language Understanding (NLU) and Watson Visual Recognition technologies on IBM Cloud to create a web content filter.**

By Yehuda Corsia and Michael Rakhsha | August 15, 2018

tags: [Artificial Intelligence] [Cloud Functions] [Natural Language Understanding] [Visual Recognition] [Cloudant Database]

**SUMMERY**

This code pattern will show you how to create your own content filtering API. This example focuses on explicit pornographic content embedded within webpages. The code can easily be altered to filter other mature-rated content such as: violence, drugs and more.

**DESCRIPTION**

It has been for years now that the internet is playing a main role in our day to day lives. Surfing the world wide web is more common than ever, with an ever-growing number of users. It is important for many of us to control the content of what we see on the web, as there are many things we may not want to expose to ourselves and the people surrounding us, for whatever reason may be.

In this code pattern, you will learn how to create your own content filtering system using IBM’s cloud functions and Watson capabilities. We will show you how to make your own API, which will indicate whether a website is safe to visit based on what you define as inappropriate content. In this pattern we defined inappropriate content as explicit pornographic and sexual content.

Analyzing the content on a webpage can be tricky, as there are so many different components that have to be checked. Analyzing the text is a good start, but what about when certain keywords that define the essence of our inappropriate content aren’t explicitly written? We must understand the general theme of the webpage. Let’s not forget we must analyze the images as well. But wait, what about videos and audio files…

When you have completed this code pattern, you will understand how to:

- Create an IBM Cloud Function which responds to an API request event.
- Store and retrieve data from IBM’s scalable json document database, Cloudant.
- Extract concepts and relations from text analyzed by the Natural Language Understanding (NLU) model.
- Analyze images for scenes and objects with the help of the Virtual Recognition model. 

**FLOW**

1. An http request is made to the Cloud Function API endpoint containing the url in question. 
2. Check Cloudant Database for the url, so we don’t analyze the same one twice.
3. Extract webpage text concepts with the Natural  Language Understanding model and compare with existing list of restricted concepts. 
4. Analyze a set number of images randomly for explicit mature content using the Visual Recognition model.
5. Send response to user, webpage is classified as appropriate.

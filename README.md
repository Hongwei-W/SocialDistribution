# SocialDistribution
A small project in order to create a de-centralised and distributed social networking app, built with Django (ft. Bootstrap). 



## Project Members
|Name|CCID||
|---|---|---|
|Darren Wang|darren3|Project initializing, Signup, README, Refactoring backend, Live update with comments & likes|
|Hongwei Wang|hongwei2|Refactoring Ajax for Like, Manage PRs & merges, Testing server & Debug, API & API Doc|
|Zihan Su|zsu5|Profile, Friend/Follow Request, Share, Like, Adapters for connecting other groups,|
|Mingwei Lu|mlu1|Search function, Visibility Functionality, Upload image and image base64 encoding, GitHub activities|
|Kiana Liu|yuetong|Post, Comments, Inbox, Unlisted posts, Refactoring(with Darren), Tests, Video|



## [API Documentation](./API_Documentation.md)



## Completed User Stories

- [x] As an author I want to make public posts.
- [x] As an author I want to edit public posts.
- [x] As an author, posts I create can link to images. Posts that contain text and images need to be separated.
- [x] As an author, posts I create can be images.
- [x] As a server admin, images can be hosted on my server.
- [x] As an author, posts I create can be private to another author
- [x] As an author, posts I create can be private to my friends
- [x] As an author, I can share other author’s public posts 
- [x] As an author, I can re-share other author’s friend posts to my friends 
- [x] As an author, posts I make can be in simple plain text
- [x] As an author, posts I make can be in CommonMark
- [x] As an author, I want a consistent identity per server
- [x] As a server admin, I want to host multiple authors on my server
- [x] As a server admin, I want to share public images with users on other servers. 
- [x] As an author, I want to pull in my github activity to my “stream”
- [x] As an author, I want to post posts to my “stream”
- [x] As an author, I want to delete my own public posts.
- [x] As an author, I want to befriend local authors
- [x] As an author, I want to befriend remote authors 
- [x] As an author, I want to feel safe about sharing images and posts with my friends – images shared to friends should only be visible to friends. [public images are public]
- [x] As an author, when someone sends me a friends only-post I want to see the likes. 
- [x] As an author, comments on friend posts are private only to me the original author. 
- [x] As an author, I want un-befriend local and remote authors 
- [x] As an author, I want to be able to use my web-browser to manage my profile
- [x] As an author, I want to be able to use my web-browser to manage/author my posts 
- [x] As a server admin, I want to be able add, modify, and remove authors.
- [x] As a server admin, I want to OPTIONALLY be able allow users to sign up but require my OK to finally be on my server
- [x] As a server admin, I don’t want to do heavy setup to get the posts of my author’s friends.
- [x] As a server admin, I want a restful interface for most operations
- [x] As an author, other authors cannot modify my public post
- [x] As an author, other authors cannot modify my shared to friends post. 
- [x] As an author, I want to comment on posts that I can access
- [x] As an author, I want to like posts that I can access
- [x] As an author, my server will know about my friends
- [x] As an author, When I befriend someone (they accept my friend request) I follow them, only when the other author befriends me do I count as a real friend – a bi-directional follow is a true friend. 
- [x] As an author, I want to know if I have friend requests.
- [x] As an author I should be able to browse the public posts of everyone
- [x] As a server admin, I want to be able to add nodes to share with
- [x] As a server admin, I want to be able to remove nodes and stop sharing with them.
- [x] As a server admin, I can limit nodes connecting to me via authentication.
- [x] As a server admin, node to node connections can be authenticated with HTTP Basic Auth
- [x] As a server admin, I can disable the node to node interfaces for connections that are not authenticated!
- [x] As an author, I want to be able to make posts that are unlisted, that are publicly shareable by URI alone (or for embedding images)




## License

Apache 2.0

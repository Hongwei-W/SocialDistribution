# SocialDistribution
A small project in order to create a de-centralised and distributed social networking app, built with Django (ft. Bootstrap). WIP.



## Project Members
|Name|CCID|
|---|---|
|Darren Wang|darren3|
|Hongwei Wang|hongwei2|
|Zihan Su|zsu5|
|Mingwei Lu|mlu1|
|Kiana Liu|yuetong|



## [API Documentation](./API_Documentation.md)





## Project Contribution Breakdown

All members made meaningful contributions to the growth of the project which are listed below:

Hongwei Wang (hongwei2)
- Login page (front and backend)
- Accounts tests
- API and API documentation
- Merging branches and reviewing PRs

Kiana Liu (yuetong)
- Post
- Inbox
- Comments
- Tests for myapp

Zihan Su (zsu5)
- Profile
- Follow/Unfollow
- Like
- Share

Darren Wang (darren3)
- Signup (front and backend)
- Initialised models and backend
- Wrote this amazing README

Mingwei Lu (mlu1)
- Search
- Image post
- Github activity things



## Completed User Stories

- [x] As an author I want to make public posts.
- [x] As an author I want to edit public posts.
- [ ] As an author, posts I create can link to images. Posts that contain text and images need to be separated.
- [x] As an author, posts I create can be images.
- [ ] As a server admin, images can be hosted on my server.
- [ ] As an author, posts I create can be private to another author
- [ ] As an author, posts I create can be private to my friends
- [x] As an author, I can share other author’s public posts **NEEDS CONFIRMATION**
- [ ] As an author, I can re-share other author’s friend posts to my friends **STILL NEEDS IMAGES, VISIBILITY**
- [x] As an author, posts I make can be in simple plain text
- [x] As an author, posts I make can be in CommonMark
- [x] As an author, I want a consistent identity per server
- [x] As a server admin, I want to host multiple authors on my server
- [ ] As a server admin, I want to share public images with users on other servers. **NEEDS CONFIRMATION**
- [x] As an author, I want to pull in my github activity to my “stream”
- [x] As an author, I want to post posts to my “stream”
- [x] As an author, I want to delete my own public posts.
- [ ] As an author, I want to befriend local authors **THIS IS BROKEN** remove backslash from URL in request (ln: 509)
- [ ] As an author, I want to befriend remote authors **ALSO BROKEN** remove backslash from URL in request (ln: 509)
- [ ] As an author, I want to feel safe about sharing images and posts with my friends – images shared to friends should only be visible to friends. [public images are public] **STILL NEEDS VISIBILITY**
- [ ] As an author, when someone sends me a friends only-post I want to see the likes. **STILL NEEDS VISIBILITY**
- [ ] As an author, comments on friend posts are private only to me the original author. **STILL NEEDS VISIBILITY**
- [ ] As an author, I want un-befriend local and remote authors 
- [ ] As an author, I want to be able to use my web-browser to manage my profile
- [ ] As an author, I want to be able to use my web-browser to manage/author my posts **We can modify friend posts, spec doesn't allow that**
- [x] As a server admin, I want to be able add, modify, and remove authors.
- [ ] As a server admin, I want to OPTIONALLY be able allow users to sign up but require my OK to finally be on my server
- [ ] As a server admin, I don’t want to do heavy setup to get the posts of my author’s friends.
- [x] As a server admin, I want a restful interface for most operations
- [x] As an author, other authors cannot modify my public post
- [ ] As an author, other authors cannot modify my shared to friends post. **STILL NEEDS CONFIRMIATION AFTER**
- [x] As an author, I want to comment on posts that I can access
- [x] As an author, I want to like posts that I can access
- [x] As an author, my server will know about my friends
- [ ] As an author, When I befriend someone (they accept my friend request) I follow them, only when the other author befriends me do I count as a real friend – a bi-directional follow is a true friend. **CONFIRM AFTER FIXING IMPLEMENTATIONS**
- [x] As an author, I want to know if I have friend requests.
- [x] As an author I should be able to browse the public posts of everyone
- [ ] As a server admin, I want to be able to add nodes to share with
- [ ] As a server admin, I want to be able to remove nodes and stop sharing with them.
- [x] As a server admin, I can limit nodes connecting to me via authentication.
- [x] As a server admin, node to node connections can be authenticated with HTTP Basic Auth
- [x] As a server admin, I can disable the node to node interfaces for connections that are not authenticated!
- [ ] As an author, I want to be able to make posts that are unlisted, that are publicly shareable by URI alone (or for embedding images)
- [ ] API:
  - [ ] API Pagination
  - [ ] Friend request API
- [ ] Inbox needs comments and likes (not currently in there)
- [ ] Liking a comment




## License

Apache 2.0

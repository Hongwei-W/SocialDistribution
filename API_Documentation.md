# API Documentation

## Authors 



```
URL:://service/authors
```



### GET (remote)

retrieve all authors on the node, it supports pagination

*Example:* `GET ://service/authors/` will retrieve 5 authors on page 10.

*Example:* `GET ://service/authors?page=10&size=5` will retrieve 5 authors on page 10.



## Author



```
URL:://service/authors/{author_id}
```



### GET (remote)

retrieve one author's profile.

*Example:* `GET ://service/authors/25e8f446-efc3-4f44-af8c-3af5c42993d4` will retreieve Johnny's profile.



### PUT

update one author's profile.

*Example:* `POST ://service/authors/25e8f446-efc3-4f44-af8c-3af5c42993d4` will update Johnny's profile.

```json
(body) 
{
    "type": "author",
    "id": "127.0.0.1:8000/authors/25e8f446-efc3-4f44-af8c-3af5c42993d4",		
    "username": "Johnny",														
    "host": "127.0.0.1:8000",
    "displayName": "someone",
    "github": "https://github.com/someone",
    "profileImage": "https://an_image.url"
}
```



## Followers



```
URL:://service/authors/{author_id}/followers
```



### GET (remote)

retreive a list of authors that are `author_id`'s followers.

*Example:* `GET ://service/authors/25e8f446-efc3-4f44-af8c-3af5c42993d4/followers` will retreieve Johnny's followers.





```
URL:://service/authors/{author_id}/followers/{another_author_id}
```



### GET (remote)

check if `another_author_id` is `author_id`'s follower. 

Returns:

	Will return `{'following_relation_exist': 'True'}` if  `another_author_id` is `author_id`'s follower;
	
	Will return `{'following_relation_exist': 'False'}` if  `another_author_id` is not `author_id`'s follower. 

*Example:* `GET ://service/authors/25e8f446-efc3-4f44-af8c-3af5c42993d4/followers/44603e25-39c7-4343-b779-baf9e137c155/` will check if wong is one of jonny's followers.



### PUT

add `another_author_id` as `author_id`'s follower.

Returns:

	Will return `{'following_relation_exist': 'True', 'following_relation_put': 'False'}` if `another_author_id` is already `author_id`'s follower;
	
	Will return `{'following_relation_exist': 'False', 'following_relation_put': 'True'}` if `another_author_id` is not `author_id`'s follower, and the addition process succeed;
	
	Will return `{'following_relation_exist': 'False', 'following_relation_put': 'True'}` if `another_author_id` is not `author_id`'s follower, and the addition process is not success.

*Example*:  `PUT ://service/authors/25e8f446-efc3-4f44-af8c-3af5c42993d4/followers/44603e25-39c7-4343-b779-baf9e137c155/` will try to add wong as Johnny's follower.



### DELETE

remove `another_author_id` from `author_id`'s follower.

Returns:

	Will return `{'following_relation_exist': 'True', 'following_relation_delete': 'True'}` if `another_author_id` is `author_id`'s follower and now the removing process succeed;
	
	Will return `{'following_relation_exist': 'True', 'following_relation_delete': 'False'}` if `another_author_id` is `author_id`'s follower, and the removing process is not success;
	
	Will return `{'following_relation_exist': 'False', 'following_relation_delete': 'False'}` if `another_author_id` is not `author_id`'s follower.

*Example*:  `DELETE ://service/authors/25e8f446-efc3-4f44-af8c-3af5c42993d4/followers/44603e25-39c7-4343-b779-baf9e137c155/` will try to remove wong from Johnny's follower.



## Friend/Follow Request



send a friend/follow request to another user's inbox

please refer to [inbox API](#inbox) 



## Posts



```
URL::/service/authors/{author_id}/posts
```



### GET (remote)

retrieve all the posts published by `author_id`.

*Example:*  `GET ://service/authors/Johnny/posts` will retrieve all Johnny's post.



### POST

publish a new post by using `author_id`

*Example:* `POST ://service/authors/25e8f446-efc3-4f44-af8c-3af5c42993d4/posts` will publish a post using `author_id` as Johnny, the field below are all mandatory

```json
(body)
{
    "title": "new post",
    "description": "this is a new post",
    "content": "whatever you wanna write",
    "contentType": "text/markdown", // choose from {text/markdown, text/plain, application/base64, 		
    								// image/png;base64, image/jpeg;base64}
    "categories": "post web_dev", 	// separate categories with space
    "visibility": "PUBLIC", 		// choose from {PUBLIC, FRIENDS, PRIVATE}
    "post_image": null, 			// or an base64 enocoded image
}
```



## Post



```
URL::/service/authors/{author_id}/posts/{post_id}/
```



### GET (remote)

retrieve public post published by `author_id` and that is `post_id`. 

*Example:* `GET ://service/authors/25e8f446-efc3-4f44-af8c-3af5c42993d4/posts/338ef917-789e-4db7-99e6-b00169fb9326/` will retrieve Johnny's post with id as `338ef917-789e-4db7-99e6-b00169fb9326`.



### POST

publish a new post with `post_id` by using account `author_id`

*Example:* `POST ://service/authors/25e8f446-efc3-4f44-af8c-3af5c42993d4/posts/338ef917-789e-4db7-99e6-b00169fb9326/` will publish a new post, id as `338ef917-789e-4db7-99e6-b00169fb9326`, by using Johnny's account.  The field below are all mandatory

```json
(body)
{
    "title": "new post",
    "description": "this is a new post",
    "content": "whatever you wanna write",
    "contentType": "text/markdown", // choose from {text/markdown, text/plain, application/base64, 		
    								// image/png;base64, image/jpeg;base64}
    "categories": "post web_dev", 	// separate categories with space
    "visibility": "PUBLIC", 		// choose from {PUBLIC, FRIENDS, PRIVATE}
    "post_image": null, 			// or an base64 enocoded image
}
```

<span style="color:grey">

### PUT

update an existing post that id is `post_id` and published by `author_id`

*Example:* `PUT ://service/authors/Johnny/posts/338ef917-789e-4db7-99e6-b00169fb9326/` will update an existing post, id as 338ef917-789e-4db7-99e6-b00169fb9326, by using Johnny's account

```
(body)
{
    "id": "338ef917-789e-4db7-99e6-b00169fb9326",
    "type": "post",
    "title": "new post",
    "description": "a post",
    "contentType": "md",
    "categories": "post",
    "count": 0,
    "published": "2022-03-04T18:05:48.566281Z",
    "visibility": "PUBLIC",
    "post_image": null,
    "author": {Johnny's author object}
}
```

</span>

### DELETE

remove an existing post that id is `post_id` and published by `author_id`

*Example:* `DELETE ://service/authors/Johnny/posts/338ef917-789e-4db7-99e6-b00169fb9326/` will delete an existing post, id as 338ef917-789e-4db7-99e6-b00169fb9326, by using Johnny's account



## Image Posts



```
URL::/service/authors/{author_id}/posts/{post_id}/image
```



### GET (remote)

retrieve an image post if it is an image post, otherwise return `404 not found`

*Example*: `GET :://service/authors/Johnny/posts/338ef917-789e-4db7-99e6-b00169fb9326/image` will return the post if it is one, or `404` if it is not an image



## Comments

for POST-ing to another author's inbox, please see [inbox API](#inbox_comment)

```
URL::/service/authors/{author_id}/posts/{post_id}/comments
```

### GET (remote) 

retrieve a list of comments of a post whose id is POST_ID, pagination enabled 

*Example*: `GET :://service/authors/Johnny/posts/338ef917-789e-4db7-99e6-b00169fb9326/comments` will all comments on that post



### POST

publish a new comment on that post, using the author's name

*Example:* `POST ://service/authors/Johnny/posts/338ef917-789e-4db7-99e6-b00169fb9326/comments` will publish a new comment on post 338ef917-789e-4db7-99e6-b00169fb9326, by using Johnny's account.  The field below are all mandatory

```
(body)
{
    "contentType": "text/markdown", // choose from {text/markdown, text/plain}
    "comment": "this is a comment"
}
```



## Likes

for sending likes to inbox, please go to [inbox API](#inbox)

```
# for getting likes on a post
URL::/service/authors/{author_id}/posts/{post_id}/like

# for getting likes on a comment
URL::/service/authors/{author_id}/posts/{post_id}/comments/{comment_id}/like
```



### GET (remote)

retrieve a list of authors who liked on a POST_ID

*Example*: `GET :://service/authors/Johnny/posts/338ef917-789e-4db7-99e6-b00169fb9326/likes` will show all authors who likes on a post 



retrieve a list of authors who liked on a COMMENT_ID

*Example* `GET :://service/authors/Johnny/posts/338ef917-789e-4db7-99e6-b00169fb9326/comments/338ef917-789e-4db7-99e6-b00169fb9326/likes` get a list of likes on the post



## Liked



```
URL::/service/authors/{author_id}/liked
```



### GET (remote)

retrieve a list of public posts that an author liked

*Example*: `GET :://service/authors/Johnny/liked` will show a list of public posts that Johnny liked 



## <a name='inbox'>Inbox</a>



`URL::/service/authors/{author_id}/inbox`



### GET (remote)

retrieve author_id's inbox 

*Example*: `GET :://service/authors/Johnny/inbox` will show all stuff in Johnny's inbox

```
{
    "type":"inbox",
    "author":"http://127.0.0.1:5454/authors/c1e3db8ccea4541a0f3d7e5c75feb3fb", 		// id of author of the inbox (John)
    "items":[
        {Post Object},
        {Another Post object},
        {Sample comment object}
    ]
}
```



<span style="color:grey">

### POST (remote) 

posting to an author will result in these one of these cases:

#### <a name="inbox_post">POST a post</a>

publish a post, if the person who send the post is the author_id's follower, author_id's inbox will have that post 

*Example:* `POST ://service/authors/wong/inbox` will publish a post using `author_id` as Johnny, the field below are all mandatory. If `wong` is following `Johnny`, `wong`'s inbox will have such a post

```
(body)
{
    "type": "post",					// have to declare it is a post
    "title": "new post",
    "description": "this is a new post",
    "contentType": "text/markdown", // choose from {text/markdown, text/plain, application/base64, 		
    								// image/png;base64, image/jpeg;base64}
    "categories": "post web_dev", 	// separate categories with space
    "visibility": "PUBLIC", 		// choose from {PUBLIC, FRIENDS, PRIVATE}
    "post_image": null, 			// or an base64 enocoded image
    "author": {Johnny's user object}				// "author" have to specify, it could be the same person as author_id
}
```



#### <a name="inbox_friend_follow">POST a friend/follow request </a>

send a friend/follow request to another author's inbox

*Example* `POST ://service/authors/wong/inbox` will send friend/follow request from John to Wong.

```
(b0dy)
{
	"type": "Follow",
	"summary": "John wants to follow Wang"
	"actor": {John's user object} 			// the author object for John (not included for the sake of readability)
	"object": {Wong's user object}			// the author object for Wong (not included for the sake of readability)
}
```



#### <a name="inbox_like">POST a like on an object</a>

publish a like object on a comment or post, and have it sent to the authors inbox

*Example:* `POST ://service/authors/wong/inbox` will publish a like on post `338ef917-789e-4db7-99e6-b00169fb9326` using `author_id` as Johnny, the field below are all mandatory. If `wong` is following `Johnny`, `wong`'s inbox will have such a like

```
(body)
{
    "type": "like",					// have to declare it is a like
	"object": "338ef917-789e-4db7-99e6-b00169fb9326"
    "author": {John's author object}				// the author object for John (not included for the sake of readability)
}
```

*Example*: `POST ://service/authors/won/inbox` will publish a like on comment `338ef917-789e-4db7-99e6-b00169fb9326` 

```
(body)
{
    "type": "like",						// have to declare it is a like
	"object": "http://127.0.0.1:5454/authors/338ef917-789e-4db7-99e6-b00169fb9326/posts/338ef917-789e-4db7-99e6-b00169fb9326"
    "author": {John's author object}	// the author object for John (not included for the sake of readability)
}
```

#### <a name="inbox_comment">POST a comment to a user</a>

push a comment to a user's inbox

*Example:* `POST ://service/authors/wong/inbox` will push a comment to the author's inbox

```
(body)
{
    "type":"comment",
    "author":{John's author object}								// author object of the comment
    "comment":"Some random comment",							// actual contents of the comment
    "contentType":"text/markdown",								// content type of the comment
    "published":"2015-03-09T13:07:04+00:00",
    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",			// id of the comment
}
```



</span>



### DELETE

will empty the entire inbox of author_id

*Example:* `DELETE ://service/authors/wong/inbox` will empty `wong`'s inbox, so there won't be anything in `wong`'s  inbox after this DELETE is executed 

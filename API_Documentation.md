# API Documentation



The API now can use on authors, followers, posts. 

API for Inbox, like, liked and comments will starts after project part 2 submission.

The returned format is not aligned with spec, but will fix after project part 2 submission.

The autentication has not functioning yet. 



## Authors 



```
URL:://service/authors/
```



### GET 

retrieve all authors on the node, it supports pagination

*Example:* `GET ://service/authors/` will retrieve 5 authors on page 10.

*Example:* `GET ://service/authors?page=10&size=5` will retrieve 5 authors on page 10.



## Author



```
URL:://service/authors/{author_id}
```



### GET

retrieve one author's profile.

*Example:* `GET ://service/authors/johnny/` will retreieve johnny's profile.



### PUT

update one author's profile.

*Example:* `POST ://service/authors/johnny/` will update johnny's profile.

```
(body) 
{
    "id": "johnny",
    "type": "author",
    "host": "localhost:8000",
    "displayName": "johnny",
    "github": "https://github.com/johnny",
    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
}
```



## Followers



```
URL:://service/authors/{author_id}/followers
```



### GET

retreive a list of authors that are `author_id`'s followers.

*Example:* `GET ://service/authors/johnny/followers/` will retreieve johnny's followers.





```
URL:://service/authors/{author_id}/followers/{another_author_id}
```



### GET

check if `another_author_id` is `author_id`'s follower. 

Returns:

​	Will return `{'following_relation_exist': 'True'}` if  `another_author_id` is `author_id`'s follower;

​	Will return `{'following_relation_exist': 'False'}` if  `another_author_id` is not `author_id`'s follower. 

*Example:* `GET ://service/authors/johnny/followers/wong/` will check if wong is one of jonny's followers.



### PUT

add `another_author_id` as `author_id`'s follower.

Returns:

​	Will return `{'following_relation_exist': 'True', 'following_relation_put': 'False'}` if `another_author_id` is already `author_id`'s follower;

​	Will return `{'following_relation_exist': 'False', 'following_relation_put': 'True'}` if `another_author_id` is not `author_id`'s follower, and the addition process succeed;

​	Will return `{'following_relation_exist': 'False', 'following_relation_put': 'True'}` if `another_author_id` is not `author_id`'s follower, and the addition process is not success.

*Example*:  `POST ://service/authors/johnny/followers/wong/` will try to add wong as johnny's follower.



### DELETE

remove `another_author_id` from `author_id`'s follower.

Returns:

​	Will return `{'following_relation_exist': 'True', 'following_relation_delete': 'True'}` if `another_author_id` is `author_id`'s follower and now the removing process succeed;

​	Will return `{'following_relation_exist': 'True', 'following_relation_delete': 'False'}` if `another_author_id` is `author_id`'s follower, and the removing process is not success;

​	Will return `{'following_relation_exist': 'False', 'following_relation_delete': 'False'}` if `another_author_id` is not `author_id`'s follower.

*Example*:  `DELETE ://service/authors/johnny/followers/wong/` will try to remove wong from johnny's follower.



## Posts



```
URL::/service/authors/{author_id}/posts/
```



### GET

retrieve all the posts published by `author_id`.

*Example:*  `GET ://service/authors/johnny/posts/` will retrieve all johnny's post.



### POST

publish a new post by using `author_id`

*Example:* `POST ://service/authors/johnny/posts/` will publish a post using `author_id` as johnny

```
(body)
{
    "id": "338ef917-589e-4db7-99e6-b00169fb9326",
    "type": "post",
    "title": "new post",
    "description": "this is a new post",
    "contentType": "md",
    "categories": "post",
    "count": 0,
    "published": "2022-03-04T18:05:48.566281Z",
    "visibility": "PUBLIC",
    "post_image": null,
    "author": "johnny"
}
```



## Post



```
URL::/service/authors/{author_id}/posts/{post_id}/
```



### GET

retrieve public post published by `author_id` and that is `post_id`.

*Example:* `GET ://service/authors/johnny/posts/338ef917-789e-4db7-99e6-b00169fb9326/` will retrieve johnny's post with id as 338ef917-789e-4db7-99e6-b00169fb9326.



### POST

publish a new post with `post_id` by using account `author_id`

*Example:* `POST ://service/authors/johnny/posts/338ef917-789e-4db7-99e6-b00169fb9326/` will publish a new post, id as 338ef917-789e-4db7-99e6-b00169fb9326, by using johnny's account

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
    "author": "johnny"
}
```



### PUT

update an existing post that id is `post_id` and published by `author_id`

*Example:* `PUT ://service/authors/johnny/posts/338ef917-789e-4db7-99e6-b00169fb9326/` will update an existing post, id as 338ef917-789e-4db7-99e6-b00169fb9326, by using johnny's account

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
    "author": "johnny"
}
```



### DELETE

remove an existing post that id is `post_id` and published by `author_id`

*Example:* `DELETE ://service/authors/johnny/posts/338ef917-789e-4db7-99e6-b00169fb9326/` will delete an existing post, id as 338ef917-789e-4db7-99e6-b00169fb9326, by using johnny's account
















let redirect_url = '/like';

function like_handler(object_id, author_host, author_id, object_likes) {
    const data = {"object_id": object_id, "author_host": author_host, "author_id": author_id};
    $.ajax({
        type: "post",
        url: redirect_url,
        dataType: "json",
        data: data,
        success: function (response) {
            if (response.liked == "success") {
                like_num = parseInt(object_likes) + 1;
                console.log(like_num)
                selector = document.getElementById(object_id);
                $(selector).text(like_num);
            } else if (response.liked == 'before') {
                alert("You have liked before");
            } else {
                alert("Like failed");
            }
        }
    });
}
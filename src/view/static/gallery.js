function approveImage(value, image_hash) {
  var data = {
      'status' : value,
      'image': image_hash
  }
  
  $.ajax({
      type: "POST",
      url: '/approve_image',
      data: JSON.stringify(data),
      success: function (data) {
          if (data.redirect) {
              window.location.href = data.redirect
          }
      },
      contentType: "application/json; charset=utf-8"
    });
}

function postComment(user, image) {
    var data = {
        'user' : user,
        'image_hash': image,
        'comment': $('#Comment').val()
    }
    $.ajax({
      type: "POST",
      url: '/post_comment',
      data: JSON.stringify(data),
      success: function (data) {
          if (data.redirect) {
              window.location.href = data.redirect
          }
      },
      contentType: "application/json; charset=utf-8"
    });
}

function likePost(user, image, color) {
    let data = {
        'user' : user,
        'image_hash': image,
        'liked': true
    }
    if (color == 'black'){
        $.ajax({
        type: "POST",
        url: '/like_post',
        data: JSON.stringify(data),
        success: function (data) {
            if (data.redirect) {
                window.location.href = data.redirect
            }
        },
        contentType: "application/json; charset=utf-8"
        });
    }
    else {
        data['liked'] = false
        $.ajax({
        type: "POST",
        url: '/like_post',
        data: JSON.stringify(data),
        success: function (data) {
            if (data.redirect) {
                window.location.href = data.redirect
            }
        },
        contentType: "application/json; charset=utf-8"
        });
    }
}
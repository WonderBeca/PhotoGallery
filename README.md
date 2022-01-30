# Photo Gallery

This is a simple project to make a shared gallery for a wedding event.

Technology used: Flask, s3, mongoDB and aws ec2 for deploy.

Demo on: http://52.67.73.16/

## API Reference

#### Register user

```http
  GET /register
```
Return register html page.

```http
  POST /register
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` |  Account username |
| `email`      | `string` |  Account email |
| `username`      | `string` |  Account password |
| `role`      | `string` |  Account role |


Register an user. By clicking admin on register page it will sign up an admin user (wife&husband), and by sign up on register button it will sign up an type user (guests). 

```http
  POST /login
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email`      | `string` |  Account email |
| `username`   | `string` |  Account password |

Login user.

```http
  POST /upload_image
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file`      | `png, jpeg` |  Image sended by user |

Upload image by current user.

```http
  POST /approve_image
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `image`      | `str` |  Image hash refference |
| `status`      | `string` |  Admin response to photo (accepted, refused) |

Upload image by current user.

```http
  POST /post_comment
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `image`      | `str` |  Image hash refference |
| `user`      | `string` |  Current user |
| `comment`      | `string` |  User comment |

Post comment by current user.

```http
  POST /like_post
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `image`      | `str` |  Image hash refference |
| `user`      | `string` |  Current user |

Register user like on image and increment total likes of the image.


## How to run

First set variables of Dockerfile, then run: 

```bash
  docker build -t gallery:latest .
  docker run --rm -p 5000:5000 gallery:latest
```

Then the application will be runing at :
```bash
http://localhost:5000/
```

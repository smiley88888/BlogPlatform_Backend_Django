_**Task Description**_

See the 'Task Description.md' file.

_**How to test the project:**_

- Test the MySQL connection

    `mysql -u root -p -h localhost -P 3306`

- Signup and Login

  `curl -X POST "http://127.0.0.1:8000/signup" -H "Content-Type: application/json" -d '{"email":"user@example.com", "password":"password"}'`
  
  `curl -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=user@example.com&password=password"`

- AddPost and GetPosts

  `curl -X POST "http://127.0.0.1:8000/addpost" -H "Authorization: Bearer your_token_here" -H "Content-Type: application/json" -d '{"text":"This is a new post"}'`
  
  `curl -X GET "http://127.0.0.1:8000/getposts" -H "Authorization: Bearer your_token_here"`

- DeletePost
  
  `curl -X DELETE "http://127.0.0.1:8000/deletepost/{post_id}" -H "Authorization: Bearer your_token_here"`

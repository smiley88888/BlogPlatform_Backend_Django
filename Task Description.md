_**Task Description:**_

- Develop a web application following the MVC design pattern.(Meaning 3 different Levels for Routing, Business Logic, DB calls for each call Functionality)
  
- Interface with a MySQL database using SQLAlchemy for ORM.
  
- Implement field validation and dependency injection as needed.
  
- Use Python and Django for building the application.

_**Submission Guidelines:**_

- Submit your code via GitHub by sharing the repository link to lucidtasksubmission@gmail.com.

_**Application Requirements:**_

**1. Endpoints:**

All data entities should have defined a SQLAlchemy model and a Pydantic model with extensive type validation for both.(validating all their fields in schema and model field type)

  - Signup Endpoint:
    
    Accepts `email` and `password`.
    
    Returns a token (JWT or randomly generated string).

  - Login Endpoint:
    
    Accepts `email` and `password`.
    
    Returns a token upon successful login; error response if login fails.

  - AddPost Endpoint:
    
    Accepts `text` and a `token` for authentication.
    
    Validates payload size (limit to 1 MB), saves the post in memory, returning `postID`.
    
    Returns an error for invalid or missing token.
    
    Dependency injection for token authentication.
    
  - GetPosts Endpoint:
    
    Requires a token for authentication.
    
    Returns all user's posts.
    
    Implements response caching for up to 5 minutes for the same user.
    
    Returns an error for invalid or missing token.
    
    Dependency injection for token authentication.

  - DeletePost Endpoint:
    
    Accepts `postID` and a `token` for authentication.
    
    Deletes the corresponding post from memory.
    
    Returns an error for invalid or missing token.
    
    Dependency injection for token authentication.

**2. Additional Requirements:**
  - Utilize token-based authentication for the "AddPost" and "GetPosts" endpoints, obtainable from the "Login" endpoint.
    
  - Implement request validation for the "AddPost" endpoint to ensure the payload does not exceed 1 MB.
  
  - Use in-memory caching for "GetPosts" to cache data for up to 5 minutes, employing tools like `cachetools` for this purpose.
  
  - Ensure the implementation of both SQLAlchemy and Pydantic models for each endpoint includes extensive type validation to guarantee the accuracy and integrity of data being processed. 
    
  - Documentation and comments should be comprehensive, elucidating the purpose and functionality of the code.

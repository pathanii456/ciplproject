ciplproject

steps-
run 
1.create one folder "NewProject"

2.create and activate vertual invironment-
python -m venv cipl
.\cipl\Scripts\activate

3.clone repository or open zip file shared 
cd ciplproject

4.download dependencies in activated venv -
pip install -r requirements.txt
or better to go for below options 
pip install Django
pip install django-filter
pip install django-rest-framework
pip install djangorestframework
pip install djangorestframework_simplejwt
pip install openpyxl
pip install pillow
pip install python-dotenv

5.make sure all dependencies are loading and working with
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
eg:
(email- admin@example.com, name- admin, password- admin, tc- True)
open admin interface for database view
http://127.0.0.1:8000/admin/
for time being for assignment I kept inbuilt sqlite3
py manage.py runserver

6.go to postman
import "(ciplproject.postman_collection.json)" file in postman 
and test endpoinds(apis)
There are two folders "Account" and "Product" with respective API's

open "Account" API's--

1.User Registration-

select POST method
http://127.0.0.1:8000/api/user/register/
Request Headers-
key Accept, value application/json
Request Body -- raw, json
eg:
{
    "email":"Boni@example.com",
    "name":"Boni",
    "password":"12345",
    "password2":"12345",
    "role":"user",
    "tc":"True"
}
send
test for any other exeptions as well 

2.User Login-

Method- POST
http://127.0.0.1:8000/api/user/login/
Request Headers-
key Accept, value application/json
Request Body -- raw, json
eg:
{
    "email":"admin@example.com",
    "password":"admin"
}
send
you will get response with both access and refresh token as mentioned
copy access token for further use
we are storing tokens in clint machin with HTTP_only Cookie as not accessible by js
so we have to send response from server side to cleanup cookies on logout of user as you can see in our logout logic
for CSRF and script attacks we are going with "HTTP_only Cookie" with "samesite" and "secure" attributes
all validations are added for authentication
test for any other exeptions as well  


3. User Profile

Method- GET
http://127.0.0.1:8000/api/user/profile/
Request Headers-
key Accept, value application/json
key Autherization, value Bearer <access_token> 
send

you will get response with user info for user related to token you sent
all validations are added
test for any other exeptions as well 


4.User Logout

Method- POST
http://127.0.0.1:8000/api/user/logout/
Request Headers-
key Accept, value application/json
key Autherization, value Bearer <access_token> 
send

You will get response with lofout message
Here we are trying to save refresh token in database for better control
also we are taking care of refresh token deactivation for refresh token rotation on logout
and deletion from clint cookies in logout logic 
we can cleanup inactive refresh token periodically
all validations are added
test for any other exeptions as well 


5. Token Refresh

Method- POST
http://127.0.0.1:8000/api/user/token/refresh/
Request Headers-
key Content-Type, value application/json
request Body
{<refresh_token>}
send

You will get response with new access token
for access token generation using refresh token if access token expires
as life span of refresh token is more than access token
all validations are added
test for any other exeptions as well 

6.Product Create
Method - Post
http://127.0.0.1:8000/api/product/create/
request Body 
choose "form-data" and add values as shown in postman document
In headers give access token as given in postman document

all validations are added for both authentication and permissions based on role
you can test by user with different role
only admin can perform CRUD
test for any other exeptions as well 


7.Product Update

Method - PUT
http://127.0.0.1:8000/api/product/update/1/
request Body -
choose "form-data" and add values as shown in postman document
Request Headers-
key Autherization, value Bearer <access_token> 

all validations are added for both authentication and permissions based on role
you can test by user with different role
only admin can perform CRUD
test for any other exeptions as well 


8.Product Partial Update

Method - PATCH
http://127.0.0.1:8000/api/product/update/1/
request Body -
choose "form-data" and add values as shown in postman document
Request Headers-
key Autherization, value Bearer <access_token> 

all validations are added for both authentication and permissions based on role
you can test by user with different role
only admin can perform CRUD
test for any other exeptions as well 


9.Product Delete
Method - DELETE
http://127.0.0.1:8000/api/product/delete/1/
Request Headers-
key Accept, value application/json 
key Autherization, value Bearer <access_token> 

here soft delete is performed onle deactivataed product not deleted from db
all validations are added for both authentication and permissions based on role
you can test by user with different role
only admin can perform CRUD
test for any other exeptions as well 


10.Product List
Method - GET
http://127.0.0.1:8000/api/product/list/
Request Headers-
key Accept, value application/json 
key Autherization, value Bearer <access_token>

gives list of all active products
all validations are added for both authentication and permissions based on role
you can test by user with different role
only admin can perform CRUD
test for any other exeptions as well 


10.Product Disable
Method - PATCH
http://127.0.0.1:8000/api/product/disable/1/
Request Headers-
key Accept, value application/json 
key Autherization, value Bearer <access_token> 

here disable product by id is performed onle disabled product 
all validations are added for both authentication and permissions based on role
you can test by user with different role
only admin can perform CRUD
test for any other exeptions as well 

11.Export Product
Method- GET
http://127.0.0.1:8000/api/product/export/products/
Request Headers-
key Autherization, value Bearer <access_token> 
send

once you send go to response body you will get binary data visible 
click on save resonse button in top right corner of response body to save products.xlsx file 
open in excel


postman documentation-
https://documenter.getpostman.com/view/40948011/2sAYQWKZR2


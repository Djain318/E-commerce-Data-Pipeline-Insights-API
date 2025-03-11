# E-commerce Data Pipeline & Insights API
 
## 🚀 Deployment 
 
**Live API Base URL:** [https://opinium-ai-backend-engineer-intern.onrender.com/](https://opinium-ai-backend-engineer-intern.onrender.com/) 
 
## 🚀 Overview 
 
This project implements a data transformation pipeline that fetches raw event data from multiple public APIs, normalizes and enriches it using business rules, and provides an API to query the processed data. 

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.110.0-009688?style=flat&logo=fastapi">
  <img src="https://img.shields.io/badge/Uvicorn-0.29.0-ff69b4?style=flat&logo=python">
  <img src="https://img.shields.io/badge/Requests-2.31.0-007ec6?style=flat&logo=python">
</p>


## 🚀 Features 
 
- Fetches data from three public sources: 
  - E-commerce product data 
  - User data 
  - Transaction/order data 
- Transforms and normalizes data into a unified format. 
- Applies business rules: 
  - Joins transaction data with product data to include product details. 
  - Joins transaction data with user data for complete purchase records. 
  - Calculates total spending per user. 
  - Identifies the most popular product categories. 
  - Computes the average transaction value. 
- Provides FastAPI-based endpoints for querying processed data. 
 
## 🚀 Data Sources 
 
The following public APIs are used: 
 
**1️⃣ Products API**: [FakeStoreAPI](https://fakestoreapi.com/products) 
 
- Endpoint: `https://fakestoreapi.com/products` 
- Represents the product catalog. 
 
**2️⃣ Users API**: [RandomUser API](https://randomuser.me/api/?results=20) 
 
- Endpoint: `https://randomuser.me/api/?results=20` 
- Represents user profiles. 
 
**3️⃣ Transactions API**: [Mockaroo API](https://my.api.mockaroo.com/orders.json?key=e49e6840) 
 
- Endpoint: `https://my.api.mockaroo.com/orders.json?key=e49e6840` 
- Represents purchase transactions. 
 
## 🚀 Data Transformation 
 
All fetched data is transformed into the following standardized format: 
 
```json 
{ 
    "entity_id": "generated-unique-id", 
    "entity_type": "product|user|transaction", 
    "timestamp": "ISO-8601-format", 
    "data": { 
      "Normalized fields from the source" 
    }, 
    "metadata": { 
        "source": "which API", 
        "processed_at": "processing timestamp" 
    } 
} 
``` 
 
## 🚀 API Endpoints 
 
### **1️⃣ Retrieve Processed Data** 
 
```http 
GET /data/{entity_type} 
``` 
 
- Fetches processed data based on entity type (`product`, `user`, or `transaction`). 
- Hosted API Endpoint: 
  [https://opinium-ai-backend-engineer-intern.onrender.com/data/{entity\_type}](https://opinium-ai-backend-engineer-intern.onrender.com/data/{entity_type}) 
 
#### Example Response for 
```http 
GET /data/user
```                                       
```json 
{ 
  
  {
    "entity_id": "user-3f159cd2-80ec-4d8c-918f-ace69f416f7d",
    "entity_type": "user",
    "timestamp": "2025-03-09T11:27:54.463526+00:00",
    "data": {
      "gender": "male",
      "name": {
        "title": "Mr",
        "first": "Aleksi",
        "last": "Ojala"
      },
      "location": {
        "street": {
          "number": 6747,
          "name": "Hatanpään Valtatie"
        },
        "city": "Koski",
        "state": "Lapland",
        "country": "Finland",
        "postcode": 88333,
        "coordinates": {
          "latitude": "-21.7129",
          "longitude": "-140.9710"
        },
        "timezone": {
          "offset": "+2:00",
          "description": "Kaliningrad, South Africa"
        }
      },
      "email": "aleksi.ojala@example.com",
      "login": {
        "uuid": "1a8a254d-3308-4936-a8f9-ca15cfd46eb2",
        "username": "yellowmeercat778",
        "password": "keisha",
        "salt": "mmcGKnAQ",
        "md5": "96d14b84f0017bb0cea3734c608f0cb4",
        "sha1": "737bc0578261ad1ea9dcb49e6e3e434dcec4f696",
        "sha256": "8c149eb701c2e68989e377ca2f5151e61acb494acd073b7b8ae2f4c1299406c3"
      },
      "dob": {
        "date": "1982-12-18T00:07:47.343Z",
        "age": 42
      },
      "registered": {
        "date": "2004-06-12T05:27:10.072Z",
        "age": 20
      },
      "phone": "08-982-487",
      "cell": "041-932-92-04",
      "id": {
        "name": "HETU",
        "value": "NaNNA815undefined"
      },
      "picture": {
        "large": "https://randomuser.me/api/portraits/men/31.jpg",
        "medium": "https://randomuser.me/api/portraits/med/men/31.jpg",
        "thumbnail": "https://randomuser.me/api/portraits/thumb/men/31.jpg"
      },
      "nat": "FI"
    },
    "metadata": {
      "source": "https://randomuser.me/api/?results=20",
      "processed_at": "2025-03-09T11:27:54.463578+00:00"
    }
  },
``` 
 
### **2️⃣ User Spending Insights** 
 
```http 
GET /insights/users 
``` 
 
- Returns total spending per user. 
- Hosted API Endpoint: 
  [https://opinium-ai-backend-engineer-intern.onrender.com/insights/users](https://opinium-ai-backend-engineer-intern.onrender.com/insights/users) 
 
### **3️⃣ Product Popularity Insights** 
 
```http 
GET /insights/products 
``` 
 
- Identifies the most popular product categories. 
- Hosted API Endpoint: 
  [https://opinium-ai-backend-engineer-intern.onrender.com/insights/products](https://opinium-ai-backend-engineer-intern.onrender.com/insights/products) 
 
### **4️⃣ Test the Endpoints Using Swagger UI** 
 
FastAPI provides an interactive API documentation using Swagger UI. Once the server is running: 
 
- Open your browser and go to: `http://127.0.0.1:8000/docs` 
- You can interact with all the API endpoints directly from this interface. 
 
Alternatively, you can use Redoc: 
 
- Open `http://127.0.0.1:8000/redoc` 
 
#### Swagger UI Preview
![Swagger UI](app/Public/Swagger.png)
 
## 🚀 Project Setup Instructions 
 
### **1️⃣ Clone the Repository** 
 
```sh 
git clone https://github.com/Djain318/Opinium.ai-Backend-Engineer-Intern-Project.git 
cd Opinium.ai-Backend-Engineer-Intern-Project 
``` 
 
### **2️⃣ Create a Virtual Environment** 
 
```sh 
python -m venv .venv 
``` 
 
On Windows: 
 
```sh 
.venv\Scripts\activate 
``` 
 
On macOS/Linux: 
 
```sh 
source .venv/bin/activate 
``` 
 
### **3️⃣ Install Dependencies** 
 
```sh 
pip install -r requirements.txt 
``` 
 
### **4️⃣ Run the Application** 
 
```sh 
uvicorn main:app --host 0.0.0.0 --port 8000 --reload 
``` 
## 🚀 **How I approach to solve the Problem ?**   
 
I started by understanding the requirements, which involved building a FastAPI backend that fetches data from multiple APIs, processes it, and provides insights on users, transactions, and products.  
- For data fetching and transformation, I used `requests` to get data from external APIs and applied a decorator (`transform_response`) to standardize the format, adding metadata and timestamps.   
- To process the data efficiently, I created lookup dictionaries for users and products, then enriched transactions by merging them with relevant details.   
- For insights, I calculated total spending per user, identified the most popular product category, and computed the average transaction value.   
- FastAPI endpoints were set up to fetch raw data (`/data/{entity_type}`) and provide insights on user spending (`/insights/user`) and popular product categories (`/insights/product`).   
- To optimize performance, I made fetched data global to avoid redundant API calls. Debugging included fixing issues like `AttributeError: 'tuple' object has no attribute 'get'` by ensuring correct data structures.   

Finally, for deployment, I considered Render.

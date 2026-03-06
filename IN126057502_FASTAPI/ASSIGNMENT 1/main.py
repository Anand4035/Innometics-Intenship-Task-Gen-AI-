from fastapi import FastAPI, Query

app = FastAPI()

products = [
 {"id":1,"name":"Wireless Mouse","price":499,"category":"Electronics","in_stock":True},
 {"id":2,"name":"Notebook","price":99,"category":"Stationery","in_stock":True},
 {"id":3,"name":"USB Hub","price":799,"category":"Electronics","in_stock":False},
 {"id":4,"name":"Pen Set","price":49,"category":"Stationery","in_stock":True},
 {"id":5,"name":"Laptop Stand","price":1499,"category":"Electronics","in_stock":True},
 {"id":6,"name":"Mechanical Keyboard","price":11999,"category":"Electronics","in_stock":True},
 {"id":7,"name":"Webcam","price":2499,"category":"Electronics","in_stock":False},
]

@app.get("/")
def home():
    return {"message":"Welcome to our E-commerce API"}

@app.get("/products")
def all_products():
    return {"products":products,"total":len(products)}

@app.get("/products/filter")
def filter_products(category:str=None,max_price:int=None,in_stock:bool=None):
    result=products
    if category: result=[p for p in result if p["category"]==category]
    if max_price: result=[p for p in result if p["price"]<=max_price]
    if in_stock is not None: result=[p for p in result if p["in_stock"]==in_stock]
    return {"filtered_products":result,"count":len(result)}

@app.get("/products/instock")
def instock():
    r=[p for p in products if p["in_stock"]]
    return {"in_stock_products":r,"count":len(r)}

@app.get("/products/deals")
def deals():
    return {
        "best_deal":min(products,key=lambda p:p["price"]),
        "premium_pick":max(products,key=lambda p:p["price"])
    }

@app.get("/products/{product_id}")
def get_product(product_id:int):
    for p in products:
        if p["id"]==product_id: return {"product":p}
    return {"error":"Product not found"}

@app.get("/products/category/{category}")
def by_category(category:str):
    r=[p for p in products if p["category"]==category]
    return r if r else {"error":"No products found in this category"}

@app.get("/store/summary")
def summary():
    total=len(products)
    instock=sum(1 for p in products if p["in_stock"])
    return {
        "store_name":"My E-commerce Store",
        "total_products":total,
        "in_stock_count":instock,
        "out_of_stock_count":total-instock,
        "unique_categories":list({p["category"] for p in products})
    }

@app.get("/products/search/{keyword}")
def search(keyword:str):
    r=[p for p in products if keyword.lower() in p["name"].lower()]
    return {"keyword":keyword,"total_matches":len(r),"products":r} if r else {"message":"No products matched your search"}
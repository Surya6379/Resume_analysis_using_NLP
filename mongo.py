import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://surya_mongodb:P3ass57word@cluster0.6ns8n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["resume"]
collection = db["employee"]

def insert(post,category):
    collection = db[category]
    if "_id" in post.keys():
        collection.insert_one(post) 
    else:

        results = collection.find({})
        id_list = []
        for result in results:
            id_list.append(result["_id"])
        if len(id_list) == 0:
            final_id = 1
        else:
            final_id = id_list[-1]+1
        post["_id"] = final_id
        collection.insert_one(post) 
    print("Inserted")

def present_or_not(post,category):
    collection = db[category]
    if(collection.find(post).count())==0:
        return 0
    else:
        return 1

def get_field(post,field,category):
    collection = db[category]
    results = collection.find_one(post)
    return results[field]

def get_post(post,category):
    collection = db[category]
    results = collection.find_one(post)
    return results

def get_collection(category):
    collection = db[category]
    results = collection.find()
    op = []
    for result in results:
        op.append(result)
    return op

def delete_post(post,category):
    collection = db[category]
    collection.delete_many(post)

def get_employer_view():

    collection = db["resume"]

    results = collection.find({})

    op = {}
    for result in results:
        for key in result:
            if key in op.keys():
                op[key].append(result[key])
            else:
                op[key] = [result[key]]
        
    return op


# resume = get_post("1",'resume')
# emp_skills = str(resume['Skills'])
# print(str(emp_skills))
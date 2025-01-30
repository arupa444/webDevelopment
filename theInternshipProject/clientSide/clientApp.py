import os
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    mongo_uri = os.environ.get("MONGODB_URI")
    client = MongoClient(mongo_uri) if mongo_uri else MongoClient("mongodb+srv://tljne:4BMNBXEZS7gqrnqM@tljne.gw0jc.mongodb.net/")
    db = client["tljne"]
    return app, db

def render_nested(data, key_types=None, level=0):
    if isinstance(data, list):
        html = '<div class="nested-list-box">'
        for item in data:
           html += render_nested(item,key_types,level+1)
        html += '</div>'
        return html
    elif isinstance(data, dict):
       html = '<div class="nested-list-box">'
       for key, value in data.items():
           data_type = ""
           if key_types and key in key_types:
               data_type = f'<span class="data-type">({key_types[key]})</span>'
           html += f"<span class='ms-{level*1}'><strong>{key}:</strong> {render_nested(value,key_types,level+1)}{data_type}</span>"
       html +='</div>'
       return html
    else:
        data_type=""
        if key_types:
           if isinstance(data,int):
                data_type = '<span class="data-type">(int)</span>'
           elif isinstance(data,float):
                 data_type = '<span class="data-type">(float)</span>'
           elif isinstance(data,bool):
                data_type ='<span class="data-type">(bool)</span>'
           elif isinstance(data,str):
                 data_type = '<span class="data-type">(string)</span>'
        return f"<span class='ms-{level*1}'>{str(data)}{data_type}<br><br></span>"

def register_filters(app):
    app.jinja_env.filters['render_nested'] = render_nested


app, db = create_app()
register_filters(app)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    collections = db.list_collection_names()
    filtered_collections = None
    search_term = request.form.get("search_term") if request.method == "POST" else None
    if search_term:
        filtered_collections = [collection for collection in collections if search_term.lower() in collection.lower()]
        if not filtered_collections:
            flash("Collection does not exists!", "error")
    return render_template("dashboard.html", collections=collections, filtered_collections=filtered_collections, search_term=search_term)

@app.route("/collection/<collection>", methods=["GET","POST"])
def collection_page(collection):
      search_term = request.form.get("search_key") if request.method == "POST" else None
      items = list(db[collection].find())
      keys = set()
      filtered_keys= None
      key_types = {}


      if items:
           for item in items:
               for key, value in item.items():
                   if isinstance(value, str):
                       try:
                           item[key] = json.loads(value)
                       except json.JSONDecodeError:
                            pass
               if "_type_map" in item:
                   key_types = item["_type_map"]
               keys.update(item.keys())

           if search_term:
                filtered_keys = [ key for key in keys if search_term.lower() in key.lower() ]
           # Truncate here as it will not cause issues, if item is not list or dict

           for item in items:
               for key, value in item.items():
                 if not isinstance(value, (dict, list)) and value is not None :
                      item[key] = str(value)[:70] #truncation logic


      keys = list(keys - {"_id", "_type_map"})
      return render_template("collection_page.html", collection=collection, items=items, keys= keys, filtered_keys=filtered_keys, search_term=search_term, key_types = key_types)


@app.route("/add_collection", methods=["POST"])
def add_collection():
    collection_name = request.form.get("collection_name")
    keys = request.form.getlist("keys[]")
    types = request.form.getlist("types[]")

    if not collection_name:
        flash("Collection name is required", "error")
        return redirect(url_for("dashboard"))
    if not keys:
        flash("Keys cannot be empty.", "error")
        return redirect(url_for("dashboard"))
    if not types:
        flash("Types cannot be empty.", "error")
        return redirect(url_for("dashboard"))


    if len(keys) != len(types):
          flash("The number of types must be equal to keys.", 'error')
          return redirect(url_for("dashboard"))

    try:
        type_map = {keys[i]: types[i] for i in range(len(keys))}
        sample_item = {key: "" for key in keys}
        sample_item["_id"] = ObjectId()
        sample_item["_type_map"] = type_map
        db[collection_name].insert_one(sample_item)

        flash(f"Collection '{collection_name}' created successfully!", 'success')
    except Exception as e:
        flash(f"Error creating collection: {e}", 'error')
        return redirect(url_for("dashboard"))

    return redirect(url_for("dashboard"))



@app.route("/delete_collection/<collection>", methods=["POST"])
def delete_collection(collection):
    try:
         db.drop_collection(collection)
         flash(f"Collection '{collection}' deleted successfully!", 'success')
    except Exception as e:
           flash(f"Error deleting collection: {e}", 'error')
    return redirect(url_for("dashboard"))


@app.route("/rename_collection/<collection>", methods=["POST"])
def rename_collection(collection):
    new_name = request.form.get("new_name")
    if not new_name:
          flash("Collection new name cannot be empty.", 'error')
          return redirect(url_for("dashboard"))
    if new_name and new_name != collection:
       try:
            db[collection].rename(new_name)
            flash(f"Collection '{collection}' renamed to '{new_name}' successfully!", 'success')
       except Exception as e:
             flash(f"Error renaming collection: {e}", 'error')
    return redirect(url_for("dashboard"))

@app.route("/add/<collection>", methods=["POST"])
def add_item(collection):
     items = list(db[collection].find())
     data = {}
     key_types={}
     if items and "_type_map" in items[0]:
       key_types= items[0]["_type_map"]
     i=0
     types= request.form.getlist("types[]")
     for key, value in request.form.items():
          if key != 'collection_name' and key != "types[]":
               try:
                  if key_types.get(key) =="int" or key_types.get(key) =="Int32":
                       data[key]=int(value)
                  elif key_types.get(key) =="float"  or key_types.get(key) =="Double" :
                        data[key]=float(value)
                  elif key_types.get(key) =="bool" or key_types.get(key) =="Boolean":
                      data[key]=value.lower()=="true"
                  elif key_types.get(key) =="list" or key_types.get(key) == "dict" or key_types.get(key) =="Array"  or key_types.get(key) =="Object":
                       data[key]=json.loads(value)
                  else:
                      if(key == "content"):
                          value = json.loads(value)
                          print(value,type(value))
                      data[key]=value
               except (ValueError, json.JSONDecodeError):
                   data[key] = value
               if types:
                    key_types[key]=types[i]
                    i +=1

     data["_id"] = ObjectId()
     try:
       db[collection].insert_one(data)
       db[collection].update_one(
            {"_id": ObjectId(data["_id"])},
            {"content": data["content"]}
            # {"$set": {"_type_map": key_types}}
        )
       flash(f"Item added to '{collection}' successfully!", 'success')
     except Exception as e:
          flash(f"Error inserting data: {e}", 'error')
     return redirect(url_for("collection_page", collection=collection))


@app.route("/edit/<collection>/<item_id>", methods=["POST"])
def edit_item(collection, item_id):
    items = list(db[collection].find())
    data = {}
    key_types={}
    if items and "_type_map" in items[0]:
         key_types = items[0]["_type_map"]

    types= request.form.getlist("types[]")
    i=0
    for key, value in request.form.items():
        if key != 'collection_name' and key!= "_id" and key != "types[]":
             try:
                 if key_types.get(key) =="int" or key_types.get(key) =="Int32":
                     data[key]=int(value)
                 elif key_types.get(key) =="float"  or key_types.get(key) =="Double" :
                     data[key]=float(value)
                 elif key_types.get(key) =="bool" or key_types.get(key) =="Boolean":
                    data[key]=value.lower()=="true"
                 elif key_types.get(key) =="list" or key_types.get(key) == "dict" or key_types.get(key) =="Array"  or key_types.get(key) =="Object":
                       data[key]=json.loads(value)
                 else:
                     if(key == "content"):
                         value = json.loads(value)
                         print(value,type(value))
                     data[key]=value

                 if types:
                     key_types[key] = types[i]
                     i +=1
             except (ValueError, json.JSONDecodeError):
                 data[key] = value
    try:
        db[collection].update_one(
            {"_id": ObjectId(item_id)},
            {"content": data["content"]}
            # {"$set": data, "$set": {"_type_map": key_types}}
        )
        flash(f"Item '{item_id}' updated in '{collection}' successfully!", 'success')
    except Exception as e:
       flash(f"Error updating data: {e}", 'error')
    return redirect(url_for("collection_page", collection=collection))



@app.route("/rename_key/<collection>/<old_key>", methods=["POST"])
def rename_key(collection, old_key):
      new_key = request.form.get("new_key")
      if not new_key:
          flash("New Key value cannot be empty", "error")
          return redirect(url_for("collection_page", collection=collection))
      if new_key and new_key != old_key:
          try:
            items = list(db[collection].find())
            key_types = {}
            if items and "_type_map" in items[0]:
                 key_types = items[0]["_type_map"]
            if old_key in key_types:
                key_types[new_key]= key_types.pop(old_key)
                db[collection].update_many(
                     {},
                    {"$rename": {old_key: new_key},  "$set": {"_type_map": key_types}}
                )
            else:
                 db[collection].update_many(
                      {},
                      {"$rename": {old_key: new_key}}
                 )
            flash(f"Key '{old_key}' renamed to '{new_key}' successfully!", 'success')
          except Exception as e:
            flash(f"Error renaming key: {e}", 'error')
      return redirect(url_for("collection_page", collection=collection))

@app.route("/delete/<collection>/<item_id>", methods=["POST"])
def delete_item(collection, item_id):
    try:
        db[collection].delete_one({"_id": ObjectId(item_id)})
        flash(f"Item '{item_id}' deleted from '{collection}' successfully!", 'success')
    except Exception as e:
        flash(f"Error deleting item: {e}", 'error')
    return redirect(url_for("collection_page", collection=collection))


@app.route("/delete_key/<collection>/<key>", methods=["POST"])
def delete_key(collection, key):
    try:
        items = list(db[collection].find())
        key_types = {}
        if items and "_type_map" in items[0]:
            key_types = items[0]["_type_map"]
        if key in key_types:
            key_types.pop(key)
            db[collection].update_many(
                 {},
                {"$unset": {key : ""}, "$set": {"_type_map": key_types}}
            )
        else:
            db[collection].update_many(
                {},
                {"$unset": {key : ""}}
            )

        flash(f"Key '{key}' deleted from '{collection}' successfully!", 'success')
    except Exception as e:
          flash(f"Error deleting key: {e}", 'error')
    return redirect(url_for("collection_page", collection=collection))


@app.route("/add_null_collection/<collection>", methods=["POST"])
def add_null_collection(collection):
    data = {}
    key_types={}
    i=0
    for key, value in request.form.items():
         if key.startswith("key_"):
            key_index = key.split("_")[1]
            value_key = f"value_{key_index}"
            type_key= f"type_{key_index}"
            try:
                data[request.form.get(key)] = json.loads(request.form.get(value_key))
            except json.JSONDecodeError:
                data[request.form.get(key)] = request.form.get(value_key)
            if request.form.get(key):
               key_types[request.form.get(key)]= request.form.get(type_key)
    data["_id"] = ObjectId()
    data["_type_map"] = key_types
    try:
      db[collection].insert_one(data)
      flash(f"Data added to '{collection}' successfully!", 'success')
    except Exception as e:
      flash(f"Error adding data: {e}", "error")
    return redirect(url_for("collection_page", collection=collection))

if __name__ == "__main__":
    app.run(debug=True)
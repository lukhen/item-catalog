# How to run the app.
1. Clone the app from github.
2. Run command: cd item-catalog
3. Run command: python -m venv .venv
4. Run command: source ./.venv/bin/activate
5. Run command: pip install flask flask-login flask-dance sqlalchemy python-dotenv
6. Create .env file with following lines:
  FLASK_APP=flaskapp
  FLASK_SECRET_KEY=supersecret
  GOOGLE_OAUTH_CLIENT_ID=850148895071-7kitc1lgf03ooem3asrpngj8g07u0k33.apps.googleusercontent.com
  GOOGLE_OAUTH_CLIENT_SECRET=z4dGFMjc0pjhL2W1pWqV2oeM
  OAUTHLIB_RELAX_TOKEN_SCOPE=true
  OAUTHLIB_INSECURE_TRANSPORT=true
7. Run command: flask createdb
8. Run command: flask run
9. Visit localhost:5000 in the browser.


# How to add an item:
1. Click "Add Item" link.
2. Fill in the form.
3. Click add button.

# How to edit an item:
0. Only the item creator can edit it.
1. If you are the item's creator you will see edit link on the item's page.
2. Click it, introduce modifications and click "Edit" button.

# How to delete an item:
1. If you are the item's creator you will see delete link on the item's page.
2. Click it and confirm.

# Json endpoint:
1. All items endpoint: catalog/json
2. Category items endpoint: "category-name"/json

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
#
# cred = credentials.Certificate('service.json')
# firebase_admin.initialize_app(cred, {
#     'databaseURL' : 'https://zywie-2b7c2.firebaseio.com'
# })
# rootDB = db.reference().child("food_exchange_list_tag")
# #
# # root = rootDB.get()
# #
# # for cat, arrItem in root.items():
# #     for key, item in enumerate(arrItem):
# #          db.reference().child("food_exchange_list_tag_mig").child(cat).update({
# #              item: True
# #          })
# db.reference().child("food_each_category").set({
#     'n':'n'
# })

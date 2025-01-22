
import base64
import pymongo
from io import BytesIO
from PIL import Image
import numpy as np
import face_recognition
import pickle

# Connect to MongoDB Atlas
client = pymongo.MongoClient("mongodb+srv://lakshan0714:lakshan123@hr.mb9wr19.mongodb.net/")


db=client["test"]
col=db["employeees"]

x=col.find()


#Function for find face_encodings
def findencodingss(imagelist):
    encodelist=[]

    for img in imagelist:
        
        encode=face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist






#Code For store image,id ,name datas into array
Names=[]
Ids=[]
Images=[]
for data in x:
    #print(data)
    uri=data["image"]
    base64_str=uri.split(",")[1]
    image_data=base64.b64decode(base64_str)

    image=Image.open(BytesIO(image_data))

    np_image=np.array(image)


    Names.append(data["Name"])
    Ids.append(data["_id"])
    Images.append(np_image)

knownencodelist=findencodingss(Images)

encodelistknownwithnameid=[knownencodelist,Names,Ids]

file=open("EncodeFile.p",'wb')
pickle.dump(encodelistknownwithnameid,file)
file.close()



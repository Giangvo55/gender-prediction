import pandas as pd 
from pickle import NONE
import mysql.connector
from mysql.connector import Error
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib 

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='myaloha',
                                         user='root'
                                        )
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

query = ("SELECT user_id, name FROM user LIMIT 100000")
cursor.execute(query)    
myresult = cursor.fetchall()

record = []

for x in myresult:
  record.append(x)

list_names = []
user_id = []
for i in range(len(record)):
    user_id.append(record[i][0])
    list_names.append(record[i][1])

df_db = pd.DataFrame({
    "User ID":user_id,
     "Name":list_names 
})
print("Save data to DataFrame")
df_db.dropna(how = 'all')

tf_idf = TfidfVectorizer(analyzer='word', ngram_range=(1,2), max_features = 4000)
tf_idf.fit(df_db['Name'])

name_enc = tf_idf.transform(df_db['Name']) 
print("Load model")
model = joblib.load('model.joblib')
predict = model.predict(name_enc)
print("Predicted")

df_db['Gender predicted'] = predict
print("Saving data to database")
val = []
for i in range(len(df_db)):
    val.append(( int(df_db['Gender predicted'][i]), int(df_db['User ID'][i])))

sql = "UPDATE user SET gender =%s WHERE user_id = %s"
cursor.executemany(sql, val)
connection.commit()
print("Updated!!!")



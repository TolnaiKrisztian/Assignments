#create database tables
python3 -c'import DML; DML.CreateDB()'
#insert random data into database tables
python3 -c'import DML; DML.InsertAllRandom()'
#disconnect from database
python3 -c'import DML; DML.Disconnect()'
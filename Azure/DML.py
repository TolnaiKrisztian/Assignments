from faker import Faker
faker = Faker()
import random
import datetime
import psycopg2
from psycopg2.extras import Json

#connect to database
connection = psycopg2.connect(user="postgres",password="root",host="localhost",port="5432",database="azure")
cursor = connection.cursor()

#create database tables
def CreateDB():
    try:
        cursor.execute(""" CREATE TABLE "User" (
            "UserID" serial,
            "EmployerNumber" int,
            "CreationDate" date,
            "Username" text,
            "Password" text,
            "Level" int,
            "Active" bool,
            PRIMARY KEY ("UserID")
            );

            CREATE TABLE "Platform" (
            "PlatformID" serial,
            "PlatformName" text,
            "HyperlinkPath" text,
            "Active" bool,
            PRIMARY KEY ("PlatformID")
            );

            CREATE TABLE "Course" (
            "CourseID" serial,
            "CourseName" text,
            "PlatformID" int,
            "Duration" int,
            "CreationDate" date,
            "Tags" text,
            "Photo" jsonb,
            "Active" bool,
            PRIMARY KEY ("CourseID"),
            CONSTRAINT "FK_Course.PlatformID"
                FOREIGN KEY ("PlatformID")
                REFERENCES "Platform"("PlatformID")
            );

            CREATE TABLE "OngoingTraining" (
            "TrainingID" serial,
            "UserID" int,
            "CourseID" int,
            "Status" text,
            "CompletionPercentage" decimal(3,2),
            "StartDate" date,
            "FinishDate" date,
            "LastUpdated" date,
            "Active" bool,
            PRIMARY KEY ("TrainingID"),
            CONSTRAINT "FK_OngoingTraining.UserID"
                FOREIGN KEY ("UserID")
                REFERENCES "User"("UserID"),
            CONSTRAINT "FK_OngoingTraining.CourseID"
                FOREIGN KEY ("CourseID")
                REFERENCES "Course"("CourseID")
            );

            CREATE TABLE "Review" (
            "ReviewID" serial,
            "UserID" int,
            "CourseID" int,
            "Feedback" text,
            "Positive" bool,
            "ranking" int,
            "Active" bool,
            PRIMARY KEY ("ReviewID"),
            CONSTRAINT "FK_Review.UserID"
                FOREIGN KEY ("UserID")
                REFERENCES "User"("UserID"),
            CONSTRAINT "FK_Review.CourseID"
                FOREIGN KEY ("CourseID")
                REFERENCES "Course"("CourseID")
            );

            CREATE TABLE "Certification" (
            "CertificationID" serial,
            "UserID" int,
            "CourseID" int,
            "CompletionDuration" int,
            "CompletionDate" date,
            "Active" bool,
            PRIMARY KEY ("CertificationID"),
            CONSTRAINT "FK_Certification.UserID"
                FOREIGN KEY ("UserID")
                REFERENCES "User"("UserID"),
            CONSTRAINT "FK_Certification.CourseID"
                FOREIGN KEY ("CourseID")
                REFERENCES "Course"("CourseID")
            );
        """)
    except (Exception, psycopg2.Error) as error:
        print("Failed: {}".format(error))
    connection.commit()

#generate a random date
start_date = datetime.date(2010, 1, 1)
end_date = datetime.date(2020, 1, 1)

time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days
random_number_of_days = random.randrange(days_between_dates)
random_date = start_date + datetime.timedelta(days=random_number_of_days)


#random insertion functions for each table // order matters because of foreign keys
def RandomInsertUser():
    def CreateUser(records):
        try:
            sql_insert_query = """ INSERT INTO "User" ("EmployerNumber","CreationDate","Username","Password","Level","Active") 
                            VALUES (%s,%s,%s,%s,%s,%s) """
            # executemany() to insert multiple rows
            result = cursor.executemany(sql_insert_query, records)
            connection.commit()
            print(cursor.rowcount, "records inserted successfully into User table")

        except (Exception, psycopg2.Error) as error:
            print("Failed inserting records into User table {}".format(error))

    records_to_insert = []
    for i in range(1,1001):
        row = [random.randint(1,1000000), str(faker.date_between(start_date='-12y', end_date='-2y')) , faker.user_name() , faker.password() , random.randint(1,5),True]
        records_to_insert.append(row)
    #print(records_to_insert)
    CreateUser(records_to_insert)

def RandomInsertPlatform():
    def CreatePlatform(records):
        try:
            sql_insert_query = """ INSERT INTO "Platform" ("PlatformName", "HyperlinkPath","Active") 
                            VALUES (%s,%s,%s) """
            # executemany() to insert multiple rows
            result = cursor.executemany(sql_insert_query, records)
            connection.commit()
            print(cursor.rowcount, "records inserted successfully into Platform table")

        except (Exception, psycopg2.Error) as error:
            print("Failed inserting records into Platform table {}".format(error))

    records_to_insert = []
    for i in range(1,11):
        row = [faker.word(), faker.url(),True]
        records_to_insert.append(row)
    #print(records_to_insert)
    CreatePlatform(records_to_insert)

def RandomInsertCourse():
    def CreateCourse(records):
        try:
            sql_insert_query = """ INSERT INTO "Course" ("CourseName", "PlatformID", "Duration", "CreationDate", "Tags", "Photo","Active") 
                            VALUES (%s,%s,%s,%s,%s,%s,%s) """
            # executemany() to insert multiple rows
            result = cursor.executemany(sql_insert_query, records)
            connection.commit()
            print(cursor.rowcount, "records inserted successfully into Course table")

        except (Exception, psycopg2.Error) as error:
            print("Failed inserting records into Course table {}".format(error))

    #take the avaible primary keys from the Platform table and put it into a list, so later we get the foreign keys to match
    PlatformIDs = []
    selectPlatformID = """select * from "Platform" """
    cursor.execute(selectPlatformID)
    PlatformIDfetch = cursor.fetchall()
    for row in PlatformIDfetch:
        PlatformIDs.append(row[0])
    
        #take the avaible primary keys from the Course table and put it into a list, so later we get the foreign keys to match
    CourseIDs = []
    selectCourseID = """select * from "Course" """
    cursor.execute(selectCourseID)
    CourseIDfetch = cursor.fetchall()
    for row in CourseIDfetch:
        CourseIDs.append(row[0])

    #take the avaible primary keys from the User table and put it into a list, so later we get the foreign keys to match
    UserIDs = []
    selectUserID = """select * from "User" """
    cursor.execute(selectUserID)
    UserIDfetch = cursor.fetchall()
    for row in UserIDfetch:
        UserIDs.append(row[0])

    #avaible tags
    tags = ["programming","communication","engineering","science","design"]

    

    records_to_insert = []
    for i in range(1,151):
        dictionary = {'UserID':random.choice(UserIDs), 'PlatformID':random.choice(PlatformIDs), 'ImageObject': 'https://images.pling.com/img/00/00/48/70/84/1220648/e4fff450a6306e045f5c26801ce31c3efaeb.jpg'}
        row = [faker.word(),random.choice(PlatformIDs), random.randint(45,300), str(faker.date_between(start_date='-14y', end_date='-13y')), random.choice(tags), Json(dictionary),True]
        records_to_insert.append(row)
    #print(records_to_insert)
    CreateCourse(records_to_insert)

#RandomInsertCourse()

def RandomInsertCertfification():
    def CreateCertification(records):
        try:
            sql_insert_query = """ INSERT INTO "Certification" ("UserID", "CourseID", "CompletionDuration", "CompletionDate","Active") 
                            VALUES (%s,%s,%s,%s,%s) """
            # executemany() to insert multiple rows
            result = cursor.executemany(sql_insert_query, records)
            connection.commit()
            print(cursor.rowcount, "records inserted successfully into Certification table")

        except (Exception, psycopg2.Error) as error:
            print("Failed inserting records into Certification table {}".format(error))

    #take the avaible primary keys from the Course table and put it into a list, so later we get the foreign keys to match
    CourseIDs = []
    selectCourseID = """select * from "Course" """
    cursor.execute(selectCourseID)
    CourseIDfetch = cursor.fetchall()
    for row in CourseIDfetch:
        CourseIDs.append(row[0])

    #take the avaible primary keys from the User table and put it into a list, so later we get the foreign keys to match
    UserIDs = []
    selectUserID = """select * from "User" """
    cursor.execute(selectUserID)
    UserIDfetch = cursor.fetchall()
    for row in UserIDfetch:
        UserIDs.append(row[0])

    records_to_insert = []
    for i in range(1,101):
        row = [random.choice(UserIDs),random.choice(CourseIDs),random.randint(45,300),str(faker.date_between(start_date='-2y', end_date='-1y')),True]
        records_to_insert.append(row)
    #print(records_to_insert)
    CreateCertification(records_to_insert)

def RandomInsertReview():
    def CreateReview(records):
        try:
            sql_insert_query = """ INSERT INTO "Review" ("UserID", "CourseID", "Feedback", "Positive", "ranking","Active") 
                            VALUES (%s,%s,%s,%s,%s,%s) """
            # executemany() to insert multiple rows
            result = cursor.executemany(sql_insert_query, records)
            connection.commit()
            print(cursor.rowcount, "records inserted successfully into Ranking table")

        except (Exception, psycopg2.Error) as error:
            print("Failed inserting records into Ranking table {}".format(error))

    #take the avaible primary keys from the Course table and put it into a list, so later we get the foreign keys to match
    CourseIDs = []
    selectCourseID = """select * from "Course" """
    cursor.execute(selectCourseID)
    CourseIDfetch = cursor.fetchall()
    for row in CourseIDfetch:
        CourseIDs.append(row[0])

    #take the avaible primary keys from the User table and put it into a list, so later we get the foreign keys to match
    UserIDs = []
    selectUserID = """select * from "User" """
    cursor.execute(selectUserID)
    UserIDfetch = cursor.fetchall()
    for row in UserIDfetch:
        UserIDs.append(row[0])
    
    #review text
    reviews = ["very useful","super helpful","boring","easy to follow","alright"]

    records_to_insert = []
    for i in range(1,101):
        row = [random.choice(UserIDs),random.choice(CourseIDs),random.choice(reviews),random.choice([True,False]),random.randint(1,5),True]
        records_to_insert.append(row)
    #print(records_to_insert)
    CreateReview(records_to_insert)

def RandomInsertOngoingTraining():
    def CreateOngoingTraining(records):
        try:
            sql_insert_query = """ INSERT INTO "OngoingTraining" ("UserID", "CourseID", "Status", "CompletionPercentage", "StartDate", "FinishDate", "LastUpdated","Active") 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """
            # executemany() to insert multiple rows
            result = cursor.executemany(sql_insert_query, records)
            connection.commit()
            print(cursor.rowcount, "records inserted successfully into OngoingTable table")

        except (Exception, psycopg2.Error) as error:
            print("Failed inserting records into OngoingTable table {}".format(error))

    #take the avaible primary keys from the Course table and put it into a list, so later we get the foreign keys to match
    CourseIDs = []
    selectCourseID = """select * from "Course" """
    cursor.execute(selectCourseID)
    CourseIDfetch = cursor.fetchall()
    for row in CourseIDfetch:
        CourseIDs.append(row[0])

    #take the avaible primary keys from the User table and put it into a list, so later we get the foreign keys to match
    UserIDs = []
    selectUserID = """select * from "User" """
    cursor.execute(selectUserID)
    UserIDfetch = cursor.fetchall()
    for row in UserIDfetch:
        UserIDs.append(row[0])
    
    #in progress
    records_to_insert = []
    for i in range(1,81):
        row = [random.choice(UserIDs),random.choice(CourseIDs),"in progress",round(random.random(),2),str(faker.date_between(start_date='-2y', end_date='-1y')),str(faker.date_between(start_date='-2y', end_date='-1y')),str(faker.date_between(start_date='-2y', end_date='-1y')),True]
        records_to_insert.append(row)
    #print(records_to_insert)
    CreateOngoingTraining(records_to_insert)

    #completed
    records_to_insert2 = []
    for i in range(1,81):
        row = [random.choice(UserIDs),random.choice(CourseIDs),"completed",1,str(faker.date_between(start_date='-2y', end_date='-1y')),str(faker.date_between(start_date='-2y', end_date='-1y')),str(faker.date_between(start_date='-2y', end_date='-1y')),True]
        records_to_insert2.append(row)
    #print(records_to_insert2)
    CreateOngoingTraining(records_to_insert)

def InsertAllRandom():
    #creation order matters because of foreign key constrants
    RandomInsertUser()
    RandomInsertPlatform()
    RandomInsertCourse()
    RandomInsertCertfification()
    RandomInsertReview()
    RandomInsertOngoingTraining()

### custom Insertion functions for each table###
 

def InsertUser(EmployerNumber=random.randint(1,1000000), CreationDate=random_date, Username=faker.user_name(), Password=faker.password(),Level=random.randint(1,5)):
    try:
        postgres_insert_query = """ INSERT INTO "User" ("EmployerNumber","CreationDate","Username","Password","Level") VALUES (%s,%s,%s,%s,%s) """
        record_to_insert = (EmployerNumber,CreationDate,Username,Password,Level)
        cursor.execute(postgres_insert_query, record_to_insert)


        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into User table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into User table", error)


def InsertPlatform(PlatformName=None,HyperLinkPath=None):
    try:
        postgres_insert_query = """ INSERT INTO "Platform" ("PlatformName", "HyperlinkPath") VALUES (%s,%s) """
        record_to_insert = (PlatformName,HyperLinkPath)
        cursor.execute(postgres_insert_query, record_to_insert)


        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into Platform table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into Platform table", error)

def InsertCourse(CourseName=None,PlatformID=None,Duration=None,CreationDate=None,Tags=None):
    try:
        postgres_insert_query = """ INSERT INTO "Course" ("CourseName", "PlatformID", "Duration", "CreationDate", "Tags") VALUES (%s,%s,%s,%s,%s) """
        record_to_insert = (CourseName,PlatformID,Duration,CreationDate,Tags)
        cursor.execute(postgres_insert_query, record_to_insert)


        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into Course table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into Course table", error)

def InsertCertification(UserID=None,CourseID=None,CompletionDuration=None,CompletionDate=None):
    try:
        postgres_insert_query = """ INSERT INTO "Certification" ("UserID", "CourseID", "CompletionDuration", "CompletionDate") VALUES (%s,%s,%s,%s) """
        record_to_insert = (UserID,CourseID,CompletionDuration,CompletionDate)
        cursor.execute(postgres_insert_query, record_to_insert)


        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into Certification table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into Certification table", error)

def InsertReview(UserID=None,CourseID=None,Feedback=None,Positive=None,Ranking=None):
    try:
        postgres_insert_query = """ INSERT INTO "Review" ("UserID", "CourseID", "Feedback", "Positive", "ranking") VALUES (%s,%s,%s,%s,%s) """
        record_to_insert = (UserID,CourseID,Feedback,Positive,Ranking)
        cursor.execute(postgres_insert_query, record_to_insert)


        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into Review table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into Review table", error)

def InsertOngoingTraning(UserID=None,CourseID=None,Status=None,CompletionPercentage=None,StartDate=None,FinishDate=None,LastUpdated=None):
    try:
        postgres_insert_query = """ INSERT INTO "OngoingTraining" ("UserID", "CourseID", "Status", "CompletionPercentage", "StartDate", "FinishDate", "LastUpdated") VALUES (%s,%s,%s,%s,%s,%s,%s) """
        record_to_insert = (UserID,CourseID,Status,CompletionPercentage,StartDate,FinishDate,LastUpdated)
        cursor.execute(postgres_insert_query, record_to_insert)


        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into Review table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into Review table", error)

#InsertUser(EmployerNumber=10,Username="test")
#InsertPlatform("udemy","www.test.com")

### UPDATE TABLE FUNCTIONS ###

def UpdateUser(Id, NewPassword):
    try:
        print("Table Before updating record ")
        sql_select_query = """select * from "User" where "UserID" = %s """
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

        # Update single record now
        sql_update_query = """Update "User" set "Password" = %s where "UserID" = %s"""
        cursor.execute(sql_update_query, (NewPassword, Id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

        print("Table After updating record ")
        sql_select_query = """select * from "User" where "UserID" = %s"""
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

#UpdateUser(1070, "mistyhaynes")

def UpdatePlatform(Id,NewUrl):
    try:
        print("Table Before updating record ")
        sql_select_query = """select * from "Platform" where "PlatformID" = %s """
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

        # Update single record now
        sql_update_query = """Update "Platform" set "HyperinkPath" = %s where "PlatformID" = %s"""
        cursor.execute(sql_update_query, (NewUrl, Id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

        print("Table After updating record ")
        sql_select_query = """select * from "Platform" where "PlatformID" = %s"""
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

def UpdateCourse(Id,NewDuration):
    try:
        print("Table Before updating record ")
        sql_select_query = """select * from "Course" where "CourseID" = %s """
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

        # Update single record now
        sql_update_query = """Update "Course" set "Duration" = %s where "CourseID" = %s"""
        cursor.execute(sql_update_query, (NewDuration, Id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

        print("Table After updating record ")
        sql_select_query = """select * from "Platform" where "CourseID" = %s"""
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

def UpdateCertification(Id,NewCompletionDuration):
    try:
        print("Table Before updating record ")
        sql_select_query = """select * from "Certification" where "CertificationID" = %s """
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

        # Update single record now
        sql_update_query = """Update "Certification" set "CompletionDuration" = %s where "CertificationID" = %s"""
        cursor.execute(sql_update_query, (NewCompletionDuration, Id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

        print("Table After updating record ")
        sql_select_query = """select * from "Certification" where "CertificationID" = %s"""
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

def UpdateReview(Id,NewRank):
    try:
        print("Table Before updating record ")
        sql_select_query = """select * from "Review" where "ReviewID" = %s """
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

        # Update single record now
        sql_update_query = """Update "Review" set "ranking" = %s where "ReviewID" = %s"""
        cursor.execute(sql_update_query, (NewRank, Id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

        print("Table After updating record ")
        sql_select_query = """select * from "Review" where "ReviewID" = %s"""
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

def UpdateOngoingTraning(Id,NewCompletionPercentage):
    try:
        print("Table Before updating record ")
        sql_select_query = """select * from "OngoingTraining" where "TrainingID" = %s """
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

        # Update single record now
        sql_update_query = """Update "OngoingTraining" set "CompletionPercentage" = %s where "TrainingID" = %s"""
        cursor.execute(sql_update_query, (NewCompletionPercentage, Id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

        print("Table After updating record ")
        sql_select_query = """select * from "OngoingTraining" where "TrainingID" = %s"""
        cursor.execute(sql_select_query, (Id,))
        record = cursor.fetchone()
        print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)


## activate functions and deactivate functions ##
#1 = active
#0 = inactive
def StatusUser(Activity,Id):
    sql_update_query = """Update "User" set "Active" = %s where "UserID" = %s"""
    cursor.execute(sql_update_query, (Activity, Id))
    connection.commit()
    count = cursor.rowcount
    print(count, "Record Updated successfully ")

def StatusPlatform(Activity,Id):
    sql_update_query = """Update "Platform" set "Active" = %s where "PlatformID" = %s"""
    cursor.execute(sql_update_query, (Activity, Id))
    connection.commit()
    count = cursor.rowcount
    print(count, "Record Updated successfully ")

def StatusCourse(Activity,Id):
    sql_update_query = """Update "Course" set "Active" = %s where "CourseID" = %s"""
    cursor.execute(sql_update_query, (Activity, Id))
    connection.commit()
    count = cursor.rowcount
    print(count, "Record Updated successfully ")

def StatusCertification(Activity,Id):
    sql_update_query = """Update "Certification" set "Active" = %s where "CertificationID" = %s"""
    cursor.execute(sql_update_query, (Activity, Id))
    connection.commit()
    count = cursor.rowcount
    print(count, "Record Updated successfully ")

def StatusReview(Activity,Id):
    sql_update_query = """Update "Review" set "Active" = %s where "ReviewID" = %s"""
    cursor.execute(sql_update_query, (Activity, Id))
    connection.commit()
    count = cursor.rowcount
    print(count, "Record Updated successfully ")

def StatusOngoingTraining(Activity,Id):
    sql_update_query = """Update "OngoingTraining" set "Active" = %s where "TrainingID" = %s"""
    cursor.execute(sql_update_query, (Activity, Id))
    connection.commit()
    count = cursor.rowcount
    print(count, "Record Updated successfully ")

## permanently delete function ##

def DeleteUser(Id):
    try:
        sql_delete_query2 = """Delete from "Certification" where "UserID" = %s"""
        cursor.execute(sql_delete_query2, (Id,))
        connection.commit()
        sql_delete_query3 = """Delete from "OngoingTraining" where "UserID" = %s"""
        cursor.execute(sql_delete_query3, (Id,))
        connection.commit()
        sql_delete_query4 = """Delete from "Review" where "UserID" = %s"""
        cursor.execute(sql_delete_query4, (Id,))
        connection.commit()  
        sql_delete_query = """Delete from "User" where "UserID" = %s"""
        cursor.execute(sql_delete_query, (Id,))
        connection.commit()                  
        count = cursor.rowcount
        print(count, "User deleted successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation", error)
#DeleteUser(1247)

def DeletePlatform(Id):
    try:
        sql_delete_query5 = """Delete from "Certification" where "PlatformID" = %s"""
        cursor.execute(sql_delete_query5, (Id,))
        connection.commit()
        sql_delete_query4 = """Delete from "OngoingTraining" where "PlatformID" = %s"""
        cursor.execute(sql_delete_query4, (Id,))
        connection.commit()
        sql_delete_query3 = """Delete from "Review" where "PlatformID" = %s"""
        cursor.execute(sql_delete_query3, (Id,))
        connection.commit()
        sql_delete_query2 = """Delete from "Course" where "PlatformID" = %s"""
        cursor.execute(sql_delete_query2, (Id,))
        connection.commit()
        sql_delete_query = """Delete from "Platform" where "PlatformID" = %s"""
        cursor.execute(sql_delete_query, (Id,))
        connection.commit()
        count = cursor.rowcount
        print(count, "Platform deleted successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation", error)

def DeleteCourse(Id):
    try:
        sql_delete_query4 = """Delete from "Review" where "CourseID" = %s"""
        cursor.execute(sql_delete_query4, (Id,))
        connection.commit()
        sql_delete_query3 = """Delete from "OngoingTraining" where "CourseID" = %s"""
        cursor.execute(sql_delete_query3, (Id,))
        connection.commit()
        sql_delete_query2 = """Delete from "Certification" where "CourseID" = %s"""
        cursor.execute(sql_delete_query2, (Id,))
        connection.commit()        
        sql_delete_query = """Delete from "Course" where "CourseID" = %s"""
        cursor.execute(sql_delete_query, (Id,))
        connection.commit()
        count = cursor.rowcount
        print(count, "Course deleted successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation", error)

def DeleteCertification(Id):
    try:
        # Update single record now
        sql_delete_query = """Delete from "Certification" where "CertificationID" = %s"""
        cursor.execute(sql_delete_query, (Id,))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation", error)

def DeleteReview(Id):
    try:
        # Update single record now
        sql_delete_query = """Delete from "Review" where "ReviewID" = %s"""
        cursor.execute(sql_delete_query, (Id,))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation", error)

def DeleteOngoingTraining(Id):
    try:
        # Update single record now
        sql_delete_query = """Delete from "OngoingTraining" where "TrainingID" = %s"""
        cursor.execute(sql_delete_query, (Id,))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation", error)


## select function ##

#selects the contents of the certification table
def SelectCertification():
    try:
        sql_select_query = """ SELECT "User"."Username", "Course"."CourseName", "Certification"."CompletionDuration", "Certification"."CompletionDate", "Platform"."PlatformName" FROM "Certification"
            JOIN "User" ON "User"."UserID" = "Certification"."UserID"
            JOIN "Course" ON "Course"."CourseID" = "Certification"."CourseID"
            JOIN "Platform" ON "Platform"."PlatformID" = "Course"."PlatformID" """

        cursor.execute(sql_select_query)
        select_query_records = cursor.fetchall()
        for row in select_query_records:
            print(row)
    except (Exception, psycopg2.Error) as error:
        print("Error in Select operation", error)

#disconnect from database
def Disconnect():
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is now closed")

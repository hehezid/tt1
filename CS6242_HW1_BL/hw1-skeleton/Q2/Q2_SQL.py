########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = False

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = " bli418"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = """
        CREATE TABLE IF NOT EXISTS movies(
        id INTEGER,
        title TEXT,
        score REAL
        );"""

        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = """
        CREATE TABLE IF NOT EXISTS MOVIE_CAST(
        movie_id INT,
        cast_id INT,
        cast_name TEXT,
        birthday TEXT,
        popularity REAL
        );
        """
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
        cursor = connection.cursor()
        with open(path,'r') as fin:
            reader=csv.reader(fin)
            for i in reader:
                try:
                    sql = "INSERT INTO movies(id,title,score) VALUES (?,?,?);"
                    cursor.execute(sql,i)
                    connection.commit()
                except Error as e:
                    return "Error occurred: " + str(e)


       ######################################################################
        
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        cursor = connection.cursor()
        with open(path, 'r') as fin:
            reader = csv.reader(fin)
            for i in reader:
                try:
                    sql = "INSERT INTO movie_cast(movie_id,cast_id,cast_name,birthday,popularity) VALUES (?,?,?,?,?);"
                    cursor.execute(sql, i)
                    connection.commit()
                except Error as e:
                    return "Error occurred: " + str(e)




        ######################################################################
        
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = """
        CREATE TABLE IF NOT EXISTS cast_bio(
        cast_id INT not null unique,
        cast_name TEXT, 
        birthday TEXT 
        );
        """
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = """
        INSERT INTO cast_bio(cast_id,cast_name,birthday)
        select  distinct  cast_id, cast_name, birthday from movie_cast;
        """
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = "create index movie_index on movies(id);"
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = "create index cast_index on movie_cast(cast_id);"
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = "create unique index cast_bio_index on cast_bio(cast_id);"
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = '''
        select  printf('%.2f',100.0*count(*)/(select count(*) from movies))
         FROM movies WHERE score > 50 AND title like '%war%';
        '''
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = '''
        select distinct movie_cast.cast_name, coun.appearance_count from movie_cast inner join 
        (
        select cast_id, count(movie_id) as appearance_count
        from movie_cast where popularity >10 group by cast_id 
        ) as coun on coun.cast_id=movie_cast.cast_id
        order by coun.appearance_count desc ,movie_cast.cast_name LIMIT 5;
        '''
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = '''
        select movies.title as movie_title, printf('%.2f',movies.score) as movie_score, coun.tota as cast_count from 
        movies inner join (
        select movie_id, count(cast_id) as tota from movie_cast group by movie_id 
        ) as coun  on movies.id=coun.movie_id
        order by  movies.score  desc , coun.tota asc, movies.title asc limit 5 ;
        '''
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = '''
         select distinct movie_cast.cast_id, movie_cast.cast_name, printf('%.2f',average_score) as average_score from movie_cast inner join (
         select t1.cast_id, count(t1.movie_id) as coun, avg(t1.score) as  average_score from        
         (select cast_id, cast_name, movie_id, b.score from movie_cast       
         inner join (        
         select id, score from movies where score >25 )b on movie_id=b.id ) t1 
         group by t1.cast_id having coun>2) as t2 on t2.cast_id= movie_cast.cast_id order by average_score desc, movie_cast.cast_name asc limit 10;
        '''


        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql ="""
        create view if not exists good_collaboration as
        select b.t1id as cast_member_id1, b.t2id as cast_member_id2, count(id) as movie_count, avg(score) as average_movie_score from (
        select  id,score, a.t1id,a.t2id from movies inner join (
        select distinct t1.cast_id as t1id, t2.cast_id as t2id, t1.movie_id from 
        (select cast_id, movie_id from  movie_cast )as t1, 
        (select cast_id, movie_id from  movie_cast )as t2 
        where t1.movie_id=t2.movie_id and t1.cast_id <t2.cast_id) as a on a.movie_id=movies.id)b  group by b.t1id, b.t2id having movie_count>=3 and 
        average_movie_score>=40;
        """
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = '''
        select distinct cast_id, cast_name, printf('%.2f', collaboration_score) as collaboration_score from MOVIE_CAST inner join (
        select cast_member_id1, avg(average_movie_score) as collaboration_score from (
        select cast_member_id1,average_movie_score from good_collaboration  union all 
        select cast_member_id2,average_movie_score from good_collaboration ) a group by a.cast_member_id1 
         )as b on b.cast_member_id1=movie_cast.cast_id order by collaboration_score desc, cast_name asc limit 5 
        '''


        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = "CREATE VIRTUAL TABLE IF NOT EXISTS movie_overview using fts4(id integer ,overview text);"
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        cursor = connection.cursor()
        with open(path, 'r') as fin:
            reader = csv.reader(fin)
            for i in reader:
                try:
                    sql = "INSERT INTO movie_overview(id,overview) VALUES (?,?);"
                    cursor.execute(sql, i)
                    connection.commit()
                except Error as e:
                    return "Error occurred: " + str(e)


        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = "select count(*) from movie_overview where overview match 'FIGHT';"
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = "select count(*) from movie_overview where overview match 'space NEAR/5 program';"
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except:
         print("Error in Part a.i")

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except:
        print("Error in part a.ii")

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except:
        print("Error in part a.iii")

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except:
        print("Error in part b")

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except:
        print("Error in part c")

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except:
        print("Error in part d")

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part e")

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part f")
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part g")

    try:   
        print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    except:
        print("Error in part h")

    conn.close()
    #################################################################################
    #################################################################################
  

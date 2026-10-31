import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db

def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host, 
        settings.mysql_user, 
        settings.mysql_passwd, 
        settings.mysql_schema)
    
    return con

def  findTrips(x,a,b):
    li = []

    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    
    sql = """SELECT t.cost_per_person, t.max_num_participants,COUNT(r.Reservation_id),t.trip_start, t.trip_end , t.trip_package_id
    FROM trip_package t , reservation r 
    WHERE r.offer_trip_package_id = t.trip_package_id AND t.trip_start >= %s AND t.trip_start <= %s AND r.travel_agency_branch_id = %s
    GROUP BY t.cost_per_person, t.max_num_participants,t.trip_start, t.trip_end, t.trip_package_id"""

    sql2 = '''SELECT e.name , e.surname , t.trip_package_id
    FROM employees e , trip_package t , reservation r , guided_tour g
    WHERE r.offer_trip_package_id = t.trip_package_id AND g.trip_package_id = t.trip_package_id AND g.travel_guide_employee_AM = e.employees_AM AND t.trip_start >= %s AND t.trip_start <= %s AND r.travel_agency_branch_id = %s
    GROUP BY e.name , e.surname , t.trip_package_id '''
    params = (a, b, int(x))  # parameterized: the driver escapes the values
    cur.execute(sql, params)
    data = cur.fetchall()

    cur.execute(sql2, params)
    result = cur.fetchall()

    
    for row in data:
        guide_list = []
        for bid in result:
            if row[5] == bid[2]:
                guide_list.append(bid[0]+" "+bid[1])
        cpp = row[0]
        mnp = row[1]
        nofres = row[2]
        trip_start = row[3]
        trip_end = row[4]
        empty_seats = mnp - nofres 
        tu = (cpp,mnp,nofres,empty_seats,trip_start,trip_end,guide_list)
        li.append(tu)

    # disconnect the Database connection
    cur.close()


    li.insert(0,("cost_per_person","max_num_participants", "reservations", "empty_seats", "trip_start", "trip_end","guide(s)"))
    return li


def findRevenue(x):
    if (x!="ASC"):
        if (x!="DESC"):
            return [("invalid  input")]
    

    li = []
    
   # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()

    sql = """SELECT b.travel_agency_branch_id , COUNT(e.employees_AM) AS employess_num , SUM(e.salary) AS salaries
                FROM travel_agency_branch b , employees e
                WHERE e.travel_agency_branch_travel_agency_branch_id = b.travel_agency_branch_id
                GROUP BY b.travel_agency_branch_id """
    
    sql2 = """SELECT   b.travel_agency_branch_id , o.cost , COUNT(r.Reservation_id) AS res_num
                FROM travel_agency_branch b , offer o , reservation r
                WHERE o.offer_id = r.offer_id AND r.travel_agency_branch_id = b.travel_agency_branch_id
                GROUP BY b.travel_agency_branch_id , o.cost
                ORDER BY b.travel_agency_branch_id ASC"""

    
    cur.execute(sql)
    data = cur.fetchall()

    cur.execute(sql2)
    result = cur.fetchall()



    if x=="DESC":
        bid_list=[]
        income = []
        res_num = []
        for row in data:
            bid_list.append(row[0])
            inc = 0
            sumres = 0
            for bid in result:
                if bid[0] == row[0]:
                    inc += (bid[1]*bid[2])  #computing the total income of each offer for each branch
                    sumres += bid[2]    #counting the total number of reservations
            income.append(inc)
            res_num.append(sumres)

        for n in range(len(income)-1, 0, -1):
            for i in range(n):
                if income[i] < income[i + 1]:
                    # swapping data if the income is greater than next element in the array
                    income[i], income[i + 1] = income[i + 1], income[i]
                    bid_list[i], bid_list[i + 1] = bid_list[i + 1], bid_list[i]
                    res_num[i], res_num[i + 1] = res_num[i + 1], res_num[i]
        
        for i in range(len(income)):
            tu = (bid_list[i],res_num[i],income[i],data[bid_list[i]-1][1],data[bid_list[i]-1][2]) #     data[bid_list[i]-1][1] #number of employees , #total salary
            li.append(tu)
    
    elif x=="ASC":
        bid_list=[]
        income = []
        res_num = []
        for row in data:
            bid_list.append(row[0])
            inc = 0
            sumres = 0
            for bid in result:
                if bid[0] == row[0]:
                    inc += (bid[1]*bid[2]) #computing the total income of each offer for each branch
                    sumres += bid[2] #counting the total number of reservations
            income.append(inc)
            res_num.append(sumres)

        for n in range(len(income)-1, 0, -1):
            for i in range(n):
                if income[i] > income[i + 1]:
                    # swapping data if the income is greater than next element in the array
                    income[i], income[i + 1] = income[i + 1], income[i]
                    bid_list[i], bid_list[i + 1] = bid_list[i + 1], bid_list[i]
                    res_num[i], res_num[i + 1] = res_num[i + 1], res_num[i]
        for i in range(len(income)):
            tu = (bid_list[i],res_num[i],income[i],data[bid_list[i]-1][1],data[bid_list[i]-1][2]) #     data[bid_list[i]-1][1] #number of employees , #total salary
            li.append(tu)
    
    # disconnect the Database connection
    cur.close()

    li.insert(0,("travel_agency_branch_id", "total_num_reservations", "total_income", "total_num_employees", "total_salary"))
    return li

def bestClient(x):
    if x!= "BEST":
        return ["invalid  input"]
    
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()

    #queries
    sql1 = '''SELECT tr.traveler_id , tr.name , tr.surname , COUNT(DISTINCT d.country) AS countries , COUNT(DISTINCT d.name) AS cities
    FROM traveler tr , reservation r , offer o , trip_package_has_destination tph , destination d 
    WHERE tr.traveler_id = r.Customer_id AND r.offer_id = o.offer_id AND o.trip_package_id = tph.trip_package_trip_package_id AND tph.destination_destination_id = d.destination_id
    GROUP BY tr.traveler_id , tr.name , tr.surname'''

    sql2 = '''SELECT tr.traveler_id , COUNT(DISTINCT r.Reservation_id) , o.cost
    FROM traveler tr , reservation r , offer o
    WHERE tr.traveler_id = r.Customer_id AND r.offer_id = o.offer_id 
    GROUP BY tr.traveler_id , o.cost 
    ORDER BY tr.traveler_id'''

    sql3 = '''SELECT tr.traveler_id , t.name
    FROM traveler tr , reservation r , offer o , guided_tour g , tourist_attraction t
    WHERE tr.traveler_id = r.Customer_id AND r.offer_id = o.offer_id AND o.trip_package_id = g.trip_package_id AND g.tourist_attraction_id = t.tourist_attraction_id
    GROUP BY tr.traveler_id , t.name 
    ORDER BY tr.traveler_id '''

    

    cur.execute(sql1)
    cc = cur.fetchall()

    cur.execute(sql2)
    costs = cur.fetchall()

    cur.execute(sql3)
    attractions  = cur.fetchall()

    Matrix1 = {}
    Matrix2 = {}
    Matrix3 = {}
    counter = 0

    for row in cc:
        
        #finding attractions for each traveler
        at_list = []
        for bid1 in attractions:
            if row[0] == bid1[0]:
                at_list.append(bid1[1])

        #calculating revenue for each traveler
        revenue  = 0 
        for bid2 in costs:
            if row[0] == bid2[0]:
                revenue = revenue + (bid2[1] * bid2[2])
        
        #inserting into a helping array
        Matrix1[counter,0] = row[1]
        Matrix1[counter,1] = row[2]
        Matrix2[counter,0] = row[3]
        Matrix2[counter,1] = row[4]
        Matrix2[counter,2] = revenue 
        Matrix3[counter,0] = at_list

        counter = counter + 1
    
    #kind of bubble sort 
    for i in range(counter):
        for j in range(0, counter-i-1):
            if Matrix2[j,2] < Matrix2[j+1,2]:
                for k in range(3):
                    Matrix2[j,k] , Matrix2[j+1,k] = Matrix2[j+1,k] , Matrix2[j,k]
                for k in range(2):
                    Matrix1[j,k] , Matrix1[j+1,k] = Matrix1[j+1,k] , Matrix1[j,k]
                Matrix3[j,0] , Matrix3[j+1,0] = Matrix3[j+1,0] , Matrix3[j,0]

    i = 1 
    while i <= counter and Matrix2[i,2] == Matrix2[i-1,2]:
        i = i + 1
    
    #kind of bubble sort 
    if i > 1:
        for j in range(i):
            for k in range(0,i-j-1):
                if Matrix1[k,1] > Matrix1[k+1,1]:
                    for y in range(3):
                        Matrix2[j,y] , Matrix2[j+1,y] = Matrix2[j+1,y] , Matrix2[j,y]
                    for y in range(2):
                        Matrix1[j,y] , Matrix1[j+1,y] = Matrix1[j+1,y] , Matrix1[j,y]
                    Matrix3[j,0] , Matrix3[j+1,0] = Matrix3[j+1,0] , Matrix3[j,0]

    li = []
    tu = (Matrix1[0,0] , Matrix1[0,1] , Matrix2[0,0] , Matrix2[0,1] , Matrix3[0,0])
    li.append(tu)
    i = 1
    while i <= counter and Matrix2[i,2] == Matrix2[i-1,2]:
        tu = (Matrix1[i,0] , Matrix1[i,1] , Matrix2[i,0] , Matrix2[i,1] , Matrix3[i,0])
        li.append(tu)
        i = i + 1
    

    # disconnect the Database connection
    cur.close()


    li.insert(0,("name" , "surname" , "countries" , "cities" , "attractions"))
    return li

-- Analytical SQL queries (MySQL) over the course-provided travel_agency database.
-- Each query answers one question from the assignment; see the README for the list.

#1:
	SELECT  DISTINCT e.name , e.surname
	FROM employees e , destination d , guided_tour g, tourist_attraction t
	WHERE d.country = "Germany" and d.destination_id = t.destination_destination_id and t.tourist_attraction_id = g.tourist_attraction_id and g.travel_guide_employee_AM = e.employees_AM
	ORDER BY e.name;

#2:
	SELECT g.travel_guide_employee_AM AS travel_guide_id , COUNT(t.trip_package_id) AS number_of_guided_tours
	FROM guided_tour g, trip_package t 
	WHERE t.trip_package_id = g.trip_package_id and t.trip_start >= '2019-01-01' and t.trip_end <= '2019-12-31' 
	GROUP BY g.travel_guide_employee_AM
	HAVING COUNT(t.trip_package_id) > 3;


#3:
	SELECT b.travel_agency_branch_id, COUNT(e.employees_AM) AS number_of_travel_guides
	FROM employees e , travel_agency_branch b
	WHERE b.travel_agency_branch_id = e.travel_agency_branch_travel_agency_branch_id
	GROUP BY b.travel_agency_branch_id;

	
#4:
	SELECT t.trip_package_id , COUNT(r.offer_id) AS number_of_reservations
	FROM trip_package t , trip_package_has_destination tp , destination d , reservation r 
	WHERE tp.destination_destination_id = d.destination_id AND d.name = 'Paris' AND t.trip_package_id = r.offer_trip_package_id  AND t.trip_package_id IN 
		(SELECT t.trip_package_id
		FROM trip_package t
		WHERE t.trip_start >= '2021-01-01' AND t.trip_end <= '2021-12-31' AND tp.trip_package_trip_package_id = t.trip_package_id)
	GROUP BY t.trip_package_id 
	ORDER BY t.trip_package_id

#5:
	SELECT  e.name , e.surname 
	FROM employees e, guided_tour g
	WHERE g.travel_guide_employee_AM = e.employees_AM 
	GROUP BY e.name , e.surname 
	HAVING COUNT(DISTINCT g.travel_guide_language_id) = 1 ;
	
#6:
	SELECT DISTINCT "yes" AS answer
	FROM offer o , reservation r
	WHERE  o.offer_start >= '2020-01-01' AND o.offer_end <= '2020-12-31' AND r.offer_id = o.offer_id 
	GROUP BY r.offer_id
	HAVING COUNT(r.Reservation_id) = 0
	UNION 
	SELECT DISTINCT "no" AS answer
	FROM offer o , reservation r
	WHERE  o.offer_start >= '2020-01-01' AND o.offer_end <= '2020-12-31' AND r.offer_id = o.offer_id
	GROUP BY r.offer_id
	HAVING COUNT(r.Reservation_id) <> 0
     

#7:
	SELECT  DISTINCT t.name , t.surname
	FROM traveler t , reservation r	
	WHERE t.age >= 40 and t.gender = 'MALE' and t.traveler_id = r.Customer_id
	GROUP BY t.name , t.surname
	HAVING COUNT(DISTINCT r.offer_trip_package_id) > 3;
	
#8:
	SELECT g.travel_guide_employee_AM AS travel_guide_id , e.name ,  e.surname , COUNT(DISTINCT g.tourist_attraction_id) AS number_of_attractions
	FROM employees e , guided_tour g , languages l , travel_guide_has_languages tg
	WHERE (l.name = "english" and tg.languages_id = l.languages_id) and tg.travel_guide_employee_AM = e.employees_AM and (g.travel_guide_employee_AM = tg.travel_guide_employee_AM) and (g.travel_guide_language_id = l.languages_id and l.name = "english")
	GROUP BY travel_guide_id , e.name , e.surname ;

#9:
	SELECT x.country
	FROM (SELECT COUNT(DISTINCT t.trip_package_id) AS id_count , d.country
	FROM destination d, trip_package t, trip_package_has_destination tp
	WHERE d.destination_id = tp.destination_destination_id AND tp.trip_package_trip_package_id = t.trip_package_id
    GROUP BY d.country) x
    WHERE  x.id_count = (SELECT MAX(m.idcount) FROM (SELECT COUNT(DISTINCT t1.trip_package_id) AS idcount , d1.country
	FROM destination d1, trip_package t1, trip_package_has_destination tp1
	WHERE d1.destination_id = tp1.destination_destination_id AND tp1.trip_package_trip_package_id = t1.trip_package_id
    GROUP BY d1.country) m);
	
#10:
	SELECT t.trip_package_id
	FROM trip_package t , trip_package_has_destination tp , destination d
	WHERE tp.destination_destination_id = d.destination_id AND d.country = 'Ireland' AND tp.trip_package_trip_package_id = t.trip_package_id AND t.trip_package_id NOT IN 
			(SELECT t.trip_package_id 
			FROM trip_package t , trip_package_has_destination tp , destination d , destination d2
			WHERE tp.destination_destination_id = d.destination_id AND d.country = 'Ireland' AND tp.trip_package_trip_package_id = t.trip_package_id AND d2.country = 'Ireland'
			GROUP BY t.trip_package_id
			HAVING COUNT(DISTINCT d.name) < COUNT(DISTINCT d2.name))
	GROUP BY t.trip_package_id 
	ORDER BY t.trip_package_id


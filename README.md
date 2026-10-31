# Travel Agency Database

Relational database design and SQL for a travel-agency chain. The project has two parts: an **ER model and MySQL schema** designed from a written specification, and **analytical SQL queries plus a small Python web app** that runs reports against a travel-agency database.

> Team project for the *Databases* course (Dept. of Informatics & Telecommunications, University of Athens, Spring 2023), by Giorgos Fragkakis and Fotios Iasonas Oikonomopoulos.

## Part 1: ER model & schema ([`schema/`](schema))

The schema was designed in MySQL Workbench from the assignment's requirements and forward-engineered to MySQL. It has **18 tables** with primary and foreign keys:

- **Organization:** `main_agency`, `branch_store`, `employee`, and employee specializations (`administrative_officers`, `tour_guides`, `drivers`, `head_of_informatics`)
- **Products:** `package`, `trip`, `destination`, `sights`, `events`, `tour`, `offer`
- **Customers:** `traveller`, `reservation`
- **Many-to-many links:** `trip_has_destination`, `offer_has_reservation`

Design decisions:
- Employee roles are modelled as **specialization tables** sharing the employee key, rather than a single wide table.
- **Trip ↔ destination** and **offer ↔ reservation** are many-to-many: one trip visits several destinations, and one reservation can combine several offers.
- Reservations and events are separate entities. A traveller can make many reservations.
- Each branch's manager is stored as the manager's employee number on the branch, not as a separate entity.

Files: [`schema.sql`](schema/schema.sql) (DDL) · [`er-model.mwb`](schema/er-model.mwb) (open with MySQL Workbench to see the ER diagram)

## Part 2: Analytical SQL ([`queries/`](queries/analytical_queries.sql))

Ten report queries over the course-provided `travel_agency` database. They use multi-table joins, `GROUP BY`/`HAVING`, correlated and nested subqueries, `UNION` and `NOT IN`:

| # | Question answered | Techniques |
|---|---|---|
| 1 | Guides who led tours to attractions in Germany | 4-table join, `DISTINCT` |
| 2 | Guides who led more than 3 trips in 2019 | `GROUP BY` + `HAVING` |
| 3 | Number of employees per branch | aggregation |
| 4 | Reservations per Paris trip package in 2021 | `IN` subquery |
| 5 | Guides who guided in exactly one language | `COUNT(DISTINCT)` in `HAVING` |
| 6 | Did any 2020 offer receive zero reservations? | `UNION` of two aggregates |
| 7 | Male travellers aged 40+ who booked more than 3 trip packages | join + `HAVING` |
| 8 | English-speaking guides and the attractions they guided in English | many-to-many joins |
| 9 | Country with the most trip packages | aggregate of an aggregate (`MAX` over a derived table) |
| 10 | Trip packages that visit **every** destination in Ireland | relational division with `NOT IN` |

## Part 2: Web app ([`app/`](app))

A Python web app ([Bottle](https://bottlepy.org/) + [PyMySQL](https://github.com/PyMySQL/PyMySQL)) that runs parameterized reports and renders them as HTML tables:

| Endpoint | Report |
|---|---|
| `/findTrips?x=<branch>&a=<from>&b=<to>` | Trips of a branch in a date range: price, capacity, reservations, empty seats and assigned guides |
| `/findRevenue?x=ASC\|DESC` | Per-branch reservations, total income, staff count and total salaries, sorted by income |
| `/bestClient?x=BEST` | The traveller(s) who spent the most, with the countries, cities and attractions they visited |

User input is passed to the database as **query parameters** (not string formatting), so it is escaped by the driver.

```bash
pip install -r requirements.txt
cp app/settings.example.py app/settings.py     # fill in your MySQL credentials
cd app && python website.py                     # http://localhost:8080
```

The app expects the course-provided `travel_agency` database, which is not included in this repository.

**Tech:** MySQL · SQL · MySQL Workbench (ER modelling) · Python · Bottle · PyMySQL

## Authors

- **Giorgos Fragkakis** · [GitHub](https://github.com/fragk17)
- **Fotios Iasonas Oikonomopoulos** · [GitHub](https://github.com/sdi2100125)

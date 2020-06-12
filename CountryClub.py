

#<markdown>
/* QUESTIONS
/* Q1: Some of the facilities charge a fee to members, but some do not.
Write a SQL query to produce a list of the names of the facilities that do. */
#<codecell>
SELECT name
FROM `Facilities`
WHERE membercost >0
#<markdown>
/* Q2: How many facilities do not charge a fee to members? */
#<codecell>
SELECT COUNT(name)
FROM `Facilities`
WHERE membercost = 0
#<markdown>
/* Q3: Write an SQL query to show a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost.
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */
#<codecell>
SELECT facid, name, membercost, monthlymaintenance
FROM Facilities
WHERE membercost > (monthlymaintenance*0.20)
#<markdown>
/* Q4: Write an SQL query to retrieve the details of facilities with ID 1 and 5.
Try writing the query without using the OR operator. */
#<codecell>

CASE facid
WHEN 1 THEN 1
WHEN 2 THEN 2
END
FROM Facilities

#<markdown>
/* Q5: Produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100. Return the name and monthly maintenance of the facilities
in question. */

#<codecell>
SELECT name, monthlymaintenance,
CASE
	WHEN monthlymaintenance < 100 THEN 'cheap'
	WHEN monthlymaintenance > 100 THEN 'expensive'
	END AS CostType
FROM Facilities

#<markdown>
/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Try not to use the LIMIT clause for your solution. */

#<codecell>
SELECT firstname, surname
FROM `Members`
WHERE YEAR(joindate) >= 2012 AND MONTH(joindate) >= 9 AND DAY(joindate) >= 25;

#<markdown>
/* Q7: Produce a list of all members who have used a tennis court.
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */

#<codecell>
SELECT DISTINCT CONCAT(m.firstname,' ', m.surname,' ', f.name )
FROM Bookings AS b
LEFT JOIN Facilities AS f
ON b.facid = f.facid
LEFT JOIN Members AS m
ON b.memid = m.memid
WHERE f.name LIKE 'Tennis Court%'
ORDER BY m.surname

#<markdown>
/* Q8: Produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30. Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

#<codecell>
SELECT f.name AS Facility, CONCAT(m.firstname, ' ', m.surname) AS Name, CONCAT(f.membercost,'/', f.guestcost) AS cost
	FROM Bookings AS b
	INNER JOIN Facilities AS f
	ON b.facid= f.facid
	INNER JOIN Members AS m
     ON b.memid = m.memid WHERE b.starttime LIKE '2012-09-14%' AND (f.membercost > 30 OR f.guestcost > 30)
GROUP BY Cost DESC


#<markdown>
/* Q9: This time, produce the same result as in Q8, but using a subquery. */

#<codecell>
SELECT * FROM
(SELECT f.name AS Facility, CONCAT(m.firstname, ' ', m.surname) AS Name, f.membercost AS Cost
	FROM Bookings AS b
	INNER JOIN Facilities AS f
	ON b.facid = f.facid
	INNER JOIN Members AS m
     ON b.memid = m.memid WHERE b.starttime LIKE '2012-09-14%'
UNION
SELECT f.name AS Facility, CONCAT(m.firstname, ' ', m.surname) AS Name, f.guestcost AS Cost
	FROM Bookings AS b
	INNER JOIN Facilities AS f
	ON b.facid = f.facid
	INNER JOIN Members AS m
     ON b.memid = m.memid
             WHERE b.starttime LIKE '2012-09-14%') AS df
WHERE df.Cost > 30
GROUP BY df.Cost DESC;
#<markdown>____________________________________________________________________
/* PART 2: SQLite

Export the country club data from PHPMyAdmin, and connect to a local SQLite instance from Jupyter notebook
for the following questions.
#<codecell>____________________________________________________________________
import pandas as pd
import sqlite3
path = 'data/'
file = 'cc.db'
def query(query, file, path=''):
	"""Simple sqlite query function that returns the SQL query as a Pandas DataFrame"""
	with sqlite3.connect(path+file) as connection:
		cursor = connection.cursor()
		query = cursor.execute(query)
		return pd.DataFrame(query)
#<markdown>____________________________________________________________________
QUESTIONS:
/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */
#<codecell>____________________________________________________________________
df = query(("""
SELECT facility, SUM(cost) FROM (
	SELECT f.name AS facility, SUM(f.membercost) AS cost
	FROM Facilities AS f
	INNER JOIN Bookings AS b
	ON b.facid = f.facid
    WHERE b.memid != 0
	GROUP BY facility
UNION ALL
	SELECT f.name AS facility, SUM(f.guestcost) AS cost
	FROM Facilities AS f
	INNER JOIN Bookings AS b
	ON b.facid = f.facid
    WHERE b.memid = 0
	GROUP BY facility) as db
WHERE cost < 1000
GROUP BY facility
ORDER BY cost DESC;
"""),file, path=path)
df.columns = ['Facility', 'Revenue']
df

#<markdown>____________________________________________________________________
/* Q11: Produce a report of members and who recommended them in alphabetic surname,firstname order */
#<codecell>____________________________________________________________________
df = query("""
SELECT m.surname, m.firstname, (r.surname || ' ' || r.firstname)
FROM Members AS m
LEFT JOIN Members AS r
ON r.recommendedby = m.memid
ORDER BY m.surname, m.firstname;
""", file, path=path)
df.columns = ['LastName', 'FirstName', 'RecommendedBy']
df
#<markdown>____________________________________________________________________
/* Q12: Find the facilities with their usage by member, but not guests */


/* Q13: Find the facilities usage by month, but not guests */

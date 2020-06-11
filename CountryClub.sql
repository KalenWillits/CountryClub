


/* QUESTIONS
/* Q1: Some of the facilities charge a fee to members, but some do not.
Write a SQL query to produce a list of the names of the facilities that do. */

SELECT name
FROM `Facilities`
WHERE membercost >0

/* Q2: How many facilities do not charge a fee to members? */

SELECT COUNT(name)
FROM `Facilities`
WHERE membercost = 0

/* Q3: Write an SQL query to show a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost.
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */
SELECT facid, name, membercost, monthlymaintenance
FROM Facilities
WHERE membercost > (monthlymaintenance*0.20)

/* Q4: Write an SQL query to retrieve the details of facilities with ID 1 and 5.
Try writing the query without using the OR operator. */

CASE facid
WHEN 1 THEN 1
WHEN 2 THEN 2
END
FROM Facilities


/* Q5: Produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100. Return the name and monthly maintenance of the facilities
in question. */

SELECT name, monthlymaintenance,
CASE
	WHEN monthlymaintenance < 100 THEN 'cheap'
	WHEN monthlymaintenance > 100 THEN 'expensive'
	END AS CostType
FROM Facilities


/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Try not to use the LIMIT clause for your solution. */

SELECT firstname, surname
FROM `Members`
WHERE YEAR(joindate) >= 2012 AND MONTH(joindate) >= 9 AND DAY(joindate) >= 25;



/* Q7: Produce a list of all members who have used a tennis court.
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */


SELECT DISTINCT CONCAT(m.firstname,' ', m.surname,' ', f.name )
FROM Bookings AS b
LEFT JOIN Facilities AS f
ON b.facid = f.facid
LEFT JOIN Members AS m
ON b.memid = m.memid
WHERE f.name LIKE 'Tennis Court%'
ORDER BY m.surname


/* Q8: Produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30. Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

SELECT DISTINCT f.name AS facility, CONCAT(m.firstname, ' ', m.surname) AS name, CONCAT(f.membercost,'/', f.guestcost) AS cost
FROM Bookings AS b
INNER JOIN Facilities AS f
ON b.facid = f.facid
INNER JOIN Members AS m
ON b.memid = m.memid
WHERE b.starttime like '2012-09-14%' AND (f.guestcost > 30 OR f.membercost > 30)
ORDER BY cost DESC;


/* Q9: This time, produce the same result as in Q8, but using a subquery. */

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

/* PART 2: SQLite

Export the country club data from PHPMyAdmin, and connect to a local SQLite instance from Jupyter notebook
for the following questions.

QUESTIONS:
/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */

/* Q11: Produce a report of members and who recommended them in alphabetic surname,firstname order */


/* Q12: Find the facilities with their usage by member, but not guests */


/* Q13: Find the facilities usage by month, but not guests */

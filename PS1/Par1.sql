-- List, for every boat, the number of times it has been reserved, excluding those boats that have never been reserved (list the id and the name).
SELECT b.bid, b.bname, COUNT(*) as nReserved
FROM boats b, reserves r
WHERE b.bid = r.bid
GROUP BY b.bid;

-- List those sailors who have reserved every red boat (list the id and the name).
SELECT s.sid, s.sname
FROM sailors s
WHERE NOT EXISTS 
    (SELECT * FROM boats b
    WHERE b.color = 'red' AND NOT EXISTS 
        (SELECT * FROM reserves R
        WHERE S.sid = R.sid AND B.bid = R.bid));

-- List those sailors who have reserved only red boats.
SELECT DISTINCT s.sname, s.sid 
FROM sailors s, reserves r, boats b
WHERE s.sid = r.sid AND r.bid = b.bid AND b.color = 'red' AND s.sid NOT IN
(SELECT s.sid 
FROM sailors s, boats b, reserves r
WHERE s.sid = r.sid AND r.bid = b.bid AND b.color !='red');

-- For which boat are there the most reservations?
SELECT b.bid, b.bname
FROM boats b, reserves r
WHERE b.bid = r.bid
GROUP BY b.bid
ORDER BY COUNT(b.bid) DESC LIMIT 1;

-- Select all sailors who have never reserved a red boat.
SELECT DISTINCT s.sid, s.sname
FROM sailors s, boats b, reserves r 
WHERE s.sid = r.sid AND r.bid AND b.bid AND s.sid NOT IN
(SELECT s.sid 
FROM sailors s, reserves r, boats b
WHERE s.sid = r.sid AND r.bid = b.bid AND b.color = 'red')
UNION
SELECT s.sid, s.sname
FROM sailors s
WHERE s.sid NOT IN
(SELECT r.sid FROM reserves r);

-- Find the average age of sailors with a rating of 10.
SELECT AVG(s.age) as AvgAge_10RateSailors
FROM sailors s
WHERE s.rating = 10;

-- For each rating, find the name and id of the youngest sailor.
SELECT s.sid, s.sname, s.rating, MIN(s.age) as Age
FROM sailors s 
GROUP BY s.rating;

-- Select, for each boat, the sailor who made the highest number of reservations for that boat.
WITH reserveCounts AS (
     SELECT bid, sid, COUNT(*) res_count
     FROM boats
     JOIN reserves USING (bid)
     GROUP BY bid, sid)
SELECT bid, sid, sname, res_count
FROM 
    (SELECT bid, MAX(res_count) res_count
     FROM reserveCounts
     GROUP BY bid)_
JOIN reserveCounts USING (bid, res_count)
JOIN sailors USING (sid);



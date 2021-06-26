# aristotle°
A free, open-source learning management system (LMS) build on Django and deployed on Heroku.

## Dev Notes
* 6/19/2021 (v.0.1.1): Patch refining existing features:
  * Used CloudFlare proxy for HTTPS protocol to get website working on secure browsers (still unsafe due to half of protocol being unsecure)
  * Clicking on students on the Students page for teachers now shows a tabular summary of the student assignments.
  * Assignment page for students and teachers has been switched from a simple list of assignment names to a tabular summary of grades and submissions.
  * UI improvements such as clearer course selection and render distinctions between finished and unfinished / graded and ungraded assignments.
  * Bug fixes.
* 6/13/2021 (v0.1.0): Skeleton release. Many bugs and incomplete pages. Key features include:
  * Creating courses as a teacher and joining them as a student using the course UUID.
  * Creating assignments as a teacher and grading student submissions.
  * Submitting text submissions to assignments as a student and viewing the grades once available.

## Priority Backlog (Next Patch)
* Use an iframe to display readme on home pages
* Add "report an issue" button
* Add social media sharing tags
* Cumulative grade displaying
* Email notifications for assignment updates
* Cookie 

## Backlog
* File uploads for assignments and submissions
* Status tags instead of unread/read formatting for assignments
* Non-assignment pages
* Actual SSL certification

## Issues/bugs
Submit issues on the [issues page](https://github.com/dabslee/aristotle/issues)

## Contribute
Feel free to contribute by submitting pull requests!

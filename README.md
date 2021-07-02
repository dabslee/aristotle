# aristotle°
A free, open-source learning management system (LMS) build on Django and deployed on Heroku.

## Dev Notes
* 7/2/2021 (v0.1.2): Minor UI additions patch:
  * Now use an iframe to display GitHub readme on home pages
  * Added "report an issue" button to page footer
  * Added social media sharing buttons to page footer
  * Now display cumulative grade on student assignments overview
  * Added delete button for assignments on assignment details page
* 6/19/2021 (v0.1.1): Patch refining existing features:
  * Used CloudFlare proxy for HTTPS protocol to get website working on secure browsers (still unsafe due to half of protocol being unsecure)
  * Clicking on students on the Students page for teachers now shows a tabular summary of the student assignments.
  * Assignment page for students and teachers has been switched from a simple list of assignment names to a tabular summary of grades and submissions.
  * UI improvements such as clearer course selection and render distinctions between finished and unfinished / graded and ungraded assignments.
  * Bug fixes.
* 6/13/2021 (v0.1.0): Skeleton release. Many bugs and incomplete pages. Key features include:
  * Creating courses as a teacher and joining them as a student using the course UUID.
  * Creating assignments as a teacher and grading student submissions.
  * Submitting text submissions to assignments as a student and viewing the grades once available.

## Priority Backlog (Next Patch - v0.1.3)
- [ ] Show cumulative grade for students on teacher views
- [ ] "Unsaved changes" confirmation dialogue before leaving form pages
- [ ] Show assignment details on new submission form
- [ ] File attachment uploading for assignments and submissions

## Backlog
* Email notifications for assignment updates
* Status tags instead of unread/read formatting for assignments
* Feature voting
* Non-assignment pages
* Full SSL certification
* Switch session course tracking method from cookies to request kwargs
* Render readme iframe as formatted HTML
* A breadcrumbs navigation bar
* Modules/groupings for assignments
* Editable table views
* Duplicate option for assignments

## Issues/bugs
If there are urgent bugs, [email me](mailto:brandon.sangmin.lee@gmail.com). Otherwise, for nonurgent bugs and issues, make a submission on the [issues page](https://github.com/dabslee/aristotle/issues).

## Contribute
Feel free to contribute by submitting pull requests!

# Sports Sports Sports ⚽

**`How I Built a Match Ranking Algorithm And Sports Website Backend`**
   </br>

## 📜 The Why
This project is dear to my heart - it is the first code I’ve ever written, just after finishing the Python course of the University of Helsinki. I learned Python because it was recommended to me as a flexible language that can be useful in many different situations. Once the course was over, it was time to start building something for real, and I love sports and stats. I wanted to understand how APIs work, so this was the perfect project to tackle.

   </br>

## 📜 The What
The Morning Kickoff is the backend of a sports website, written in Python. The backend takes its data from sportsdb’s API, and uses Postgres as a database. I’ve also built an API that has a few endpoints, such as the ability to query for teams in a league, or matches for a team. 

The part I like the most is the match ranking algorithm, which if we’re fair, is simply a formula with a few coefficients to find the most interesting games on any given day, in case you need a recommendation. I built this for my friends who used to ask me what to watch, and they love it.

   </br>

## 📜 The How
This project was built in vanilla Python, and its first iteration sent emails with the games. But email HTML is a pain, so I kept it simple. As I learned about frameworks and APIs, I knew I wanted to try and build one, so I rebuilt everything with Django. 

The project itself runs on two containers, one for the code, and one with the database. There is also a third container that updates the database daily and runs as a cron job.

   </br>

## 📜 The Challenges
This was my first project ever, and safe to say that everything was a challenge. I remember a specific issue with creating a virtual environment that took me half a day to figure out. I remember another issue with connecting the containers that took me a while to get right. The biggest challenge was perhaps that my ideas outpaced my skills by quite the margin.

   </br>

## 📜 The Lessons
Python is nice to learn in a class, but this is where I really started to feel the power at my fingertips. Automate everything. Seeing code run and work is such a satisfying feeling. I really learned Python doing this, but I also learned about APIs, containers, databases, cron jobs. I also learned that following my curiosity is a great way to go about acquiring new skills. I’m really happy that this set the stage, code-wise.

   </br>


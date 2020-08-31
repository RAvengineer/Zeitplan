# Zeitplan
A Timetable management web app using Google Calendar API for VITians

### Setup
#### Create an Environment (Optional :fast_forward: )
```bash
conda create --name zeitplan python=3.7
```
#### Activate the Environment (Optional :fast_forward: )
```bash
conda activate zeitplan
```
Here, I have shown Conda as the environment management system. You may use other management system.
#### Clone the repo
```bash
git clone https://github.com/RAvengineer/Zeitplan.git
```
#### Install required packages
```bash
cd Zeitplan/
pip install -r requirements.txt
```
---
### Hosting
```bash
cd Zeitplan/
ls
> app.py  README.md  requirements.txt  Utilities  Zeitplan
```
:point_up_2: Check you are in correct directory.

#### Set up the environment variables
For Linux and Mac users,
```bash
set FLASK_APP=app.py
```
For Windows users,
```bash
export FLASK_APP=app.py
```
##### If you are hosting locally, then an extra environment needs to be set up :eyes:
For Linux and Mac users,
```bash
set ZEITPLAN_LOCALHOST=1
```
For Windows users,
```bash
export ZEITPLAN_LOCALHOST=1
```
#### Finally, host it :sweat_smile:
```bash
flask run
```

The application is built on Python Flask.
Database is deployed to AWS RDS, so no need to install or initialize database.

1. Install required dependencies list in requirements.txt, run "pip install -r requirements". Better to have python virtual environment.
2. Go to directory obs-v2, run "python run.py".
3. The website is running on http://127.0.0.1:5000/, open your browser and paste this URL to visit.

if installation failed, please visit http://ec2-54-152-233-37.compute-1.amazonaws.com/, the deployed version which we preferred to be tested.

**** Implemented functions ****
1. Login (username: obs, password: obs, security question: are u rich?, security answer: yes)
2. check account activities
3. transfer funds
4. pay bill - add bills
5. deposit
6. setting - account setting
7. customer service - chat online (blue float icon on bottom-right)
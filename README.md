# Installation Guide
1. Download binary and install node in windows system (https://nodejs.org/en/download/)
2. Download binary and install python 3.x.x in windows system (https://www.python.org/downloads/)
3. Go inside screenshare-server folder and run command from command prompt `npm install` and wait until it is finished.
4. Next run another command `node server.js` - if everything is ok, you should be able to see output **listening on :3000**
5. Now go to screenshare/communication folder and run command `python ClientInterface.py` - if all setup is ok, then you should be able to see output **Connected**
6. Now go to Chrome browser and open URL localhost:3000/ui/index.html

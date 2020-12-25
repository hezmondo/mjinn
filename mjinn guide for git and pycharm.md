# Git and PyChram notes (mainly for Windows) updated 16 Dec 2020 for mysql 8.0.21, Python 3.7.5

### Development PC:

**Download and install git for Windows**, accepting all the default options.

Make sure you have already created an empty folder **C:\Flask\samjinn**.

Type git into the Windows search bar and right click on `Git bash` and either pin to taskbar or set as desktop shortcut.

Start git bash and then execute these commands:

`git --version` (to check it is working)

`git config --global user.name "yourusername"` (to connect git to your github username - use hezmondo if you are not a github user)

`git config --global user.name` (to check you are connected to the correct username)

`git config --global email.address "youremailaddress"` (to connect git to your github emailaddress - hez use hez emailaddress)

`git config --global email.address` (to check you are connected to the correct email address)

`cd C:\Flask\samjinn`

`git clone https://github.com/hezmondo/mjinn .`  (the dot persuades git to clone the repo into the folder you are already in)

This will clone the Master branch of minn into C:\Flask\samjinn along with the git connections to our Github repo


**How to switch branches using git bash:**

`git branch -a` will list all available branches and show you connected to the master branch

`git branch` will show just the brach you are connected to

`git checkout samjinn` switches you to the samjinn branch

`git branch -a` or `git branch` will now show you connected to the samjinn branch

Learn more about the specific role of checkout here https://www.atlassian.com/git/tutorials/undoing-changes


**Use git bash to push local a PC project to a githup repo:**

An example is a new project C:/Flask/micro.  Set up a suitably named repo at github, say mjinn,
but do not initialise it at this stage by creating a readme.

Start git bash and then execute these commands:

	cd C:/Flask
	cd micro
	git init
	git add .
	git commit -m "First commit"
	git remote add origin https://github.com/hezmondo/mjinn.git
	git remote -v (to check you are connected)
	git push origin master
	history (shows you bash history)
	exit (to retain bash history)

If you find that your github repo contains folders which you do not wish to host publicly, but which you need locally:

Start git bash and then execute these commands:

	cd C:/Flask
	cd micro
	
example 1 removes from git the .idea directory created by Pycharm:

	mv .idea ../.idea_backup
	rm .idea # in case you forgot to close your IDE
	git rm -r .idea
	git commit -m "Remove .idea from repo"
	mv ../.idea_backup .idea 

example 2 removes from git the __pycache__ directory, which I had trouble removing:

	git rm -r --cached __pycache__
	git commit -m "Remove __pycache__ from repo"
	git push origin master

example 3 removes from git the **logs** directory, which I also had trouble removing:

	git rm -r --cached logs
	git commit -m "Remove logs directory"
	git push origin master


**Download and install Pycharm**  choose the free community edition, such as `pycharm-community-2019.2.exe from JetBrains`

Open Pycharm (if you have already been using Pycharm, close any previous project) and open C:\Flask\mjinn as a new project.

If you wish to switch branches using PyCharm:

Click the `VCS` tab at the top 

then select `Git` 

then `Pull` 

then switch from `origin/master` to `origin/samjinn` by ticking the relevant box

then click the `Pull` button.

You are now connected to the samjinn branch and all subsequent pushes and pulls will link to that branch.

**How to count lines of code in project**  Open powershell window in Code folder and try this:

    dir -Recurse *.py | Get-Content | Measure-Object -Line
    dir -Recurse *.html | Get-Content | Measure-Object -Line
    dir -Recurse *.css | Get-Content | Measure-Object -Line
    dir -Recurse *.txt | Get-Content | Measure-Object -Line

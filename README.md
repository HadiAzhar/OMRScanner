**What this project entails**

This project is done to create a scanner for OMR paper and do so using Kivy platform and python language. How to run  and how to implement the package is explained in details

---

## Instruction on installing the package

I would assume that you are aware of how to use anaconda or any plarform to utilize python and packages. You’ll start by creating new environment that uses the python==2.7.15

1. (if using anaconda3 like me) Open the cmd panel and run "conda create -n kivyproject python==2.7.15" and press Y if prompted
2. after creating the environment change the directory to where the file is and run the command "pip install requirements.txt". This will install all the required packages according to what works in my laptop.   
3.  After everything has been installed, create the buildozer.init file by using cmd command "buildozer init"
4.  The buildozer init will allow you to configure the specification of the android apk that you would like to create including the name, sdk and permissions etc etc.
5. After making your change, type "buildozer android debug" to create the APK file. you may wanna wait for awhile until the APK and all the required files are successfully converted. if you are familiar with android developer tools and developer mode. you can 'create' and  'push' the app straight to your phone when connected via usb debugging by the command "buildozer android debug deploy" and if you wish to view the logcat just add "logcat" eg. "buildozer android debug deploy logcat"
6. If there are any problem please do contact me for further clarification.

---

## Clone a repository

Use these steps to clone from SourceTree, our client for using the repository command-line free. Cloning allows you to work on your files locally. If you don't yet have SourceTree, [download and install first](https://www.sourcetreeapp.com/). If you prefer to clone from the command line, see [Clone a repository](https://confluence.atlassian.com/x/4whODQ).

1. You’ll see the clone button under the **Source** heading. Click that button.
2. Now click **Check out in SourceTree**. You may need to create a SourceTree account or log in.
3. When you see the **Clone New** dialog in SourceTree, update the destination path and name if you’d like to and then click **Clone**.
4. Open the directory you just created to see your repository’s files.

Now that you're more familiar with your Bitbucket repository, go ahead and add a new file locally. You can [push your change back to Bitbucket with SourceTree](https://confluence.atlassian.com/x/iqyBMg), or you can [add, commit,](https://confluence.atlassian.com/x/8QhODQ) and [push from the command line](https://confluence.atlassian.com/x/NQ0zDQ).

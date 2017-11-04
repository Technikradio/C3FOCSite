# Contributing guidelines
Below you will find some hints on how to make our and especially you live easier.
## Issues
### Bugs
If you decide to submit the lastest and greatest bug you've found that's nice of you.
But please make sure to follow these instructions:
 * In case you found the bug using your own installation:
    - Make sure that you're using python >= 3.6.1
    - Make sure that all required PyPy packages are installed and up to date
    - Make sure that your database engine is configured correctly.
    - Make sure that you have the latest version of the repository installed
 * In case you're not following the master branch please do not submit issues regarding
   "Form X contains field Y but its not used by handler Z." Chances are good that these
   issues will be fixed within the next few commits.
If you think that you checked the above things feel free to continue using the following
instructions:
 1. Please use a descriptive label for the issue.
 2. Please provide a way to reproduce the bug inside the comments
 3. If you're using your own installation and are nice person you provide some information
    about your environment. You don't have to since it may reveal some personal stuff but
    it could help a lot to track down the issue. I you decide to provide some information
    simply paste the output of the following commands into the command section:
    ```shell
    $ uname -v
    $ python3 --version
    $ pip3 freeze
    $ pip3 check
    ``` 
 4. Please label them with 'Bug'.
 ### Enhancements
 In case you have a super cool idea on how to improve the C3FOC experience but struggle to
 create your own extensions let us know via an issue. But please follow the following instructions:
  1. Use a descriptive headline
  2. Describe what should be added and especially why. Keep in mind that we won't implement
     anything requiring JavaScript.
  3. Label your issue with enhancement.

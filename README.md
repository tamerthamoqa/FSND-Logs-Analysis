# FSND-Logs-Analysis
This is a repository for the "Logs Analysis" udacity project which is the third project required for completing the Udacity Full Stack Web Developer Nanodegree program.

The main purpose of this project is to let students understand the fundamentals of SQL by building an internal reporting tool that queries a PostgreSQL&trade; database containing over a million rows that contains a newspaper's newspaper articles, article authors, and the web server log for the newspaper site to answer three questions:

1. What are the most popular three articles of all time?  
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The database includes three tables:
* authors table
* articles table
* log table

# Contents
* newsdata.zip - contains the compressed data from the PostgreSQL database.
* log_analysis.py - contains the code for the reporting tool.
* database-table-schema.txt - contains the schema of the PostgreSQL database.
* output_screenshot.PNG - an image of the expected output of running the reporting tool.
* Vagrantfile - contains necessary Virtual Machine configurations for the project from this this udacity [repository](https://github.com/udacity/fullstack-nanodegree-vm).

# Requirements
### Running on the pre-configured virtual machine:
[Vagrant](https://www.vagrantup.com/) and [Virtualbox](https://www.virtualbox.org/) to be installed.

# How to run
1. Unzip the _newsdata.zip_ file, the uncompressed file is a 120MB SQL file, keep the resulting file in the directory of the project (with Vagrantfile).

2. Open a terminal and cd to the project directory and run the command ```vagrant up```, this will build the virtual machine and may take some time.

3. After the virtual machine is set up, log into it with the command ```vagrant ssh``` and enter your password (default password is: vagrant).

4. Inside the virtual machine cd to the /vagrant/ directory ```cd /vagrant/``` and do the ```ls``` command to make sure the files in the virtual machine exist on the project directory on your actual PC.

5. Run the following command (only works inside the virtual machine):
```python log_analysis.py```

# Expected output
![Alt text](output_screenshot.PNG "expected output")

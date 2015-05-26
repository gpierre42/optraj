sudo apt-get update
sudo apt-get -y install apache2
sudo apt-get -y install php5
sudo apt-get -y install php5-curl
sudo apt-get -y install curl
sudo apt-get -y install python2.7
sudo apt-get -y install python-pip
sudo apt-get -y install python-dev
sudo apt-get -y install libgraphviz-dev
sudo pip install Flask
sudo pip install pymysql
sudo pip install pp
sudo pip install pygraphviz
sudo pip install deap
sudo pip install isoweek
sudo pip install nose-cov
sudo pip install pygeocoder
sudo apt-get -y install mysql-client
sudo /etc/init.d/apache2 restart
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password password password'
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password_again password password'
sudo apt-get -y install mysql-server-5.5
sudo apt-get -y install python-mock python-nose python-coverage pylint jenkins
java -jar /vagrant/jenkins-cli.jar -s http://localhost:8080 create-job OPTRAJTest < /vagrant/jenkins/OPTRAJTest.xml

cd /vagrant
cd optraj.istic.univ-rennes1.fr/
#python2.7 src/index.py &
sudo rm -f /var/www/index.html
sudo ln -s /vagrant/optraj.istic.univ-rennes1.fr/GUI/htdocs/ /var/www/optraj
sudo cp /vagrant/optraj.conf /etc/apache2/sites-available/
sudo cp /vagrant/my.cnf /etc/mysql/
sudo a2ensite optraj.conf
sudo service apache2 reload
sudo service mysql restart
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/createclient.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/createtables.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadcars.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadconsumers.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadcraft.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadqualifs.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadpositions.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadworkers.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadsites.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadpickups.sql
java -jar /vagrant/jenkins-cli.jar -s http://localhost:8080 create-job OPTRAJTest < /vagrant/jenkins/OPTRAJTest.xml
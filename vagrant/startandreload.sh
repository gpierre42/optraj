mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/createtables.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadcars.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadconsumers.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadcraft.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadqualifs.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadpositions.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadworkers.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadsites.sql
mysql  --user=root -ppassword --local-infile < /vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/loadpickups.sql
cd /vagrant
sh killIndex.sh
sh killIndex.sh
sh killIndex.sh
cd optraj.istic.univ-rennes1.fr/
python src/index.py &

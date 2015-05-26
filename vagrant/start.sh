cd /vagrant
#sh killIndex.sh
#sh killIndex.sh
#sh killIndex.sh
echo "anciens process pythons:"
ps -e | grep python
echo "kill des process"
pkill python
echo "process pythons en cours:"
ps -e | grep python
echo "lancement du serveur"
cd optraj.istic.univ-rennes1.fr/
python src/index.py &

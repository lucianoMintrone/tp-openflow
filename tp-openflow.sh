SWITCHES_COUNT=$1
export SWITCHES_COUNT
sudo mn --custom topo-linear.py --topo mytopo --test pingall
import pysmile_license
import pysmile

net = pysmile.Network()
net.read_file("data/red_bayesiana.xdsl")
h = net.get_first_node()
print(net.get_node_value(h))
net.set_evidence("H", "Alto")
net.set_evidence("W", "Armado")
net.set_evidence("OW", "Armado")
net.set_evidence("HN", "SeOye")
net.set_evidence("NE", "Si")
net.set_evidence("PW", "Si")
net.set_evidence("PH", "Si")
net.update_beliefs()
beliefs = net.get_node_value("St_1")
for i in range(0, len(beliefs)):
  print(net.get_outcome_id("St_1", i) + ": " + str(beliefs[i]))


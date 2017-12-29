import os
import matplotlib.pyplot as plt
import numpy as np
from scapy.all import *

def pcap2line(file):
	pcap = PcapReader(file)
	statistic = []
	count = 0
	while True:
		p = pcap.read_packet()
		tmp = []
		if p:
			tmp.append(p.time)
			try:
				tmp.append(p.len)
			except Exception as e:
				tmp.append(-1)
			statistic.append(tmp)
			count += 1
		else:
			break
	timeseg = (statistic[-1][0]-statistic[0][0])/100.0
	print timeseg
	segments = [(statistic[0][0]+i*timeseg) for i in range(100)] #x array
	cumulate = [0 for i in range(100)]
	for i in range(count):
		cumulate[int((statistic[i][0] - statistic[0][0])/timeseg)] += 1
	print cumulate
	plt.figure()
	plt.plot(segments,cumulate)
	plt.show()
	
	# for i in range(count):



if __name__ == '__main__':
	pcap2line("/Users/chenzhipeng/Documents/Courses/AdvancedNetwork/SuriWeb/app/pcap/1_42.pcap")
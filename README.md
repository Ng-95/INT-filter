# INT-filter: INT-filter: Mitigating State Collection Overhead for High-Resolution In-band Network Telemetry

To safeguard large-scale modern data center networks, fine-grained, network-wide visibility is of extremely crucial importance, which is able to accommodate heterogeneous applications. 
One of the killer applications of P4 is In-band Network Telemetry (INT), which makes the device's internal state such as queuing latency and queue depth obtainable for probe or data packets as they pass through the data plane pipeline.
More importantly, for network applications such as load balancing, fault localization and management automation, these switch status information such as queue depth is endowed with increasing great insight.
These information, however, needs to be uploaded to the controller through the southbound interface for analysis, the bandwidth of which is not limitless.
According to our measurement, the FatTree topology with 1 Gbps bandwidth can accommodate no more than 8 pods and 128 hosts when HULA is used for network-wide telemetry with a resolution of 10 ms.
In addition, the southbound interface is also at the service of other functions such as Packet-In messages and new flow entries, which need sufficient bandwidth as well.

INT, a chip-level primitive, simply gives a definition of the interaction between the device-internal states and the incoming packets with the aim of monitoring.  
Further orchestration on INT is essential for network-wide telemetry.
HULA adopts the ToR switches to pour probes into the multi-root topology to achieve measurement coverage. So a link will be repetitively monitored simultaneously by multitudes of probes due to the broadcast mechanism, resulting in significant switching and southbound bandwidth overhead. 
For high-resolution monitoring at mega-scale network topology, the bandwidth waste will become much graver. 	
For surmounting the limitation, INT-path collects the network topology and uses an algorithm based on Euler trail to generate non-overlapped probing paths covering the whole network with a minimum number of paths.
Due to the elimination of a great quantity of redundant probes, INT-path reduces the switch-controller channel bandwidth occupation to some extent.
These methods, however, upload all the detected INT information directly to the controller.
According to our measurement, Hula's upload rate even reached 3.03Tbps under the massive data center FatTree topology, a quite terrible number for the bandwidth occupation of probe packets.
In comparison, the upload rate of INT-path also reached 702Mbps. 

![Image text](https://github.com/Ng-95/INT-filter/blob/master/Experiment%20result/fig3/Architecture.png)

To tackle the above problems, in this work, we propose INT-label, an ultra-lightweight In-band Network-Wide Telemetry architecture. Distinct from previous work, INT-label follows a “probeless” architecture, that is, the INT-label-capable device periodically labels device-internal states onto data packets rather than explicitly introducing probe packets. Specifically, on each outgoing port of the device, the packets will be sampled according to a predefined label interval T and labelled with the instant device-internal states. As a result, INT-label can still achieve network-wide coverage with finegrained telemetry resolution while introducing minor bandwidth overhead. Along the forwarding path consisting of different devices, the same packet will be labelled independently simply according to the local sample decision, that is to say, INT-label is completely stateless without involving any probing path-related dependency. Therefore, there is no need to leverage the SDN controller for conducting centralized path planning. 

To tackle the above-mentioned problems, INT-filter architecture is proposed in this work, which is able to decrease the southbound bandwidth occupation for High-Resolution In-Band Network Telemetry.
Unlike previous work, INT-filter aims to reduce unnecessary uploaded INT information.
Since INT-path can implement network-wide telemetry with a minimum probe packets number, its uploaded INT information volume is already fairly small.
In this case, we propose a INT-path-based prediction mechanism, reducing the southbound interface bandwidth consumption by using prediction rather than uploading true values.
Furthermore, we introduce an ensemble prediction mechanism that uses the first-, second-, and third-order polynomial fitting for prediction, and uploads the least-error method to the controller.
The mechanism requires the extension of 1-bit flag to 2-bit flag to indicate that the prediction is not used and which of the first-, second- and third-order polynomial fitting is adopted.

# Experiment result
Experiment result contains preliminary experimental results data and figures.

## Fig.1
Upload rates under different probe intervals (INT-path vs. HULA).

## Fig.2
Upload rates under different network sizes of FatTree topology.

## Fig.3
The architecture of INT-filter.

## Fig.4
The impact of degree of polynomial fitting on the upload decrease.

## Fig.5
The impact of data plane probe frequency on upload rate.

## Fig.6
The impact of prediction window size on the computational complexity and upload rate.

## Fig.7
The impact of threshold on the computational complexity and upload rate.

# INT-filter
We build an emulation-based network prototype to demonstrate INT-label performance. The hardware configuration is 20*2Ghz CPU and 64GB memory with Ubuntu 16.04 OS. The prototype is based on Mininet and consists of 1 controller, 4 Spine switches, 4 Leaf switches, 4 ToR switches and 8 servers.
The INT_filter include five modules:topology, flow_table, p4_source_code, packet, controller and args.

## topology
Establish a mininet topology and start the packet send&receive process.

### clos.py
First, compile p4 program.
Establish a mininet topology. Here we can control the link bandwidth, delay, maximum queue length, etc.
And initialize the database and start the packet send&receive process.

## flow_table
Initialize the OpenFlow Pipeline of each OVS.

### flow_table_gen.py
Generate the flow table.

### command.sh
Update the flow table.

### flow_table
Include OpenFlow Pipeline.

## p4_source_code
Include p4 source code, implemented SR-based INT function and data plane labelling function of INT-label.

### my_int.p4
Include Headers, Metadatas, parser, deparser and checksum calculator.
SR-based INT function and data plane labelling function are implemented in the program.

### my_int.json
The json file that compiled from my_int.p4 by p4c compiler.

### run.sh
For compiling the my_int.p4.

## packet
Implement send&receive packet on the server.

### send
Send packet.

#### send_int_probe.py
Based on SR and INT-path, each host send probe packet to a host which is not in the same pod.

### send_data.py
Based on SR, server1, server3, server6 and server8 send randomly-generated traffic (packet size = 1kB) to the other servers.

### receive
Receive packet and parse it.

#### parse.py
Extract the INT information.

#### predict.py
Predict the state using historical data.

#### receive_basic.py
Receive packets and parse them using parse.py. And write the latest INT information into the database without filtering.

#### receive_filter.py
Filter the uploaded data and update the historical state database.

## controller 
Implement controller-driven adaptive labelling function and calculate the coverage rate.

### read_redis.py
Read experimental results.

## args
Store global variable of the prediction window size.

# How to run INT-filter
If you installed the dependencies and configured the database successfully, then you can run the system with commands below:

## Base
```
cd topology/
python clos.py
```

You can change bandwidth, max queue size and background traffic rate in clos.py to test INT-filter under different conditions.
If you change the topology, you need to modify packet/send/send.py.
You can view the results of the experiment through controller/read_redis.py.

# HULA
We reproduce the code of HULA.
Its the role of each file and usage are similar to those of INT-label.

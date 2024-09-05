# Smart TV Automatic Content Recognition (ACR) Analysis

This repository is dedicated to the analysis of Automatic Content Recognition (ACR) technology on two popular smart television brands: LG and Samsung. The aim is to delve into how these TVs implement ACR and understand their behavior through experimentation and analysis.

The following paper associated with this repository is published at the IMC 2024:
___
**Watching TV with the Second-Party: A First Look at Automatic Content Recognition Tracking in Smart TVs**<br>
Gianluca Anselmi*, Yash Vekaria*, Alex D’Souza, Patricia Callejo, Anna Maria Mandalari, Zubair Shafiq (*_joint first authors_)<br>
_24th ACM Internet Measurement Conference (IMC), 2024_<br>
Acceptance rate: **21.3%** (54/253)
___

**Code**

`trigger_validation_scripts`: This folder contains scripts for conducting experiments to automatically test different functionalities of the TVs. The primary script, experiment.sh, automates the process of turning on the TV, capturing network traffic for a specified duration, and then turning off the TV. During the experiment, manual interaction may be required to perform specific actions on the TV, such as opening Netflix. This script additionally checks whether the experiment is successful by checking the size of the generated pcap file.

`analysis_scripts`: Here, you'll find scripts designed to extract meaningful insights from the captured network traffic (PCAP files) and comprehend the behavior of the television sets.

**Data**

The collected .pcap files are available at the following Google drive link:
[https://drive.google.com/drive/folders/1cqK2IJ6h-t92XyKy93zZ2NT2NxrXS_Nz?usp=share_link](https://drive.google.com/drive/folders/1cqK2IJ6h-t92XyKy93zZ2NT2NxrXS_Nz?usp=share_link)

**Usage**

To run the experiments, follow these steps:

Navigate to the trigger_validation_scripts directory.
Execute the experiment.sh script with the following parameters:

`./experiment.sh <.txt file of the TV> <time duration of the experiment>`

Replace `<.txt file of the TV>` with either `exp_lg.txt` or `exp_samsung.txt`, depending on the TV brand you want to analyze.
Replace <time duration of the experiment> with the desired duration of the experiment in seconds.

**Citation**

If you find our research or resources helpful, please cite our work as follows:
```
Gianluca Anselmi, Yash Vekaria, Alexander D’Souza, Patricia Callejo, Anna Maria Mandalari, and Zubair Shafiq. 2024. Watching TV with the Second- Party: A First Look at Automatic Content Recognition Tracking in Smart TVs. In Proceedings of the 2024 ACM Internet Measurement Conference (IMC ’24), November 4–6, 2024, Madrid, Spain. ACM, New York, NY, USA, 13 pages. https://doi.org/10.1145/3646547.3689013
```

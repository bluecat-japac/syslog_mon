# SYSLOG MONITORING

## SETUP SYSLOG MONITORING ON BDDS

1.  Download the syslog monitoring package from Nexus.

2.  Go to the directory that contains the package and extract it
    > tar -xzvf syslog_mon_in_dds.tar.gz
    
    then go to the extracted folder
    > cd syslog_mon_in_dds/
###### Run `setup.sh` with the directory that stores syslog_monitoring/ as parameter 
    
   > sh setup.sh /absolute/destination/path
    
   * Note: 
        * Internet connection is required. 
        * If no destination path is specified, syslog_monitoring/ will be copied to /opt/ by default.
    
###### or install manual with the following steps
    
1.  Move syslog_monitoring folder to where you want (example: /opt/)
    > mv syslog_monitoring/ /opt/
   
2.  Install requirements
    > cd /opt/syslog_monitoring/
    
    > pip install wheel && pip install -r requirements.txt

3.  Install mod-python for syslog-ng to recognize python destination
    > apt-get install syslog-ng-mod-python 

4.  Copy `filters.conf` file to `scl` folder
    > mkdir /usr/share/syslog-ng/include/scl/syslog_mon/ && cp filters.conf $_  
    
5.  Export path of the python destination
    
    Open /etc/sysconfig/syslog-ng (create if it doesn't exist) and add this line
    > PYTHONPATH=$PYTHONPATH:/opt/syslog_monitoring/

6.  Create directory to store log
    > mkdir /var/log/mon-app

7.  Disable firewall for the bdds to be able to send SNMP trap
    > PsmClient node set firewall-enable=0
      
8.  Restart syslog-ng service
    > service syslog-ng restart

## CONFIGURE SYSLOG SERVICE TO CORRECT THE HOST NAME OF THIS DNS/DHCP SERVER
1.  Get hostname provided in the init script
2.  Open /usr/share/syslog-ng/include/scl/filter/filters.conf
	
	Add this anywhere
	```
	rewrite r_rewrite_set {
		set("the_hostname_above", value("HOST"));
    };
	```
	Then add
	```
    rewrite(r_rewrite_set); 
    ```

	below the 
	```
    source(local);
    ```
	
	Finally it should be look like this
	```
	   ...
	   rewrite r_rewrite_set {
		set("the_hostname_above", value("HOST"));
    };
    
    # BlueCat log paths
    log {
           source(local);
           rewrite(r_rewrite_set);
           destination(d_fw_log);
           ...
    };
     ```
    
3.  Save file and restart syslog-ng service
    > service syslog-ng restart


## SETUP CONFIG FILE
The file named config.ini contains the information for configuration, which is located at syslog_monitoring/Config/.
1. The SCHEDULER_CONFIG configuration for DNS healthcheck:

    | Keys | Value | Description |
    | --- | --- | --- |
    | interval | 1 | Interval time in minutes |
    | domain | www.google.com | The domain name which is checked by DNS Health Check |
    | vm_host_name | vmname | The name of the host VM |

2. The NTP_CONFIG configuration for NtpClocksUnsynchronized:

    | Keys | Value | Description |
    | --- | --- | --- |
    | interval | 1 | Interval time (in minutes) |
    | threshold | 2000 | The acceptable time gap (in milliseconds) between the bdds and its NTP servers |
    | bdds_server | <ip_address>,<ip_address>,<ip_address> | The list of bdds which is going to be checked time gap | 
    
3. The TCP_LIMIT_EXCEED_CONFIG configuration for TcpConnectionLimitExceeded:

    | Keys | Value | Description |
    | --- | --- | --- |
    | interval | 20 | Interval time (in minutes) before sending clear alarm for tcp connection limit exceed log |

## SNMP CONFIGURATION
1. The file named snmp_config.json, which is located at syslog_monitoring/Config/, contains the configuration for the trap destinations.
	In which: \
	a. For each trap destinations, it is a list of json objects. \
	b. Each object contains the key and value. Please see the example below:

     | Keys | Value Type | Example value |
     | --- | --- | --- |
     |`userName`| string | usm-user |
     |`authKey`| string | <encrypted_password> |
     |`privKey`| string | <encrypted_password> |
     |`authProtocol`| string | SHA |
     |`privProtocol`| string | AES |
     |`transportTarget`| string | <ip_address> |
     |`port`| integer | 162 |

	Note: The userName, authKey, privKey, authProtocol, privProtocol and securityEngineId is the information configured for SNMPv3 in the trap receiver. In which:
		- The authProtocol allows value as SHA or MD5.
		- The privProtocol allows value as DES, AES, AES-196 or AES-256.
		- The authKey and privKey have to be encrypted using snmp_password_process.py. See below "Generate encrypted password" section for more details.
	The transportTarget field is the IPv4 or IPv6 of the SNMP trap receiver.
	The port is the one that SNMP trap receiver is listening on.

2. The EngineID can be edited by administrator in /var/lib/net-snmp/snmpd.conf

3. The log of syslog monitoring application is at /var/log/mon-app
## CONFIG OID FOR EACH LOG TYPE
1. Open file Snmp/map_oid.py and config OID, bcnSyslogMonAlarmCond, bcnSyslogMonAlarmSeverity, bcnSyslogMonKeyPair, bcnSyslogMonAlarmMsg for each type of log
    
    | Log Type | OID |
    | --- | --- |
    | `TestQueryFailed` | 1.3.6.1.4.1.13315.6.1.2.0.1 |
    | `LoadConfigurationFailed` | 1.3.6.1.4.1.13315.6.1.2.0.2 |
    | `TsigBadTime` | 1.3.6.1.4.1.13315.6.1.2.0.3 |
    | `StorageReadOnly` | 1.3.6.1.4.1.13315.6.1.2.0.4 |
    | `ZoneTransferFailed` | 1.3.6.1.4.1.13315.6.1.2.0.5 |
    | `TcpConnectionLimitExceeded` | 1.3.6.1.4.1.13315.6.1.2.0.6 |
    | `LoadZoneFailed` | 1.3.6.1.4.1.13315.6.1.2.0.7 |
    | `NtpClocksUnsynchronized` | 1.3.6.1.4.1.13315.6.1.2.0.8 |
    | `NetworkInterfaceDown` | 1.3.6.1.4.1.13315.6.1.2.0.9 |
    Note: "log_type" is defined in syslog-ng.conf. OID is mapped based on `BCN-SYSLOG-MON-MIB.mib`. Follow the format:

    
    "log_type":{
        "oid":"oid_value",
        "bcnSyslogMonAlarmCond":"bcnSyslogMonAlarmCond_value",
        "bcnSyslogMonAlarmSeverity":"bcnSyslogMonAlarmSeverity_value", 
        "bcnSyslogMonKeyPair":"bcnSyslogMonKeyPair_value",
        "bcnSyslogMonHostInfo":"bcnSyslogMonHostInfo_value", 
        "bcnSyslogMonAlarmMsg":"bcnSyslogMonAlarmMsg_value"
     }
    

For example:


     "TestQueryFailed": {
        "OID":"1.3.6.1.4.1.13315.6.1.2.0.1",
        "bcnSyslogMonAlarmCond": "1.3.6.1.4.1.13315.6.1.2.1.1.0",
        "bcnSyslogMonAlarmSeverity": "1.3.6.1.4.1.13315.6.1.2.1.2.0",
        "bcnSyslogMonKeyPair": "1.3.6.1.4.1.13315.6.1.2.1.3.0",
        "bcnSyslogMonHostInfo": "1.3.6.1.4.1.13315.6.1.2.1.4.0",
        "bcnSyslogMonAlarmMsg": "1.3.6.1.4.1.13315.6.1.2.1.5.0"
    }

The fields like bcnSyslogMonAlarmCond, bcnSyslogMonAlarmSeverity, bcnSyslogMonKeyPair, bcnSyslogMonAlarmMsg shall be the same for any trap destinations.

## GENERATE ENCRYPTED PASSWORD
1. Run snmp_password_process.py which is located at syslog_monitoring/Config/ to create and encrypt password

	<code>python snmp_password_process.py</code>

2. Input the password
	
3. Copy the encrypted password to snmp_config.json


## HEALTH CHECK THE 3RD PARTY DNS SERVER 
1. The list of 3rd party DNS servers can be configured in syslog_monitoring/Config/resolv.conf

2. The interval (in minutes) to send DNS query and the example of DNS query can be configured in syslog_monitoring/Config/config.ini

####Note
* SSH to the VM host, run terminal command `hostname` to get `vmname`.<br/>
* Then open syslog_monitoring/Config/config.ini, <br/> 
    in [SCHEDULER_CONFIG] section, replace the `vm_host_name` value: `test.host.name` by the correct string of `vmname` returned above. 
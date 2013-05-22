#include <SPI.h>
#include <Ethernet.h>
#include <EEPROM.h>

//############################################################
//############################################################
//############################################################
int eeprom_pin=9;
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192,168,1,123);
IPAddress subnet(255,255,0,0);
//pin mode 2-12
int modes[]={0,0,0,0,0,0,0,0,0,0};
//
EthernetServer server(23);
//############################################################
//############################################################
//############################################################

//tcp max msg len
const int msg_len=5;
const int buff_len=20;
//init
bool initEth = true;

//-------------------------------------------------
//set pin mode
bool setMode(int pin,int mode){
	if(modes[pin]!=mode){
		modes[pin]=mode;
		return true;
	}
	return false;
}
void readSerial(EthernetClient conn){
	char val;
	//
	int cnt=0;
	//clean buffer
	char msg[buff_len];
	for(int i=0;i<buff_len;i++){
		msg[i]='_';
	}
	//check end of line
	while(cnt<buff_len){
		if(Serial.available()>0){
			val=Serial.read();
			if(val=='\n' || val=='\r'){
				break;
			}
			msg[cnt]=val;
			cnt++;
		}else{
			//@@@@@@@@@@@@@@@@
			break;
		}
	}
	//send back to client
	conn.print("@|");
	conn.print(msg);
	conn.print("\n");
}
void readCommand(EthernetClient conn){
	char val;
	//check first char
	val=conn.read();
	
	//CMD
	if(val=='#'){
		int cnt=0;
		//clean buffer
		char msg[msg_len];
		for(int i=0;i<msg_len;i++){
			msg[i]='_';
		}
		//check end of line
		while(cnt<msg_len){
			if(conn.available()>0){
				val=conn.read();
				if(val=='\n' || val=='\r'){
					break;
				}
				msg[cnt]=val;
				cnt++;
			}
		}
		// --- PARSE ------------------------------------------
		// #>C1\n
		// set pin 2 to out mode and set it to high
		// #<E\n
		// set pin 4 as imput and read digital value
		// #~A\n
		// read analog input 0 and return value 
		// #|mymessage\n
		// sends to serial TX message 
		// ----------------------------------------------------
		char val=msg[0];
		//pin defined as ASCII A=0,B=1
		int pin=msg[1]-65;
		//value HIGH,LOW
		int pinval=msg[2]-48;
		//default value
		int ival=0;

		//
		bool found=true;
		
		//dispatch commands 
		//------------------------------------------------------
		//set as mode output 
		if(val=='>'){
			if(setMode(pin,1)){
				//check status
				pinMode(pin,OUTPUT);
			}
			digitalWrite(pin,pinval);
			ival=2;
		//set as mode input
		}else if(val=='<'){
			if(setMode(pin,2)){
				pinMode(pin,INPUT);
			}
			ival=digitalRead(pin);
		//analog input
		}else if(val=='~'){
			ival=analogRead(pin);
		//serial TX
		}else if(val=='|'){
			Serial.println(msg);
			ival=1;
		//set ip 192.168.x.x ex: 192.168.0.10
		}else if(val=='^'){
			EEPROM.write(0,msg[1]-32);
			EEPROM.write(1,msg[2]-32);
			ival=1;
          
		//not found
		}else{
			found=false;
		}
		//------------------------------------------------------
		//return to server
		conn.print("@");
		//conn.print("[");
		char buff[3];
		//conn.print(itoa(1,buff,10));
		//conn.print("]");
		//
		conn.print(msg[0]);
		conn.print(msg[1]);
		//
		if(found){
			//return value
			conn.print(ival);
			conn.print("\n");
		}else{
			conn.print("0\n");
		}
	//PING
	}else if(val=='*'){
		conn.print("*\n");
	}
}
void flushSerial(){
	while (Serial.available() > 0) {
		Serial.read(); 
	}
}

//------------------------------------------------
void setup() {	
        //get EEPROM ip
	setMode(eeprom_pin,INPUT);
	//pullup
	digitalWrite(eeprom_pin,HIGH);
	//if jumper on gnd to pin X
	if(!digitalRead(eeprom_pin)){
		ip[2]=EEPROM.read(0);
		ip[3]=EEPROM.read(1);
	}

	//ethernet 
	Ethernet.begin(mac, ip, subnet);
	server.begin();
	
	//serial speed
	Serial.begin(9600);
}

//------------------------------------------------
void loop() {
 	initEth = true;
	EthernetClient client = server.available();
	if (client) {
		//client.print("READY\n");
		client.flush();
		//if client connected
		while (client.connected()){
			//init
			if(initEth){
				//send alive 
				client.print("^\n");
				Serial.flush();
				initEth=false;
			}
			//read reply if data available 
			else if (client.available()) {
				//get reply
				readCommand(client);
			}
			//serial
                        /*
			else if (Serial.available()) {
				//get serial buffer and push
				readSerial(client);
			}
                        */
		}
		//
		client.stop();
		//disconnected
	}
}

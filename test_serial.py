import logging.config
import re
from gsmmodem.pdu import decodeSmsPdu
import serial
import yaml


log = logging.getLogger("request")

class GetSMS:
    def __init__(self, com):
        self.com = com
        self.ser = serial.Serial(self.com, 115200, timeout=1)
        log.info('>>start config port {0}<<'.format(self.com))
        log.info("residual  info:".format(self.ser.readlines()))     # 读取剩余的信息
        self.ser.write(str(chr(27)).encode() )
        log.info(self.ser.readlines())

        self.ser.write(b"AT&V\r\n")                  # 显示当前所有配置信息
        log.info(self.ser.readlines())

        self.ser.write(b'AT+CLCK="AB",0\r\n')       # 禁止所有服务
        log.info(self.ser.readlines())

        self.ser.write(b'AT+CLCK="AC",0\r\n')       # 禁止所有呼入服务
        log.info(self.ser.readlines())

        self.ser.write(b'AT+CLCK="AG",0\r\n')       # 禁止所有呼出服务
        log.info(self.ser.readlines())

        self.ser.write(b"AT+QCCID\r\n")              # 读取sim卡唯一标识
        log.info(self.ser.readlines())

        self.ser.write(b"AT+CNMI?\r\n")              # 读取当前的短消息配置
        log.info(self.ser.readlines())

        self.ser.write(b"AT+CNMI=2,1,0,0,0\r\n")     # 设置短消息配置
        log.info(self.ser.readlines())

        self.ser.write(b'AT+CSCS="GSM"\r\n')         # 设置TE字符集
        log.info(self.ser.readlines())

        self.ser.write(b"AT+CMGF=0\r\n")             # 设置PDU模式0
        log.info(self.ser.readlines())

        self.ser.write(b"AT+CSCA?\r\n")              # 读取消息中心地址
        ser_output = self.ser.readlines()
        log.info(ser_output)
        ser_output = ser_output[1].decode()
        self.ser.smsc = re.search(r'\+CSCA: "(.*)"', ser_output).groups()[0]
        log.info('SMSC: {0}'.format(self.ser.smsc))

    def sms(self):
        self.ser.write(b'AT+CMGL=0\r\n')
        ser_output = self.ser.readlines()
        print(ser_output)
        if len(ser_output) > 2:
            log.info('SendRecvSmsTask {0} {1} recv_message: {2}'.format(self.com, ser_output))
            next_parse_flag = False
            for code in ser_output:
                code = code.decode()
                print("code: ", code)
                if next_parse_flag:
                    code = code.strip()
                    log.info('SendRecvSmsTask decodeSmsPdu {0}'.format(code))
                    print("codestrip: ", code)
                    msg_data = decodeSmsPdu(code)
                    log.info('SendRecvSmsTask {0} {1} msg_data: {2}'.format(self.com, msg_data))
                    print("msg_data: ", msg_data)
                    delsms = "AT+CMGD={0}\r\n".format(msg_index_no).encode()
                    print("delete:",delsms)
                    self.ser.write(delsms)
                    next_parse_flag = False
                elif code[:6] == '+CMGL:' and code[9:10] == "0":
                    msg_index_no = code[7:8]
                    next_parse_flag = True



    def controller(self):
        while True:
            self.sms()


if __name__ == "__main__":
    log_config = yaml.load(open('logging.yaml', 'r'))
    logging.config.dictConfig(log_config)
    work_task = GetSMS("COM7")

    work_task.controller()

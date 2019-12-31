class switch(object):
    def __init__(self, sw_id, sw_name, port_list):
        self.sw_id=sw_id
        self.sw_name=sw_name
        self.port_list=port_list
    
    def set_sw(self):
        return self.sw_id, self.sw_name, self.port_list

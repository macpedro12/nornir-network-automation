class Service:
    
    def __init__(self,id,service_name, applied_config,initial_config,status):
        self._id = id
        self._service_name = service_name
        self._applied_config = applied_config
        self._initial_config = initial_config
        self._status = status
    
    @property
    def id(self):
        return self._id
    
    @property
    def service_name(self):
        return self._service_name
    
    @property
    def applied_config(self):
        return self._applied_config
    
    @property
    def initial_config(self):
        return self._initial_config

    @property
    def status(self):
        return self._status
    
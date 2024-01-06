

class Car():
    
    MAX_TIME_STATIONARY = 5
    STATIONARY_THRESHOLD = 10
    
    def __init__(self):
        self.car_id = None
        self.car_parked = None #parked or not
        self.car_previous_position = None
        self.car_position = None
        self.time_stationary_start = None
        self.time_stationary_end = None
        self.time_stationary = None
        self.time_elapsed_feed = None
    
    def checkTime(self):
        if self.car_position is not None and self.car_previous_position is not None:
            current_pos = self.car_position
            previous_pos = self.car_previous_position
            motion_speed = abs(current_pos[0] - previous_pos[0]) + abs(current_pos[1] - previous_pos[1])
            # update stationary time if counters are set
            if self.time_stationary_start and self.time_stationary_end:
                self.time_stationary = self.time_stationary_end - self.time_stationary_start
                self.car_parked = self.time_stationary > self.MAX_TIME_STATIONARY
            # if is stationary , set start_counter
            if motion_speed < self.STATIONARY_THRESHOLD:
                if self.time_stationary_start is None:
                    self.time_stationary_start = self.time_elapsed_feed
                else:
                    self.time_stationary_end = self.time_elapsed_feed
            else:
            # if is moving, reset counters          
                if self.time_stationary_start is not None:
                    self.time_stationary_end = None
                    self.time_stationary_start = None  
                      
        return
        
    def updateCar(self, car_id, car_previous_position, car_position, time_elapsed):    
        self.car_id = car_id
        self.car_position = car_position
        self.car_previous_position = car_previous_position
        self.time_elapsed_feed = time_elapsed
        self.server_notified = None
        self.checkTime()
               
    def __str__ (self):
        return "car_id={0} ; car_parked={1} ; car_position:{2};".format(self.car_id, self.car_parked, self.car_position)
# simple low pass filter (dt aware)

class LowPass:
    def __init__(self, time_factor=1.0, init_val=0.0):
        self.time_factor = time_factor
        self.filter_value = init_val
        self.inited = False
        
    def update(self, value, dt):
        if not self.inited:
            self.filter_value = value
            self.inited = True
    
        # weight_factor: the actual low pass filter value for the
        # current dt.
        if self.time_factor > 0.0:
            weight_factor = dt / self.time_factor
        else:
            weight_factor = 1.0

        # The greater the weight, the noisier the filter, but the
        # faster it converges.  Must be > 0.0 or value will never
        # converge.  Max weight is 1.0 which means we just use the raw
        # input value with no filtering.  Min weight is 0.0 which
        # means we do not change the filtered value (but might drift
        # over time with numerical rounding.)
        if weight_factor < 0.0:
            weight_factor = 0.0
        if weight_factor > 1.0:
            weight_factor = 1.0
        self.filter_value = (1.0 - weight_factor) * self.filter_value \
            + weight_factor * value;
        return self.filter_value

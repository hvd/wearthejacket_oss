
class decision_engine:
    def __init__(self):
        self.wear_a_jacket = 'Wear the jacket'
        self.take_a_jacket = 'Take the jacket'
        self.dont_wear_a_jacket = 'Do not wear the jacket'
        self.umbrella = 'Take the umbrella'
        self.wear_ear_muffs = 'Wear earmuffs'
        self.wear_shorts = 'Wear shorts'
        self.tshirt = 'Wear a tshirt'
        self.polo = 'Wear a polo'
        self.full_sleeves = 'Wear a shirt with full sleeves'
        self.wear_jacket_threshold = 63
        self.take_jacket_theshold = 70

    '''This is the business logic of the application based on preset thresholds. Candidate for upgrade with a learning algorithm'''
    def get_decision(self,weather_report={},threshold=0):
        if weather_report:
            if weather_report['currently']['apparentTemperature']:
                temperature = weather_report['currently']['apparentTemperature']
            else:
                temperature = weather_report['currently']['temperature']
            if temperature < self.wear_jacket_threshold:
                decision = self.wear_a_jacket
                return decision
            elif temperature > self.wear_jacket_threshold and temperature < self.take_jacket_theshold:
                decision = self.dont_wear_a_jacket + 'but, ' + self.take_a_jacket
                return decision
            else:
                return self.dont_wear_a_jacket

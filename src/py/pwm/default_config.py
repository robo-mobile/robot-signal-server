def_config = '''

title = "PWM manager config"

pwm_type = "L9110S"             # choose  one of: L9110S/L298N/DL298N (double L298N with ilon wheels)/ 
                                # DL298NU (double L298N with usual wheels)
                                
log_level = "INFO"              # EMERGENCY/ALERT/CRITICAL/ERROR/WARNING/NOTICE/INFO/DEBUG

# standat pwm engine type

# [outputs]
# channel1 = 36
# channel2 = 37
# channel3 = 38
# channel4 = 39

# l298n engine type

# [outputs]
# enA = 35
# channel1 = 36
# channel2 = 37
# enB = 40
# channel3 = 38
# channel4 = 39

# double l298n engine type (ilon and usual wheel)

# [outputs]
# enA1 = 40
# channel11 = 38
# channel12 = 36
# enB1 = 33
# channel13 = 35
# channel14 = 37
# enA2 = 11
# channel21 = 13
# channel22 = 15
# enB2 = 12
# channel23 = 16
# channel24 = 18
'''


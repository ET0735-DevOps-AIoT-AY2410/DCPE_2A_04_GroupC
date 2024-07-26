def test_accelerometer():
    import force_detect
    g_force = 30
    force_detect.monitor_accelerometer(g_force)
    
    assert force_detect.test_value == 3 
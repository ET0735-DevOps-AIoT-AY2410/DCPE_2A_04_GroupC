<<<<<<< HEAD
import force_detect as test_acc

def test_accelerometer():
   test_acc.start()
   g_force = 30
   test_acc.monitor_accelerometer(g_force)
   assert test_acc.monitor
=======
def test_accelerometer():
    import force_detect
    g_force = 30
    force_detect.monitor_accelerometer(g_force)
    
    assert force_detect.test_value == 3 
>>>>>>> renzo

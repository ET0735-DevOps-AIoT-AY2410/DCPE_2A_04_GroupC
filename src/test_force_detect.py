import force_detect as test_acc

def test_accelerometer():
   test_acc.start()
   g_force = 30
   test_acc.monitor_accelerometer(g_force)
   assert test_acc.monitor
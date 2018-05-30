import pyautogui as pyg
pyg.FAILSAFE = True
while True:
	pyg.moveTo(100,100,duration=3)
	pyg.moveTo(1700,100,duration=3)
	pyg.moveTo(1700,950,duration=3)
	pyg.moveTo(100,950,duration=3)

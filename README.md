# DevOps MiniProject Group C
## Smart Vending Machine
![alt text](https://github.com/ET0735-DevOps-AIoT-AY2410/DCPE_2A_04_GroupC/blob/master/src/vending_machine.png "Vending Machine Icon")


## Functional Requirements

1. **Function Menu**:
    - LCD displays the options of the Smart Vending Machine. (i.e. method of payment, or drink type)
    - LCD displays the processes that are happening. (e.g. "Dispensing Drink")

2. **Collection of Drinks**:
    - User will be given a QR Code from the purchased drink.
    - After scanning and verifying the QR Code, the purchased drink is dispensed.

3. **Physical Payment**:
    - User can select between Card or website payment.
    - __App payment__:
        - A QR Code generated from the website will be scanned by the Vending Machine to make payment.
    - __Card payment__:
        - The Vending Machine will scan the RFID card that the user is using.

4. **Vending Machine Door**
    - The Vending Machine door can only be accessed by servicing employees that will log in by keying in a password to unlock the door.
    - The Vending Machine door has a anti-burglar system where the alarm will sound if there has been an attempt to open the door. The alarm will also sound if the door is open without the password keyed in.

5. **Remote Services**
    - The user can pay and collect their drink using the website.


## Non-Functional Requirements

1. **Power Management**:
    - When the Vending Machine is not interacted with for more than 1 minute, the Vending Machine will enter Low Power Mode. (i.e. LCD will turn off)
    - Whenever the user interacts with the Vending Machine (i.e. presses a key on the keypad), the Vending Machine will enter High Power Mode. (i.e. LCD will turn on)


## Contributors

- **Renzo Oracion Gandicela**
- **Er Zhong Xun Ervin**
- **Koh Jia Sheng**
- **Lee Hong Yi**
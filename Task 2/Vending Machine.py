import time

##=======================================================================================================

class State:
    pass

class System:
    pass

##========================================================================================================

class Drink():
    def __init__(self,name,quantity, price, code):
        self.name=name
        self.quantity=quantity
        self.price=price
        self.code=code

##========================================================================================================
## Drink Segment


class Drink_System(System):
    def __init__(self):
        self.drinks={}
        self.drinks['PEPS'] = pepsi = Drink('Pepsi', 0, 30, 'PEPS')
        self.drinks['MDEW'] = mountain_dew = Drink('Mountain Dew', 0, 30, 'MDEW')
        self.drinks['DPEP'] = dr_pepper = Drink('Dr. Pepper', 0, 50, 'DPEP')
        self.drinks['COKE'] = coke = Drink('Coke', 0, 20, 'COKE')
        self.drinks['GATO'] = gatorade = Drink('Gatorade', 0, 20, 'GATO')
        self.drinks['DCOK'] = diet_coke = Drink('Diet Coke', 0, 30, 'DCOK')
        self.drinks['MINM'] = minute_maid = Drink('Minute Maid', 0, 25, 'MINM')
        self.drinks['TROP'] = tropicana = Drink('Tropicana', 0, 30, 'TROP')


    def get_code(self, curr_code):
        self.curr_drink=self.drinks[curr_code]


##========================================================================================================
## States Definitions


class Interface(State):
    def __init__(self, drink_system):
        self.curr_code=input("Enter drink code: ")
        time.sleep(0.5)
        print("Checking code....")
        while (self.curr_code not in drink_system.drinks):
            time.sleep(0.5)
            print("Wrong code. PLease re-enter code")
            time.sleep(0.5)
            self.curr_code = input("Enter drink code: ")
            print("Checking code....")
        time.sleep(0.5)
        print("Code accepted!")
        time.sleep(1)



class Quantity_Checker(State):
    def __init__(self, drink_system, curr_code):
        self.curr_drink_quantity=drink_system.drinks[curr_code].quantity
        if self.curr_drink_quantity==0:
            print(f'{drink_system.drinks[curr_code].name} is not available. Please try another drink')
            self.q_check=False
            time.sleep(0.4)
        else:
            print("Drink available")
            self.q_check = True
            time.sleep(0.4)



class Q_Check(State):
    def __init__(self,drink_system):
        drink_objects=list(drink_system.drinks.values())
        quantities=[]
        for i in drink_objects:
            quantities.append(i.quantity)
        self.res = all(x == 0 for x in quantities)



class Deploy(State):
    def __init__(self, drink_system):
        print("Please wait... ")
        time.sleep(1)
        print("Your drink is being fetched.....")
        time.sleep(3)
        drink_system.curr_drink.quantity-=1
        print(f'{drink_system.curr_drink.name} has been deployed')
        time.sleep(1)
        print("Enjoy your drink!")



class Display(State):
    def __init__(self, drink_system):
        self.drink_system=drink_system
        print (f'''
        ||====================================================================||
        || Sl. No.      Drink           Code        Cost         Quantity     ||
        ||====================================================================||
        ||    1         Pepsi           PEPS         30             {drink_system.drinks['PEPS'].quantity}        ||
        ||--------------------------------------------------------------------||
        ||    2      Mowntain Dew       MDEW         30             {drink_system.drinks['MDEW'].quantity}        ||
        ||--------------------------------------------------------------------||
        ||    3       Dr. Pepper        DPEP         50             {drink_system.drinks['DPEP'].quantity}        ||
        ||--------------------------------------------------------------------||
        ||    4         Coke            COKE         20             {drink_system.drinks['COKE'].quantity}        ||
        ||--------------------------------------------------------------------||
        ||    5        Gatorade         GATO         20             {drink_system.drinks['GATO'].quantity}        ||
        ||--------------------------------------------------------------------||
        ||    6       Diet Coke         DCOK         30             {drink_system.drinks['DCOK'].quantity}        ||
        ||--------------------------------------------------------------------||
        ||    7      Minute Maid        MINM         25             {drink_system.drinks['MINM'].quantity}        ||
        ||--------------------------------------------------------------------||
        ||    8       Tropicana         TROP         30             {drink_system.drinks['TROP'].quantity}        ||
        ||====================================================================||        
        ''')


class Fill(State):
    def fill(selfself,drink_system):
        for dks in drink_system.drinks:
            drink_system.drinks[dks].quantity=50

    def refill(self, drink_system):
        choice = input("All empty. Enter 'REFILL' to refill")

        while (choice != "REFILL"):
            choice=input("Please enter 'REFILL' before proceeding")

        for dks in drink_system.drinks:
            drink_system.drinks[dks].quantity=50
        time.sleep(1)
        print("Please wait while Drinks are being refilled.....")
        time.sleep(3)
        print("Drinks are refilled")
        time.sleep(1)
        print("Vending Machine is ready for use")
        time.sleep(1)
        self.interface = Display(drink_system)


##========================================================================================================
## Payment Segment


class Payment_System(System):
    def __init__(self):
        self.amount=0



class Accept_Pay(State):
    def accept_payment(self,drink_cost, payment_system):
        self.inserted=int(input(f"\nEnter amount Rs. {drink_cost} or more: "))
        while (self.inserted < drink_cost):
            time.sleep(1)
            self.inserted += int(input(f"Enter Rs. {drink_cost - self.inserted}  or more: "))
        payment_system.amount+= self.inserted
        time.sleep(1)
        print("Payment accepted")
        time.sleep(1)



class Give_Change(State):
    def give_change(self,drink_cost, inserted, payment_system):
        if inserted==drink_cost:
            print("No change")
            time.sleep(0.5)
        else:
            self.change=inserted-drink_cost
            payment_system.amount-=self.change
            print(f'Change given: Rs. {self.change}')
            time.sleep(0.5)


##========================================================================================================
## FSM Definition


class FSM(object):

    def __init__(self):
        self.payment_system=Payment_System()
        self.drink_system=Drink_System()


    def Start_Machine(self):
        print("Starting Vending Machine....")
        time.sleep(1)
        print("Please wait....")
        time.sleep(2)
        print("Vending Machine is On")
        time.sleep(0.8)


    def Transition_to_Fill(self):
        print("Just a moment")
        time.sleep(1)


    def Initial_Fill(self):
        fill=Fill()
        fill.fill(self.drink_system)

        for dks in self.drink_system.drinks:
            self.drink_system.drinks[dks].quantity=50
        print("Filling drinks...")
        time.sleep(2)


    def Transition_to_Ready_State(self):
        print("Vending Machine is ready for use")
        time.sleep(0.8)


    def Set_to_State_display(self):
        self.interface=Display(self.drink_system)


    def Set_to_State_accept_code(self):
        self.interface=Interface(self.drink_system)


    def Transition_quality_checker(self):
        print("\nChecking for availability....")
        time.sleep(1)


    def Set_to_State_quantity_checker(self):
        q_c=Quantity_Checker(self.drink_system, self.interface.curr_code)
        return q_c.q_check


    def Transition_transfer(self):
        print("\nReferring to Payment System.....")
        self.drink_system.get_code(self.interface.curr_code)
        time.sleep(1)


    def Transition_deploy(self):
        print("\nRedirecting to Drink System......")


    def Set_to_State_accept_payment(self):
        self.accept_pay=Accept_Pay()
        self.accept_pay.accept_payment(self.drink_system.curr_drink.price, self.payment_system)


    def Transition_payment_change(self):
        print("Transacting change......")
        time.sleep(2)


    def Set_to_State_give_change(self):
        self.give_change=Give_Change()
        self.give_change.give_change(self.drink_system.curr_drink.price,self.accept_pay.inserted,self.payment_system)


    def Set_to_State_deploy_drink(self):
        self.deploy=Deploy(self.drink_system)
        time.sleep(2)


    def Set_to_State_Refill_Necessity_Checker(self):
        q_c_all=Q_Check(self.drink_system)
        if q_c_all.res==True:
            refill=Fill()
            refill.refill(self.drink_system)


    def Transition_to_Initial(self):
        print("Resetting for Next Use......")
        time.sleep(1)
        print("Resetting Done. Vending Machine is again ready for use")
        time.sleep(0.8)


    def Transition_to_Stop(self):
        print("Shutting down Vending Machine.....")


##========================================================================================================
## Operator Function


def operation_VM():

    machine = FSM()

    machine.Start_Machine()

    machine.Transition_to_Fill()

    machine.Initial_Fill()

    machine.Transition_to_Ready_State()

    while True:


        machine.Set_to_State_display()

        machine.Set_to_State_Refill_Necessity_Checker()

        machine.Set_to_State_accept_code()

        machine.Transition_quality_checker()

        if (machine.Set_to_State_quantity_checker() == False):
            time.sleep(2)
            continue

        machine. Transition_transfer()

        machine.Set_to_State_accept_payment()

        machine.Transition_payment_change()

        machine.Set_to_State_give_change()

        machine.Transition_deploy()

        machine.Set_to_State_deploy_drink()


        choice=input("\nDo you want to buy another drink? (y/n)")
        if choice=='y':
            time.sleep(0.4)
            machine.Transition_to_Initial()
        elif choice=='n':
            machine.Transition_to_Stop()
            time.sleep(1)
            break


##========================================================================================================
## script

if __name__=="__main__":
    operation_VM()



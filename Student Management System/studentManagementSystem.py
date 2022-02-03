import platform
import uuid
import pickle
import os

try:
    from prettytable import PrettyTable
except ModuleNotFoundError:
    import requests
    url = 'https://raw.githubusercontent.com/jazzband/prettytable/master/src/prettytable/prettytable.py'
    r = requests.get(url, allow_redirects=True)
    with open('prettytable.py', 'wb') as f:
        f.write(r.content)
        from prettytable import PrettyTable


data = {
    "columns": ["UID", "Roll No", "Name", "Age", "Class", "Section"],
    "rows": {
    }
}

msg = """
choose an option:

[1] Show data
[2] Enter data
[3] Update an entry
[4] Delete an entry
[99999] Delete \033[91mALL\033[0m data ⚠️

[0] Exit
"""

tb = PrettyTable()
tb.field_names = data["columns"]


def clr():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')


def createTable():
    global l
    global tb
    l = []
    for i in data["rows"]:
        x = [i] + data["rows"][i]
        l.append(x)
    tb.clear_rows()
    tb.add_rows(l)


def showData():
    global data
    try:
        with open("data.dat", "rb") as f:
            data = pickle.load(f)
            createTable()
            print(tb)

    except FileNotFoundError:
        with open("data.dat", "wb") as f:
            pickle.dump(data, f)
        showData()

        with open("data.dat", "rb") as f:
            data = pickle.load(f)

    except EOFError:
        print("Nothing found in file!")
        with open("data.dat", "wb") as f:
            pickle.dump(data, f)

    except:
        print("An error occurred!")


def inputData():
    clr()
    global data
    print("\033[4m\033[96m\033[1mInput Data\033[0m\n")
    try:
        uid = str(uuid.uuid4())[:6]
        roll_no = int(input("Enter Roll No: "))
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        class_ = input("Enter class: ")
        section = input("Enter section: ")
    except:
        print("An error occoured!")
        pass

    try:
        with open("data.dat", "rb") as f:
            data = pickle.load(f)
        data["rows"][uid] = [roll_no, name, age, class_, section]
        with open("data.dat", "wb") as f:
            pickle.dump(data, f)
            clr()
            print("\033[92mData entered succesfully!\033[0m \n")
    except FileNotFoundError:
        data["rows"][uid] = [roll_no, name, age, class_, section]
        with open("data.dat", "wb") as f:
            pickle.dump(data, f)
            clr()
            print("\033[92mData entered succesfully!\033[0m \n")
    except:
        clr()
        print("\033[91mData was not entered!\033[0m")
        pass


def updateData():

    print("\033[4m\033[96m\033[1mUpdate Data\033[0m\n")
    showData()
    try:
        with open("data.dat", "rb") as f:
            data_ = pickle.load(f)
            data_ = data_["rows"]

        uid = input("Enter UID of student to update: ")
        print("NOTE: Leave fields empty to keep same")
        if uid in data_:
            data_ = data_[uid]
            roll_no_ = input("Enter Roll no.: ")
            if len(roll_no_) == 0:
                roll_no_ = int(data_[0])
            else:
                roll_no_ = int(roll_no_)
            name_ = input("Enter name: ")
            if len(name_) == 0:
                name_ = data_[1]
            age_ = input("Enter age: ")
            if len(age_) == 0:
                age_ = int(data_[2])
            else:
                age_ = int(age_)
            class__ = input("Enter class: ")
            if len(class__) == 0:
                class__ = data_[3]
            section_ = input("Enter section: ")
            if len(section_) == 0:
                section_ = data_[4]

            datToEnter = [roll_no_, name_, age_, class__, section_]

    except:
        print("An error occoured!")
        pass

    try:
        with open("data.dat", "rb") as f:
            data = pickle.load(f)
        data["rows"][uid] = datToEnter
        with open("data.dat", "wb") as f:
            pickle.dump(data, f)
            clr()
        print("\033[92mData update succesful!\033[0m \n")
    except:
        clr()
        print("\033[91mData was not updated!\033[0m")
        pass


def deleteData():
    print("\033[4m\033[96m\033[1mDelete Data\033[0m\n")
    showData()
    try:
        uid = input("Enter UID of student to delete: ")
        c = input("Are you sure(y/N): ")

    except:
        print("An error occured!")

    try:
        if c.lower() == 'y' or c.lower() == 'yes':

            with open("data.dat", "rb") as f:
                data = pickle.load(f)
            del data["rows"][uid]
            with open("data.dat", "wb") as f:
                pickle.dump(data, f)
                clr()
                print("\033[92mRecord deleted succesfully!\033[0m \n")
    except:
        clr()
        print("\033[91mData was not deleted!\033[0m")
        pass


def delAll():
    print("\033[4m\033[91m\033[1mDelete ALL data\033[0m\n")
    try:
        with open("data.dat", "rb") as f:
            data = pickle.load(f)
            n = len(data["rows"])
        if n > 0:
            print(
                f"\033[91mWARNING\033[0m: You will lose all your {n} records")

            i = input("Enter 'CONFIRM' to delete all data: ")
            if i == 'CONFIRM':
                data = {"columns": ["UID", "Roll No", "Name",
                                    "Age", "Class", "Section"], "rows": {}}
                with open("data.dat", "wb") as f:
                    pickle.dump(data, f)
                    clr()
                    print("\033[92mAll data deleted!\033[0m")
            else:
                raise SyntaxError
        else:
            clr()
            print("\033[91mNumber of records is zero!\033[0m")
    except SyntaxError:
        clr()
        print("Aborted!")
        print("\033[91mData not deleted\033[0m")
    except FileNotFoundError:
        clr()
        data = {"columns": ["UID", "Roll No", "Name",
                            "Age", "Class", "Section"], "rows": {}}
        with open("data.dat", "wb") as f:
            pickle.dump(data, f)
        print("\033[91mThere are no records!\033[0m")
        print("\033[91mData not deleted\033[0m")

    except:
        clr()
        print("\033[91mData not deleted\033[0m")


def main():
    clr()
    print("\033[1m\033[93mWelcome to Student Management System\033[0m")
    print("""
   _____ __  __  _____ 
  / ____|  \/  |/ ____|
 | (___ | \  / | (___  
  \___ \| |\/| |\___ \ 
  ____) | |  | |____) |
 |_____/|_|  |_|_____/ 
                       
              -- Lakshya Mahajan, XII-C, SLPS          """)
    x = True
    while x:
        print(msg)
        try:
            inp = int(input("\n> "))
            if inp == 0:
                x = False
                clr()
                print("Bye Bye! Thank you for using Student Management System\n")
                exit()
            elif inp == 1:
                clr()
                showData()
            elif inp == 2:
                inputData()
            elif inp == 3:
                clr()
                updateData()
            elif inp == 4:
                clr()
                deleteData()
            elif inp == 99999:
                clr()
                delAll()
            else:
                raise ValueError
        except ValueError:
            clr()
            print("\033[91mInvalid input!\033[0m")
        except KeyboardInterrupt:
            clr()
            print("Bye Bye! Thank you for using Student Management System\n")
            exit()


if __name__ == '__main__':
    main()

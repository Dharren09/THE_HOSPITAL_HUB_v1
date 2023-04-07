#!/usr/bin/python3
""" This module defines a command interpreter to manage JSON data storage
"""
import cmd
from datetime import datetime
import models
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from colorama import init, Fore, Back, Style
from models.parent_model import ParentModel
from models.patients import Patient
from models.pharmacy import Pharmacy
from models.TeleHealth import TeleHealth
from models.billing_and_payment import BillingInvoice
from models.staff import Staff
import shlex  # splits line along spaces except in double quotes

classes = {"Patient": Patient, "TeleHealth": TeleHealth, "Pharmacy": Pharmacy, 
           "BillingInvoice": BillingInvoice, "Staff": Staff}


class THE_HOSPITAL_HUBCommand(cmd.Cmd):
    
    prompt = Style.BRIGHT + Fore.BLUE + "TheHospitalHub>>> " + Style.RESET_ALL

    def do_quit(self, arg):
        """Exit THE_HOSPITAL_HUB console."""
        print("Exiting THE_HOSPITAL_HUB console...")
        return True

    def do_EOF(self, arg):
        """Exit THE_HOSPITAL_HUB console when EOF is received."""
        print("Exiting THE_HOSPITAL_HUB console...")
        return True
    
    def preloop(self):
        print(Style.BRIGHT + Fore.CYAN + "\nHello and Welcome to The Hospital Hub" +
              Style.RESET_ALL + "  (default, February 12 2023, 08:01:47)")
        print("\nStay on top of your health with our comprehensive health ", end="")
        print("management system. Keep track of your medical history, appointments ", end="")
        print("and health goals all in one place.\n")
        print("Ver 1.0\n")

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for key, value in args.items():
            if isinstance(value, str) and value[0] == value[-1] == '"':
                # If the value is a string enclosed in double quotes, remove the quotes and replace underscores with spaces
                value = shlex.split(value)[0].replace('_', ' ')
            new_dict[key] = value
        return new_dict

    def do_count(self, args):
        """Counts all objects"""
        try:
            if len(args) == 0:
                print("The total number of objects in Storage is {}".
                      format(len(models.storage.all())))
                return
            arguments = args.split(" ")
            if len(arguments) == 1:
                if arguments[0] in classes:
                    obj_count = len(models.storage.all(arguments[0]))
                    print("The total number of {}s within the TheHospitalHub "
                          + "Hospital Management System is ".
                          format(arguments[0]) + Fore.ORANGE
                          + "{}".format(obj_count)
                          + Style.RESET_ALL)
                    return
                else:
                    print(Fore.RED + "Please enter a valid class" +
                          Style.RESET_ALL)
        except Exception:
            pass

    def do_show(self, args):
        """shows an individual object"""
        arguments = args.split(" ")
        try:
            if len(arguments) == 1:
                for key in models.storage.all().keys():
                    obj_id = key.split(".")[1]
                    if arguments[0] == obj_id:
                        class_name = key.split(".")[0]
                        print(models.storage.get(class_name, obj_id).to_dict())
        except Exception:
            pass

    def do_create(self, args):
        """Creates a new instance, saves it to the JSON file then prints the id"""
        try:
            if len(args) == 0:
                print("Please enter Class Name to create Object")
                return
            arguments = args.split(" ")

            if arguments[0] not in classes:
                print("**Invalid Class**")
                return

            if len(arguments) == 1:
                obj = eval(arguments[0])()
                obj.save()
                print(Fore.LIGHTBLUE_EX +
                      f"Successfully created {obj.__class__.__name__}"
                      +
                      f" object: TheHospitalHu_id --  {obj.id}" + Style.RESET_ALL)
                return
            if len(arguments) > 1:
                new_dict = {}
                for entry in arguments[1:len(arguments)]:
                    key = entry.split("=")[0]
                    key = str(key)
                    key = key.replace('"', "")
                    key = key.replace("'", "")
                    attr = entry.split("=")[1]

                    if attr == "True" or attr == "False":
                        attr = bool(attr)
                    elif (attr[0] == '"'
                          and attr[len(attr) - 1] == '"' or
                          attr[0] == "'" and attr[len(attr) - 1] == "'"):
                        attr = str(attr)
                        attr = attr.replace('"', "")
                        attr = attr.replace("'", "")
                        attr = attr.replace("_", " ")
                    else:
                        try:
                            attr = int(attr)
                        except TypeError:
                            print("Not an integer")
                    new_dict.update({key: attr})
                obj = eval(arguments[0])(**new_dict)
                obj.save()
                print(f"Successfully Created {obj.__class__.__name__} object: "
                      + Fore.BLUE
                      + f" TheHospitalHub_id --  {obj.id}"
                      + Style.RESET_ALL)
        except Exception:
            pass


    def do_delete(self, args):
        """Deletes an instance based on the class and id"""
        try:
            arguments = args.split(" ")
            if len(arguments) == 1:
                cid = args
                for key, value in models.storage.all().items():
                    obj_id = key.split(".")[1]
                    if cid == obj_id:
                        models.storage.delete(value)
                        print(Fore.RED + "Deleted" + Style.RESET_ALL)
        except Exception:
            pass

    def do_update(self, args):
        """Update an instance based on the class name, id, attribute & value"""
        try:
            arguments = args.split(" ")
            if len(arguments) > 1:
                new_dict = {}
                for entry in arguments[1:len(arguments)]:
                    key = entry.split("=")[0]
                    key = str(key)
                    key = key.replace('"', "")
                    key = key.replace("'", "")
                    attr = entry.split("=")[1]

                    if attr == "True" or attr == "False":
                        attr = bool(attr)
                    elif (attr[0] == '"' and attr[len(attr) - 1] == '"'
                          or attr[0] == "'" and attr[len(attr) - 1] == "'"):
                        attr = str(attr)
                        attr = attr.replace('"', "")
                        attr = attr.replace("'", "")
                        attr = attr.replace("_", " ")
                    else:
                        try:
                            attr = int(attr)
                        except TypeError:
                            print("Not an integer")
                    new_dict.update({key: attr})
                cid = arguments[0]
                for key in models.storage.all().keys():
                    obj_id = key.split(".")[1]
                    if cid == obj_id:
                        models.storage.update(key, **new_dict)
                        print(Fore.YELLOW + "Instance Updated"
                              + Style.RESET_ALL)
        except Exception:
            pass
    
    def do_all(self, args):
        """returns all objects in storage"""
        try:
            if len(args) == 0:
                all_objects = []
                for key, value in models.storage.all().items():
                    all_objects.append(str(value))
                print(all_objects)
                return
            arguments = args.split(" ")
            if len(arguments) == 1:
                class_objects = []
                if arguments[0] in classes:
                    for value in models.storage.all(arguments[0]).values():
                        class_objects.append(str(value))
                    print(class_objects)
                else:
                    print(Fore.BLUE + "Please enter a valid class"
                          + Style.RESET_ALL)
        except Exception:
            pass 


if __name__ == '__main__':
    THE_HOSPITAL_HUBCommand().cmdloop()

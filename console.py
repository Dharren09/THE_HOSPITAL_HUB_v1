#!/usr/bin/python3
""" This module defines a command interpreter to manage JSON data storage
"""
import cmd
from datetime import datetime
import models
from models.engine.file_storage import FileStorage
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
    intro = "Welcome to THE_HOSPITAL_HUB console. Type help or ? to list commands.\n"
    prompt = "(THE_HOSPITAL_HUB) "

    def do_quit(self, arg):
        """Exit THE_HOSPITAL_HUB console."""
        print("Exiting THE_HOSPITAL_HUB console...")
        return True

    def do_EOF(self, arg):
        """Exit THE_HOSPITAL_HUB console when EOF is received."""
        print("Exiting THE_HOSPITAL_HUB console...")
        return True

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

    def do_show(self, arg):
        """shows an individual object"""
        # Split the arguments into a list
        tokens = shlex.split(arg)
        if len(tokens) < 2:
            print("** class name and instance id missing **")
            return
        
        # Creates variables of class name and id
        class_name = tokens[0]
        instance_id = tokens[1]

        if len(tokens) > 2:
            print("** too many arguments **")
            return
        
        if not class_name:
            print("** class name missing **")
            return
        
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        
        # if the instance id is missing
        if not instance_id:
            print("** instance id missing **")
            return
        
        # Get the key for the instance from the class name and id
        key = (classes[class_name]) + '.' + instance_id
        try:
            print(models.storage.all()[key])
        except KeyError:
            print("** no instance found **")
            return

    def do_create(self, arg):
        """Creates a new instance, saves it to the JSON file then prints the id"""
        tokens = shlex.split(arg)
        if not tokens:
            print("** class name missing **")
            return
        
        class_name = tokens[0]
        if class_name not in classes:
             print("** class doesn't exist **")
             return
        
        try:
            # create new instance of the class
            new_instance = classes[class_name]()
            # assuming a class has a method 'set_attr(name, value)'
            for attr in tokens[1:]:
                name, value = attr.split("=")
                # convert the value to the appropriate data type
                value = eval(value)
                setattr(new_instance, name, value)
            # Save the new instance and print its id
            models.storage.new(new_instance)
            models.storage.save()
            print(new_instance.id)
        except Exception as e:
            print("** could not create instance: {}".format(str(e)))

    def do_delete(self, arg):
        """Deletes an instance based on the class and id"""
        tokens = shlex.split(arg)
        
        if not tokens:
            print("** class name missing **")
            return
        class_name = tokens[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        
        if len(tokens) < 2:
            print("** instance id missing **")
            return

        instance_id = tokens[1]
        key = "{}.{}".format(class_name, instance_id)

        try:
            # get the instance from the storage object
            instance = models.storage.all()[key]
            # delete the instance from the storage object
            del models.storage.all()[key]
            # save the changes in JSON file
            models.storage.save()
        except KeyError:
            print("** no instance found **")
            return

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        tokens = shlex.split(arg)
        
        if not tokens:
            print("** class name missing **")
            return
        
        class_name = tokens[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return

        if len(tokens) < 2:
            print("** instance id missing **")
            return

        instance_id = tokens[1]
        key = "{}.{}".format(class_name, instance_id)
        
        try:
            instance = models.storage.all()[key]
        except KeyError:
            print("** no instance found **")
            return

        if len(tokens) < 3:
            print("** attribute name missing **")
            return

        attribute_name = tokens[2]
        if not hasattr(instance, attribute_name):
            print("** no attribute missing **")
            return

        if len(tokens) < 4:
            print("** value missing **")
            return

        # converting the value to a correct type using eval method
        try:
            value = eval(tokens[3])
        except (NameError, SyntaxError):
            value = tokens[3]

        # update the attribute
        setattr(instance, attribute_name, value)

        # save the changes to the JSON file
        models.storage.save()

    def do_all(self, arg):
        """ Prints all string representations of instances """
        tokens = shlex.split(arg)

        if tokens and tokens[0] not in classes:
            print("** class doesn't exist **")
            return

        instance = models.storage.all()
        if not tokens:
            # print all instances
            print([str(instance) for instance in instance.values()])
        else:
            # print instances of specific class
            class_name = tokens[0]
            print([str(instance) for instance in instance.values() if type(instance).__name__ == class_name])



if __name__ == '__main__':
    THE_HOSPITAL_HUBCommand().cmdloop()

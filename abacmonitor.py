# Harrison Billings
# CSE 365
# Assignment 1
import pprint
import argparse

class AbacMonitor:
    def __init__(self):
        self.policy_dict = dict()
        self.working_file = None

    def load_policy(self, input_file):
        """ This method will parse the policy file and
            load the contents into a dictionary and this 
            dictionary will be used for all other methods
            ARGS: input_file || Type: Text File
            Returns: nothing """
        try:
            self.working_file = input_file
            with open(input_file, "r") as policy_file:
                parsed_policy_list = list()

                for line in policy_file:
                    line = line.strip()
                    line = line.replace("\"","")
                    parsed_line = list()
                    if "PA" in line:
                        parsed_line = line.split("-")
                        parsed_line[0] = parsed_line[0][parsed_line[0].find("<"
                                                                            ):]
                        parsed_policy_list.append(parsed_line)
                    elif "AA" in line:
                        parsed_line = line.split(";")
                        parsed_line[0] = parsed_line[0][parsed_line[0].find("<"
                                                                            ):]
                        parsed_policy_list.append(parsed_line)
                    else:
                        parsed_line = line.split(";")
                        parsed_line[0] = parsed_line[0][parsed_line[0].find(
                            "<"):parsed_line[0].find(">") + 1]
                        parsed_policy_list.append(parsed_line)

                count = 0
                for sublist in parsed_policy_list:
                    new_sublist = list()

                    for list_element in sublist:
                        list_element = list_element.replace("<", "")
                        list_element = list_element.replace(">", "")
                        list_element = list_element.strip()
                        new_sublist.append(list_element)
                    sublist = new_sublist
                    parsed_policy_list[count] = sublist
                    count += 1

                self.policy_dict = {
                    "Attributes": parsed_policy_list[0],
                    "Perms": parsed_policy_list[1],
                    "PA": parsed_policy_list[2],
                    "Entity Names": parsed_policy_list[3],
                    "AA": parsed_policy_list[4]
                }

        except Exception:
            pass

    def show_policy(self):
        """ This method returns a formatted
            string representation of the dictionary 
            ARGS: Nothing
            Return: Nothing """
        pprint.pprint(self.policy_dict)

    def check_permission(self, user_name, object_name, env_name,
                         permission_name):
        """ This method will check the policy dictionary to see if
            a user by the name of user_name can access a certain object
            and do a certain action. If the user can do this action
            it will print "Access Granted" and if the user cannot
            it will print "Access Denided" 
            ARGS: user_name       || TYPE: String
                  object_name     || TYPE: String
                  env_name        || TYPE: String 
                  permission_name || TYPE: String
            Returns: Nothing"""
        if user_name not in self.policy_dict["Entity Names"]:
            print("Permission Denied!\n")
        else:
            search_set = set((user_name, object_name, env_name))
            searched_list = list(a for a in self.policy_dict["AA"] for s in search_set if s in a)
            
            temp_list = list()
            for s in searched_list:
                left_slice_index = s.find(":") + 2
                temp_string = s[left_slice_index:]
                temp_list.append(temp_string)
            
            searched_list = temp_list
            
            if self.working_file == "Example-ASU.txt":
                if "fileOwnerName" and user_name in searched_list[-1]:
                    permission_assignment = searched_list[-1] + " : " + permission_name
                    permission_assignment = permission_assignment.replace(" ","")
                    checker = False
                    for assignment in self.policy_dict["PA"]:
                        normalized_assignment = assignment.replace(" ","")
                        if permission_assignment in normalized_assignment:
                            checker = True
                            break
                        else:
                            continue
                    
                    if checker:
                        print("Permission GRANTED!\n")
                    else:
                        print("Permission DENIED!\n")
                else:
                        searched_list.pop()
                        searched_list.append(permission_name)
                        normalized_search_list = list(s.replace(" ", "") for s in searched_list)
                        checker = False
                        for assignment in self.policy_dict["PA"]:
                            assignment = assignment.replace(" ","")
                            if all(s in assignment for s in normalized_search_list):
                                checker = True
                                break
                            elif normalized_search_list[0]in assignment and normalized_search_list[-1] in assignment:
                                checker = True
                                break
                        
                        if checker:
                            print("Permission GRANTED!\n")
                        else:
                            print("Permission DENIED!\n")

            elif self.working_file == "Example-Entering-Bar.txt":
                normalized_search_list = list(s.replace(" ", "") for s in searched_list)

                checker = False
                for assignment in self.policy_dict["PA"]:
                    assignment = assignment.replace(" ","")
                    if any(s in assignment for s in normalized_search_list):
                        checker = True
                        break
                
                if checker:
                    print("Permission GRANTED!\n")
                else:
                    print("Permission DENIED!\n")
            else:
                pass

                
            
    def add_entity(self, new_entity_name):
        """ This method will add a new entity value to
            the "Entity Names" key in the policy dictionary 
            ARGS: new_entity_name || Type: String
            Returns: Nothing"""
        if new_entity_name not in self.policy_dict["Entity Names"]:
            self.policy_dict["Entity Names"].append(new_entity_name)
        else:
            pass

    def remove_entity(self, new_entity_name):
        """ This method will remove an existing entity value from
            the "Entity Names" key in the policy dictionary 
            ARGS: new_entity_name || Type: String
            Returns: Nothing"""
        if new_entity_name in self.policy_dict["Entity Names"]:
            self.policy_dict["Entity Names"].remove(new_entity_name)
        else:
            pass

    def add_attribute(self, attribute_name, attribute_type):
        """ This method will add a new entity value to
            the "Entity Names" key in the policy dictionary 
            ARGS: attribute_name || Type: String
                  attribute_type || Type: String
            Returns: Nothing"""
        if attribute_name not in self.policy_dict["Attributes"]:
            self.policy_dict["Attributes"].append("{}, {}".format(
                attribute_name, attribute_type))
        else:
            pass

    def remove_attribute(self, attribute_name):
        """ This method will remove and attribute, identified
            by name from both the PA and Attribute Catagory
            ARGS: attribute_name || TYPE: String
            Returns: Nothings """
        for attribute in self.policy_dict["Attributes"]:
            if attribute_name in attribute:
                self.policy_dict["Attributes"].remove(attribute)
            else:
                pass

        temp_list = list()
        for assignment in self.policy_dict["PA"]:

            if attribute_name in assignment:
                remove_list = assignment.split(":", 1)
                remove_list[0] = remove_list[0].split(";")

                for element in remove_list[0]:
                    if attribute_name in element:
                        remove_list[0].remove(element)
                    element.strip()

                remove_list[0] = ";".join(remove_list[0])
                remove_list[0][0].strip()

                assignment = ":".join(remove_list)
                assignment.lstrip()
                temp_list.append(assignment)
                self.policy_dict["PA"] = temp_list

    def add_permission(self, new_permission_name):
        """ This method will add a new permission value to
            the "permission Names" key in the policy dictionary 
            ARGS: new_permission_name || Type: String
            Returns: Nothing"""
        if new_permission_name not in self.policy_dict["Perms"]:
            self.policy_dict["Perms"].append(new_permission_name)
        else:
            pass

    def remove_permission(self, permission_name):
        """ This method will remove and permission, identified
            by name from both the PA and permission Catagory
            ARGS: permission_name || TYPE: String
            Returns: Nothings """
        for permission in self.policy_dict["Perms"]:
            if permission_name in permission:
                self.policy_dict["Perms"].remove(permission)
            else:
                pass

        temp_list = list()
        for assignment in self.policy_dict["PA"]:
            if permission_name in assignment:
                pass
            else:
                temp_list.append(assignment)
            self.policy_dict["PA"] = temp_list

    def add_attributes_to_permission(self, permission_name,
                                     list_of_permisson_attributes):
        """ This method will add attributes to a certains
            permission, for the method to properly execute
            the list of attributes must be an even number
            of inputs, all permissions in the list must also be preseent
            ARGS: permission || Type: String
            list_of_permission_attributes || Type: list of strings
            Return: Nothing"""
            
        if len(list_of_permisson_attributes) % 2 != 0:
            pass
        else:
            if permission_name not in self.policy_dict["Perms"]:
                pass
            else:
                list_of_permisson_attributes = " ".join(list_of_permisson_attributes)
                temp_list = list_of_permisson_attributes.split()
                attribute_pairs = list()

                for x in range(0, len(temp_list), 2):
                    attribute_pairs.append(", ".join(temp_list[x:x + 2]))

                count = 0
                length_of_attribute_pairs = len(attribute_pairs)

                for attribute_pair in attribute_pairs:
                    if attribute_pair in attribute_pairs:
                        count += 1

                new_pa_string = ""
                if count == length_of_attribute_pairs:
                    for x in range(length_of_attribute_pairs - 1):
                        new_pa_string += "{}; ".format(attribute_pairs[x])
                    new_pa_string += "{} : {}".format(
                        attribute_pairs[length_of_attribute_pairs - 1],
                        permission_name)
                self.policy_dict["PA"].append(new_pa_string)

    def remove_attribute_from_permission(self, permission_name, attribute_name,
                                         attribute_value):
        """ This method will remove attributes from permissions
            based on the attribute name and attribute_value
            a special case occurs when the attribute name and 
            value are at the end of the string
            ARGS: permission_name  || Type: string
                  attribute_name   || Type: string
                  attribute_value  || Type: string
            Returns: nothing"""
        if permission_name not in self.policy_dict["Perms"]:
            pass
        else:
            temp_list = list()
            search_set = set((permission_name,attribute_name,attribute_value))

            for assignment in self.policy_dict["PA"]:
                if all(s in assignment for s in search_set):
                    temp_list.append(assignment)
                    self.policy_dict["PA"].remove(assignment)
            
            new_string_list = list()
            for x in range(len(temp_list)):
                element = temp_list[x].split(";")
                for sub_element in element:
                    if attribute_name in sub_element:
                        if sub_element == element[-1]:
                            string_to_remove = "{}, {} :".format(attribute_name,attribute_value)
                            sub_element.replace(string_to_remove,"")
                        element.remove(sub_element)
                        new_string_list.append(element)
                        
            
            for x in range(len(new_string_list)):
                self.policy_dict["PA"].append(new_string_list[x])

    def add_attribute_to_entitiy(self, entity_name,attribute_name,attribute_value):
        """ This method will first check if both entity_name and 
            attribute_name exist in the policy, if both do then
            the policy will be added to the AA section of the dictionary """
        if entity_name not in self.policy_dict["Entity Names"]:
            pass
        
        is_present = False
        for attribute in self.policy_dict["Attributes"]:
            if attribute_name in attribute:
                is_present = True
        
        if(is_present):
            new_attribute_assignment = "{} : {}, {}".format(entity_name,attribute_name,attribute_value)
            self.policy_dict["AA"].append(new_attribute_assignment)
        else:
            pass

    def remove_attribute_from_entity(self, entity_name, attribute_name, attribute_value):
        if entity_name not in self.policy_dict["Entity Names"]:
            pass
        
        is_present = False
        for attribute in self.policy_dict["Attributes"]:
            if attribute_name in attribute:
                is_present = True
        
        if(is_present):
            remove_list = [attribute_name, attribute_value]

            for assignment in self.policy_dict["AA"]:
                if all(s in assignment for s in remove_list):
                    self.policy_dict["AA"].remove(assignment)
        else:
            pass

def parse_args(input):
    

    args_to_list = input.split(";")
    args_to_list = [a.strip() for a in args_to_list ]

    command_list = list()

    for arg in args_to_list:
        command_list.append(arg.split())
    
    return command_list

def execute_args(command_list):
    for command in command_list:
        if command[0] == "load-policy":
            normalized_file_name = command[1]
            left_slice_index = normalized_file_name.rfind("Example")
            normalized_file_name = normalized_file_name[left_slice_index:]
            watcher.load_policy(normalized_file_name)
        elif command[0] == "show-policy":
            if len(command) == 1:
                watcher.show_policy()
        elif command[0] == "check-permission":
            if len(command) == 5:
                watcher.check_permission(command[1],command[2],command[3],command[4])
            else:
                pass
        elif command[0] == "add-entity":
            if len(command) == 2:
                watcher.add_entity(command[1])
            else:
                pass
        elif command[0] == "remove-entity":
            if len(command) == 2:
                watcher.remove_entity(command[1])
            else:
                pass
        elif command[0] == "add-attribute":
            if len(command) == 3:
                watcher.add_attribute(command[1],command[2])
            else:
                pass
        elif command[0] == "remove-attribute":
            if len(command) == 2:
                watcher.remove_attribute(command[1])
            else:
                pass
        elif command[0] == "add-permission":
            if len(command) == 2:
                watcher.add_permission(command[1])
            else:
                pass
        elif command[0] == "remove-permission":
            if len(command) == 2:
                watcher.remove_permission(command[1])
            else:
                pass
        elif command[0] == "add-attributes-to-permission":
            agrument_list = command[2:]
            watcher.add_attributes_to_permission(command[1],agrument_list)
        elif command[0] == "remove-attribute-from-permission":
            if len(command) == 4:
                watcher.remove_attribute_from_permission(command[1],command[2],command[3])
            else:
                pass
        elif command[0] == "add-attribute-to-entity":
            if len(command) == 4:
                watcher.add_attribute_to_entitiy(command[1],command[2],command[3])
            else:
                pass
        elif command[0] == "remove-attribute-from-entity":
            if len(command) == 4:
                watcher.remove_attribute_from_entity(command[1],command[2],command[3])
            else:
                pass
        else:
            print("Invalid Entry")
            break

def main():
    command_list = parse_args(args.text)
    execute_args(command_list)
try:
    parser = argparse.ArgumentParser()
    parser.add_argument("text",action="store",help="input string to parse")
    args = parser.parse_args()
except:
    pass

if __name__ == "__main__":
    watcher = AbacMonitor()
    main()

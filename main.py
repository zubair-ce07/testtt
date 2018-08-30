#!/usr/bin/python3
import sys
import datetime
import calendar
import calculations as results
import filehandler
import output_generator


class Main:
    '''
    This is the main class that recieves report request
    '''

    output = output_generator.OutputGenerator()

    def main(self):
        '''
        This methaod is main method tha handle weather report request from
        command arguments
        '''

        if len(sys.argv) >= 3:
            self.output.dir_path = sys.argv[1]

            current_index = 2
            while(current_index+1 < len(sys.argv)):
                if(sys.argv[current_index] == '-e'):
                    try:
                        year = int(sys.argv[current_index+1])
                        self.output.print_e_output(sys.argv[current_index+1])
                        print()

                    except ValueError:
                        print("Invalid Arguments")
                elif sys.argv[current_index] == '-a':
                    date = sys.argv[current_index+1]
                    self.output.print_a_output(date)
                    print()
                elif sys.argv[current_index] == '-c':
                    date = sys.argv[current_index+1]
                    self.output.print_c_output_bounus(date)
                else:
                    print("Invalid Argument.")

                current_index += 2
        else:
            print('Please enter valid arguments')


repo = Main()
repo.main()

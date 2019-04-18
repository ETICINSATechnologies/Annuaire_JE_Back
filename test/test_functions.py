#!/usr/bin/env python3
# coding: utf8

from colorama import init, Fore, Style


def display_error(error=True):
    if error:
        print(Fore.RED, "[ error ]", end=" ")
    else:
        print(Fore.GREEN, "[success]", end=" ")
    print(Style.RESET_ALL, end="")


def make_test(old_function):
    def new_function(TestClass, description, expecting_error):
        happened_error = False
        function_result = ""
        exception = ""
        try:
            function_result = old_function()
        except Exception as e:
            exception = e
            happened_error = True
        finally:
            display_error(expecting_error != happened_error)
            display_error(expecting_error)
            display_error(happened_error)
            print("{:<32}".format(description + ":"), end="")
            print(Fore.RED, str(exception).replace("\n", ""),
                  end="")
            print(Fore.BLUE, function_result, sep="", end="")
            print(Style.RESET_ALL, sep="")

            TestClass.nb_tests += 1
            if expecting_error == happened_error:
                TestClass.nb_tests_succeed += 1

    return new_function

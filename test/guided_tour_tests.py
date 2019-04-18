#!/usr/bin/env python3
# coding: utf8


from controller.Controller import Controller
from controller.DocController import DocController
from controller.TourController import TourController

from test.test_functions import *


class GuidedTourTest:
    nb_tests = 0
    nb_tests_succeed = 0

    # @TODO: create a method to check the success of uploading a file

    @staticmethod
    def create_tours():
        print("\033[01m## Creation of tours ##\033[0m")
        make_test(lambda: TourController.create_tour(
            "First tour",
            "This is the first guided tour"
        ))(GuidedTourTest, "all needed attributes", False)

        make_test(lambda: TourController.create_tour(
            "Second tour",
            "This is the second guided tour"
        ))(GuidedTourTest, "all needed attributes", False)

        make_test(lambda: TourController.create_tour(
            "Third tour",
            "This is the third guided tour"
        ))(GuidedTourTest, "all needed attributes", False)

        make_test(lambda: TourController.create_tour(
        ))(GuidedTourTest, "needed argument missing", True)

    @staticmethod
    def create_documents():
        print("\n\033[01m## Creation of documents ##\033[0m")
        make_test(lambda: DocController.create_document({
            "title": "title",
            "subject": "Subject1",
            "type": "type",
            "description": "a description",
            "link": "1.gif"
        }))(GuidedTourTest, "all needed attributes", False)

        make_test(lambda: DocController.create_document({
            "title": "title2",
            "subject": "Subject2",
            "type": "type",
            "description": "a description",
            "link": "1.gif"
        }))(GuidedTourTest, "all needed attributes", False)

    @staticmethod
    def read_tours():
        print("\n\033[01m## Reading ##\033[0m")

        make_test(lambda: TourController.get_tours())(
            GuidedTourTest, "all tours", False)

        # @TODO: create method to filter docs
        make_test(lambda: TourController.get_tours())(
            GuidedTourTest, "specific tour", False)

        make_test(lambda: TourController.get_tour_by_id(2))(
            GuidedTourTest, "tour with existing id", False)

        make_test(lambda: TourController.get_tour_by_id(-1))(
            GuidedTourTest, "tour with non existing id", True)

    @staticmethod
    def update_tours():
        print("\n\033[01m## Updating ##\033[0m")
        make_test(lambda: TourController.add_document(1, 1))(
            GuidedTourTest, "adding existing document", False)

        make_test(lambda: TourController.add_document(1, 1))(
            GuidedTourTest, "adding twice existing document", False)

        make_test(lambda: TourController.add_document(1, 2))(
            GuidedTourTest, "adding existing document", False)

        make_test(lambda: TourController.add_document(2, 1))(
            GuidedTourTest, "adding existing document", False)

        make_test(lambda: TourController.add_document(1, 3))(
            GuidedTourTest, "adding non existing document", True)

        make_test(lambda: TourController.add_document(-1, 3))(
            GuidedTourTest, "adding non existing document", True)

        make_test(lambda: TourController.update(1, {
            'title': 'this is a new title',
            'description': 'new description'
        }))(GuidedTourTest, "updating existing guided tour", False)

        make_test(lambda: TourController.update_document(1, 1, {
            'text1': 'this is a text'
        }))(GuidedTourTest, "updating guided tour document", False)

    @staticmethod
    def delete_tours():
        print("\n\033[01m## Deletion ##\033[0m")
        make_test(lambda: TourController.delete_tour(3))(
            GuidedTourTest, "existing document", False)

        make_test(lambda: TourController.delete_tour(3))(
            GuidedTourTest, "existing document", True)


if __name__ == "__main__":
    Controller.recreate_tables()
    GuidedTourTest.create_tours()
    GuidedTourTest.create_documents()
    GuidedTourTest.read_tours()
    GuidedTourTest.update_tours()
    GuidedTourTest.read_tours()
    GuidedTourTest.delete_tours()
    GuidedTourTest.read_tours()

    print("\n\n\033[04mSuccess\033[01m: ",
          GuidedTourTest.nb_tests_succeed, "/",
          GuidedTourTest.nb_tests, sep="")
